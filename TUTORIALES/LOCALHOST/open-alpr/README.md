## Build Image

docker build --tag openalpr .

## Run Container

docker run -d --name test -p 8090:8080 openalpr

## Test Single Image

curl -s -X POST -F name=file -F "image=@sample.jpg" 'http://localhost:8090/v1/identify/plate?country=us'


