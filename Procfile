#web: gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 app:app
web: gunicorn --bind 0.0.0.0:$PORT app:app
#web: gunicorn --worker-class eventlet -w 1 app:app