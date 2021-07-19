document.addEventListener("DOMContentLoaded", function () {
    var endpoint = "/financial/dashboard/month/data/chart/";
    $.ajax({
        method: "GET",
        url: endpoint,
        success: function (response_data) {
            dataSeries = response_data.series;
            dataLabels = response_data.labels;
            window.ApexCharts && (new ApexCharts(document.getElementById('chart-asset-liability-month-pie'), {
                chart: {
                    type: "donut",
                    width: "100%",
                    height: 300,
                },
                series: dataSeries,
                colors: ['#028c6a', '#990f44'],
                responsive: [{
                    breakpoint: 480,
                    options: {
                        chart: {
                            width: "100%",
                        },
                        legend: {
                            position: 'bottom'
                        }
                    }
                }],
                legend: {
                    position: 'bottom',
                },
                labels: dataLabels,
            })).render();
        },
        error: function (error_data) {
            console.log(error_data);
        }
    });
});