web: daphne appmanager.asgi:application --port $PORT --proxy-headers --bind 0.0.0.0 -v2 
worker: worker: python manage.py runworker channels --settings=appmanager.settings -v2
