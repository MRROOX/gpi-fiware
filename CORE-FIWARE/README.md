# GPI-Fiware

## Core Context Management
Referencia: https://fiwaretourguide.readthedocs.io/en/latest/core/introduction/

## Implementación 

### Iniciar los contenedores.

```
docker-compose up -d
```
### Creación de Context Data 



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



