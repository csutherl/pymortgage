function getTerm(URL) {
    if (URL.indexOf("year") != -1)
        return "Year";
    else
        return "Month";
}

function getLineChart(name, data) {
    var lc = nv.models.lineChart()
        .x(function(d) { return d[0] })
        .y(function(d) { return d[1] });

    lc.xAxis
        .axisLabel(getTerm(URL))
        .tickFormat(d3.format("d"));

    lc.yAxis
        .axisLabel("Dollars")
        .tickFormat(d3.format(",.2f"));

    d3.select(name)
        .datum(data)
        .transition().duration(500).call(lc);

    nv.utils.windowResize(lc.update);

    return lc;
}

function getStackedChart(name, data) {
    var sc = nv.models.multiBarChart()
        .x(function(d) { return d[0] })
        .y(function(d) { return d[1] });

    sc.stacked(true);

    sc.xAxis
        .axisLabel(getTerm(URL))
        .tickFormat(d3.format("d"));

    sc.yAxis
        .axisLabel("Dollars")
        .tickFormat(d3.format(",.2f"));

    d3.select(name)
        .datum(data)
        .transition().duration(500).call(sc);

    nv.utils.windowResize(sc.update);

    return sc;
}

var URL =  "http://localhost:4001/api/d3/amort?r=.0425&P=245000&n=360&t=1836&i=1056";
d3.json(URL, function(error, data) {
    if (error) return console.warn(error);

    nv.addGraph(getLineChart("#thirtyyr svg", data));
    nv.addGraph(getStackedChart("#thirtyyr-stacked svg", data));
});

URL =  "http://localhost:4001/api/d3/amort?r=.0425&P=245000&n=360&t=1836&i=1056&af=2&ac=.01&lc=.06";
d3.json(URL, function(error, data) {
    if (error) return console.warn(error);

    nv.addGraph(getLineChart("#twentyyr svg", data));
    nv.addGraph(getStackedChart("#twentyyr-stacked svg", data));
});

URL =  "http://localhost:4001/api/d3/amort?r=.0425&P=245000&n=360&t=1836&i=1056&af=2&ac=.01&lc=.06&e=100";
d3.json(URL, function(error, data) {
    if (error) return console.warn(error);

    nv.addGraph(getLineChart("#twentyyr-adj svg", data));
    nv.addGraph(getStackedChart("#twentyyr-adj-stacked svg", data));
});
