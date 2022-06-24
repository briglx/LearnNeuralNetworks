# Label Maker

## Overview
This project makes it easy to tag images for traing data.

## Install

You may need to setup nginx in order to load images from a data directory

```bash
c:/nginx/nginx.exe
```

Create a virtualenv and activate it:

```
conda create -n label-maker python=3.6
activate label-maker
pip3 install -r requirements.txt
python3 app.py
```

Set environment variables

(Windows)

```
pip install -e .
```
## Running from command line

Set environment variables

On Windows
```
set FLASK_APP "label_maker_server"
set FLASK_ENV "development"

flask run
```

Navigate your browser to http://localhost:5000/


## Running with Docker

To run the server on a Docker container, please execute the following from the root directory:

```bash
# building the image
docker build -t label_maker .

# starting up a container
docker run -p 8080:8080 label_maker
```

## TODO

Export to the YOLO, KITTI, COCO JSON, and CSV format
Read and write in the PASCAL VOC XML format
PASCAL VOC format XML annotation 

See
- https://rectlabel.com/
- https://labelbox.com/product
- https://dataturks.com/features/image-bounding-box.php
- https://github.com/NaturalIntelligence/imglab
- https://alpslabel.wordpress.com/
- https://github.com/tzutalin/labelImg
- https://github.com/kinhong/OpenLabeler