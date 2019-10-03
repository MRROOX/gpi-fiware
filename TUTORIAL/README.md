# Tutorial -> Rasbperry + Fiware.

## Creacion de Entidad DHT para medir temperatura y humedad

fuente: https://fiware-training.readthedocs.io/es_MX/latest/casodeestudio/descripcion/

https://hub.docker.com/r/fiware/quantum-leap/dockerfile

```
POST http://localhost:1026/v2/entities
Header: Content-Type: "application/json"

{
    "id":"DHT22001",
    "type":"DHT22",
    "dateObserved":{
        "type":"DateTime",
        "value":""
    },
    "address": {
        "type": "StructuredValue",
        "value": {
            "addressCountry": "CL",
            "addressLocality": "Temuco",
            "streetAddress": "UFRO"           
        }
   },
    "location": {
         "value": {
            "type": "Point",
            "coordinates": [0,0]
        },
        "type": "geo:json"
  },
    "temperature":{
        "type":"Number",
        "value":"0"
    },
    "relativeHumidity":{
        "type":"Number",
        "value":"0"
    }
}
```