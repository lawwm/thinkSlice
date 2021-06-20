web: daphne appmanager.asgi:application --port $PORT --bind 0.0.0.0 -v2 --proxyheaders
chatworker: python manage.py runworker --settings=appmanager.settings -v2
