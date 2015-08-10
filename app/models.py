from app import db


class Competitor(db.Model):

    __tablename__ = 'competitor'
    
    ticker = db.Column(db.String(10), primary_key=True)
    competitorJSON = db.Column(db.String(250))

    def __init__(self, ticker, json):
    	self.ticker = ticker
    	self.competitorJSON = json

    def __repr__(self):
        return '<Competitor %r>' % (self.ticker)

class BalanceSheet(db.Model):

    __tablename__ = 'balance_sheet'

    ticker = db.Column(db.String(10), primary_key=True)
    bsJSON = db.Column(db.String(500))

    def __init__(self, ticker, json):
    	self.ticker = ticker
    	self.bsJSON = json

    def __repr__(self):
        return '<BalanceSheet %r>' % (self.ticker)   


class IncomeStatement(db.Model):

    __tablename__ = 'income_statement'

    ticker = db.Column(db.String(10), primary_key=True)
    isJSON = db.Column(db.String(500))

    def __init__(self, ticker, json):
    	self.ticker = ticker
    	self.isJSON = json

    def __repr__(self):
        return '<IncomeStatement %r>' % (self.ticker)   