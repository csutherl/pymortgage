function updateChart() {
    var base_URL =  "http://localhost:8080/api/d3/amort";

    var term = $('#termbtn').text();
    if (term.indexOf("Year") != -1)
        base_URL = base_URL + '/year';

    var params = "?";

    var rate = "r=" + ($('#r').val() / 100);
    var prin = "&P=" + $('#P').val();
    var num = "&n=" + $('#n').val();
    var taxes = "&t=" + $('#t').val();
    var ins = "&i=" + $('#i').val();

    URL = base_URL + params + rate + prin + num + taxes + ins;

    if ($('#arm_type').is(':checked')) {
        var adj_freq = "&af=" + $('#af').val();
        var adj_cap = "&ac=" + ($('#ac').val() / 100);
        var life_cap = "&lc=" + ($('#lc').val() / 100);

        URL = URL + adj_freq + adj_cap + life_cap;
    }

    d3.json(URL, function(error, json) {
        if (error) return console.warn(error);
        var data = json;

        nv.addGraph(function() {
            var chart1 = nv.models.lineChart()
                .x(function(d) { return d[0] })
                .y(function(d) { return d[1] });

            chart1.xAxis
                .axisLabel(term)
                .tickFormat(d3.format("d"));

            chart1.yAxis
                .axisLabel("Dollars")
                .tickFormat(d3.format(",.2f"));

            d3.select("#chart1 svg")
                .datum(data)
                .transition().duration(500).call(chart1);

            nv.utils.windowResize(chart1.update);

            return chart1;
        });

        nv.addGraph(function() {
            var chart2 = nv.models.multiBarChart()
                .x(function(d) { return d[0] })
                .y(function(d) { return d[1] });

            chart2.stacked(true);

            chart2.xAxis
                .axisLabel(term)
                .tickFormat(d3.format("d"));

            chart2.yAxis
                .axisLabel("Dollars")
                .tickFormat(d3.format(",.2f"));

            d3.select("#chart2 svg")
                .datum(data)
                .transition().duration(500).call(chart2);

            nv.utils.windowResize(chart2.update);

            return chart2;
        });
    });
}

// initial display of the chart
updateChart();