# GPI-Fiware

## Core Context Management
Referencia: https://fiwaretourguide.readthedocs.io/en/latest/core/introduction/

## Implementación 

### Iniciar los contenedores.

```
docker-compose up -d
```
### Query Context Data


# CrateDB 

## Crate UI

http://localhost:4200

# Configuracion de Grafana

En localhost:3000 ingresar utilizando con el usario `admin` y la password `admin`, cambiar password por una adecuada.

## Configurar CrateDB en Grafana.

En la opcion `create your first data source` seleccionar PostgreSQL 

```
Name: CrateDB
Host: crate-db:5432
Database: doc
User: crate
SSL Mode: disable 
```
## Creación de Entidades 

Entity es un único elemento de Context descrito por un objeto JSON. 
Creamos entidades enviando una solicitud POST a Orion Context Broker.
```
curl -iX POST \
  'http://localhost:1026/v2/entities' \ 
  -H 'Content-Type: application/json' \ 
  -d '{
      "id": "urn:ngsi-ld:Segment:001", 
       "type": "Segment" 
       }' 
```
```
curl -iX POST \
  'http://localhost:1026/v2/entities' \
  -H 'Content-Type: application/json' \ 
  -d '{
    "id": "urn:ngsi-ld:DHT22:001", 
    "type": "DHT", 
    "location": { 
        "type": "geo:json", 
        "value": { 
             "type": "Point", 
             "coordinates": [-38.748890, -72.617191] 
        } 
    }, 
    "sector": { 
        "type": "Text", 
        "value": "UFRO" 
    } 
}
```
```
curl -iX POST \
  'http://localhost:1026/v2/entities' \
  -H 'Content-Type: application/json' \ 
  -d '{
    "id": "urn:ngsi-ld:DHT22:002", 
    "type": "DHT", 
    "location": { 
        "type": "geo:json", 
        "value": { 
             "type": "Point", 
             "coordinates": [-38.748890, -72.617191] 
        } 
    }, 
    "sector": { 
        "type": "Text", 
        "value": "UFRO" 
    } 
}
```
## Actualización de Entidades

Podemos actualizar las entidades después de la creación. En este ejemplo añadimos refArgumento adicional que es responsable de crear una relación. El trabajo con las relaciones de ordenación se explica en el siguiente capítulo. 
La relación es un vínculo entre dos o más entidades.

```
curl -iX POST \ 
  'http://localhost:1026/v2/op/update' \ 

  -H 'Content-Type: application/json' \ 
  -d '{ 
  "actionType":"APPEND", 
  "entities":[ 
    {
      "id":"urn:ngsi-ld:DHT22:001",
      "type":"DHT",
      "refSegment": { 
        "type": "Relationship", 
        "value": "urn:ngsi-ld:Segment:001" 
      } 
    }, 
    { 
      "id":"urn:ngsi-ld:DHT22:002",
      "type":"DHT", 
      "refSegment": { 
        "type": "Relationship", 
        "value": "urn:ngsi-ld:Segment:001" 
      } 
    }  
 ] 

}' 
```
Con ese comando actualizamos las dos entidades de cruce que creamos anteriormente y añadimos un argumento refSegment a cada una de ellas. 

## Relationships
La creación de relaciones de ordenación se trata en la actualización de Entidades. 
Podemos leer tanto de la entidad hija como de la entidad matriz: 


```
curl -X -G GET 'http://localhost:1026/v2/entities/urn:ngsi-ld:DHT22:001' 
-d 'type=DHT' 
-d 'options=values' 
-d 'attrs=refSegment' | python -mjson.tool 
```
y de padre a hijo o hijos: 

```
curl -G -X GET \ 
  'http://localhost:1026/v2/entities' \ 
  -d 'q=refSegment==urn:ngsi-ld:DHT22:001' \ 
  -d 'type=DHT' \ 
  -d 'options=values' \ 
  -d 'attrs=location' \ 
 | python -mjson.tool 

```

Podemos leer en ambos sentidos, de padre a hijo y de niño rom a padre, por lo que necesitamos crear refArgument sólo en uno de ellos. 

# Agente de IOT

fuente: https://github.com/FIWARE/tutorials.IoT-Agent

Un agente IoT es un componente que permite a un grupo de dispositivos enviar sus datos y ser gestionados desde un Context Broker utilizando sus propios protocolos nativos. Los agentes de IO también deberían poder ocuparse de los aspectos de seguridad de la plataforma FIWARE (autenticación y autorización del canal) y prestar otros servicios comunes al programador del dispositivo.

El Orion Context Broker utiliza exclusivamente peticiones NGSI para todas sus interacciones. Cada agente IoT proporciona una interfaz NGSI de puerto norte que se utiliza para las interacciones con el agente de contexto y todas las interacciones debajo de este puerto se producen utilizando el protocolo nativo de los dispositivos conectados.

En efecto, esto proporciona una interfaz estándar para todas las interacciones de la IO a nivel de gestión de la información contextual. Cada grupo de dispositivos de IO es capaz de utilizar sus propios protocolos propietarios y mecanismos de transporte dispares bajo el capó, mientras que el agente de IOT asociado ofrece un patrón de fachada para manejar esta complejidad.


