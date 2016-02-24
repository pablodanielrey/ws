# -*- coding: utf-8 -*-
from ladon.ladonizer import ladonize
from ladon.types.ladontype import LadonType

import json
from SilegData import SilegData
from SilegTypes import *


class SilegWS(object):

    def __init__(self):
        self.sileg = SilegData()

    @ladonize(rtype=MateriaList)
    def getMaterias(self):
        materias = self.sileg.getListadoMaterias()
        result = MateriaList()
        result.materias = []
        for materia in materias:
            m = Materia()
            m.id = materia["materia_id"]
            m.nombre = materia["materia_nombre"]
            result.materias.append(m)
        return result

    @ladonize(int, rtype=MateriaList)
    def getMateriasDpto(self, idDepartamento):
        materias = self.sileg.getListadoMateriasDpto(idDepartamento)
        result = MateriaList()
        result.materias = []
        for materia in materias:
            m = Materia()
            m.id = materia["materia_id"]
            m.nombre = materia["materia_nombre"]
            result.materias.append(m)
        return result

    @ladonize(rtype=DepartamentoList)
    def getDepartamento(self):
        departamentos = self.sileg.getListadoDpto()
        result = DepartamentoList()
        result.departamentos = []
        for departamento in departamentos:
            d = Departamento()
            d.id = departamento["dpto_id"]
            d.nombre = departamento["dpto_nombre"]
            result.departamentos.append(d)
        return result

    @ladonize(int, rtype=CatedraList)
    def getCatedras(self, idMateria):
        catedras = self.sileg.getCatedras(idMateria)
        result = CatedraList()
        result.catedras = []
        for catedra in catedras:
            c = Catedra()
            c.id = catedra["catxmat_id"]
            c.nombre = catedra["catedra_nombre"]
            result.catedras.append(c)
        return result

    def _defineEmpleado(self, empleadoData, idCatedra):
        e = Empleado()
        e.idCatedra = idCatedra
        e.observacion = empleadoData["observacion"]
        e.idEmpleado = empleadoData["pers_id"]
        e.nombre = empleadoData["nombre"]
        e.apellido = empleadoData["apellido"]
        e.numeroDocumento = empleadoData["pers_nrodoc"]
        e.tipoDocumento = empleadoData["tipodoc_descripcion"]
        e.cargo = empleadoData["tipocargo_nombre"]
        e.titulo = empleadoData["titulo"]
        return e

    def _defineEmpleadoData(self, empleadoData, empleadoDataOld = None):

        #si tiene cargados titulos de posgrado, tendran mayor prioridad que los titulos "generales" solo si se encuentran en la siguiente lista, si no se encuentran en la siguiente lista, entonces se dara prioridad a los titulos "generales"
        titulosPosgrados = ("Dr.", "Dr.Cs.Ecs.", "Dr.en Administraci\363n", "Mg.", "M.Sc.", "MBA.", "Lic.");

        empleado = empleadoData if not empleadoDataOld else empleadoDataOld

        if "observacion" not in empleado:
            empleado["observacion"] = ""

        if "titulo" not in empleado:
            empleado["titulo"] = ""


        if "posgrado" not in empleado:
            empleado["posgrado"] = 0


        if "a/c tit." in empleadoData["desig_observaciones"]:
            empleado["observacion"] = "A cargo de la titularidad"

        if not empleadoData["titposemp_titulo_abrev"]:
            if not empleado["titulo"] or empleado["posgrado"] <= 0:
                empleado["titulo"] = empleadoData["titgenerico_abrev"] if empleadoData["titgenerico_abrev"] else ""

        else:
            empleado["titulo"] = empleadoData["titposemp_titulo_abrev"]
            empleado["posgrado"] = titulosPosgrados.index(empleado["titulo"]) if empleado["titulo"] in titulosPosgrados else 0

        return empleado

    @ladonize(int, rtype=EmpleadoList)
    def getCuerpoDocente(self, idCatedra):
        empleados = self.sileg.getCuerpoDocente(idCatedra)
        result = EmpleadoList()
        result.empleados = []

        if len(empleados) < 1:
            return result

        idEmpleadoAnterior = empleados[0]["empleado_id"]

        empleadoData = self._defineEmpleadoData(empleados[0])

        for empleado in empleados:
            if empleado["empleado_id"] == idEmpleadoAnterior:
                #redefinir empleado con los nuevos valores
                empleadoData = self._defineEmpleadoData(empleadoData, empleado)

            else:
                e = self._defineEmpleado(empleadoData, idCatedra) #definir Empleado
                result.empleados.append(e) #agregar Empleado
                empleadoData = self._defineEmpleadoData(empleado) #definir nuevos datos de empleado

            idEmpleadoAnterior = empleado["empleado_id"]

        e = self._defineEmpleado(empleadoData, idCatedra) #definir ultimo Empleado
        result.empleados.append(e) #agregar ultimoEmpleado

        return result

    @ladonize(int, str, rtype=EmpleadoList)
    def getCuerpoDocenteCargo(self, idCatedra, cargo):
        empleados = self.sileg.getCuerpoDocenteCargo(idCatedra, cargo)
        result = EmpleadoList()
        result.empleados = []

        if len(empleados) < 1:
            return result

        idEmpleadoAnterior = empleados[0]["empleado_id"]
        empleadoData = self._defineEmpleadoData(empleados[0])

        for empleado in empleados:
            if empleado["empleado_id"] == idEmpleadoAnterior:
                #redefinir empleado con los nuevos valores
                empleadoData = self._defineEmpleadoData(empleadoData, empleado)

            else:
                e = self._defineEmpleado(empleadoData, idCatedra) #definir Empleado
                result.empleados.append(e) #agregar Empleado
                empleadoData = self._defineEmpleadoData(empleado) #definir nuevos datos de empleado

            idEmpleadoAnterior = empleado["empleado_id"]

        e = self._defineEmpleado(empleadoData, idCatedra) #definir ultimo Empleado
        result.empleados.append(e) #agregar ultimoEmpleado

        return result
