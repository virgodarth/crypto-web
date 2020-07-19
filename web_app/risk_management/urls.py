from django.urls import path
from risk_management import views

urlpatterns = [
    # path('config/', views.BotConfigurationView.as_view(), name='bot-config'),
    path('visualizer/<str:ticker>/', views.RiskChartView.as_view(), name='chart-detail'),
]
