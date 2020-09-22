def count_mean(data):
	size = len(data)
	datasum = 0
	for i in range(size):
		datasum += data[i]
	mean = datasum / size
	return mean

def count_variance(data, mean):
	size = len(data)
	datasum = 0
	for i in range(size):
		datasum += (data[i] - mean) * (data[i] - mean)
	variance = datasum / size
	return variance

def print_result(date, quarantine_list, money):
	print(date, " : ")
	data = []
	density = []
	inhabited = 0
	for i in range(len(quarantine_list)):
		#print(i, " infection rate : ", quarantine_list[i].infect_rate, " density : ", quarantine_list[i].inhabited / quarantine_list[i].capacity, "inhabited : ", quarantine_list[i].inhabited)
		data.append(quarantine_list[i].infect_rate)
		density.append(quarantine_list[i].inhabited / quarantine_list[i].capacity)
		inhabited += quarantine_list[i].inhabited
	mean = count_mean(data)
	var = count_variance(data, mean)
	density_mean = count_mean(density)
	density_variance = count_variance(density, mean)
	print("infection rate mean : ", mean)
	print("infection rate variance : ", var)
	#print("inhabited room : " , inhabited)
	#print("density mean : ", density_mean)
	#print("density variance : ", density_variance)
	print("cost : ", int(money))

def add_cost(quarantine_list):
	total_cost = 0
	for location in quarantine_list:
		total_cost = total_cost + 116000 * location.infect_rate
	return total_cost

class Country(object):
	def __init__(self, CountryName, CountryID, pop):
		self.name = CountryName
		self.id   = CountryID
		self.confirmed = 0
		self.population = pop   #該國
		self.abroad_cases = 0   #該國在台灣確診人數
		self.country_infection_rate = 0	 
		self.country_abroad_rate = 0
	def increase(self, confirmed_num, abroad_num, all_cases_sum):
		self.confirmed = self.confirmed + confirmed_num
		self.abroad_cases = self.abroad_cases + abroad_num
		self.country_infection_rate = self.confirmed / self.population
		self.country_abroad_rate = self.abroad_cases / all_cases_sum #該國在台灣確診人數 / 境外移入病例總人數

class Quarantine(object):
	def __init__(self, dist, cap, money, time):
		self.distance = dist
		self.capacity = cap
		self.inhabited = 0
		self.full = False
		self.infect_rate = 0
		self.customer_list = []
		self.cost = money
		self.customer_today = 0
		self.time = time
		self.cap_per_taxi = int(480 / (time * 2))
	def increase(self, customer, country_list, country_dict):
		if self.full:
			print("Error!")
		else:
			self.customer_today = self.customer_today + 1
			self.inhabited = self.inhabited + 1
			self.customer_list.append(customer)
			self.infect_rate = self.count_rate(country_list, country_dict)
			if self.inhabited == self.capacity:
				self.full = True
	def decrease(self, index, country_list, country_dict):
		if self.customer_today != 0:
			self.customer_today -= 1
		self.customer_list.pop(index)
		self.inhabited = self.inhabited - 1
		self.full = False
		self.infect_rate = self.count_rate(country_list, country_dict)
	def count_rate(self, country_list, country_dict):
		#感染率平方和 * 入住率
		total = 0
		for i in self.customer_list:
			i.infect_rate = i.count_rate(country_list, country_dict)
			total = total + i.infect_rate * i.infect_rate
		return total * self.inhabited / self.capacity
	def kick_out(self, date, country_list, country_dict):
		self.customer_today = 0
		kick_out_count = 0
		kick_list = []
		for i in range(len(self.customer_list)):
			if (self.customer_list[i].date + 14) <= date:
				kick_list.append(i)
		kick_list.sort(reverse=True)
		kick_out_count = 0
		for i in range(len(kick_list)):
			self.decrease(kick_list[i], country_list, country_dict)

class Passenger(object):
	def __init__(self, state, require, sympt1, sympt2, day):
		self.country = state #country from
		self.need = require #need to live in hotel
		self.symptom1 = sympt1 #cough
		self.symptom2 = sympt2 #fever
		self.infect_rate = 0
		self.date = day #arrive date in integer
	def count_rate(self, country_list, country_dict):
		return 0.3 * (self.symptom1) + 0.3 * (self.symptom2) + 0.2 * country_list[country_dict[self.country]].country_infection_rate + 0.2 * country_list[country_dict[self.country]].country_abroad_rate  
		#0.3 * sympt1 + 0.3 * sympt2 + 0.2 * country infection rate + 0.2 * abroad case rate

class Patient(object):
	def __init__(self, date, countries):
		self.confirm_date = date
		self.country = []
		while countries:
			self.country.append(countries.pop())
			



