
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
        var value;

        var s = $scope.data[index]['Symbol'];
        var BS = $scope.financialData[s]['BS'];
        var IS = $scope.financialData[s]['IS'];
        var CF = $scope.financialData[s]['CF'];

        // Current Ratio
        value = (BS['Total Current Assets']/BS['Total Current Liabilities']).toFixed(2);
        $scope.data[index]['Current Ratio'] = isNaN(value) ? 'N/A' : value;

        // Quick Ratio
        value = (BS['Total Current Assets']-BS['Total Inventory']/BS['Total Current Liabilities']).toFixed(2);
        $scope.data[index]['Quick Ratio'] = isNaN(value) ? 'N/A' : value;

        // Cash Conversion Cycle
        value = (((BS['Total Inventory']+BS['Total Receivables, Net']-BS['Accounts Payable'])/IS['Cost of Revenue, Total'])*365).toFixed(0);
        $scope.data[index]['Cash Conversion Cycle'] = isNaN(value) ? 'N/A' : value;

        // Cash Ratio
        value = (BS['Cash and Short Term Investments']/BS['Total Current Liabilities']).toFixed(2);
        $scope.data[index]['Cash Ratio'] = isNaN(value) ? 'N/A' : value;

        // Gross Margin
        value = ((IS['Gross Profit'])/IS['Total Revenue']).toFixed(2);
        $scope.data[index]['Gross Margin'] = isNaN(value) ? 'N/A' : value;

        // Operating Margin
        value = (IS['Operating Income']/IS['Total Revenue']).toFixed(2);
        $scope.data[index]['Operating Margin'] = isNaN(value) ? 'N/A' : value;

        // Net Profit Margin
        value = ((IS['Gross Profit']-IS['Total Operating Expense']-(IS['Income Before Tax']-IS['Income After Tax']))/IS['Total Revenue']).toFixed(2);
        $scope.data[index]['Net Profit Margin'] = isNaN(value) ? 'N/A' : value;

        // Return on Assets
        value = (IS['Net Income']/BS['Total Assets']).toFixed(2);
        $scope.data[index]['Return on Assets'] = isNaN(value) ? 'N/A' : value;

        // Return on Equity
        value = (IS['Net Income']/BS['Total Equity']).toFixed(2);
        $scope.data[index]['Return on Equity'] = isNaN(value) ? 'N/A' : value;

        // Return on Invested Capital
        value = ((IS['Net Income']-IS['Preferred Dividends'])/(BS['Total Long Term Debt']+BS['Total Equity'])).toFixed(2);
        $scope.data[index]['Return on Invested Capital'] = isNaN(value) ? 'N/A' : value;

        // Debt to Asset
        value = ((BS['Notes Payable/Short Term Debt']+BS['Total Long Term Debt'])/BS['Total Assets']).toFixed(2);
        $scope.data[index]['Debt to Asset'] = isNaN(value) ? 'N/A' : value;

        // Debt to Equity
        value = (BS['Total Liabilities']/BS['Total Equity']).toFixed(2);
        $scope.data[index]['Debt to Equity'] = isNaN(value) ? 'N/A' : value;

        // Capital Structure

        // Interest Coverage Ratio
        value = ((IS['Interest Expense(Income) - Net Operating']+IS['Interest Income(Expense), Net Non-Operating'])/IS['Income Before Tax']).toFixed(2)
        $scope.data[index]['Interest Coverage Ratio'] = isNaN(value) ? 'N/A' : value;

        // FCF to Debt
        value = (CF['Cash from Operating Activities']/(BS['Notes Payable/Short Term Debt']+BS['Total Long Term Debt'])).toFixed(2);
        $scope.data[index]['FCF to Debt'] = isNaN(value) ? 'N/A' : value;

        // Asset Turnover Ratio
        value = (IS['Total Revenue']/BS['Total Assets']).toFixed(2);
        $scope.data[index]['Asset Turnover Ratio'] = isNaN(value) ? 'N/A' : value;

        // Operating Cash Flow/Sales
        value = (CF['Cash from Operating Activities']/BS['Total Revenue']).toFixed(2);
        $scope.data[index]['Operating Cash Flow/Sales'] = isNaN(value) ? 'N/A' : value;

        // Free Cash Flow/Operating Cash
        value = ((CF['Cash from Operating Activities']-CF['Capital Expenditures'])/CF['Cash from Operating Activities']).toFixed(2);
        $scope.data[index]['Free Cash Flow/Operating Cash'] = isNaN(value) ? 'N/A' : value;

        // Cash Flow Coverage
        value = (CF['Cash from Operating Activities']/BS['Notes Payable/Short Term Debt']).toFixed(2);
        $scope.data[index]['Cash Flow Coverage'] = isNaN(value) ? 'N/A' : value;
    }
});
