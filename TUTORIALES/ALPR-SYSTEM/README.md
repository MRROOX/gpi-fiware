# Tutorial Sistema ALPR 


# Despliegue 

docker-compose up -d

## Lista de Servicios
| Service               | Port | Access  |
| --------------------- | ---- | ------- |
| APLR Service          | 8888 | Public  |




# Servicios de ALPR

http://localhost:8888/

    /v1/identify/plate
    /v1/info
    /v1/healthcheck}

## Lista de Paises:



## Ejemplo:

curl -s -X POST -F name=file -F "image=@sample.jpg" 'http://localhost:8888/v1/identify/plate?country=us'




# Referencias
#### Stream Video RPI

https://arduinoinfo.mywikis.net/wiki/LicensePlateRecognition

https://github.com/marcbelmont/deep-license-plate-recognition/blob/master/alpr_video.py

http://doc.openalpr.com/video_processing.html

https://gist.github.com/jkjung-avt/790a1410b91c170187f8dbdb8cc698c8

##### openALPR
Es una libreria en C++ que utiliza openCV y Ocr para la deteccion de matriculas, mediante openCV se identifica la matricula y mediante OCR se crean los modelos para la identificacion, se procede al entrenamiento mediante datos de entrada o set de datos (imagenes de matriculas).

### https://github.com/openalpr/openalpr

# OCR
# train OCR Documentacion

### http://doc.openalpr.com/opensource.html#training-ocr

### https://github.com/openalpr/train-ocr


## Patente Chile:

### https://es.wikipedia.org/wiki/Archivo:Matr%C3%ADcula_automovil%C3%ADstica_Chile_2014_GK%E2%80%A2SB*78_particular_con_FE-Schrift.jpg

### https://www.dafont.com/es/fe-font.font

## Teasser OCR

### https://github.com/tesseract-ocr/tesseract






