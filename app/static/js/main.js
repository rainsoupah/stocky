var stocky = angular.module('stocky',['ngResource', 'ngRoute', 'datatables', 'datatables.fixedcolumns']);


stocky.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
            when('/compAnalysis', {
                templateUrl: 'static/partials/competitor-analysis.html',
                controller: 'compAnalysisController'
            }).
            otherwise({
                redirectTo: '/compAnalysis'
            });
}]);


// I act a repository for the remote friend collection.
stocky.service( "apiHandler", function( $http, $q ) {

    // Return public API.
    return({
        getQuotes: getQuotes,
        getProfile: getProfile,
        getCompetitors: getCompetitors,
        getRatios: getRatios,
        getFinancials: getFinancials,
        getScreenerResults: getScreenerResults,
    });

    function getScreenerResults(last_price, last_price_comp, market_cap, market_cap_comp, sector, industry) {
        var request = $http.get("api/nasdaq/screener", {
            params: {
                ls: last_price,
                ls_comp: last_price_comp,
                mc: market_cap,
                mc_comp: market_cap_comp,
                sec: sector,
                ind: industry
            }
        })
        return(request.then(function(response) {
            return {result: response.data, index: i};
        }, handleError));
    }

    function getFinancials(ticker, i) {
        var request = $http.get("api/google/getAllFinances", {
            params: {s: ticker}
        })
        return(request.then(function(response) {
            return {result: response.data, index: i};
        }, handleError));
    }

    function getRatios(ticker, i) {
        var request = $http.get("api/nasdaq/getRatios", {
            params: {s: ticker}
        })
        return(request.then(function(response) {
            return {result: response.data, index: i};
        }, handleError));
    }

    function getCompetitors(ticker) {
        var request = $http.get("api/nasdaq/getCompetitors", {
            params: {s: ticker}
        })
        return(request.then(function(response) {
            return response.data.data;
        }, handleError));
    }

    function getProfile(ticker) {
        var request = $http.get("api/yahoo/getProfile", {
            params: {s: ticker}
        })
        return(request.then(function(response) {
            return response.data;
        }, handleError));
    }

    function getQuotes(tickers) {
        var request = $http({
            method: "GET",
            url: "api/yahoo/getQuotes",
            params: {
                s: tickers.join("+")
            }
        });
        return(request.then(function(response) {
            return response.data.data;
        }, handleError));
    }


    // I transform the error response, unwrapping the application dta from
    // the API response payload.
    function handleError( response ) {
        if (
            ! angular.isObject( response.data ) ||
            ! response.data.message
            ) {
            return( $q.reject( "An unknown error occurred." ) );
        }
        // Otherwise, use expected error message.
        return( $q.reject( response.data.message ) );
    }
});