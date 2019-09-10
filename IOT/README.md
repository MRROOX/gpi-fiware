# Sensor DHT22 en Raspberry Pi 3 model B.

## Configuracion del Sensor DHT22.

#### Pin 1 is VCC (Power Supply)
#### Pin 2 is DATA (The data signal)
#### Pin 3 is NULL (Do not connect)
#### Pin 4 is GND (Ground)

# Raspberry -> DHT22 Circuito.


#### Utilizar una resistencia de  10k entre el Pin 1 y el Pin 2 del sensor DHT22
#### Pin 1 del DHT22 al Pin 1 (3v3) en la Raspberry pi
#### Pin 2 del DHT22 al Pin 7 (GPIO4) en la Raspberry pi
#### Pin 4 del DHT22 al Pin 6 (GND) en la Raspberry pi

# Preparando la Raspberry Pi 

 ```
 sudo apt update 
 ```

  ```
  sudo apt upgrade
  ```

  ### Python 3 and Pip

   ```
   sudo apt-get install python3-dev python3-pip
   ```

   ### Instalacion de herramientas Python, Wheel y Pip

   ```
   sudo python3 -m pip install --upgrade pip setuptools wheel
   ```

   ### DHT Libreria Python.

   ```
   sudo pip3 install Adafruit_DHT
   ```


