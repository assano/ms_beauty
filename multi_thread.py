import threading

def run_thread():
	for i in range(10000):
		print 'this is',threading.current_thread().name,i

t1 = threading.Thread(target=run_thread)
t2 = threading.Thread(target=run_thread)
t1.start()
t2.start()