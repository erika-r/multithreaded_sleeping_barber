import threading,time,random,string

waiting_room = []
sleeping = []		#list of sleeping barbers
lock = threading.Lock()
seats = 15		#amount of seats in the waiting room

class Barber():

	def __init__(self, name):
		self.name = name
		self.event = threading.Event()
		print("{}: Hello :)\n".format(self.name))

	def cut(self):
		customer = waiting_room.pop(0)		#first in first out
		lock.release()				#exiting critical section
		print("{}: What would you like, {}?\n".format(self.name,customer.name))
		print("{}: Just a little trim please, {}.\n\n{}: * Cutting {}'s hair *\n".format(customer.name,self.name,self.name,customer.name))
		time.sleep(random.randrange(1,3)*0.80)		#how long the cut takes
		print("{}: You're done now, {}, please come again!! ....Next!!\n".format(self.name, customer.name))

	def work(self):
		global customers
		self.event.wait()
		while True:

			while self.event.is_set():		#while barber is awake
	
				lock.acquire()				#entering critical section
				if len(waiting_room) >= 1:
					self.cut()
	
				elif len(waiting_room) == 0:
					sleeping.append(self)
					print("{}: No customers? Guess I'll take a little nap ... zzzzz\n".format(self.name))
					self.sleep()

	def sleep(self):
		self.event.clear()
		lock.release()		#exiting critical section

	def wakeUp(self):
		sleeping.pop(sleeping.index(self))
		print("{}: Me? Sleeping on the job? Never!\n".format(self.name))
		self.event.set()		#allow barber to work again


class Customer():
	global Bob, Bobby, Robert

	def __init__(self,name):
		self.name = name

	def get_barber():						#look for the free barber
		return random.choice(sleeping)		#give random barber that was sleeping

	def look_for_seat(customers):

		waiting_room.append(customers.pop(0))
		time.sleep(2)		#give barbers time to set up

		while customers:

			time.sleep(random.randrange(0,3)*0.25)

			if len(sleeping) >= 1 and len(waiting_room) == 0:		#conditions must be checked again since time has passed
				lock.acquire()			#critical section
				print("{}: Is he sleeping..?\n".format(customers[0].name))
				waiting_room.append(customers.pop(0))
				Customer.get_barber().wakeUp()
				lock.release()			#exiting critical section

			while customers and len(sleeping) == 0:

				time.sleep(random.randrange(0,3)*0.25)

				if len(waiting_room) < seats and len(sleeping) == 0:			#len(sleeping) must be checked again because time has passed 
					lock.acquire()		#critical section
					print("{}: I'll wait\n".format(customers[0].name))
					waiting_room.append(customers.pop(0))
					lock.release()		#exiting critical section
	
				elif len(waiting_room) == seats:
					lock.acquire()			#critical section 
					print("{}: Waiting room is full, guess I'll come back tomorrow.\n".format(customers.pop(0).name))
					lock.release()		#exiting critical section

def main():

	global Bob, Bobby, Robert, customers
	
	#Barbers
	Bob = Barber("Bob")
	Bobby = Barber("Bobby")
	Robert = Barber("Robert")
	
	customers = [Customer("Customer {}".format(i)) for i in (range(1000))]	#customers that will enter at some point

	customer = threading.Thread(target=Customer.look_for_seat, args=[customers]).start()
	Bob.event.set()
	Bobby.event.set()
	Robert.event.set()
	
	workingBarber1 = threading.Thread(target=Barber.work,args=[Bob]).start()
	workingBarber2 = threading.Thread(target=Barber.work,args=[Bobby]).start()
	workingBarber3 = threading.Thread(target=Barber.work,args=[Robert]).start()

if __name__ == '__main__':
	main()