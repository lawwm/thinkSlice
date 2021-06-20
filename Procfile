web: daphne appmanager.asgi:application --port $PORT --proxy-headers --bind 0.0.0.0 -v2 
worker: python manage.py runworker channel_layer --settings=appmanager.settings -v2
