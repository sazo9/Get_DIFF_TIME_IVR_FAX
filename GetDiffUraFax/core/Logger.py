#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Andre Sazonov - DDS Solucoes em Tecnologia.
import glob
import logging
import logging.handlers
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
LOG_FILENAME = os.path.join(BASEDIR + '/log', 'Log.log')


class OneLineExceptionFormatter(logging.Formatter):
    def formatException(self, exc_info):
        """
        Format an exception so that it prints on a single line.
        """
        result = super(OneLineExceptionFormatter, self).formatException(exc_info)
        return repr(result) # or format into one line however you want to

    def format(self, record):
        s = super(OneLineExceptionFormatter, self).format(record)
        if record.exc_text:
            s = s.replace('\n', '') + '|'
        return s
    
def configure_logging(msg):
    
    #fh = logging.FileHandler('output.txt', 'w')
    # Add the log message handler to the logger
    handler = logging.handlers.RotatingFileHandler(
                LOG_FILENAME, maxBytes=1000, backupCount=5)

    f = OneLineExceptionFormatter('%(asctime)s|%(levelname)s|%(name)s|%(message)s','%d/%m/%Y %H:%M:%S')

    handler.setFormatter(f)
    root = logging.getLogger('GETDIFF')
    root.setLevel(logging.DEBUG)
    root.addHandler(handler)

    root.info(msg)
    # See what files are created
    logfiles = glob.glob('%s*' % LOG_FILENAME)


class Logger():
    def __init__(self, msg):
        configure_logging(msg)

        

        
