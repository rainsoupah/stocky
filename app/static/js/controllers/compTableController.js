stocky.controller('compTableController', function($scope, DTOptionsBuilder, DTColumnDefBuilder) {
 
    $scope.dtInstance = {};

    $scope.tableOptions =  DTOptionsBuilder.newOptions()
        .withOption('scrollY', '450px')
        .withOption('scrollX', '100%')
        .withOption('paging', false)
        .withOption('scrollCollapse', true)
        .withOption('bSort', false)
        .withOption('bFilter', false)
        .withFixedColumns({
            leftColumns: 1
        });

    $scope.tableColumnDefs = [
        DTColumnDefBuilder.newColumnDef(0)      // ticker
            .notSortable(),
        DTColumnDefBuilder.newColumnDef(1)      // Market Capitalization
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(2)     // Stock Price
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(3)     // 52 Week Range
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(4)     // Short Interest Ratio
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(5)     // Current Ratio
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(6)     // Quick Ratio
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(7)     // Cash Conversion Cycle
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(8)     // Cash Ratio
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(9)     // Gross Profit Margin
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(10)    // Operating Profit Margin
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(11)    // Net Profit Margin
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(12)    // Return on Assets
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(13)    // Return on Equity
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(14)    // Return on Invested Capital
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(15)    // Debt to Asset
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(16)    // Debt to Equity
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(17)    // Capital Structure
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(18)    // Interest Coverage Ratio
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(19)    // FCF to Debt
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(20)    // Asset Turnover Ratio
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(21)    // Operating Cycle
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(22)    // Inventory Cycle
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(23)    // Operating Cash Flow/Sales
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(24)    // Free Cash Flow / Operating Cash
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(25)    // Cash Flow Coverage
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(26)    // Dividend/Share
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(27)    // Price/Book
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(28)    // P/E (Forward, Trailing)
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(29)    // P/E to Growth
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(30)    // Price/Sales
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(31)    // Price/NAV
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(32)    // Dividend Yield
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(33)    // Cash Flow Coverage
            .withOption('defaultContent', 'N/A'),
        DTColumnDefBuilder.newColumnDef(34)     // EV/EBITDA
            .withOption('defaultContent', 'N/A')
    ]


});