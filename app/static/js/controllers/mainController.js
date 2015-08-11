
stocky.controller('mainController', function($scope, yahooService) {
    $scope.ticker = "";
    $scope.tickerDisplay = "";
    $scope.profile = {};

    $scope.data = []
    $scope.financialData = {};

    $scope.go = function() {
        $scope.data = [];
        $scope.tickerDisplay = $scope.ticker;

        yahooService.getQuotes([$scope.ticker]).then(function(data) {
            $scope.data.push(data[0]);
            yahooService.getFinancials($scope.ticker, 0).then(function(data) {
                $scope.financialData[$scope.ticker] = data.result;
                parseFinancials(0);
            })
        }, handleError);

        yahooService.getProfile($scope.ticker).then(function(data) {
            $scope.profile = data;
        }, handleError);

        yahooService.getCompetitors($scope.ticker).then(function(competitors) {
            yahooService.getQuotes(competitors).then(function(data) {
                $scope.data = $scope.data.concat(data);
                for (var i = 0; i < competitors.length; i++) {
                    yahooService.getFinancials(competitors[i], i).then(function(data) {
                        $scope.financialData[competitors[data.index]] = data.result;
                        parseFinancials(data.index+1);
                    })
                }
            }); 
        }, handleError);
    }

    var handleError = function(error) {
        alert(error);
        console.log(error);
    }

    var parseFinancials = function(index) {

        var s = $scope.data[index]['Symbol'];
        var BS = $scope.financialData[s]['BS'];
        var IS = $scope.financialData[s]['IS'];
        var CF = $scope.financialData[s]['CF'];
        console.log($scope.financialData[s]);

        // Current Ratio
        if (!(isNum(BS['Total Current Assets']) && isNum(BS['Total Current Liabilities']))) {
            $scope.data[index]['Current Ratio'] = 'N/A';
        } else {
            $scope.data[index]['Current Ratio'] = (toNum(BS['Total Current Assets'])/toNum(BS['Total Current Liabilities'])).toFixed(3);
        }

        // Quick Ratio
        if (!(isNum(BS['Total Current Assets']) 
            && isNum(BS['Total Inventory']) 
            && isNum(BS['Total Current Liabilities']))) {
            $scope.data[index]['Quick Ratio'] = 'N/A';
        } else {
            $scope.data[index]['Quick Ratio'] = (toNum(BS['Total Current Assets'])-toNum(BS['Total Inventory'])/toNum(BS['Total Current Liabilities'])).toFixed(3);
        }

        // Cash Conversion Cycle
        // http://www.investopedia.com/articles/06/cashconversioncycle.asp
    }

    var isNum = function(s) {
        if (s == undefined) return false;
        return !isNaN(s.replace(',', ''));
    }
    var toNum = function(s) {
        return Number(s.replace(',', ''));
    }
});
