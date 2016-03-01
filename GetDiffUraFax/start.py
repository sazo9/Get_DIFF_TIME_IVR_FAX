#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__  = "Andre Sazonov <andre.sazonov@gmail.com>"
__status__  = "homologando"
__version__ = "0.1"
__date__    = "01 Marco 2016"

import subprocess
import os
import sys
import datetime
import Monitor

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