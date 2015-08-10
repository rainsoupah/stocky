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

class FinancialStatement(db.Model):

    __tablename__ = 'balance_sheet'

    ticker = db.Column(db.String(10), primary_key=True)
    fsJSON = db.Column(db.Text)

    def __init__(self, ticker, json):
    	self.ticker = ticker
    	self.fsJSON = json

    def __repr__(self):
        return '<FinancialStatement %r>' % (self.ticker)     