from . import db
import datetime


class Competitor(db.Model):

    __tablename__ = 'competitor'
    __table_args__ = {'extend_existing': True}

    ticker = db.Column(db.String(10), primary_key=True)
    competitorJSON = db.Column(db.String(250))

    def __init__(self, ticker, json):
    	self.ticker = ticker
    	self.competitorJSON = json

    def __repr__(self):
        return '<Competitor %r>' % (self.ticker)

class FinancialStatement(db.Model):

    __tablename__ = 'financial_statement'
    __table_args__ = {'extend_existing': True} 

    ticker = db.Column(db.String(10), primary_key=True)
    lastUpdated = db.Column(db.DateTime, default = datetime.datetime.now)
    fsJSON = db.Column(db.Text)

    def __init__(self, ticker, json):
    	self.ticker = ticker
    	self.fsJSON = json

    def __repr__(self):
        return '<FinancialStatement %r>' % (self.ticker)     