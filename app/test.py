import csv
import urllib2

url = "http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download"
response = urllib2.urlopen(url)
table = csv.reader(response)

for row in table:
	print row[2]

