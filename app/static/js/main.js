var stocky = angular.module('stocky',['ngResource']);

stocky.controller('mainController', function($scope, yahooService) {
    $scope.ticker = "";
    $scope.tickerDisplay = "";
    $scope.profile = {};

    $scope.data = []

    $scope.go = function() {
        $scope.data = [];
        $scope.tickerDisplay = $scope.ticker;

        yahooService.getQuotes([$scope.ticker]).then(function(data) {
            $scope.data.push(data[0]);
            yahooService.getRatios($scope.ticker).then(function(data) {
                for (var attr in data.result) {
                    $scope.data[0][attr] = data.result[attr];
                }
            })
        }, handleError);

        yahooService.getProfile($scope.ticker).then(function(data) {
            $scope.profile = data;
        }, handleError);

        yahooService.getCompetitors($scope.ticker).then(function(competitors) {
            yahooService.getQuotes(competitors).then(function(data) {
                $scope.data = $scope.data.concat(data);
                for (var i = 0; i < competitors.length; i++) {
                    yahooService.getRatios(competitors[i], i).then(function(data) {
                        for (var attr in data.result) {
                            $scope.data[data.index+1][attr] = data.result[attr];
                        }
                    })
                }
            });
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
        getProfile: getProfile,
        getCompetitors: getCompetitors,
        getRatios: getRatios
    });

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