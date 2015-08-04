var stocky = angular.module('stocky',['ngResource']);

stocky.controller('mainController', function($scope, yahooService) {
    $scope.ticker = "";

    $scope.data = []

    $scope.go = function() {
        yahooService.getQuotes([$scope.ticker]).then(function(data) {
            $scope.data.push(data[0]);
            console.log($scope.data);
        }, 
        function(error) {
            alert(error);
            console.log(error);
        });
    }
});

// I act a repository for the remote friend collection.
stocky.service( "yahooService", function( $http, $q ) {

    // Return public API.
    return({
        getQuotes: getQuotes,
    });

    function getQuotes(tickers) {
        var request = $http({
            method: "GET",
            url: "/api/yahoo/getQuotes",
            params: {
                s: tickers.join("+")
            }
        });
        return( request.then( handleSuccess, handleError ) );
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

    // I transform the successful response, unwrapping the application data
    // from the API response payload.
    function handleSuccess( response ) {
        return( response.data.data );
    }
});