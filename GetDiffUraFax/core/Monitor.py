#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Andre Sazonov - DDS Solucoes em Tecnologia.

import time
import sys
import subprocess
import datetime
import os
import telnetlib
import datetime as dt
import color_console as cons
import logging
import Logger as _log
import ConfigParser as cp
import pysftp

logging.basicConfig(level=logging.ERROR,format='%(asctime)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
BASEDIR = os.path.abspath(os.path.dirname(__file__))
LOG_FILENAME = os.path.join(BASEDIR + '\\log', 'diff.properties')

logging.info('teste')

default_colors = cons.get_text_attr()
default_bg = default_colors & 0x0070

def setYellow():
    cons.set_text_attr(cons.FOREGROUND_YELLOW | default_bg | cons.FOREGROUND_INTENSITY)

def setGreen():
    cons.set_text_attr(cons.FOREGROUND_GREEN | default_bg)

def setRed():
    cons.set_text_attr(cons.FOREGROUND_RED | default_bg)

def setGray():
    cons.set_text_attr(cons.FOREGROUND_INTENSITY | default_bg | cons.FOREGROUND_INTENSITY)

setGray()
print("\rLoading Busca Diff Fax Ura.")

#CARREGA CONTEUDO DO ARQUIVO DE CONFIGURACAO
config = cp.ConfigParser()
config.read('\\config\\roboConfig.config')

# CARREGA VARIAVEIS DO ARQUIVO roboConfig.config
print('\rCarregando arquivo de configuracao.')
host = config.get('URA', 'host')
password = config.get('URA', 'password')
username = config.get('URA', 'username')
hostFAX = config.get('FAXSERVER', 'host')
portaFAX = config.get('FAXSERVER', 'port')
tempoEspera = config.get('CONFIG', 'tempoEspera')

def isExisteDiffLog():
    try:
        if os.path.exists(BASEDIR + '\\log'):
            return True
        else:
            return False
    except Exception, e:
        setRed()
        "Error: %s - %s." % (e.filename,e.strerror)

if isExisteDiffLog() == False:
    os.mkdir(BASEDIR + '\\log')


def getExt(filename):
    #Get the file extension.
    return os.path.splitext(filename)[-1].lower()

def get_now():
    #Get the current date and time as a string
    return datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

# ACESSA O FAX SERVER VIA TELNET PARA PEGAR HORA LOCAL
def getHoraFaxServer(aux=None):
    ret = '15:20:20'
    if  aux == 'teste':
        tn = telnetlib.Telnet(hostFAX, portaFAX)
        tn.write("ls\n")
        tn.write("exit\n")
        lst = str(tn.read_all()).split(' ')
        tmp = lst[11].split(':')
        aux = str(int(tmp[0]) - 3)
        tmp = aux + ':'+tmp[1]+':'+tmp[2]
        print 'HORA FAX: ' + str(tmp)
        return tmp
    else:
        tmp = ret.split(':')
        aux = str(int(tmp[0]) - 3)
        tmp = aux + ':'+tmp[1]+':'+tmp[2]
        return tmp

# ACESSA A URA VIA SFTP PARA PEGAR HORA LOCAL
def getHoraURA(aux=None):
    if  aux == 'teste':
        print("\rIniciando captura de data e hora da URA.\n")
        with pysftp.Connection(host, username=username, password=password) as sftp:
            lst = str(sftp.execute('date')).split(' ')
            sftp.close()
            print 'HORA URA: ' + str(lst[4])

        return lst[4]
    else:
        return '12:20:40'

# COMPARA A HORA DA URA COM A HORA DO FAX E RETORNA A DIFERENCA EM SEGUNDOS
def compareTime(start, end):
    
    if len(start) > 0 and len(end) > 0:
        try:
            start_dt = dt.datetime.strptime(start, '%H:%M:%S')
            end_dt = dt.datetime.strptime(end, '%H:%M:%S')
            diff = (end_dt - start_dt) 

            if str(diff).find('-1 day') == 0:
                diff = (start_dt - end_dt) 
            
            return diff.seconds
        except Exception, e:
            setRed()
            
            "\rError: %s - %s." % (e.filename,e.strerror)


def progress(count, total, suffix=''):
    setYellow()
    bar_len = 45
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s %s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()  # As suggested by Rom Ruben

def initProgress():
    i = 0
    total = 100
    while i < total:
        progress(i, total, 'Buscando Diferencas.')
        time.sleep(float(tempoEspera))  # emulating long-playing job
        i += 1



def logDiff(msg=None):


    setRed()
    print '\n---> DIFERENCA ENTRE A URA E O FAX: %s SEGUNDOS.\n' % (msg)
    setYellow()
    with open(LOG_FILENAME, 'w') as f:
        f.write(str('diff=' + msg))

class Teste():
    
    def run_tests():
        "Run unit tests with unittest."
        print >> sys.stderr, "Running unit tests at %s" % get_now()
        os.chdir(BASEDIR)
        subprocess.call(r'python -m unittest discover -b')

def main():

        try:
            while True:
                diff = compareTime(getHoraURA(), getHoraFaxServer())
                logDiff(str(diff))
                initProgress()
               # time.sleep(float( tempoEspera))

        except KeyboardInterrupt:
            setRed()
            print '\r---->>> FALHA NA EXECUCAO!!!\n'
            observer.stop()

        observer.join()


if __name__ == '__main__':
    main()
