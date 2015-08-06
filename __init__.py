from flask import Flask, render_template, request, jsonify, make_response
app = Flask(__name__)
app.debug = True

import os
import urllib2, urllib
import csv, StringIO
import requests, json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def home():
    return make_response(open('%s/templates/index.html' % BASE_DIR).read())

# APIs

@app.route('/api/nasdaq/getCompetitors', methods=['GET'])
def nasdaqGetCompetitors():
    symbol = request.args.get('s', '')
    pages = request.args.get('p', 2)
    result = []

    for page in xrange(1, int(pages+1)):
        url = """http://query.yahooapis.com/v1/public/yql?q=
                        select * 
                        from html 
                        where url="%s" 
                        and xpath='//td[contains(@class,"TalignL")]'&format=json
                    &format=json
                """ % urllib.quote_plus(
                    "http://www.nasdaq.com/symbol/%s/competitors?sortname=marketcapitalizationinmillions&sorttype=1&page=%d"
                    % (symbol.lower(), page))

        r = requests.get(url)
        raw = json.loads(r.text)
        print raw
        for competitor in raw['query']['results']['td']:
            if competitor['a']['content'] != symbol and not competitor['a']['content'] in result:
                result.append(competitor['a']['content'])

    return jsonify(**{'data': result})

@app.route('/api/yahoo/getProfile', methods=['GET'])
def yahooGetProfile():
    symbol = request.args.get('s', '')

    url = """http://query.yahooapis.com/v1/public/yql?q=
                    select * 
                    from html 
                    where url="http://finance.yahoo.com/q/pr?s=%s" 
                    and xpath='//td[contains(@class,"yfnc_tabledata1")]'
                &format=json
            """ % (symbol)

    r = requests.get(url)
    raw = json.loads(r.text)

    result = {
        'sector': raw['query']['results']['td'][1]['a']['content'],
        'industry': raw['query']['results']['td'][2]['a']['content']
    }
    return jsonify(**result)

@app.route('/api/yahoo/getQuotes', methods=['GET'])
def yahooGetQuotes():
    QUOTES = ['a', 'a2', 'a5', 'b', 'b2', 'b3', 'b4', 'b6', 'c', 'c1', 'c3', 'c6', 'c8', 'd', 'd1', 'd2', 'e', 'e1', 'e7', 'e8', 'e9', 'f6', 'g', 'h', 'j', 'k', 'g1', 'g3', 'g4', 'g5', 'g6', 'i', 'i5', 'j1', 'j3', 'j4', 'j5', 'j6', 'k1', 'k2', 'k3', 'k4', 'k5', 'l', 'l1', 'l2', 'l3', 'm', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'n', 'n4', 'o', 'p', 'p1', 'p2', 'p5', 'p6', 'q', 'r', 'r1', 'r2', 'r5', 'r6', 'r7', 's', 's1', 's7', 't1', 't6', 't7', 't8', 'v', 'v1', 'v7', 'w', 'w1', 'w4', 'x', 'y']
    DESCRIPTION = [
        "Ask",
        "Average Daily Volume",
        "Ask Size",
        "Bid",
        "Ask (Real-time)",
        "Bid (Real-time)",
        "Book Value",
        "Bid Size",
        "Change & Percent Change",
        "Change",
        "Commission",
        "Change (Real-time)",
        "After Hours Change (Real-time)",
        "Dividend/Share",
        "Last Trade Date",
        "Trade Date",
        "Earnings/Share",
        "Error Indication (returned for symbol changed / invalid)",
        "EPS Estimate Current Year",
        "EPS Estimate Next Year",
        "EPS Estimate Next Quarter",
        "Float Shares",
        "Day's Low",
        "Day's High",
        "52-week Low",
        "52-week High",
        "Holdings Gain Percent",
        "Annualized Gain",
        "Holdings Gain",
        "Holdings Gain Percent (Real-time)",
        "Holdings Gain (Real-time)",
        "More Info",
        "Order Book (Real-time)",
        "Market Capitalization",
        "Market Cap (Real-time)",
        "EBITDA",
        "Change From 52-week Low",
        "Percent Change From 52-week Low",
        "Last Trade (Real-time) With Time",
        "Change Percent (Real-time)",
        "Last Trade Size",
        "Change From 52-week High",
        "Percebt Change From 52-week High",
        "Last Trade (With Time)",
        "Last Trade (Price Only)",
        "High Limit",
        "Low Limit",
        "Day's Range",
        "Day's Range (Real-time)",
        "50-day Moving Average",
        "200-day Moving Average",
        "Change From 200-day Moving Average",
        "Percent Change From 200-day Moving Average",
        "Change From 50-day Moving Average",
        "Percent Change From 50-day Moving Average",
        "Name",
        "Notes",
        "Open",
        "Previous Close",
        "Price Paid",
        "Change in Percent",
        "Price/Sales",
        "Price/Book",
        "Ex-Dividend Date",
        "P/E Ratio",
        "Dividend Pay Date",
        "P/E Ratio (Real-time)",
        "PEG Ratio",
        "Price/EPS Estimate Current Year",
        "Price/EPS Estimate Next Year",
        "Symbol",
        "Shares Owned",
        "Short Ratio",
        "Last Trade Time",
        "Trade Links",
        "Ticker Trend",
        "1 yr Target Price",
        "Volume",
        "Holdings Value",
        "Holdings Value (Real-time)",
        "52-week Range",
        "Day's Value Change",
        "Day's Value Change (Real-time)",
        "Stock Exchange",
        "Dividend Yield"
    ]

    symbols = request.args.get('s', '')

    url = "http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s" % (
            symbols,
            "".join(QUOTES)
        )

    scsv = urllib2.urlopen(url).read()

    results = [];

    f = StringIO.StringIO(scsv)
    reader = csv.reader(f, delimiter=',')
    for data in reader:
        result = {}
        for i, datapoint in enumerate(data):
            result[DESCRIPTION[i]] = datapoint
        results.append(result)

    return jsonify(**{'data': results})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
