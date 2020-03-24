to launch the docker version :

docker run -it --rm -v "$PWD/filestorage":/app/filestorage nightscout2diabby

docker run -it --rm -v "/Users/pierre/Documents/Personnel/code/syncNightScout2Diabby/filestorage":/app/filestorage nightscout2diabby

to build the docker : 
docker build -t nightscout2diabby .

