to launch the docker version :

docker run -it -e "TZ=Europe/Paris"  --rm -v "$PWD/filestorage":/app/filestorage nightscout2diabby


to build the docker : 
docker build -t nightscout2diabby .

