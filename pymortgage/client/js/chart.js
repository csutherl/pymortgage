var indexedSet = [];
var selectedRow = -1;
var selectedRowID = 'null';
var rowCounter = 0;

function buildURL() {
    var base_URL = "/api/d3/amort";

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
    var name = getInput('name');
    add = typeof add !== 'undefined' ? add : +1;

    if (name != 'null' && !checkName(name)) {
        // show table after adding first row
        $('#mortgages-table').show();

        // my clickable rows :)
        // Need to implement some select action on click that way you can remove/update the chart's data
        $('#mortgages-table tbody').append('<tr onclick=selectRow(this); id=row_' + rowCounter + '>' +
            '<td id=\'name\'>' + name + '</td>' +
            '<td id=\'P\'>' + parseFloat(getPrin()).formatCurrency() + '</td>' +
            '<td id=\'r\'>' + getRate() +
            '%</td>' + '<td id=\'n\'>' + getTerm() + '</td>' +
            '</tr>');

        // build index for mortgage
        var mort = getFormState();
        mort['name'] = name;
        indexedSet.push(mort);

        // add chart title - this was duplicating it, duh...
        // $("#chart1").prepend("<div class=\"chart-title\">Chart title here :)</div>");
        submitUpdate(name, add);

        // add collapsible group for amortization table tab
        addTableCollapse('row_' + rowCounter + '_table', name);

        // add collapsible group for amortization summary tab
        addSummaryCollapse('row_' + rowCounter + '_summary', name);

        // increment row counter to keep IDs unique
        rowCounter++;
    } else {
        alert('Please add a unique or non-null name.');
    }
}

function removeFromChart() {
    // if there is a row selected
    if (selectedRow >= 0) {
        // remove the row
        $('#' + selectedRowID).remove();

        // if the table only contains the header row, hide it again
        if ($('#mortgages-table tr').length == 1) {
            $('#mortgages-table').hide();
        }

        // remove it from the indexedSet
        indexedSet.splice(selectedRow, 1);

        // remove the collapsible group from table tab
        $('#' + selectedRowID + '_table').parent().remove();

        // remove the collapsible group from summary tab
        $('#' + selectedRowID + '_summary').parent().remove();

        // remove data from chart
        submitUpdate('', -1);

        // deselect row since the selectedRow since it no longer exists
        selectedRow = -1;
    } else {
        alert("Please select a row to remove.");
    }
}

// TODO: Can probably create a loop that goes through the form and grabs each input id instead of individuals.
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

