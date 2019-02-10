# Mac Setup Guide
## Requirements
* __python 3__
* __pip__
* __virtualenv__ is recommend, but not necessary

## Requirements installation
* ```Brew install python``` (make sure it's python 3)
* ```Sudo easy_install pip``` (should come with python, but use this if it isn't) (make sure it uses python 3)
* ```pip install virtualenv```

## Flask Installation Guide
* ```virtualenv pu python3```
* ```cd pu```
* ```. bin/activate```
* ```pip install Flask```

## Start the Flask Dev Server
* ```FLASK_APP=router.py flask run```
