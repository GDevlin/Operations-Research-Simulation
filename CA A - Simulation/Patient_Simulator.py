#Simulation of hospital queue
from datetime import time
from datetime import timedelta
import datetime
import random
import math

#Server Class
class Server:
	def __init__(self, number, rate):
		self.number = number
		self.rate = rate
		self.service_time = int(60/rate)
		self.is_free = True
		self.next_free = 0
		self.time_idle = 0

		self.server_gender = "unknown"
		self.server_break_times = []
		self.is_server_on_break = False
		self.experience = "normal"

	def get_server_number(self):
		return self.number

	def get_is_free(self):
		return self.is_free

	def get_service_time(self):
		return self.service_time

	def get_next_free(self):
		return self.next_free

	def get_time_idle(self):
		return self.time_idle

	def get_gender(self):
		return self.server_gender

	def get_server_break_times(self):
		return self.server_break_times

	def get_server_on_break(self):
		return self.is_server_on_break

	def get_server_experience(self):
		return self.experience

	def set_next_free(self, next_free):
		self.next_free = next_free

	def set_is_free(self, free_status):
		self.is_free = free_status

	def set_time_idle(self, time_idle):
		self.time_idle = time_idle

	def set_gender(self, server_gender):
		self.server_gender = server_gender

	def subtract_from_time_idle(self, time_to_subtract):
		time_to_subtract_seconds = timedelta(seconds = time_to_subtract * 60)
		self.time_idle = self.time_idle - time_to_subtract_seconds

	def set_server_break_times(self, server_break_times):
		self.server_break_times = server_break_times

	def set_server_on_break(self, break_status):
		self.is_server_on_break = break_status

	def set_experience(self, experience):
		self.experience = experience

#Customer Class
class Customer:
	def __init__(self, number, arrival_time):
		self.number = number
		self.arrival_time = arrival_time
		self.has_been_serviced = False

		self.time_admitted = 0
		self.time_in_queue = 0
		self.departure_time = 0
		self.which_sever = 0

		self.c_gender = "unknown"
		self.visiting_status = "regular"

	def __str__(self):
		return "Customer %s Arrival Time %s" % (self.number, self.arrival_time)

	def get_customer_number(self):
		return self.number

	def get_arrival_time(self):
		return self.arrival_time

	def get_customer_number(self):
		return self.number

	def get_has_been_serviced(self):
		return self.has_been_serviced

	def get_which_server(self):
		return self.which_sever

	def get_departure_time(self):
		return self.departure_time

	def get_time_admitted(self):
		return self.time_admitted

	def get_time_in_queue(self):
		return self.time_in_queue

	def get_customer_gender(self):
		return self.c_gender

	def get_visiting_status(self):
		return self.visiting_status

	def set_arrival_time(self, arrival_time):
		self.arrival_time = arrival_time

	def set_has_been_serviced(self, service_status):
		self.has_been_serviced = service_status

	def set_departure_time(self, departure_time):
		self.departure_time = departure_time

	def set_which_server(self, which_sever):
		self.which_sever = which_sever

	def set_time_admitted(self, time_admitted):
		self.time_admitted = time_admitted

	def set_queue_time(self, time_in_queue):
		self.time_in_queue = time_in_queue

	def set_customer_gender(self, c_gender):
		self.c_gender = c_gender

	def set_visiting_status(self, visiting_status):
		self.visiting_status = visiting_status


#Parse time to create a time object
def parse_time(time_string):
	time_input = time_string.split(".")
	input_hour = int(time_input[0])
	input_minute = int(time_input[1])
	time_object = time(input_hour, input_minute)
	return time_object

#Add/take away minutes from time
def add_minutes_to_time(time_object, minutes):
	time_hour = time_object.hour
	time_minute = time_object.minute + minutes
	if time_minute >= 60:
		time_minute = time_minute - 60
		time_hour += 1
	elif time_minute < 0:
		time_minute = 60 + (time_minute)
		time_hour -= 1

	if time_hour == 24:
		time_hour = 0
	
	new_time = time(time_hour, time_minute)
	return new_time

#Generate a uniformally distributed list of times
#Starting with start times
def generate_arrival_times(start_time, last_time, arrival_rate):
	list_of_times = []
	arrival_interval = int(60/arrival_rate)

	list_of_times.append(start_time)
	next_time = start_time
	while next_time <= last_time:
		next_time = add_minutes_to_time(next_time, arrival_interval)
		if next_time <= last_time:
			list_of_times.append(next_time)

	return list_of_times

