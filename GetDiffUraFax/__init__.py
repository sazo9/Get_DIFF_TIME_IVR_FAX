#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Andre Sazonov - DDS Solucoes em Tecnologia.

import subprocess
import os
import sys
import datetime
import core.Monitor

BASEDIR = os.path.abspath(os.path.dirname(__file__))
def get_now():
    #Get the current date and time as a string
    return datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

print >> sys.stderr, "Running unit tests at %s" % get_now()
os.chdir(BASEDIR)
subprocess.call(r'python -m unittest discover -b')

def main():

        try:
            while True:
                diff = mon.compareTime(mon.getHoraURA(), mon.getHoraFaxServer())
                mon.logDiff(str(diff))
                mon.initProgress()
               # time.sleep(float( tempoEspera))

        except BaseException, e:
            mon.setRed()
            mon.log('ERRO--> ' + e.message)
            print '\r---->>> FALHA NA EXECUCAO!!!\n'

if __name__ == '__main__':
    main()