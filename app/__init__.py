from flask import Flask, render_template, request, jsonify, make_response
from flask.ext.sqlalchemy import SQLAlchemy

import os
import urllib2, urllib
import csv, StringIO
import requests, json
import datetime

from utils import escape, toNum

BASE_DIR = os.path.dirname(os.path.abspath(__file__))       # we set this file as the base directory (so imports work from this point)

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')

# creating the SQL database with the schemas needed
db = SQLAlchemy(app)
from models import Competitor, FinancialStatement
db.create_all()


# Home Page
@app.route('/')
def home():
    return make_response(open('%s/index.html' % BASE_DIR).read())

# APIs

@app.route('/api/nasdaq/screener')
def nasdaqGetScreenerResults():

    ls = float(request.args.get('ls', 0)) # lastsale value
    ls_comp = request.args.get('ls_comp', '') # lastsale comparator
    mc = float(request.args.get('mc', 0)) # marketcap value
    mc_comp = request.args.get('mc_comp', '') # marketcap comparator
    sec = request.args.get('sec', '') # sector
    ind = request.args.get('ind', '') # industry 
    url = "http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download"

    scsv = urllib2.urlopen(url).read()
    f = StringIO.StringIO(scsv)
    reader = csv.reader(f, delimiter=',')

    LastSale = 2
    MarketCap = 3
    Sector = 6
    Industry = 7

    results = []
    i = 0
    for stock in reader:
        if stock[0] == 'Symbol':
            results.append(stock)
            continue
        if stock[LastSale] == 'n/a' or stock[MarketCap] == 'n/a':
            continue
        if not ls is '':
            stock_ls = float(stock[LastSale])
            if (ls_comp == 'gt' and stock_ls < ls) or (ls_comp == 'lt' and stock_ls > ls):
                continue
        if not mc is '':
            stock_mc = float(stock[MarketCap])
            if (mc_comp == 'gt' and stock_mc < mc) or (mc_comp == 'lt' and stock_mc > mc):
                print stock_mc
                continue
        if not sec is '' and sec != stock[Sector]:
            continue
        if not ind is '' and ind != stock[Industry]:
            continue

        results.append(stock)
        
    return jsonify(**{'data': results})
 
@app.route('/api/google/getAllFinances', methods=['GET'])
def googleGetAllFinances():
    """Gets the finanical statements given a ticker

    Args:
        s: ticker.
    Returns:
        the JSON of the 3 finance statements.
    """
    FS_TAGS = {
        'incannualdiv': 'IS',
        'balannualdiv': 'BS',
        'casannualdiv': 'CF'
    }

    symbol = request.args.get('s', '')

    fs = FinancialStatement.query.get(symbol)
    if not fs is None and fs.lastUpdated > datetime.datetime.now()-datetime.timedelta(minutes=60*24):
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
                "https://www.google.com/finance?q=%s&fstype=ii"
                % symbol)   # quote_plus to url encode the string

    result = {
        'IS': {},
        'BS': {},
        'CF': {}
    }
    blank_r = result

    max_retries = 3
    while max_retries != 0:
        max_retries -= 1
        r = requests.get(url)
        raw = json.loads(r.text)
        if raw['query']['count'] != 0:
            break
        else: 
            print raw

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

    if fs is None:                
        fs = FinancialStatement(symbol, json.dumps(result))
        db.session.add(fs)
    else:
        fs.fsJSON = json.dumps(result)
        fs.lastUpdated = datetime.datetime.now()
    db.session.commit()

    return jsonify(**result)

@app.route('/api/nasdaq/getCompetitors', methods=['GET'])
def nasdaqGetCompetitors():
    """Gets the tickers of the competitors given a ticker.
        Sometimes there are more than one page of competitors. 
        By default only 1 page (25 tickers) is retrived.
        The tickers are sorted by decending market capitalization.

    Args:
        s: ticker.
        p: num of pages to retrive (default 1)
    Returns:
        list of tickers as competitors
    """

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


        if raw['query']['count'] != 0:
            for competitor in raw['query']['results']['td']:
                if competitor['a']['content'] != symbol and not competitor['a']['content'] in result:
                    result.append(competitor['a']['content'])

    comps = Competitor(symbol, json.dumps(result))
    db.session.add(comps)
    db.session.commit()

    return jsonify(**{'data': result})

@app.route('/api/yahoo/getProfile', methods=['GET'])
def yahooGetProfile():
    """Gets the sector and industry given ticker

    Args:
        s: ticker
    Returns:
        a JSON object with sector and industry
    """

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

    if raw['query']['count'] == 0:
        return jsonify({
            'sector': 'N/A',
            'industry': 'N/A'
            })

    result = {
        'sector': raw['query']['results']['td'][1]['a']['content'],
        'industry': raw['query']['results']['td'][2]['a']['content']
    }
    return jsonify(**result)



# Given a list of tickers, find the stock information of each
# @param [String] s     (tickers)
# @return {'data': [...]}
@app.route('/api/yahoo/getQuotes', methods=['GET'])
def yahooGetQuotes():
    """Get stock information given a ticker

    Args:
        s: ticker
    Returns:
        a JSON object with stock data
    """

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

