// base form functions
function getInput(name) {
    return $('#' + name).val();
}

function setInput(name, value) {
    return $('#' + name).val(value);
}

function getInputAsDecimal(name) {
    return getInput(name) / 100;
}

// extended get functions
function getRate() {
    return getInput('r');
}

function getRateDec() {
    return getInputAsDecimal('r');
}

function getPrin() {
    return getInput('P');
}

function getTerm() {
    return getInput('n');
}

function getTax() {
    return getInput('t');
}

function getIns() {
    return getInput('i');
}

function getAdjFreq() {
    return getInput('af');
}

function getAdjCap() {
    return getInput('ac');
}

function getAdjCapDec() {
    return getInputAsDecimal('ac');
}

function getLifetimeCap() {
    return getInput('lc');
}

function getLifetimeCapDec() {
    return getInputAsDecimal('lc');
}

// extended set functions
function setRate(value) {
    setInput('r', value);
}
function setPrin(value) {
    setInput('P', value);
}
function setTerm(value) {
    setInput('n', value);
}
function setTax(value) {
    setInput('t', value);
}
function setIns(value) {
    setInput('i', value);
}
function setAdjFreq(value) {
    setInput('af', value);
}
function setAdjCap(value) {
    setInput('ac', value);
}
function setLifetimeCap(value) {
    setInput('lc', value);
}
