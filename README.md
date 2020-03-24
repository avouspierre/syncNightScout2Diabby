# A simple program to sync data between Diabby and NightScout. 

The program use the API provided by NightScout and the API founded in Diabby Web Site. 

## Current version functions 

- allow to sync the glycemia from NightScout to Diabby

## TODO 

- allow to sync the insulina provided in Diabby to NightScout to do better reports in NS


# Docker version 
To launch the docker version :

Build the docker image 

`docker build -t nightscout2diabby .`

and after run docker 

`docker run -it --rm -v "$PWD/filestorage":/app/filestorage nightscout2diabby`


