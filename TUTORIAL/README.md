# Tutorial -> Rasbperry + Fiware.

## Creacion de Entidad DHT para medir temperatura y humedad

fuente: https://fiware-training.readthedocs.io/es_MX/latest/casodeestudio/descripcion/

https://hub.docker.com/r/fiware/quantum-leap/dockerfile

https://camo.githubusercontent.com/93f44facc15bb6a9edf6ab9968fc1d8b862033fe/68747470733a2f2f6669776172652e6769746875622e696f2f7475746f7269616c732e496f542d4167656e742f696d672f6172636869746563747572652e706e67


#### Seguridad : https://github.com/FIWARE/catalogue/blob/master/security/README.md

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