stocky.controller('screenerController', function($scope, apiHandler) {
    $scope.formData = {};

    $scope.resultFilters = {};
    $scope.data = []

    // gets all data after clicking the 'go' button
    $scope.go = function() {
    	$scope.resultFilters = $scope.formData;

        apiHandler.getScreenerResults($scope.resultFilters).then(function(data) {
        	console.log(data);
        	data.result.splice(0, 1);
        	$scope.data = data.result;
        });
    }

});