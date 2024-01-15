import gevent.monkey
gevent.monkey.patch_all()

bind = "127.0.0.1:8000"
workers = 12
worker_class = "gevent"
timeout = 300
