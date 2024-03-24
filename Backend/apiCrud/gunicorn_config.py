import multiprocessing

bind = "0.0.0.0:8000"  # O el puerto que prefieras
workers = multiprocessing.cpu_count() * 2 + 1