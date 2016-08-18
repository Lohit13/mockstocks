from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import sys, logging, os, csv
from game.models import *

class Company1:
	def __init__(self,name,ticker,ind,profit,shares,init,bookvalue,curprice,dayhi,daylo,close,netchange,yearhi,yearlo,pe,volume):
		self.name = name
		self.ticker = ticker
		self.ind = ind
		self.profit = profit
		self.shares = shares
		self.init = init
		self.bookvalue = bookvalue 
		self.curprice = curprice
		self.dayhi = dayhi
		self.daylo = daylo
		self.close = close
		self.netchange = netchange
		self.yearhi = yearhi
		self.yearlo = yearlo
		self.pe = pe
		self.volume = volume


class Command(BaseCommand):
    help = 'Import company data\n'

    def handle(self, *args, **options):
        read()

def read():
	companies = []
	f = open('companies', 'rt')
	try:
	    reader = csv.reader(f)
	    for row in reader:
	        companies.append(Company1(str(row[0]),str(row[1]),str(row[2]),int(row[3]),int(row[4]),int(row[5]),int(row[6]),int(row[7]),int(row[8]),int(row[9]),int(row[10]),int(row[11]),int(row[12]),int(row[13]),int(row[14]),int(row[15])))
	finally:
	    f.close()
	for c in companies:
		Company(name=c.name,ticker=c.ticker,industry=c.ind,profit=c.profit,shares=c.shares,initshares=c.init,bookvalue=c.bookvalue,curprice=c.curprice,dayhi=c.dayhi,daylo=c.daylo,close=c.close,netchange=c.netchange,yearhi=c.yearhi,yearlo=c.yearlo,peratio=c.pe,volumes=c.volume).save()

if __name__ == '__main__':
	pass