## Creación de grupos de servicio

Creación de un grupo de servicio para conectar dispositivos del mismo tipo.  

Apikey es único para cada grupo de servicio 

```
curl -iX POST \
  'http://localhost:4061/iot/services' \ 
  -H 'Content-Type: application/json' \ 
  -H 'fiware-service: openiot' \ 
  -H 'fiware-servicepath: /' \ 
  -d '{ 
     "services": [ 
   { 
     "apikey":      "4jggokgpepnvsb2uv4s40d59ov", 
     "cbroker":     "http://orion:1026", 
     "entity_type": "Thing", 
     "resource":    "/iot/d" 
   } 
 ] 
}' 
```

## Creación de Sensores

```
curl -iX POST  'http://localhost:4061/iot/devices' \
  -H 'Content-Type: application/json'\
  -H 'fiware-service: openiot' \
  -H 'fiware-servicepath: /' \
  -d '{
    "devices": [
   { 
     "device_id": "DHT22001", 
     "entity_name": "urn:ngsi_ld:DHT22:003", 
     "entity_type": "DHT", 
     "timezone": "Chile, Santiago",
     "attributes": [ 
       { "object_id": "temdht22",
         "name": "Tem",
         "type": "Integer"
         },
       { "object_id": "humdht22",
         "name": "Hum",
         "type": "Integer"
         }], 
     "static_attributes": [ 
       {"name":"refSegment",
        "type": "Relationship",
        "value": "urn:ngsi-ld:Segment:001"
        } 
     ] 
   } 
 ] 
}' 
```
## Recursos
Enviando datos a un recurso ubicado en la url: 
 
 ```
 http://iot-agent:7896/iot/d?i=<device_id>&k=4jggokgpepnvsb2uv4s40d59ov 
```
#### Enviar datos por un Dispositivo de IO: 

```
curl -iX POST \ 
  'http://localhost:7896/iot/d?k=4jggokgpepnvsb2uv4s40d59ov&i=DHT22003' \ 
  -H 'Content-Type: text/plain' \ 
  -d 'tempdht22|19'
```
La última línea de esa consulta son los datos del protocolo 2.0 Ultralight. 
 
## Borrado de Sensores
```
curl -iX DELETE 
--url 'http://localhost:4061/iot/devices/DHT22003' 
-H 'fiware-service: openiot' 
-H 'fiware-servicepath: /' 
```
```
curl  -iX DELETE 
--url 'http://localhost:1026/v2/subscriptions/' \ 
-H 'Content-Type: application/json' \ 
-H 'fiware-service: openiot' \ 
-H 'fiware-servicepath: /' \ 
```

## Listado de todos los Sensores

```
curl -X GET 'http://localhost:4061/iot/devices' 
-H 'fiware-service: openiot' 
-H 'fiware-servicepath: /' | python -mjson.tool 
```
## Comprobación de actualización de Datos
El Agente IoT creó una entidad de sensor en Orion Context Broker y después de eso podemos comprobar esa entidad para asegurarnos de que el proceso de creación fue exitoso. 

```
curl  -i -X GET 'http://localhost:1026/v2/entities/urn:ngsi_ld:camCar:001' 
-H 'Content-Type: application/json' 
-H 'fiware-service: openiot'
-H 'fiware-servicepath: /' | python -mjson.tool 
```

## Creación del Actuador

El proceso de creación de actuadores es el mismo que el de la creación de un sensor. Lo hacemos enviando una solicitud POST a un agente de la IOT.  Luego crea una entidad en Orión. 
En el argumento "endpoint" determinamos una URL a la que se enviarán los datos de actuación.  
En el argumento "protocolario" determinamos cómo deben formatearse los datos. 

```
curl -iX POST \ 
  'http://localhost:4061/iot/devices' \ 
  -H 'Content-Type: application/json' \ 
  -H 'fiware-service: openiot' \ 
  -H 'fiware-servicepath: /' \ 
  -d '{ 
      "devices": [ 
    { 
      "device_id": "TrafficLight001", 
      "entity_name": "urn:ngsi-ld:TrafficLight:001", 
      "entity_type": "TrafficLight", 
      "protocol": "PDI-IoTA-UltraLight", 
      "transport": "HTTP", 
      "endpoint": "http://localhost:10001/iot/TrafficLight001", 
      "commands": [ 
        { "name": "color", "type": "Integer" } 
       ], 
       "static_attributes": [ 
         {
            "name":"refCrossing",
            "type": "Relationship",
            "value": "urn:ngsi-ld:Crossing:001"
        } 
      ] 
    } 
  ] 
} 

' 
```

# Almacenamiento

## Cygnus

Cygnus es un habilitador genérico responsable de los datos persistentes de Orion Context Broker a un habilitador genérico de almacenamiento para crear una vista histórica de los datos de contexto. Cygnus crea un agente para cada GE de almacenamiento. 

Con este comando comprobamos si el contenedor de Cygnus está funcionando correctamente 


```
curl -X GET \ 
  'http://localhost:5080/v1/version' 

```
Se especifica la base de datos a la que Cygnus persistirá en un archivo docker-compos.yml. 

