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

function addToChart() {
    name = prompt("Please name this mortgage: ", "Mortgage 1");

    if (name != 'null') {
        $('#myTable').show();
        $('#myTable tr:last').after('<tr>')
            .after('<td>' + getInput('t') + '</td>')
            .after('<td>' + getInputAsPercent('r') + '</td>')
            .after('<td>' + getInput('P') + '</td>')
            .after('<td>' + name + '</td>')
            .after('</tr>');
    }
}

function submitUpdate() {
    val = buildURL();
    URL = val[0];
    term = val[1];

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
    });
}

// initial display of the chart
submitUpdate();