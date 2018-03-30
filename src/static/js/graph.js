var req = new XMLHttpRequest()
req.onreadystatechange = function() {
    if (req.readyState == 4) {
        if (req.status != 200) {
            //error handling code here
            console.log("error")
        } else {
            var response = JSON.parse(req.responseText)

            if (response.status !== "OK") {
                console.log("err")
                document.getElementById('chart-area').innerHTML = "<p class='error'>Error: could not find that username</p>"
                return
            }

            var commitAmounts = response.commit_amounts;
            var series = [];

            for (var key in commitAmounts) {
                series.push({
                    name: key,
                    data: commitAmounts[key],
                    date: new Date(Date.parse(key.split("/")[0] + " 1, " + key.split("/")[1]))
                });
            }

            series.sort(function(a, b) {
                return new Date(a.date).getTime() - new Date(b.date).getTime()
            });

            var container = document.getElementById('chart-area');
            var data = {
                categories: response.unique_dates,
                series: series
            };
            var options = {
                chart: {
                    width: 1160,
                    height: 540,
                    title: 'Total Commits Per Month'
                },
                yAxis: {
                    title: 'Commit Amount',
                    pointOnColumn: true
                },
                xAxis: {
                    title: 'Month',
                    type: 'datetime',
                    dateFormat: 'MMM'
                },
                series: {
                    showDot: false,
                    zoomable: true
                },
                legend: {
                    showCheckbox: true,
                    visible: true
                }
            };

            var chart = tui.chart.lineChart(container, data, options);
        }
    }
}

req.open("POST", 'graph/' + document.querySelector("#githubUsername").getAttribute("data-name"), true);
req.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
req.send()