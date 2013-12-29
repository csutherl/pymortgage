d3.json("http://localhost:8080/api/amort/d3", function(error, json) {
    if (error) return console.warn(error);
    var data = json;

    nv.addGraph(function() {
        var chart1 = nv.models.lineChart()
            .x(function(d) { return d[0] })
            .y(function(d) { return d[1] });

        chart1.xAxis
            .axisLabel("Month")
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
            .axisLabel("Month")
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