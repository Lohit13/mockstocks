from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import sys, logging, os, csv
from game.models import *

class Command(BaseCommand):
    help = 'Import news data\n'

    def handle(self, *args, **options):
        read()

def read():
	companies = []
	f = open('news', 'rt')
	for i in range(10):
		line = f.readline()
		News(news=line).save()
	
if __name__ == '__main__':
	pass