## Suscripción a Cygnus

A continuación, debemos informar a Cygnus sobre los cambios en los datos de contexto. Lo hacemos enviando una solicitud POST a Orion para notificar a Cygnus sobre los cambios de contexto especificados por nosotros: 

Creamos un patrón de mensajería de publicación-suscripción - el creador de mensajes (editor) no determina quién recibirá un tipo específico de mensaje, sino que lo clasifica en categorías sin saber quién y si recibirá ese mensaje. 


```
curl -iX POST \ 
  'http://localhost:1026/v2/subscriptions' \ 
  -H 'Content-Type: application/json' \ 
  -H 'fiware-service: openiot' \ 
  -H 'fiware-servicepath: /' \ 
  -d '{ 
      "description": "Notify Cygnus of all context changes", 
      "subject": { 
      "entities": [ 
      { 
        "idPattern": ".*" 
      } 
    ] 
  }, 
  "notification": { 
    "http": { 
      "url": "http://cygnus:5050/notify" 
    }, 
    "attrsFormat": "legacy" 
  }, 
  "throttling": 5 
}' 
```
## Mongo DB

Mongo DB es una base de datos base que va con cada Orion Context Broker. En esta base de datos se almacena toda la información sobre las entidades, las relaciones entre ellas, etc.  

## MySQL

Utilizamos MySQL para almacenar datos de contexto. El historial de cambios en el valor de ciertos atributos. 

Usando el siguiente comando podemos conectarnos a una base de datos a través del puerto que especificamos en el archivo docker-composition: 


```
docker exec -it  db-mysql mysql -h mysql-db -P 3306  -u root -p123 

 ```
O : 
 
```
docker inspect <container name> 
```
```
docker inspect db-mysql 
```
```
mysql -u root -h <container ip> -p123 
```
```
mysql -u root -h 172.18.0.2 -p123 
```
### Alternativamente:

(1). Instalar mysql-client

```
sudo apt install mysql-client-core-5.7 
```
 (2). Ver el ip de MysSql Container:
 ```
  docker inspect <name_of_container> 
  ```
  (3). Entra en Mysql: 
  ```
  mysql -u root -h <IP_CONTAINER> -p123
  ```

 Ahora podemos usar el synax de MySQL para acceder a los datos contenidos en la base de datos.

```
SHOW DATABASES; 

SHOW SCHEMAS; 

SHOW tables FROM openiot;
```
Para obtener 10 últimas anotaciones 
```
SELECT * FROM openiot.urn_ngsi_ld_camCar_001_camCar WHERE attrType='integer'ORDER BY recvTime DESC  limit 10; 
 ```

 ```
SELECT recvTime, attrValue FROM openiot.urn_ngsi_ld_camCar_001_camCar WHERE attrType='integer' ORDER BY recvTime DESC  limit 10; 
 ```

# Visualización de datos

## Metabase

Para visualizar nuestros datos, que están en nuestra base de datos MySQL, utilizamos la herramienta Metabase. 

Metabase: https://metabase.com/docs/latest/developers-guide.html 
 
Aquí va a Añadir dependencias externas o plugins 

https://metabase.com/docs/latest/operations-guide/running-metabase-on-docker.html#adding-external-dependencies-or-plugins 


Montamos dependencias extras como el controlador jdbc en un servicio de docker en un archivo de composición de docker. 

Metabase funciona con postgreSQL como una base de datos de respaldo - almacena todos los datos necesarios para recrear los cuadros de mando después de que el servidor se bloquee. 

Necesitamos crear un usuario de base de datos antes de usarla: 

  ```
CREATE USER 'metabase_user' IDENTIFIED BY '123'; 
GRANT ALL PRIVILEGES ON openiot.* TO 'metabase_user'; 
GRANT RELOAD ON *.* TO 'metabase_user'; 
FLUSH PRIVILEGES; 
quit 
 ```

 Luego en el panel de metabase, que está disponible en localhost:32769 creamos un usuario y añadimos una base de datos MySQL. En los campos Usuario y Contraseña ponemos 'metabase_user' y una contraseña que coincida con la que hemos creado anteriormente. En host ponemos una dirección IP de nuestro servidor de base de datos MySQL , y en nombre de la base de datos escribimos el nombre de una única instancia de la base de datos MySQL que queremos usar. 

 Nos conectamos al panel de administración a través de localhost:<port number> , podemos comprobar los números de los puertos mediante consultas: 
 ```
docker ps -a 
 ```
Para formatear nuestra tabla de datos- para hacer que Metabase entienda nuestro formato, como interpretar números como números, vamos a admin -> data model 

## Creación de cuadros de mando

Después de conectar con éxito la base de datos a metabase, ahora podemos empezar a crear nuestros cuadros de mando de visualización. 

Nosotros a eso adentro: 
 

Browse data    ->    <`database name`>   ->   <`table name`> 


Obtenemos una vista de los datos en una tabla. Entonces podemos filtrar los datos directamente y crear la visualización que necesitamos. 

El panel de control será accesible en una url similar a ésta: http://localhost:32770/dashboard/2 

