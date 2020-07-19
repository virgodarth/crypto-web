import json
from collections import OrderedDict

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.template import loader
from rest_framework import VERSION
from rest_framework.compat import pygments_css
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.settings import api_settings


class RiskChartAPIRenderer(BrowsableAPIRenderer):
    format = 'custom'
    accepted_media_type = None
    renderer_context = None
    template_name = 'rest_framework/api.html'

    def get_template_name(self, response, view):
        if response.template_name:
            return response.template_name
        elif hasattr(view, 'template_name'):
            return view.template_name
        elif self.template_name:
            return self.template_name
        raise ImproperlyConfigured(
            'Returned a template response with no `template_name` attribute set on either the view or response'
        )

    def get_content(self, data, *args, **kwargs):
        """
        Get the content as if it had been rendered by the default
        non-documenting renderer.
        """
        indent = 4
        content = json.dumps(data, indent=indent)
        return content

    def get_context(self, data, accepted_media_type, renderer_context):
        """
        Returns the context used to render.
        """
        view = renderer_context['view']
        request = renderer_context['request']
        response = renderer_context['response']

        raw_data_post_form = self.get_raw_data_form(data, view, 'POST', request)
        raw_data_put_form = self.get_raw_data_form(data, view, 'PUT', request)
        raw_data_patch_form = self.get_raw_data_form(data, view, 'PATCH', request)
        raw_data_put_or_patch_form = raw_data_put_form or raw_data_patch_form

        response_headers = OrderedDict(sorted(response.items()))
        response_headers['Content-Type'] = self.charset

        if getattr(view, 'paginator', None) and view.paginator.display_page_controls:
            paginator = view.paginator
        else:
            paginator = None

        csrf_cookie_name = settings.CSRF_COOKIE_NAME
        csrf_header_name = settings.CSRF_HEADER_NAME
        if csrf_header_name.startswith('HTTP_'):
            csrf_header_name = csrf_header_name[5:]
        csrf_header_name = csrf_header_name.replace('_', '-')
        return {
            'data': data,
            'content': self.get_content(data),
            'code_style': pygments_css(self.code_style),
            'view': view,
            'request': request,
            'response': response,
            'user': request.user,
            'description': self.get_description(view, response.status_code),
            'name': self.get_name(view),
            'version': VERSION,
            'paginator': paginator,
            'breadcrumblist': self.get_breadcrumbs(request),
            'allowed_methods': view.allowed_methods,
            'available_formats': [renderer_cls.format for renderer_cls in view.renderer_classes],
            'response_headers': response_headers,

            'put_form': self.get_rendered_html_form(data, view, 'PUT', request),
            'post_form': self.get_rendered_html_form(data, view, 'POST', request),
            'delete_form': self.get_rendered_html_form(data, view, 'DELETE', request),
            'options_form': self.get_rendered_html_form(data, view, 'OPTIONS', request),

            'raw_data_put_form': raw_data_put_form,
            'raw_data_post_form': raw_data_post_form,
            'raw_data_patch_form': raw_data_patch_form,
            'raw_data_put_or_patch_form': raw_data_put_or_patch_form,

            'display_edit_forms': bool(response.status_code != 403),

            'api_settings': api_settings,
            'csrf_cookie_name': csrf_cookie_name,
            'csrf_header_name': csrf_header_name
        }

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render the HTML for the browsable API representation.
        """
        self.accepted_media_type = accepted_media_type or ''
        self.renderer_context = renderer_context or {}
        view = renderer_context['view']
        response = renderer_context['response']
        template_name = self.get_template_name(response=response, view=view)

        template = loader.get_template(template_name)
        context = self.get_context(data, accepted_media_type, renderer_context)
        ret = template.render(context, request=renderer_context['request'])

        return ret
