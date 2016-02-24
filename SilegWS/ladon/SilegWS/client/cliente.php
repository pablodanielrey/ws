<html>
  <head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"></head>
  <body>
<?php

    ini_set("soap.wsdl_cache_enabled", 0);
    
    $soapClient = new SoapClient("http://163.10.56.53/MyService/soap/description", array('soap_version' => SOAP_1_1, 'trace' => TRUE));

    //****** listado de funciones del webservice ******
    //print(print_r($soapClient->__getFunctions(), true)."");


    //****** acceso simple al webservice ******
    $departamentoParam = array("idDepartamento" => 19);
    $materiaParam = array("idMateria" => 48);
    $catedraParam = array("idCatedra" => 68);
    $catedraCargoParam = array("idCatedra" => 68, "cargo"=> "AYUDANTE DIP");
    
    //$response = $soapClient->getDepartamento();
    //$response = $soapClient->getMaterias();    
    //$response = $soapClient->getMateriasDpto($departamentoParam);
    //$response = $soapClient->getCatedras($materiaParam);
    //$response = $soapClient->getCuerpoDocente($catedraParam);
    $response = $soapClient->getCuerpoDocenteCargo($catedraCargoParam);
    print("<pre>".print_r($response, true)."</pre>");


    /****** recorrido completo *****
    $departamentosWS = $soapClient->getDepartamento();
    $departamentos = (!is_array($departamentosWS->departamentos->item)) ? array($departamentosWS->departamentos->item) : $departamentosWS->departamentos->item;
    
    echo "<ol>";
    foreach($departamentos as $departamento){
      $departamentoParam = array("idDepartamento" => $departamento->id); //turismo
      $materiasPorDepartamento = $soapClient->getMateriasDpto($departamentoParam);
      echo "<li>DEPARTAMENTO: " . $departamento->nombre . "<ol>";
      
      $materias = (!is_array($materiasPorDepartamento->materias->item)) ? array($materiasPorDepartamento->materias->item) : $materiasPorDepartamento->materias->item;
       
      foreach($materias as $materia){
        echo "<li>MATERIA: " . $materia->nombre . "<ol>
";
        $materiaParam = array("idMateria" => $materia->id); //turismo
        $catedrasPorMateria = $soapClient->getCatedras($materiaParam);

        $catedras = (!is_array($catedrasPorMateria->catedras->item)) ? array($catedrasPorMateria->catedras->item) : $catedrasPorMateria->catedras->item;
        
        foreach($catedras as $catedra){
          echo "<li>CATEDRA: " . $catedra->id . " " . $catedra->nombre . "<ol>";
          $catedraParam = array("idCatedra" => $catedra->id); 

          $cuerpoDocentePorCatedra = $soapClient->getCuerpoDocente($catedraParam);
          
          $docentes = array();
          if(!empty($cuerpoDocentePorCatedra->empleados)) $docentes = (!is_array($cuerpoDocentePorCatedra->empleados->item)) ? array($cuerpoDocentePorCatedra->empleados->item) : $cuerpoDocentePorCatedra->empleados->item;
          
          foreach($docentes as $docente){
            echo "<li>DOCENTE: " . $docente->idEmpleado . " " . $docente->titulo . " " . $docente->nombre . " " . $docente->apellido . " " . $docente->tipoDocumento . " " . $docente->numeroDocumento . " " . $docente->cargo . " " . $docente->observacion . "</li>";
          }
          
          $catedraCargoParam = array("idCatedra" => $catedra->id, "cargo" => "TITULAR");           
          $cuerpoDocentePorCatedraCargo = $soapClient->getCuerpoDocenteCargo($catedraCargoParam);
          
          $docentes = array(); 
          if(!empty($cuerpoDocentePorCatedraCargo->empleados)) $docentes = (!is_array($cuerpoDocentePorCatedraCargo->empleados->item)) ? array($cuerpoDocentePorCatedraCargo->empleados->item) : $cuerpoDocentePorCatedraCargo->empleados->item;
          
          foreach($docentes as $docente){
            echo "<li>DOCENTE TITULAR: " . $docente->idEmpleado . " " . $docente->titulo . " " . $docente->nombre . " " . $docente->apellido . " " . $docente->tipoDocumento . " " . $docente->numeroDocumento . " " . $docente->cargo . " " . $docente->observacion . "</li>";
          }
          
          $catedraCargoParam = array("idCatedra" => $catedra->id, "cargo" => "AYUDANTE");           
          $cuerpoDocentePorCatedraCargo = $soapClient->getCuerpoDocenteCargo($catedraCargoParam);
          
          $docentes = array(); 
          if(!empty($cuerpoDocentePorCatedraCargo->empleados)) $docentes = (!is_array($cuerpoDocentePorCatedraCargo->empleados->item)) ? array($cuerpoDocentePorCatedraCargo->empleados->item) : $cuerpoDocentePorCatedraCargo->empleados->item;
          
          foreach($docentes as $docente){
            echo "<li>DOCENTE AYUDANTE: " . $docente->idEmpleado . " " . $docente->titulo . " " . $docente->nombre . " " . $docente->apellido . " " . $docente->tipoDocumento . " " . $docente->numeroDocumento . " " . $docente->cargo . " " . $docente->observacion . "</li>";
          }
          
          $catedraCargoParam = array("idCatedra" => $catedra->id, "cargo" => "ADJUNTO");           
          $cuerpoDocentePorCatedraCargo = $soapClient->getCuerpoDocenteCargo($catedraCargoParam);
          
          $docentes = array(); 
          if(!empty($cuerpoDocentePorCatedraCargo->empleados)) $docentes = (!is_array($cuerpoDocentePorCatedraCargo->empleados->item)) ? array($cuerpoDocentePorCatedraCargo->empleados->item) : $cuerpoDocentePorCatedraCargo->empleados->item;
          
          foreach($docentes as $docente){
            echo "<li>DOCENTE ADJUNTO: " . $docente->idEmpleado . " " . $docente->titulo . " " . $docente->nombre . " " . $docente->apellido . " " . $docente->tipoDocumento . " " . $docente->numeroDocumento . " " . $docente->cargo . " " . $docente->observacion . "</li>";
          }
          
          $catedraCargoParam = array("idCatedra" => $catedra->id, "cargo" => "JEFE");           
          $cuerpoDocentePorCatedraCargo = $soapClient->getCuerpoDocenteCargo($catedraCargoParam);
          
          $docentes = array(); 
          if(!empty($cuerpoDocentePorCatedraCargo->empleados)) $docentes = (!is_array($cuerpoDocentePorCatedraCargo->empleados->item)) ? array($cuerpoDocentePorCatedraCargo->empleados->item) : $cuerpoDocentePorCatedraCargo->empleados->item;
          
          foreach($docentes as $docente){
            echo "<li>DOCENTE JEFE: " . $docente->idEmpleado . " " . $docente->titulo . " " . $docente->nombre . " " . $docente->apellido . " " . $docente->tipoDocumento . " " . $docente->numeroDocumento . " " . $docente->cargo . " " . $docente->observacion . "</li>";
          }                   
          echo "</ol></li>";
        } 
        echo "</ol></li>";
      }
      echo "</ol></li>";
    }
    echo "</ol>";*/
?>
</body></html>
  
