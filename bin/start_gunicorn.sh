#!/bin/bash
source /home/www/code/grids/env/bin/activate
exec gunicorn  -c "/home/www/code/grids/grids/gunicorn_config.py" grids.wsgi
