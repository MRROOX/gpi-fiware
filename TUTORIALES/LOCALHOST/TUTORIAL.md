# Tutorial

## 1. Desplegar servicios definidos en docker-compose.yml
## 2. Registro de entidad en Orion Context Brocker.
```
POST http://localhost:1026/v2/entities
Header: Content-Type: "application/json"
        fiware-service: openiot
        fiware-servicepath: /

En body, utilizadmos el contenido de dht22.json
 

```
## 3. Subscripcion de a cambio de estado de entidad.
### Se crea un subcripcion de la entidad, esto quiere decir que cuando se actualice cualquiera de los datos de la entidad estos seran notificados al servicio de Quantumleap.
### Quantumleap, recive la notificacion del cambio de estado de los datos con el valor de los datos y los percirse en la base de datos CRATE DB.
### Quantumleap cuenta con una api y su documentacion se encuentra en el siguiente link : http://localhost:8668/v2/ui/

```
POST http://localhost:1026/v2/subscriptions/
Header: Content-Type: "application/json"
        fiware-service: openiot
        fiware-servicepath: /

En body, utilizamos el contenido de dht22-sub.json

```


##  Configurar Servicios:
### CRATE DB:

```
    localhost:4200
    -> (Obervar el nombre de la base de datos generada automaicamente)
    mtopeniot



```

### Consulta por entidad registrada en base de datos.

```
select * from mtopeniot.etdht22 limit 100;
```
### Grafana:
### Grafana se configurar para ir obteniendo los datos que son percistido en la base de datos CRATE DB.
### En Grafana se pueden crear tableros par visualizar distintos tipos de datos e incluso grandes volumenes de datos.

### El nombre de la Database: mtopeniot es definido por el Header del registro en Orion Context Broker `fiware-service: openiot`.

```
    localhost:3000

    -> Postgres:
    Name: CrateDB
    Host: crate-db:5432
    Database: mtopeniot
    User: crate
    SSL Mode disable
```
```
New Dashboard

->
FROM etdht22 Time column time_index Metric column entity_id SELECT Column: temperature Column: relativehumidity 
```


## Configuracion IOT-Agent 

### Sirve de intermediario entre Orion Context Brocker y un Dispositivo IOT, para la comunicacion entre el dispositivo IOT se puede utilizar varios tipos de protocolos que son ligeros para la comunicación y el envio de datos bidireccional. Además se puede asignar una Token a cada disposivito para su identificacion e integrar una medida de seguridad.

### Configuracion de SERVICE
```
POST http://localhost:4041/iot/services
Header: Content-type: application/json
        Fiware-service: openiot
        fiware-servicepath: /

En el body se agrea el json iot-agent.service.json

```


### Configuracion de DEVICES
```
POST http://localhost:4041/iot/devices

Header: Content-type: application/json
        Fiware-service: openiot
        Fiware-servicepath: /

En el body de agrega el json iot-agent.device.json
```
#### Se va a registrar una nueva entidad en Orion, esta entidad será del tipo DHT22, entonces podra ser mapeada por Queantum leap y se podran persistir su datos en la base de datos CrateDB y luego ser visualizados mediante Grafana.


## Configuracion Cliente en Raspberry

A modo de cliente o dispositivo IOT se utiliza una raspbery pi 3 modelo b, en donde se encuentra integrado un sensor DHT22 de temperatura y humedad.