#Add standard deviation to times
def deviate_times(list_of_times, stand_dev):
	deviated_list_of_times = []

	for arr_time in list_of_times:
		minute_variation = random.randint(stand_dev * -1, stand_dev)
		deviated_time = add_minutes_to_time(arr_time, minute_variation)
		deviated_list_of_times.append(deviated_time)

	return deviated_list_of_times

#Later time should be second
def difference_between_times(first_time, second_time):
	first_delta = timedelta(hours = first_time.hour, minutes = first_time.minute, seconds = first_time.second)
	second_delta = timedelta(hours = second_time.hour, minutes = second_time.minute, seconds = second_time.second)
	time_diff = second_delta - first_delta
	return time_diff

def possoin_dristributed_times(customers, start_time, end_time):
	print("possoin_times")
	poisson_times = []
	num_of_customers = len(customers)
	p_count = 0
	while p_count < num_of_customers:
		rand_hour = random.randint(start_time.hour, end_time.hour)
		rand_minute = random.randint(0, 59)
		rand_time = time(rand_hour, rand_minute)

		if start_time <= rand_time <= end_time:
			poisson_times.append(rand_time)
			p_count += 1

	poisson_times.sort()
	i = 0
	for p_time in poisson_times:
		customers[i].set_arrival_time(p_time)
		i += 1

	return customers

def service_customers(servers, customers, start_time, last_time):
	current_time = customers[0].get_arrival_time()
	longest_server_time = 0
	for serv in servers:
		if serv.get_service_time() > longest_server_time:
			longest_server_time = serv.get_service_time()

	latest_time = add_minutes_to_time(last_time, longest_server_time)
	serviced_customers = [] 

	print()
	print("Customer arriving and being served.")

	all_customers_served = False

	while all_customers_served == False:
	#while current_time <= latest_time:
		for cust in customers:
			#Customer Arrived
			if cust.get_arrival_time() == current_time:
				print(current_time, "Customer", cust.get_customer_number(), "arrived")
			#Customer Departed
			elif cust.get_departure_time() == current_time:
				#Set server free
				for serv in servers:
					if cust.get_which_server() == serv.get_server_number():
						if serv.get_server_on_break() == False:
							serv.set_is_free(True) 

		#Is it a servers break time
		for serv in servers:
			if current_time in serv.get_server_break_times():
				if serv.get_is_free():
					end_of_break = add_minutes_to_time(current_time, 30)
					serv.set_next_free(end_of_break)
					serv.set_server_on_break(True)
				else:
					end_of_break = add_minutes_to_time(serv.get_next_free(), 30)
					serv.set_next_free(end_of_break)
					serv.set_server_on_break(True)

			#Is a break over
			if current_time == serv.get_next_free() and serv.get_server_on_break() == True:
				serv.set_is_free(True)

		#Is server free for unseen customers
		for serv in servers:
			if serv.get_is_free():
				#If a server is free, see a customer that has arrived
				for cust in customers:
					if (cust.get_arrival_time() <= current_time and 
						cust.get_has_been_serviced() == False and cust.get_customer_gender() == serv.get_gender()): 

						#Announce Action

						#Set server info
						serv.set_is_free(False)
						server_next_free = add_minutes_to_time(current_time, serv.get_service_time())
						if cust.get_visiting_status() == "new":
							server_next_free = add_minutes_to_time(current_time, serv.get_service_time()*2)	
						if serv.get_server_experience() == "experienced":
							server_next_free = add_minutes_to_time(current_time, int(serv.get_service_time()/2))

						serv.set_next_free(server_next_free)
						
						#Set customer info
						cust.set_has_been_serviced(True)
						
						customer_departure_time = add_minutes_to_time(current_time, serv.get_service_time())
						if cust.get_visiting_status() == "new":
							customer_departure_time = add_minutes_to_time(current_time, serv.get_service_time()*2)
						if serv.get_server_experience() == "experienced":
							customer_departure_time = add_minutes_to_time(current_time, int(serv.get_service_time()/2))
						cust.set_departure_time(customer_departure_time)
						cust.set_which_server(serv.get_server_number())
						cust.set_time_admitted(current_time)
						customer_queueing_time = difference_between_times(cust.get_arrival_time(), cust.get_time_admitted())
						cust.set_queue_time(customer_queueing_time)
						break

		cust_count = 0
		for cust in customers:
			if cust.get_has_been_serviced() == True:
				cust_count += 1

		if cust_count == len(customers):
			all_customers_served = True


		current_time = add_minutes_to_time(current_time, 1)

	return customers

