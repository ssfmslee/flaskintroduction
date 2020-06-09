#!/usr/bin/env python
from ftplib import FTP
from datetime import datetime
from datetime import timedelta
from time import sleep
from statistics import mean

import math
import sys
import os

from snowfort import db
from snowfort.blueprints.data.models import Datum
from snowfort.blueprints.motes.models import Mote
from snowfort.blueprints.sensors.models import Sensor
from snowfort.blueprints.stations.models import Station
from snowfort.blueprints.users.models import User

# For SQLite Development Database
# if not os.path.exists("snowfort/development.db"):
#   print "You need to have set up the development.db first!"
#   print "Create yourself or use demo.py"
#   sys.exit(1)


class name():
    def __init__(self, fileMoteInfo):
        self.extractFeature = lambda f_name: f_name.readline().split('#')[0].replace(' ','')
        
        self.ftpAddress = ''
        self.ftpUser = ''
        self.ftpPassword = ''
        self.attributeIdx = {}
        self.attribute ={}
        self.attributeAvg ={}
        self.NumLine = 10   # # of header lines
        self.pst2utc = timedelta(hours=7)
        self.Date = (datetime.utcnow() - self.pst2utc).day

        with open(fileMoteInfo) as fp_MOTE:
            self.moteName = self.extractFeature(fp_MOTE)
            self.moteId = self.extractFeature(fp_MOTE)
            self.pathRemote = self.extractFeature(fp_MOTE)
            self.pathLocal = self.extractFeature(fp_MOTE)
            self.fileNameFormat = self.extractFeature(fp_MOTE)
        
        self.mote = Mote.query.get(self.moteId)
        
        print('\nMote info:')    
        print(self.moteName, self.moteId)
        print(self.pathRemote)
        print(self.pathLocal)
        print(self.fileNameFormat)

    def addattribute(self, attribute, idxInFile):
        self.attribute[attribute] = []
        self.attributeIdx[attribute] = idxInFile

    def connectToFtp(self, fileFtpKey):
        with open(fileFtpKey) as fp_FTP:
            self.ftpAddress = self.extractFeature(fp_FTP)
            self.ftpUser = self.extractFeature(fp_FTP)
            self.ftpPassword = self.extractFeature(fp_FTP)
        
        print('\nFTP info:')
        print(self.ftpAddress)
        print(self.ftpUser, self.ftpPassword)

        self.ftp = FTP(self.ftpAddress)
        self.ftp.login(user=self.ftpUser, passwd=self.ftpPassword)
        self.ftp.set_pasv(True)


    def readFromFtp(self):
        time = datetime.utcnow() - self.pst2utc
        strDate = str(time.strftime("%Y-%m-%d"))
        self.fileRemote = self.pathRemote + self.fileNameFormat.replace('DATE',strDate)
        self.fileLocal = self.pathLocal + self.fileNameFormat.replace('DATE',strDate)
        self.fileLocalAvg = self.pathLocal + self.fileNameFormat.replace('DATE',strDate+'_avg')
        # print(strDate)
        # print(self.fileRemote)
        # print(self.fileLocal)
        # print(self.fileLocalAvg)
        

        with open(self.fileLocal,'w') as fp:
            # print('Retrieving remote data attempted')
            self.ftp.retrlines('RETR ' + self.fileRemote, lambda s, w=fp.write: w(s+'\n'))
            # print('Retrieving remote data done')


    def addToMysql(self):

        with open(self.fileLocal,'r') as fp:
            lineCount = 0
            for line in fp:
                lineCount+=1            
                if(lineCount > self.NumLine):
                    self.NumLine = lineCount
                    line_split = line.split(',')
                    try:
                        time = datetime.strptime(line_split[0], '"%Y-%m-%d %H:%M:%S"')
                        for qty in self.attribute:
                            self.attribute[qty].append(float(line_split[self.attributeIdx[qty]]))
                        if((time.second %10 == 0)):
                            message = str(time)
                            for qty in self.attribute:
                                datum = Datum(qty, round(mean(self.attribute[qty]),2), time+self.pst2utc, self.mote.tag)
                                db.session.add(datum)
                                message += ', '+str(round(mean(self.attribute[qty]),2))
                                self.attribute[qty] = []
                            print self.moteName,message, self.NumLine
                            os.system("echo "+message+" >> "+self.fileLocalAvg)
                            db.session.commit()
                    except Exception as e: 
                        print(e)
                        continue





