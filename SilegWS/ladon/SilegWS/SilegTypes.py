# -*- coding: utf-8 -*-
from ladon.types.ladontype import LadonType

#***** empleado *****
class Empleado(LadonType):
    idEmpleado = int
    idCatedra = int
    nombre = str
    apellido = str
    numeroDocumento = int
    tipoDocumento = str
    cargo = str
    observacion = str
    titulo = str


class EmpleadoList(LadonType):
    empleados = [ Empleado ]


#***** catedra *****
class Catedra(LadonType):
    id = int
    nombre = str

class CatedraList(LadonType):
    catedras = [ Catedra ]


#***** materia *****
class Materia(LadonType):
    id = int
    nombre = str

class MateriaList(LadonType):
    materias = [ Materia ]


#***** departamento *****
class Departamento(LadonType):
    id = int
    nombre = str

class DepartamentoList(LadonType):
    departamentos = [ Departamento ]
