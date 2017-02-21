#!/usr/bin/env python3

# Usage: ./csv_to_pass.py test.csv

import csv
import itertools
import sys
from subprocess import Popen, PIPE
import os

class Entry(object):
        def __init__(self,row,root="Racine"):
                self.row = row
                self.root = root
                self.login = None
                self.password = None
                self.url = None
                self.notes = None
                self.parse_row()

        def parse_row(self):
                self.folder = self.row[0][len(self.root):]
                self.name = self.row[1]
                self.path = os.path.join(self.folder,self.name)
                if self.row[2]:
                        self.login = self.row[2]
                if self.row[3]:
                        self.password = self.row[3]
                if self.row[4]:
                        self.url = self.row[4]
                if self.row[5]:
                        self.notes = self.row[5]

        def pass_import(self):
                if self.login:
                        self.insert_pass(os.path.join(self.path,"login"),self.login)
                if self.password:
                        self.insert_pass(os.path.join(self.path,"password"),self.password)
                if self.url:
                        self.insert_pass(os.path.join(self.path,"url"),self.url)
                if self.notes:
                        self.insert_pass(os.path.join(self.path,"notes"),self.notes,True)

        def insert_pass(self,path,value,multiline=False):
                print path
                if multiline:
                        p = Popen(['pass','insert','--multiline', path], stdin=PIPE, stdout=PIPE)
                        p.communicate("%s\n" % (value,))
                else:
                        p = Popen(['pass','insert',path],stdin=PIPE,stdout=PIPE)
                        p.communicate("%s\n%s\n" % (value,value))
                p.wait()

        def __str__(self):
                return "path:%r login:%r pass:%r url:%r notes:%r" % (self.path,self.login,self.password,self.url,self.notes)

def pass_import_entry(path, data):
	""" Import new password entry to password-store using pass insert command """
        print "path:%r data:%r" % (path,data)
	proc = Popen(['pass', 'insert', '--multiline', path], stdin=PIPE, stdout=PIPE)
	proc.communicate(data)
	proc.wait()

def readFile(filename):
	""" Read the file and proccess each entry """
	with open(filename, 'rU') as csvIN:
		next(csvIN)
		outCSV=(line for line in csv.reader(csvIN, dialect='excel'))
		for row in outCSV:
                        e = Entry(row)
                        e.pass_import()

def main(argv):
	inputFile = sys.argv[1]
	print("File to read: " + inputFile)
	readFile(inputFile)


main(sys.argv)