def print_output(customers, gender_choice, new_regular_choice):

	print()
	print("Output from this run")
	print("Customer no. \t\t Actual Arrival time \t Admitted to server \t departed server \t queue time")

	for cust in customers:
		server_string = "(" + str(cust.get_which_server()) + ")"

		additonal_string = "\t"
		if gender_choice == 'y':
			additonal_string += ", " + str(cust.get_customer_gender())
		if new_regular_choice == 'y':
			additonal_string += ", " + str(cust.get_visiting_status())

		print(cust.get_customer_number(), '\t\t\t', cust.get_arrival_time(), '\t\t', cust.get_time_admitted(), server_string, '\t', cust.get_departure_time(), '\t\t', cust.get_time_in_queue(), additonal_string)
		

def performence_metrics(servers, customers):

	print()
	print("Final Performence Metrics (from this cycle)")
	# Avg time a customer is in system
	total_time_in_system = 0
	total_time_in_queue = 0

	# Maximum time a customer spends in service and in queue
	max_time_in_system = 0
	max_time_in_queue = 0 

	for cust in customers:

		time_in_system = difference_between_times(cust.get_arrival_time(), cust.get_departure_time())
		#Convert time to minutes, timedeltas store time in seconds
		time_in_system = time_in_system.seconds / 60
		total_time_in_system += time_in_system

		time_in_queue = cust.get_time_in_queue().seconds / 60
		total_time_in_queue += time_in_queue

		if time_in_system > max_time_in_system:
			max_time_in_system = time_in_system

		if time_in_queue > max_time_in_queue:
			max_time_in_queue= time_in_queue


	avg_time_in_system = total_time_in_system/len(customers)
	avg_time_in_queue = total_time_in_queue/len(customers)

	#Time server spent idle
	first_time = customers[0].get_arrival_time()
	second_time = customers[len(customers)-1].get_departure_time()
	total_time_in_day = difference_between_times(first_time, second_time)

	time_all_servers_idle = timedelta()
	for serv in servers:
		serv.set_time_idle(total_time_in_day)
		for cust in customers:
			if cust.get_which_server() == serv.get_server_number():
				if serv.get_server_experience() == "experienced":
					serv.subtract_from_time_idle(int(serv.get_service_time()/2))
				else:
					serv.subtract_from_time_idle(serv.get_service_time())

		#time_server_spent_idle = difference_between_times(total_time_servicing, total_time_in_day)
		#serv.set_time_idle(time_server_spent_idle)
		print("Amount of time server ", serv.get_server_number(), "was idle:", serv.get_time_idle())
		time_all_servers_idle += serv.get_time_idle()


	#Avg number in queue, system
	current_time = first_time
	minute_count = 0
	in_system_times = []
	in_queue_times = []
	currently_in_system = 0
	currently_in_queue = 0
	while current_time <= second_time:
		for cust in customers:
			if current_time == cust.get_arrival_time():
				currently_in_system += 1
				currently_in_queue += 1

			if current_time == cust.get_time_admitted():
				currently_in_queue -= 1

			if current_time == cust.get_departure_time():
				currently_in_system -= 1

		in_system_times.append(currently_in_system)
		in_queue_times.append(currently_in_queue)

		current_time = add_minutes_to_time(current_time, 1)
		minute_count += 1

	print(minute_count)
	avg_num_in_system = sum(in_system_times)/minute_count
	avg_num_in_queue = sum(in_queue_times)/minute_count
	

	#Print Metrics
	print("Avg. time of a customer in system (W):", avg_time_in_system)
	print("Avg. time of a customer in queue (Wq):", avg_time_in_queue)
	print("Max time a customer spends in system: ", max_time_in_system)
	print("Max time a customer spends in queue: ", max_time_in_queue)
	print("Total time all servers were idle: ", time_all_servers_idle)
	print("Avg. in system at any given minute: ", avg_num_in_system)
	print("Avg. in queue at any given minute: ", avg_num_in_queue)

	rep_performence_metrics = []
	rep_performence_metrics.append(avg_time_in_system)
	rep_performence_metrics.append(avg_time_in_queue)
	rep_performence_metrics.append(max_time_in_system)
	rep_performence_metrics.append(max_time_in_queue)
	rep_performence_metrics.append(time_all_servers_idle)
	rep_performence_metrics.append(avg_num_in_system)
	rep_performence_metrics.append(avg_num_in_queue)

	#time last customer leaves
	rep_performence_metrics.append(customers[len(customers)-1].get_departure_time())

	return rep_performence_metrics

