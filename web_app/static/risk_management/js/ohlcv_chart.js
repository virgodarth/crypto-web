//Highcharts.getJSON('https://demo-live-data.highcharts.com/aapl-ohlcv.json', function (data) {
//
//    // split the data set into ohlc and volume
//    var ohlc = [],
//        volume = [],
//        dataLength = data.length,
//        i = 0;
//
//    for (i; i < dataLength; i += 1) {
//        ohlc.push([
//            data[i][0], // the date
//            data[i][1], // open
//            data[i][2], // high
//            data[i][3], // low
//            data[i][4] // close
//        ]);
//
//        volume.push([
//            data[i][0], // the date
//            data[i][5] // the volume
//        ]);
//    }
//
//    Highcharts.stockChart('container', {
//        yAxis: [{
//            labels: {
//                align: 'left'
//            },
//            height: '80%',
//            resize: {
//                enabled: true
//            }
//        }, {
//            labels: {
//                align: 'left'
//            },
//            top: '80%',
//            height: '20%',
//            offset: 0
//        }],
//        tooltip: {
//            shape: 'square',
//            headerShape: 'callout',
//            borderWidth: 0,
//            shadow: false,
//            positioner: function (width, height, point) {
//                var chart = this.chart,
//                    position;
//
//                if (point.isHeader) {
//                    position = {
//                        x: Math.max(
//                            // Left side limit
//                            chart.plotLeft,
//                            Math.min(
//                                point.plotX + chart.plotLeft - width / 2,
//                                // Right side limit
//                                chart.chartWidth - width - chart.marginRight
//                            )
//                        ),
//                        y: point.plotY
//                    };
//                } else {
//                    position = {
//                        x: point.series.chart.plotLeft,
//                        y: point.series.yAxis.top - chart.plotTop
//                    };
//                }
//
//                return position;
//            }
//        },
//        series: [{
//            type: 'ohlc',
//            id: 'aapl-ohlc',
//            name: 'AAPL Stock Price',
//            data: ohlc
//        }, {
//            type: 'column',
//            id: 'aapl-volume',
//            name: 'AAPL Volume',
//            data: volume,
//            yAxis: 1
//        }],
//        responsive: {
//            rules: [{
//                condition: {
//                    maxWidth: 800
//                },
//                chartOptions: {
//                    rangeSelector: {
//                        inputEnabled: false
//                    }
//                }
//            }]
//        }
//    });
//});

var seriesOptions = [],
    seriesCounter = 0,
    names = ['sma20', 'sma50', 'sma100', 'stda20', 'stda50', 'stda100'];

/**
 * Create the chart when all data is loaded
 * @returns {undefined}
 */
function createChart() {

    Highcharts.stockChart('container', {

        rangeSelector: {
            selected: 4
        },

        yAxis: {
            labels: {
                formatter: function () {
                    return (this.value > 0 ? ' + ' : '') + this.value + '%';
                }
            },
            plotLines: [{
                value: 0,
                width: 2,
                color: 'silver'
            }]
        },

        plotOptions: {
            series: {
                compare: 'percent',
                showInNavigator: true
            }
        },

        tooltip: {
            pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change}%)<br/>',
            valueDecimals: 2,
            split: true
        },

        series: seriesOptions
    });
}

function doChart(data, name) {
    var i = names.indexOf(name);
    seriesOptions[i] = {
        name: name,
        data: data
    };

    // As we're loading the data asynchronously, we don't know what order it
    // will arrive. So we keep a counter and create the chart when all the data is loaded.
    seriesCounter += 1;

    if (seriesCounter === names.length) {
        createChart();
    }
}