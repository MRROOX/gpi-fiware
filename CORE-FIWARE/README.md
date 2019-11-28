# GPI-Fiware

## Core Context Management
Referencia: https://fiwaretourguide.readthedocs.io/en/latest/core/introduction/

## Implementación 

### Iniciar los contenedores.

```
docker-compose up -d
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
     "entity_type": "DHT", 
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
     "entity_name": "urn:ngsi_ld:DHT22:001", 
     "entity_type": "DHT", 
     "timezone": "Chile, Santiago",
     "attributes": [ 
       { "object_id": "temdht22",
         "name": "Tem",
         "type": "Double"
         },
       { "object_id": "humdht22",
         "name": "Hum",
         "type": "Double"
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

Temperatura:
```
curl -iX POST \ 
  'http://localhost:7896/iot/d?k=4jggokgpepnvsb2uv4s40d59ov&i=DHT22003' \ 
  -H 'Content-Type: text/plain' \ 
  -d 'temdht22|19'
```
Humedad:
```
curl -iX POST \ 
  'http://localhost:7896/iot/d?k=4jggokgpepnvsb2uv4s40d59ov&i=DHT22003' \ 
  -H 'Content-Type: text/plain' \ 
  -d 'humdht22|19'
```
La última línea de esa consulta son los datos del protocolo 2.0 Ultralight. 
 
## Borrado de Sensores
```
curl -iX DELETE 
--url 'http://localhost:4061/iot/devices/DHT22001' 
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
curl  -i -X GET 'http://localhost:1026/v2/entities/urn:ngsi_ld:DHT22:003' 
-H 'Content-Type: application/json' 
-H 'fiware-service: openiot'
-H 'fiware-servicepath: /' | python -mjson.tool 
```
