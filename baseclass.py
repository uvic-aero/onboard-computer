class Base(object):

	def __init__(self):
		print("Init BASE running")
		
	
	def start(self):
		worker.start()
		worker = Thread(target=run)

	def run():
		pass


		
		
class StillReceiver(Base):

	def __init__(self):
		super().__init__()
		print("Init StillReceiver running")
		
	def run():

class StillDispatcher(object):

	def __init__(self):
		pass
	
	def accessQueue(q,lock):
