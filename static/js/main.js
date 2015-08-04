var stocky = angular.module('stocky',['ngResource']);

stocky.controller('mainController', function($scope, yahooService) {
    $scope.ticker = "";
    $scope.profile = {};

    $scope.data = []

    $scope.go = function() {
        $scope.data = [];

        yahooService.getQuotes([$scope.ticker]).then(function(data) {
            $scope.data.push(data[0]);
        }, handleError);

        yahooService.getProfile($scope.ticker).then(function(data) {
            $scope.profile = data;
        }, handleError);
    }

    var handleError = function(error) {
        alert(error);
        console.log(error);
    }
});

// I act a repository for the remote friend collection.
stocky.service( "yahooService", function( $http, $q ) {

    // Return public API.
    return({
        getQuotes: getQuotes,
        getProfile: getProfile
    });

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