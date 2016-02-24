# -*- coding: utf-8 -*-
from SilegData import SilegData

import logging

if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)
    data = SilegData()
    #result = data.getListadoDpto()
    #result = data.getListadoMateriasDpto(19)
    #result = data.getListadoMaterias()
    #result = data.getCatedras(60)
    result = data.getCuerpoDocente(16)
    for empleado in result:
        test = empleado["desig_observaciones"] if ("a/c tit." in empleado["desig_observaciones"]) else ""
        print(test)


  

