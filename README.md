# A simple API service to sync data between Diabby, Ypsomed and NightScout. 


The program use the API provided by NightScout and the API founded in Diabby Web Site. 
Ypsomed does not provide a API. So Use Web Scratching about the web site.
Use FastAPI Service to provide a API easily reusable. 


## Current version functions 

- allow to sync the glycemia from NightScout to Diabby
- allow to sync the Insulina from Ypsomed to NightScout

## TODO 

- allow to sync the insulina provided in Diabby to NightScout to do better reports in NS without web Scraping


# Docker version 
To launch the docker version :

Build the docker image 

`docker build -t nightscout2diabby .`

and after run docker 

`docker run -d -p 81:80 -e MODULE_NAME="NS2D" -e "TZ=Europe/Paris"  -v "$PWD/filestorage":/app/filestorage nightscout2diabby`

To sync NS2Diabby : http://IP:81/ns2d
To sync Yso2NS: http://IP:81/ypso2ns




