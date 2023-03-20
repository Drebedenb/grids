#!/bin/bash
source /home/www/code/grids/env/bin/activate
source /home/www/code/grids/env/bin/postactivate
exec gunicorn  -c "/home/www/code/grids/grids/gunicorn_config.py" grids.wsgi
