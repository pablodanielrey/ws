# -*- coding: utf-8 -*-
import inject
from connection.connection import Connection

class SilegData:

    conn = inject.attr(Connection)

    def _fetchall(self, sql):
        con = self.conn.get()
        try:
            cur = con.cursor()
            try:
                cur.execute(sql)
                rows = cur.fetchall()
                data = []
                for row in rows:
                    data.append(dict(row))
                return data

            finally:
                cur.close()

        finally:
            self.conn.put(con)



    def getListadoDpto(self):
        sql = """
SELECT dpto_nombre, dpto_id

FROM (
  SELECT desig_fecha_baja, desig_catxmat_id
  FROM designacion_docente
) as dd

LEFT JOIN (
  catedras_x_materia LEFT JOIN materia ON (materia.materia_id=catedras_x_materia.catxmat_materia_id)
) ON (catedras_x_materia.catxmat_id = dd.desig_catxmat_id)

LEFT JOIN (
  SELECT dpto_id, dpto_nombre
  FROM departamento WHERE NOT (
    upper(dpto_nombre) LIKE 'C. U.%'
    OR upper(dpto_nombre) like 'C.U.%'
  )
) AS dpto ON (materia_dpto_id = dpto.dpto_id)
WHERE ( desig_fecha_baja IS NULL )
AND materia_nombre IS NOT NULL
GROUP BY dpto_nombre, dpto_id
"""
        return self._fetchall(sql)


    def getListadoMateriasDpto(self, idDpto):
        sql = """
SELECT materia_nombre, materia_id

FROM (
  SELECT desig_fecha_baja, desig_catxmat_id
  FROM designacion_docente
) AS dd

LEFT JOIN (
  catedras_x_materia LEFT JOIN materia ON (materia.materia_id = catedras_x_materia.catxmat_materia_id)
) ON (catedras_x_materia.catxmat_id=dd.desig_catxmat_id)

LEFT JOIN (
  SELECT dpto_id
  FROM departamento
  WHERE not (
    upper(dpto_nombre) LIKE 'C. U.%'
    OR upper(dpto_nombre) like 'C.U.%')
  ) AS dpto ON (materia_dpto_id = dpto.dpto_id)

WHERE dpto_id = {dpto_id}
AND ( desig_fecha_baja IS NULL ) AND materia_nombre IS NOT NULL
GROUP BY materia_nombre,materia_id
ORDER BY materia_nombre ASC
""".format(dpto_id=idDpto)

        return self._fetchall(sql)


    def getListadoMaterias(self):
        sql = """
SELECT materia_nombre, materia_id
FROM (
  SELECT desig_fecha_baja, desig_catxmat_id
  FROM designacion_docente ) AS dd

  LEFT JOIN (
    catedras_x_materia
    LEFT JOIN materia ON (materia.materia_id=catedras_x_materia.catxmat_materia_id)
  ) ON (catedras_x_materia.catxmat_id=dd.desig_catxmat_id)

  LEFT JOIN (
    SELECT dpto_id
    FROM departamento
    WHERE NOT (
      UPPER(dpto_nombre) LIKE 'C. U.%'
      OR UPPER(dpto_nombre) like 'C.U.%'
    )
  ) AS dpto ON (materia_dpto_id = dpto.dpto_id)

  WHERE ( desig_fecha_baja IS NULL )
  AND materia_nombre IS NOT NULL
  GROUP BY materia_nombre,materia_id
  ORDER BY materia_nombre ASC
"""

        return self._fetchall(sql)



    def getCatedras(self, idMateria):
        sql = """
SELECT catxmat_id, catedra_nombre
FROM catedras_x_materia cm
INNER JOIN catedra c ON cm.catxmat_catedra_id = c.catedra_id
WHERE cm.catxmat_materia_id = {materia_id}
""".format(materia_id=idMateria)

        return self._fetchall(sql)



    def getCuerpoDocente(self, idCatedra):
        sql = """
SELECT p.pers_id, e.empleado_id, upper(p.pers_apellidos) AS apellido,
upper(p.pers_nombres) nombre, upper(tc.tipocargo_nombre) AS tipocargo_nombre,
tg.titgenerico_abrev, tpe.titposemp_titulo_abrev, desig_observaciones,pers_nrodoc, tipodoc_descripcion
FROM designacion_docente dd
LEFT JOIN tipo_cargo tc ON dd.desig_tipocargo_id = tc.tipocargo_id
LEFT JOIN empleado e ON dd.desig_empleado_id = e.empleado_id
LEFT JOIN persona p ON p.pers_id = e.empleado_pers_id
LEFT JOIN tipo_documento ON (tipodoc_id = pers_tipodoc_id)
LEFT JOIN titulo_grado_empleado tge ON tge.titgrademp_empleado_id = e.empleado_id
LEFT JOIN titulo_postgrado_empleado tpe ON tpe.titposemp_empleado_id = e.empleado_id
LEFT JOIN titulo_especifico te ON te.titesp_id = tge.titgrademp_esp_id
LEFT JOIN titulo_generico tg ON tg.titgenerico_id = te.titesp_gen_id
WHERE dd.desig_catxmat_id = {catedra_id}
AND dd.desig_fecha_baja IS NULL
AND dd.desig_id NOT IN (
  SELECT licencia_designacion_id
  FROM licencia
  WHERE licencia_fecha_hasta > now()
)
ORDER BY tc.tipocargo_orden, apellido
""".format(catedra_id=idCatedra)

        return self._fetchall(sql)


    def getCuerpoDocenteCargo(self, idCatedra, cargo):
        sql = """
SELECT p.pers_id, e.empleado_id, upper(p.pers_apellidos) AS apellido,
upper(p.pers_nombres) nombre, upper(tc.tipocargo_nombre) AS tipocargo_nombre,
tg.titgenerico_abrev, tpe.titposemp_titulo_abrev, desig_observaciones, pers_nrodoc, tipodoc_descripcion
FROM designacion_docente dd
LEFT JOIN tipo_cargo tc ON dd.desig_tipocargo_id = tc.tipocargo_id
LEFT JOIN empleado e ON dd.desig_empleado_id = e.empleado_id
LEFT JOIN persona p ON p.pers_id = e.empleado_pers_id
LEFT JOIN tipo_documento ON (tipodoc_id = pers_tipodoc_id)
LEFT JOIN titulo_grado_empleado tge ON tge.titgrademp_empleado_id = e.empleado_id
LEFT JOIN titulo_postgrado_empleado tpe ON tpe.titposemp_empleado_id = e.empleado_id
LEFT JOIN titulo_especifico te ON te.titesp_id = tge.titgrademp_esp_id
LEFT JOIN titulo_generico tg ON tg.titgenerico_id = te.titesp_gen_id
WHERE dd.desig_catxmat_id = {catedra_id}
AND upper(tc.tipocargo_nombre) LIKE '%{cargo}%'
AND dd.desig_fecha_baja IS NULL
AND dd.desig_id NOT IN (
  SELECT licencia_designacion_id
  FROM licencia
  WHERE licencia_fecha_hasta > now()
)
ORDER BY tc.tipocargo_orden, apellido
""".format(catedra_id=idCatedra,cargo=cargo.upper())

        return self._fetchall(sql)
