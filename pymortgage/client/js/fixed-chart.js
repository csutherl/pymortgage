var indexedSet = [];
var selectedRow = 'null';

function buildURL() {
//    var base_URL =  "http://10.13.153.78:4001/api/d3/amort";
//    var base_URL =  "http://10.10.55.54:4001/api/d3/amort";
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

    // monthly extra
    var extra = "&e=" + getInput('e');

    URL = base_URL + rate + prin + num + taxes + ins + extra;

    if ($('#arm_type').is(':checked')) {
        var adj_freq = "&af=" + getAdjFreq();
        var adj_cap = "&ac=" + getAdjCapDec();
        var life_cap = "&lc=" + getLifetimeCapDec();

        URL += adj_freq + adj_cap + life_cap;
    }

    return [URL, term];
}

function addToChart(add) {
//    var name = prompt("Please name this mortgage: ", "Mortgage 1");
    var name = getInput('name');
    add = typeof add !== 'undefined' ? add : true;

    if (name != 'null' && !checkName(name)) {
        // show table after adding first row
        $('#myTable').show();

        <!-- my clickable rows :) Need to implement some select action on click that way you can remove/update the chart's data -->
        $('#myTable tr:last').after('<tr onclick=selectRow(' + indexedSet.length +'); id=row_' + indexedSet.length + '>' +
            '<td id=\'name\'>' + name + '</td>' +
            '<td id=\'P\'>' + getPrin() + '</td>' +
            '<td id=\'r\'>' + getRate() +
            '%</td>' + '<td id=\'n\'>' + getTerm() + '</td>' +
            '</tr>');

        // build index for mortgage
        var mort = getFormState();
        mort['name'] = name;
        indexedSet.push(mort);

        submitUpdate(name, add);
    } else {
        alert('Please add a unique or non-null name.');
    }
}

// TODO: Can probably create a loop that goes through the form and grabs each input id instead of indivduals.
// Doing that would make the form state capture more automated.
function getFormState() {
    var json = { 'formstate': {
        'name': getInput('name'),
        'P': getPrin(),
        'r': getRate(),
        'n': getTerm(),
        'i': getIns(),
        't': getTax(),
        'af': getAdjFreq(),
        'ac': getAdjCap(),
        'lc': getLifetimeCap(),
        'e': getInput('e'),
        'fixed_type': $('#fixed_type').is(':checked'),
        'arm_type': $('#arm_type').is(':checked'),
        'termbtn': $('#termbtn').html()
    }};
    console.debug("Form state: " + JSON.stringify(json));

    return json;
}

function selectRow(rowNum) {
    // set the global selected row (indexedSet index)
    selectedRow = rowNum;

    // update form with selected row
    var temp = indexedSet[selectedRow]['formstate'];
    for (var key in temp) {
        // Added this check to fix issue #6. Now the form updates completely.
        switch (key) {
            case 'termbtn':
                $('#' + key).html(temp[key]);
                break;
            case 'fixed_type':
            case 'arm_type':
                $('#' + key).prop('checked', temp[key]);
                break;
            default:
                setInput(key, temp[key]);
        }
    }
}

function updateCurrentRow() {
    // Update the table row
    // grab the indexed data and set the form according to the row selected
    var temp = indexedSet[selectedRow];
    console.debug("Old row: " + JSON.stringify(temp));
    var new_set = getFormState();
    // set name on the top level of the array
    new_set['name'] = new_set['formstate']['name'];
    new_set['data'] = temp['data']; // transpose data to new set
    console.debug("New row: " + JSON.stringify(new_set));

    // update table
    $('#row_' + selectedRow).each(function() {
        $(this).find('td').each(function() {
            var id = $(this).attr('id');
            $(this).text(new_set['formstate'][id]);

            // add a % sign to the rate cell
            if (id == 'r') {
                $(this).text(new_set['formstate'][id] + "%");
            }
        });
    });

    // update index
    indexedSet[selectedRow] = new_set;
}

function checkName(name) {
    for (var i in indexedSet) {
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
    } else {
        alert("Please select a row to update or add a mortgage to the chart.");
    }
}

function getDataSet() {
    var temp = [];

    for (var key in indexedSet) {
        var data = indexedSet[key]['data'];

        for (var dkey in data) {
            temp.push(data[dkey]);
        }
    }

    return temp;
}

function submitUpdate(name, add) {
    // default for name
    name = typeof name !== 'undefined' ? name : "";
    add = typeof add !== 'undefined' ? add : false;

    var val = buildURL();
    var URL = val[0];
    var term = val[1];
    console.debug("Update URL: " + URL);

    d3.json(URL, function(error, json) {
        if (error) return console.warn(error);

        if (add) {
            var dataSet = [];
            json.forEach(function(d) {
                var new_key = name + " " + d['key'];
                console.debug("Old key: " + d['key'] + " New key: " + new_key);
                d['key'] = new_key;

                dataSet.push(d);
            });

            for (var key in indexedSet) {
                if (name == indexedSet[key]['name']) {
                    indexedSet[key]['data'] = dataSet;
                    console.debug("Added data to set: " + JSON.stringify(indexedSet[key]));
                }
            }
        } else {
            updateCurrentRow();

            indexedSet[selectedRow]['data'] = [];
            json.forEach(function(d) {
                var new_key = indexedSet[selectedRow]['name'] + " " + d['key'];
                console.debug("Old key: " + d['key'] + " New key: " + new_key);
                d['key'] = new_key;

                indexedSet[selectedRow]['data'].push(d);
            });
        }

        nv.addGraph(function() {
            var chart1 = nv.models.lineChart()
//                .margin({top: 0, right: 100, bottom: 50, left: 100})
                .x(function(d) { return d[0] })
                .y(function(d) { return d[1] });

            chart1.xAxis
                .axisLabel(term)
                .tickFormat(d3.format("d"));

            chart1.yAxis
                .axisLabel("Dollars")
                .tickFormat(d3.format(",.2f"));

            d3.select("#chart1 svg")
                .datum(getDataSet())
                .transition().duration(500).call(chart1);

            nv.utils.windowResize(chart1.update);

            return chart1;
        });
    });
}
