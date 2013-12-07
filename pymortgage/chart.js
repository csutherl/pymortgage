var data;

d3.json("http://localhost:8080/api/amort/d3", function(error, json) {
    if (error) return console.warn(error);
    data = json;
    visualize_it();
});

function visualize_it() {
    nv.addGraph(function() {
        var chart = nv.models.lineChart()
            .x(function(d) { return d[0] })
            .y(function(d) { return d[1] });
    
        chart.xAxis
            .axisLabel("Month")
            .tickFormat(d3.format("d"));
    
        chart.yAxis
            .axisLabel("Dollars")
            .tickFormat(d3.format(",.2f"));
    
        d3.select("svg")
            .datum(data)
            .transition().duration(500).call(chart);
    
        nv.utils.windowResize(chart.update);
    
        return chart;
    });
};
