#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Andre Sazonov - DDS Solucoes em Tecnologia.

import Monitor as mon

def main():

        try:
            while True:
                diff = mon.compareTime(mon.getHoraURA(), mon.getHoraFaxServer())
                mon.logDiff(str(diff))
                mon.initProgress()
               # time.sleep(float( tempoEspera))

        except KeyboardInterrupt:
            mon.setRed()
            print '\r---->>> FALHA NA EXECUCAO!!!\n'

if __name__ == '__main__':
    main()