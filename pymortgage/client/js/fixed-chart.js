var dataSet = [];

function getInput(name) {
    return $('#' + name).val();
}
function getInputAsPercent(name) {
    return getInput(name) / 100;
}

function buildURL() {
    var base_URL =  "http://localhost:4001/api/d3/amort";

    var term = $('#termbtn').text();
    if (term.indexOf("Year") != -1)
        base_URL += '/year?';
    else
        base_URL += "?";

    var rate = "r=" + getInputAsPercent('r'); // $('#r').val() / 100);
    var prin = "&P=" + getInput('P'); // $('#P').val();
    var num = "&n=" + getInput('n'); // $('#n').val();
    var taxes = "&t=" + getInput('t'); // $('#t').val();
    var ins = "&i=" + getInput('i'); //$('#i').val();

    URL = base_URL + rate + prin + num + taxes + ins;

    if ($('#arm_type').is(':checked')) {
        var adj_freq = "&af=" + getInput('af'); // $('#af').val();
        var adj_cap = "&ac=" + getInputAsPercent('ac'); // $('#ac').val() / 100);
        var life_cap = "&lc=" + getInputAsPercent('lc'); // $('#lc').val() / 100);

        URL += adj_freq + adj_cap + life_cap;
    }

    return [URL, term];
}

function addToChart(add) {
    name = prompt("Please name this mortgage: ", "Mortgage 1");
    add = typeof add !== 'undefined' ? add : true;

    if (name != 'null') {
        $('#myTable').show();
        $('#myTable tr:last').after('<tr>')
            .after('<td>' + getInput('t') + '</td>')
            .after('<td>' + getInputAsPercent('r') + '</td>')
            .after('<td>' + getInput('P') + '</td>')
            .after('<td>' + name + '</td>')
            .after('</tr>');

        submitUpdate(name, add);
    }
}

function submitUpdate(name, add) {
    // default for name
    name = typeof name !== 'undefined' ? name : "";
    add = typeof add !== 'undefined' ? add : false;

    val = buildURL();
    URL = val[0];
    term = val[1];

    d3.json(URL, function(error, json) {
        if (error) return console.warn(error);

        if (add) {
            json.forEach(function(d) {
                var new_key = name + " " + d['key'];
                console.debug("Old key: " + d['key'] + " New key: " + new_key);
                d['key'] = new_key;

                dataSet.push(d);
            });
        } else {
            dataSet = json;
        }

        console.info("Length " + dataSet.length);

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
                .datum(dataSet)
                .transition().duration(500).call(chart1);

            nv.utils.windowResize(chart1.update);

            return chart1;
        });
    });
}

// initial display of the chart
//submitUpdate();