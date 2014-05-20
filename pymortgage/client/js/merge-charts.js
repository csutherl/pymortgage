function getTerm(URL) {
    if (URL.indexOf("year") != -1)
        return "Year";
    else
        return "Month";
}

function getLineChart(URL, name, data) {
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

function getStackedChart(URL, name, data) {
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

function mergeData(keys, ds0, ds1) {
    var new_set = [];

    for (var i=0; i < ds0.length; i++) {
        var l = ds0[i];
        for (var j=0; j < keys.length; j++) {
            if (l['key'].toLowerCase() === keys[j].toLowerCase()) {
               l['key'] = "DS0-".concat(l['key'])
                new_set.push(l)
            }
        }
    }

    for (var i=0; i < ds1.length; i++) {
        l = ds1[i];
        for (var j=0; j < keys.length; j++) {
            if (l['key'].toLowerCase() === keys[j].toLowerCase()) {
                l['key'] = "DS1-".concat(l['key'])
                new_set.push(l)
            }
        }
    }

    return new_set
}

function visualizeIt(){
    var base_URL = "http://localhost:8080/api/d3/amort";
    var range = ""; //"/1/61";

    var twentyyr_data;
    var twentyyr_extra_data;

    var twentyyr_URL =  base_URL.concat(range, "?r=.045&P=245000&n=360&t=1836&i=1056&af=5&ac=.02&lc=.06");
    d3.json(twentyyr_URL, function(error, data) {
        if (error) return console.warn(error);
        twentyyr_data = data;

//        var twentyyr_extra_URL = base_URL.concat(range, "?r=.0425&P=245000&n=360&t=1836&i=1056&af=2&ac=.01&lc=.06");
        var twentyyr_extra_URL =  base_URL.concat(range, "?r=.045&P=245000&n=360&t=1836&i=1056&af=5&ac=.02&lc=.06&e=250");
        d3.json(twentyyr_extra_URL, function(error, extra_data) {
            if (error) return console.warn(error);
            twentyyr_extra_data = extra_data;

            // now that we have both data sets, we can merge them and graph
            var balance_data = mergeData(['balance'], twentyyr_data, twentyyr_extra_data);
            nv.addGraph(getLineChart(twentyyr_extra_URL, "#compare-twentyyr-balance svg", balance_data));

            var other_data = mergeData(['principal', 'amount', 'interest'], twentyyr_data, twentyyr_extra_data);
            nv.addGraph(getLineChart(twentyyr_extra_URL, "#compare-twentyyr-other svg", other_data));
            nv.addGraph(getStackedChart(twentyyr_extra_URL, "#compare-twentyyr-other-stacked svg", other_data));
        });
    });
}

visualizeIt();