var dataSet = [];
var indexedSet = [];
var selectedRow = 'null';

function buildURL() {
//    var base_URL =  "http://10.13.153.78:4001/api/d3/amort";
    var base_URL =  "http://localhost:4001/api/d3/amort";

    var term = $('#termbtn').text();
    if (term.indexOf("Year") != -1)
        base_URL += '/year?';
    else
        base_URL += "?";

    var rate = "r=" + getRateDec();
    var prin = "&P=" + getPrin();
    var num = "&n=" + getTerm();
    var taxes = "&t=" + getTax();
    var ins = "&i=" + getIns();

    URL = base_URL + rate + prin + num + taxes + ins;

    if ($('#arm_type').is(':checked')) {
        var adj_freq = "&af=" + getAdjFreq();
        var adj_cap = "&ac=" + getAdjCapDec();
        var life_cap = "&lc=" + getLifetimeCapDec();

        URL += adj_freq + adj_cap + life_cap;
    }

    return [URL, term];
}

function addToChart(add) {
    name = prompt("Please name this mortgage: ", "Mortgage 1");
    add = typeof add !== 'undefined' ? add : true;

    if (name != 'null' && !checkName(name)) {
        var name_without_spaces = name.replace(/\s+/g, ';;;');
        $('#myTable').show();
        <!-- my clickable rows :) Need to implement some select action on click that way you can remove/update the chart's data -->
//        $('#myTable tr:last').after('<tr onclick=selectRow(\'' + name_without_spaces +'\');>' + '<td>' + name + '</td>' + '<td>' + getPrin() + '</td>' + '<td>' + getRate() + '%</td>' + '<td>' + getTerm() + '</td>' + '</tr>');
        $('#myTable tr:last').after('<tr onclick=selectRow(' + indexedSet.length +'); id=' + name_without_spaces + '>' + '<td id=\'name\'>' + name + '</td>' + '<td id=\'P\'>' + getPrin() + '</td>' + '<td id=\'r\'>' + getRate() +
            '%</td>' + '<td id=\'n\'>' + getTerm() + '</td>' + '</tr>');

        // build index for mortgage
        var mort = getFormState();
        mort['name'] = name;
        indexedSet.push(mort);

        submitUpdate(name, add);
    }
}

function getFormState() {
    var json = {'P': getPrin(), 'r': getRate(), 'n': getTerm(), 'i': getIns(), 't': getTax(), 'af': getAdjFreq(), 'ac': getAdjCap(), 'lc': getLifetimeCap()};
    console.debug("Form state: " + JSON.stringify(json));

    return json;
}

function selectRow(rowNum) {
    // set the global selected row (indexedSet index)
    selectedRow = rowNum;

    // update form with selected row
    var temp = indexedSet[selectedRow];
    for (key in temp) {
        setInput(key, temp[key]);
    }
}

function updateCurrentRow() {
    // grab the indexed data and set the form according to the row selected
    var temp = indexedSet[selectedRow];
    console.debug("Old row: " + JSON.stringify(temp));
    var name = temp['name'];
    var new_set = getFormState();
    new_set['name'] = name;
    console.debug("New row: " + JSON.stringify(new_set));

    // update table
    $('#myTable tr').each(function() {
        if ($(this).attr('id') == name.replace(/\s+/g, ';;;')) {
            $(this).find('td').each(function() {
                var id = $(this).attr('id');
                $(this).text(new_set[id]);

                // add a % sign to the rate cell
                if (id == 'r') {
                    $(this).text(new_set[id] + "%");
                }
            });
        }
    });

    // update index
    indexedSet[selectedRow] = new_set;
}

function checkName(name) {
    for (i in indexedSet) {
        if (name == indexedSet[i]['name']) {
            return true;
        }
    }

    return false;
}

function tryUpdate() {
    if (selectedRow != 'null') {
        // only update when  row is selected
        submitUpdate();
        // we should also save the data to the indexedSet and update the table row as well here
        updateCurrentRow();
    } else {
        alert("Please select a row to update or add a mortgage to the chart.");
    }
}

function submitUpdate(name, add) {
    // default for name
    name = typeof name !== 'undefined' ? name : "";
    add = typeof add !== 'undefined' ? add : false;

    val = buildURL();
    URL = val[0];
    term = val[1];
    console.debug("Update URL: " + URL);

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
            <!-- Will need to change this else to handle selecting a row, then updating its data -->
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