web: daphne appmanager.asgi:application --port $PORT --proxy-headers --bind 0.0.0.0 -v2 
chatworker: python manage.py runworker --settings=appmanager.settings -v2
