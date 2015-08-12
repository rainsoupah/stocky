from flask import Flask, render_template, request, jsonify, make_response
from flask.ext.sqlalchemy import SQLAlchemy

import os
import urllib2, urllib
import csv, StringIO
import requests, json

from utils import escape, toNum

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')

db = SQLAlchemy(app)
from models import Competitor, FinancialStatement

db.create_all()

@app.route('/')
def home():
    return make_response(open('%s/templates/index.html' % BASE_DIR).read())

# APIs


@app.route('/api/google/getAllFinances', methods=['GET'])
def googleGetBalanceSheet():
    FS_TAGS = {
        'incannualdiv': 'IS',
        'balannualdiv': 'BS',
        'casannualdiv': 'CF'
    }
    symbol = request.args.get('s', '')

    fs = FinancialStatement.query.get(symbol)
    if not fs is None:
        return jsonify(**json.loads(fs.fsJSON))

    url = """http://query.yahooapis.com/v1/public/yql?q=
                    select * 
                    from html 
                    where url="%s" 
                    and xpath='//div[@id="incannualdiv" or 
                                     @id="balannualdiv" or 
                                     @id="casannualdiv"]'
                &format=json
            """ % urllib.quote_plus(
                "https://www.google.com/finance?q=NASDAQ:%s&fstype=ii"
                % symbol)


    r = requests.get(url)
    raw = json.loads(r.text)

    result = {
        'IS': {},
        'BS': {},
        'CF': {}
    }

    if raw['query']['count'] != 0:
        for table in raw['query']['results']['div']:
            if not table['table']['tbody'] is None:
                for row in table['table']['tbody']['tr']:
                    tableId = FS_TAGS[table['id']]
                    dataColumn = escape(row['td'][0]['content'])
                    if 'content' in row['td'][1]:
                        content = row['td'][1]['content']
                    else:
                        content = row['td'][1]['span']['content']
                    result[tableId][dataColumn] = toNum(content)

    fs = FinancialStatement(symbol, json.dumps(result))
    db.session.add(fs)
    db.session.commit()

    return jsonify(**result)

@app.route('/api/nasdaq/getRatios', methods=['GET'])
def nasdaqGetRatios():
    symbol = request.args.get('s', '')
    url = """http://query.yahooapis.com/v1/public/yql?q=
                    select * 
                    from html 
                    where url="%s" 
                    and xpath='//div[contains(@class,"genTable")]//th/..'
                &format=json
            """ % urllib.quote_plus(
                "http://www.nasdaq.com/symbol/%s/financials?query=ratios"
                % symbol.lower())

    r = requests.get(url)
    raw = json.loads(r.text)

    result = {};

    for row in raw['query']['results']['tr']:
        if 'td' in row:
            result[row['th']['content'] if isinstance(row['th'], dict) else row['th']] = row['td'][1]

    return jsonify(**result)


@app.route('/api/nasdaq/getCompetitors', methods=['GET'])
def nasdaqGetCompetitors():
    symbol = request.args.get('s', '')
    pages = request.args.get('p', 1)
    result = []

    comps = Competitor.query.get(symbol)
    if not comps is None:
        return jsonify(**{'data': json.loads(comps.competitorJSON)})

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

        for competitor in raw['query']['results']['td']:
            if competitor['a']['content'] != symbol and not competitor['a']['content'] in result:
                result.append(competitor['a']['content'])

    comps = Competitor(symbol, json.dumps(result))
    db.session.add(comps)
    db.session.commit()

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
    QUOTES = ['d', 'j1', 'j4', 'l1', 'n', 'p5', 'p6', 'q', 'r', 'r1', 'r2', 'r5', 's', 's1', 's7', 't1', 't6', 't7', 't8', 'v', 'v1', 'v7', 'w', 'w1', 'w4', 'x', 'y']
    DESCRIPTION = [
        "Dividend/Share",
        "Market Capitalization",
        "EBITDA",
        "Last Trade (Price Only)",
        "Name",
        "Price/Sales",
        "Price/Book",
        "Ex-Dividend Date",
        "P/E Ratio",
        "Dividend Pay Date",
        "P/E Ratio (Real-time)",
        "PEG Ratio",
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

