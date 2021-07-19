document.addEventListener("DOMContentLoaded", function () {
    var endpoint = "/financial/dashboard/day/data/chart/";
    $.ajax({
        method: "GET",
        url: endpoint,
        success: function (response_data) {
            dataSeries = response_data.series;
            dataLabels = response_data.labels;
            dataColors = response_data.colors;
            window.ApexCharts && (new ApexCharts(document.getElementById('chart-asset-liability-per-day'), {
                chart: {
                    type: "line",
                    fontFamily: 'inherit',
                    height: 300,
                    dropShadow: {
                        enabled: true,
                        color: '#000',
                        top: 18,
                        left: 7,
                        blur: 10,
                        opacity: 0.2
                    },
                    toolbar: {
                        show: false
                    },
                    zoom: {
                        enabled: false
                    }
                },
                dataLabels: {
                    enabled: true,
                },
                stroke: {
                    curve: 'smooth'
                },
                grid: {
                    borderColor: '#e7e7e7',
                    row: {
                        colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
                        opacity: 0.5
                    },
                },
                markers: {
                    size: 1
                },
                series: dataSeries,
                // labels: dataLabels,
                colors: dataColors,
                xaxis: {
                    categories: dataLabels,
                },

            })).render();
        },
        error: function (error_data) {
            console.log(error_data);
        }
    });
});