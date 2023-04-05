import multiprocessing

command = '/home/www/code/grids/env/bin/gunicorn'
pythonpath = '/home/www/code/grids/grids'
bind = '127.0.0.1:8001'
workers = multiprocessing.cpu_count() * 2 + 1
user = 'root'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=grids.settings'
