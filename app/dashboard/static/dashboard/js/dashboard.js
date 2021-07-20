document.addEventListener("DOMContentLoaded", function () {
    var endpoint = "/financial/appliance/dashboard/data/chart/donut/";
    $.ajax({
        method: "GET",
        url: endpoint,
        success: function (response_data) {
            dataSeries = response_data.series;
            dataLabels = response_data.labels;

            window.ApexCharts && (new ApexCharts(document.getElementById('chart-appliance'), {
                chart: {
                    type: "pie",
                    width: "100%",
                    height: 250
                },
                series: dataSeries,
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
                labels: dataLabels,
            })).render();
        },
        error: function (error_data) {
            console.log(error_data);
        }
    });
});