def calculate_standard_error(list_of_num):
	mean_of_list = sum(list_of_num)/float(len(list_of_num))

	deviations_from_mean = []
	for num in list_of_num:
		deviation = mean_of_list - num
		deviation = deviation * deviation#Square number to get rid of negatives
		deviations_from_mean.append(deviation)

	total_squared_deviations = sum(deviations_from_mean)
	total_squared_deviations = total_squared_deviations/(len(list_of_num)-1)
	sd = math.sqrt(total_squared_deviations)

	se = sd/(math.sqrt(len(list_of_num)))
	return se

def calculate_standard_error_timedelta(list_of_timedelta):
	td_list = []
	for t in list_of_timedelta:
		td_list.append(t.seconds)

	mean_of_list = sum(td_list)/float(len(td_list))

	deviations_from_mean = []
	for num in td_list:
		deviation = mean_of_list - num
		deviation = deviation * deviation#Square number to get rid of negatives
		deviations_from_mean.append(deviation)

	total_squared_deviations = sum(deviations_from_mean)
	total_squared_deviations = total_squared_deviations/(len(td_list)-1)
	sd = math.sqrt(total_squared_deviations)

	se = sd/(math.sqrt(len(td_list)))
	return se/60

def main():

	#Default values
	# num_servers = 2
	# server_rate = 4
	# arrival_rate = 6
	# stand_dev = 5
	# scheduling_choice = 'r'

	# time_string = "9.05"
	# last_time_string = "17.30"

	# replications = 100
	
	#User Input
	num_servers = int(input("Number of servers: "))
	server_rate = int(input("Server rate: "))# Rate servers take per hour

	arrival_rate = int(input("Arrival Rate: "))
	

	#first customer enters service
	time_string = input("Enter start time: ")
	start_time = parse_time(time_string)

	#last time a customer can enter service
	last_time_string = input("Enter end time: ")
	last_time = parse_time(last_time_string)

	stand_dev = int(input("Standard Deviation in minutes: "))#Standard Deviation in minutes
	scheduling_choice = input("Random uniform distribution (r) or Possoin Distribution (p): ")

	gender_choice = input("Would you like specific servers for each gender (y/n): ")

	break_choice = input("Would you like the servers to have breaks (y/n): ")

	new_regular_choice = input("Would you like new and regualr customers(y/n): ")
	if new_regular_choice == 'y':
		percent_new  = int(input("What percentage of the customers should be new: "))
		new_at_front = input("Would you like all new customers moved to the front (y/n): ")

	experienced_server_choice = input("Is the lead server more experienced (y/n): ")

	#Replicate from here:
	replications = int(input("How many replications: "))

	total_avg_time_in_system = []
	total_avg_time_in_queue = []
	total_max_time_in_system = []
	total_max_time_in_queue = []
	total_time_servers_idle = []
	total_avg_num_in_system = []
	total_avg_num_in_queue = []

	times_last_customer_leaves = []

	rep_count = 0
	while rep_count < replications:
		#Generated list of arrival times
		list_of_times = generate_arrival_times(start_time, last_time, arrival_rate)
		list_of_times = deviate_times(list_of_times, stand_dev)
		list_of_times.sort()

		# Create a list of servers
		servers = []
		server_count = 1
		while server_count <= num_servers:
			server_name = "Server " + str(server_count)
			server = Server(server_name, server_rate)
			servers.append(server)
			server_count += 1

		#Create a list of customers
		customers = []
		customer_count = 1
		for arr_time in list_of_times:
			new_customer = Customer(customer_count, arr_time)
			customers.append(new_customer)
			customer_count += 1

		#Poisson Distributed times
		if scheduling_choice == 'p':
			customers = possoin_dristributed_times(customers, start_time, last_time)

		#Give customers genders
		if gender_choice == 'y':
			genders = ["male", "female"]

			for cust in customers:
				cust.set_customer_gender(random.choice(genders))

			next_gender = 0
			for serv in servers:
				if next_gender == 0:
					serv.set_gender(genders[0])
					next_gender = 1
				elif  next_gender == 1:
					serv.set_gender(genders[1])
					next_gnder = 0

		#Give customers new or regular status
		if new_regular_choice == 'y':
			amount_to_change = int((len(customers)*percent_new)/100)
			if new_at_front == 'y':
				i = 0
				while i < amount_to_change:
					customers[i].set_visiting_status("new")
					i += 1
			else:
				print("change change_index", int(amount_to_change))
				i = 1
				while i <= len(customers):
					if i % int(amount_to_change) == 0:
						customers[i-1].set_visiting_status("new")
					i += 1

		
		[print(cust.get_visiting_status()) for cust in customers]

		#Make lead server more experienced
		if experienced_server_choice == 'y':
			servers[0].set_experience("experienced")

		[print(serv.get_server_experience()) for serv in servers]

		#Give serverrs break times
		set_of_break_times =[[parse_time("10.45"), parse_time("14.45")], [parse_time("11.15"), parse_time("15.15")]]
		next_break_set = 0
		if break_choice == 'y':
			for serv in servers:
				if next_break_set == 0:
					serv.set_server_break_times(set_of_break_times[0])
					next_break_set = 1
				elif next_break_set == 1:
					serv.set_server_break_times(set_of_break_times[1])
					next_break_set == 0

		print("Service customers throughout day")
		customers = service_customers(servers, customers, start_time, last_time)

		#output
		print_output(customers, gender_choice, new_regular_choice)

		rep_performence_metrics = performence_metrics(servers, customers)

		#Collect results from this cyclle
		total_avg_time_in_system.append(rep_performence_metrics[0])
		total_avg_time_in_queue.append(rep_performence_metrics[1])
		total_max_time_in_system.append(rep_performence_metrics[2])
		total_max_time_in_queue.append(rep_performence_metrics[3])
		total_time_servers_idle.append(rep_performence_metrics[4])
		total_avg_num_in_system.append(rep_performence_metrics[5])
		total_avg_num_in_queue.append(rep_performence_metrics[6])

		times_last_customer_leaves.append(rep_performence_metrics[7])

		rep_count += 1
	
	# Final Replication Results
	print()
	print("After all replications")
	print("Total average time in system: ", round(sum(total_avg_time_in_system)/replications, 4), "minutes")
	print("\t\t standarad error: ", round(calculate_standard_error(total_avg_time_in_system), 4))

	print("Total average time in queue: ", round(sum(total_avg_time_in_queue)/replications, 4), "minutes")
	print("\t\t standarad error: ", round(calculate_standard_error(total_avg_time_in_queue), 4))


	print("Average of maximum time spent in system: ", round(sum(total_max_time_in_system)/replications, 4), "minutes")
	print("\t\t standarad error: ", round(calculate_standard_error(total_max_time_in_system), 4))

	print("Average of maximum time spent in queue: ", sum(total_max_time_in_queue)/replications, "minutes")
	print("\t\t standarad error: ", round(calculate_standard_error(total_max_time_in_queue), 4))
	
	total_idle_time = 0
	for idle_time in total_time_servers_idle:
		total_idle_time += idle_time.seconds
	total_idle_time = total_idle_time/replications
	total_idle_time_delta = timedelta(seconds = int(total_idle_time))
	print("Average amount of time all servers were idle: ", total_idle_time_delta, "minutes")
	print("\t\t standarad error: ", round(calculate_standard_error_timedelta(total_time_servers_idle), 4))

	print("Average number in system at any given minute: ",	round(sum(total_avg_num_in_system)/replications, 4))
	print("\t\t standarad error: ", round(calculate_standard_error(total_avg_num_in_system), 4))

	print("Average nummber in queue at any given time: ",	round(sum(total_avg_num_in_queue)/replications, 4))
	print("\t\t standarad error: ", round(calculate_standard_error(total_avg_num_in_queue), 4))

	total_seconds = 0
	for last_time in times_last_customer_leaves:
		t_delta = timedelta(hours = last_time.hour, minutes = last_time.minute ,seconds = last_time.second)
		total_seconds += t_delta.seconds

	avg_last_time = timedelta(seconds = total_seconds/len(times_last_customer_leaves))
	print("Avg. time last customer left: ", avg_last_time)

if __name__ == '__main__':
	main()