function selectRow(tr) {
    selectedRowID = $(tr).attr('id');
    var mortgage_name = '';

    // iterate the td elements in the row and grab the name
    $(tr).find('td').each(function () {
        if ($(this).attr('id') == 'name') {
            mortgage_name = $(this).text();
        }
    });

    for (i = 0; i < indexedSet.length; i++) {
        if (indexedSet[i]['name'] == mortgage_name) {
            selectedRow = i;
        }
    }

    console.debug("Selected row: " + selectedRow);
    console.debug("Selected row id: " + selectedRowID);

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
                // this fires the click method when the saved value of the button is true; thereby causing the arm_type
                // fields to hide as they do when you click the fixed button.
//                if (temp[key]) {
//                    $('#' + key).click();
//                }
                // this way sets the checked property of the radio button
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
    $('#row_' + selectedRow).each(function () {
        $(this).find('td').each(function () {
            var id = $(this).attr('id');
            $(this).text(new_set['formstate'][id]);

            switch (id) {
                case 'r':
                    $(this).text(new_set['formstate'][id] + "%");
                    break;
                case 'P':
                    $(this).text(parseFloat(new_set['formstate'][id]).formatCurrency());
                    break;
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
    if (selectedRow >= 0) {
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

function updateTableTab() {
    // clear the table
    $('#' + selectedRowID + '_table-summary').empty();
    // repopulate the table by calling the api
    populateTableCollapse(selectedRowID + '_table');
}

function updateSummaryTab() {
    // clear the table
    $('#' + selectedRowID + '_summary-summary').empty();
    // repopulate the table by calling the api
    populateSummaryCollapse(selectedRowID + '_summary');
}

function submitUpdate(name, change) {
    // default for name
    name = typeof name !== 'undefined' ? name : "";
    change = typeof change !== 'undefined' ? change : 0;

    var val = buildURL();
    var URL = val[0];
    var term = val[1];
    console.debug("Update URL: " + URL);

    d3.json(URL, function (error, json) {
        if (error) return console.warn(error);

        // myAddGraph was a good first step but I still need to figure out how to iterate over indexedDB items and graph
        switch (change) {
            // case remove
            case -1:
                // do nothing here b/c the call to getDataSet() will basically add in all the data from indexedSet
                if (indexedSet.length == 0) {
                    // hacky solution b/c of issue 349 open against nvd3 (old data still shows when no data presented).
                    // just remove the svg for now...might need to add a no data message or something here.
                    $('#chart1 svg').remove();
                    $('#chart1').append('<svg id=\"chart-svg\" class=\"chart\"/>');
                }
                break;
            // case add
            case +1:
                $('#chart1').prepend("<div>SVG Title</div>");
                var dataSet = [];
                json.forEach(function (d) {
                    // add mortgage name to key
//                    var new_key = name + " " + d['key'];
//                    console.debug("Old key: " + d['key'] + " New key: " + new_key);
//                    d['key'] = new_key;

                    dataSet.push(d);
                });

                for (var key in indexedSet) {
                    if (name == indexedSet[key]['name']) {
                        indexedSet[key]['data'] = dataSet;
//                    console.debug("Added data to set: " + JSON.stringify(indexedSet[key]));
                    }
                }
                break;
            // case update
            case 0:
            // purposeful fall through
            default:
                updateCurrentRow();

                indexedSet[selectedRow]['data'] = [];
                json.forEach(function (d) {
                    // add mortgage name to key
//                    var new_key = indexedSet[selectedRow]['name'] + " " + d['key'];
//                    console.debug("Old key: " + d['key'] + " New key: " + new_key);
//                    d['key'] = new_key;

                    indexedSet[selectedRow]['data'].push(d);
                });

                updateTableTab();
                updateSummaryTab();
                break;
        }

        nv.addGraph(myAddGraph("chart1", term));
    });
}

function myAddGraph(name, term) {
    // this adds the stupid block that is causing the other tabs to display funny
    $('#chart-pane').show(); // show chart pane before rendering

    var chart = nv.models.lineChart()
        .useInteractiveGuideline(true)
        .margin({left: 100})
        .x(function (d) {
            return d[0]
        })
        .y(function (d) {
            return d[1]
        });

    chart.xAxis
        .axisLabel(term)
        .tickFormat(d3.format("d"));

    chart.yAxis
        //.axisLabel("Dollars") // removing this since I can use currency now :)
        .tickFormat(d3.format("$,.2f"));

    d3.select("#" + name + " svg")
        .datum(getDataSet())
        .transition().duration(500).call(chart);

    nv.utils.windowResize(chart.update);

    // remove the block style that was breaking the view...
    $('#chart-pane').removeAttr('style');

    return chart;
}

function addTableCollapse(id, name) {
    addCollapse('table-pane-accordion', id, name);
    populateTableCollapse(id);
}

function addSummaryCollapse(id, name) {
    addCollapse('summary-pane-accordion', id, name);
    populateSummaryCollapse(id);
}

function addCollapse(accord, id, name) {
    $('#' + accord).append("<div class=\"panel panel-default\"> \
        <div class=\"panel-heading\"> \
            <h4 class=\"panel-title\"> \
                <a data-toggle=\"collapse\" data-parent=\"#" + accord + "\" href=\"#" + id + "\"> \
                " + name + " \
                </a> \
            </h4> \
        </div> \
        <div id=\"" + id + "\" class=\"panel-collapse collapse in\"> \
            <div class=\"panel-body\"> \
                <table class=\"table table-bordered table-hover\" id=\"" + id + "-summary\"></table>\
            </div> \
        </div> \
    </div>");
//    $('#' + id).collapse('toggle'); // collapse by default
}

function populateTableCollapse(id) {
    var url_term = buildURL();
    var url = url_term[0].replace('d3/', '');
    var term = url_term[1].trim();

    $.getJSON(url, function (data) {
        var summary_selector = $('#' + id + '-summary').append('<thead><tr>' +
            '<td>' + term + '</td>' +
            '<td>Balance</td>' +
            '<td>Amount</td>' +
            '<td>Principal</td>' +
            '<td>Interest</td>' +
            '<td>Extra Payment</td>' +
            '</thead></tr>');
        $.each(data['table'], function (key, val) {
            var row = '<tbody><tr>' +
                '<td>' + val[term.toLowerCase()] + '</td>' +
                '<td>' + val['balance'].formatCurrency() + '</td>' +
                '<td>' + val['amount'].formatCurrency() + '</td>' +
                '<td>' + val['principal'].formatCurrency() + '</td>' +
                '<td>' + val['interest'].formatCurrency() + '</td>' +
                '<td>' + val['extra payment'].formatCurrency() + '</td>' +
                '</tr></tbody>'
            summary_selector.append(row);
        });
    });
}

function populateSummaryCollapse(id) {
    var url_term = buildURL();
    var url = url_term[0].replace('d3/', '');

    $.getJSON(url, function (data) {
        var summary_selector = $('#' + id + '-summary').append('<thead><tr>' +
            '<td>90% LTV</td>' +
            '<td>80% LTV</td>' +
            '<td>Total Amount Paid</td>' +
            '<td>Total Extra Payment Paid</td>' +
            '<td>Total Principal Paid</td>' +
            '<td>Total Interest Paid</td>' +
            '</thead></tr>');
        var val = data['summary'];
        var row = '<tbody><tr>' +
            '<td>' + val['90% ltv'].formatCurrency() + '</td>' +
            '<td>' + val['80% ltv'].formatCurrency() + '</td>' +
            '<td>' + val['total amount'].formatCurrency() + '</td>' +
            '<td>' + val['total extra payment'].formatCurrency() + '</td>' +
            '<td>' + val['total principal'].formatCurrency() + '</td>' +
            '<td>' + val['total interest'].formatCurrency() + '</td>' +
            '</tr></tbody>'
        summary_selector.append(row);
    });
}

Number.prototype.formatCurrency = function (n, x) {
    if (n == undefined) n = 2;
    var re = '\\d(?=(\\d{' + (x || 3) + '})+' + (n > 0 ? '\\.' : '$') + ')';
    return '$' + this.toFixed(Math.max(0, ~~n)).replace(new RegExp(re, 'g'), '$&,');
};