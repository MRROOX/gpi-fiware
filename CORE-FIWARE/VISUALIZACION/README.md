# VISUALIZACIÓN

fuente: https://github.com/FIWARE/tutorials.Time-Series-Data

# QuantumLeap

Una vez que un sistema de contexto dinámico está en funcionamiento, necesitamos informar a Quantum Leap directamente de los cambios en el contexto. Como es de esperar, esto se hace usando el mecanismo de suscripción del Orion Context Broker. El atributo attrsFormat=legacy no es necesario ya que QuantumLeap acepta notificaciones NGSI v2 directamente.

## Agregando el evento de Registro de Temperatura y Humedad


Esto se hace haciendo una petición POST al endpoint `/v2/subscription` del Orion Context Broker.

Las cabeceras `fiware-service` y `fiware-servicepath` se utilizan para filtrar la suscripción y escuchar únicamente las mediciones de los sensores de IOT adjuntos.

El idPattern en el cuerpo de la solicitud asegura que QuantumLeap será informado de todos los cambios en los datos del sensor.
La URL de notificación debe coincidir con el puerto expuesto.

El atributo metadata asegura que la columna time_index dentro de la base de datos de CrateDB coincida con los datos encontrados dentro de la base de datos MongoDB utilizada por el Orion Context Broker en lugar de utilizar la hora de creación del registro dentro de la propia CrateDB.

```
curl -iX POST \
  'http://localhost:1026/v2/subscriptions/' \
  -H 'Content-Type: application/json' \
  -H 'fiware-service: openiot' \
  -H 'fiware-servicepath: /' \
  -d '{
  "description": "Notify QuantumLeap changes of any DHT Sensor",
  "subject": {
    "entities": [
      {
        "idPattern": "DHT22.*",
        "type": "DHT"
      }
    ],
    "condition": {
      "attrs": [
        "temdht22",
 
      ]
    }
  },
  "notification": {
    "http": {
      "url": "http://quantumleap:8668/v2/notify"
    },
    "attrs": [
        "temdht22"
    ],
    "metadata": ["dateCreated", "dateModified"]
  },
  "throttling": 1
}'
```

```
curl -X GET \
  'http://localhost:8668/v2/entities/urn:ngsi-ld:DHT22:001/attrs/temdht22?=3&limit=3' \
  -H 'Accept: application/json' \
  -H 'Fiware-Service: openiot' \
  -H 'Fiware-ServicePath: /'
```

curl -X GET \
  'http://localhost:8668/v2/entities/' \
  -H 'Accept: application/json' \
  -H 'Fiware-Service: openiot' \
  -H 'Fiware-ServicePath: /'

## Comprobación de suscripciones para QuantumLeap

Antes de nada, compruebe que las suscripciones que ha creado en los pasos uno y dos funcionan (es decir, que se ha enviado al menos una notificación para cada una).

```
curl -X GET \
  'http://localhost:1026/v2/subscriptions/' \
  -H 'fiware-service: openiot' \
  -H 'fiware-servicepath: /'
```


# CrateDB

http://localhost:4200

# Grafana

http://localhost:3000

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

