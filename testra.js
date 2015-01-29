var page = new WebPage(),
system = require('system'),
loadInProgress = false,
testindex = 0,
param, result;

page.onLoadStarted = function() {
    loadInProgress = true;
    console.log("Load started");
};

page.onLoadFinished = function() {
    loadInProgress = false;
    console.log("Load finished");
};

var steps = [function() {
    page.settings.userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.6 Safari/537.11";
    page.open("https://sedeapl.dgt.gob.es/WEB_TTRA_CONSULTA/Todos.faces?idioma=es");
}, function() {
    console.log("Enter criteria");
    page.injectJs("jquery.min.js");
    page.evaluate(function (param) {
        jQuery('input.textoBotonBuscar').val("M7441ZB");
        console.log(document.title);
    });
}, function() {
    console.log('Search');
    page.evaluate(function() {
        jQuery('form#dato').submit();
    });
}, function () {
    result = page.evaluate(function () {
        return jQuery('li.estiloCabeceraEdicto a').attr('href');
    });
    console.log('Result: ' + result);
}]

if (system.args.length !== 2) {
    console.log('Usage: testra.js param');
    phantom.exit(1);
} else {
    param = system.args[1];
    interval = setInterval(function() {
        if (!loadInProgress && typeof steps[testindex] == "function") {
            steps[testindex]();
            testindex++;
        }
        if (typeof steps[testindex] != "function") {
            window.setTimeout(function () {
                phantom.exit(0);
            }, 5000);
        }
    }, 50);
}
