import util
import csv
import numpy as np
import random
from read_csv import read_csv

def deal_data():
    random.seed('AI_project')
    quarantine_place_list =  read_hotel()
    country_dict, country_list = read_country()
    patient_list = create_patient_list()
    passenger_list = create_passenger_list(country_list, country_dict)
    global_time_series = read_global_time_series(country_dict)
    '''for k, v in country_dict.items():
		print(k, v)
		c = country_list[v]
		print(c.name, c.id, c.population)'''
    return (quarantine_place_list, country_dict, country_list ,patient_list, passenger_list, global_time_series) 
    #quarantine_list, country_dict, country_list ,patient_list, passenger_list, global_time_series = deal_data()

'''def read_csv(file_path):
    with open(file_path, newline='') as datafile:
        data = csv.reader(datafile)
        data = list(data)
        return data'''

def read_country():
    visitor_path = 'visitor_monthly.csv'
    population_path = 'WorldPopulation2020 dataset.csv'
    #abroad_case_path = 'Abroad_Cases.csv'

    #with open(visitor_path, newline='') as datafile:
    #	visitor_data = csv.reader(datafile)
    #	visitor_data = list(visitor_data)
    visitor_data = read_csv(visitor_path)
    population_data = read_csv(population_path)
    #abroad_case_data = read_csv(abroad_case_path)
    
    population_dict = dict()
    for i in range(1, len(population_data)):
        population_dict[population_data[i][0]] = int(population_data[i][1])

    country_list = list()
    country_dict = dict()
    for i in range(1, len(visitor_data)):
    	name = visitor_data[i][0]
    	index = i - 1
    	pop = population_dict[name]

    	country_list.append(util.Country(name, index, pop))
    	country_dict[name] = index
    return (country_dict, country_list)



def read_hotel():
    file_path = 'hotel_info.csv'
	
    with open(file_path, newline='') as datafile:
    	data = csv.DictReader(datafile)
    	data = list(data)
    for d in data:
    	d.update((k, float(v)) for k, v in d.items())
    quarantine_list = list()

    for h in data:
        if h['price'] < 0:
        	break
        #q = util.Quarantine(h['distance2airport'],h['capacity'], h['price'])
        q = util.Quarantine(h['distance2airport'], h['capacity'], h['price'], h['time2airport'])
        quarantine_list.append(q)
    #for i in quarantine_list:
    #	print(i.distance, i.capacity, i.cost)

    return quarantine_list

def create_patient_list(file_path = 'Abroad_Cases.csv'):
	data = read_csv(file_path)
	patient_list = []
	data.pop(0)
	for row in data:
		countries = list(filter(None, [row[i]for i in range(3, 7)]))
		new_patient = util.Patient(int(row[7]), countries)
		patient_list.append(new_patient)
	return patient_list

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

def distribute_last_5_percent(seq, day):
    n = int(len(seq) * 0.05)
    tmp = seq[0:n]
    del seq[0:n]
    seq = list(split(seq, day))
    for i in tmp:
        index = random.randint(0, day - 1)
        seq[index].append(i)


    return seq

def create_passenger_list(country_list, country_dict, file_path = 'visitor_monthly.csv'): #passenger_list[0-3][0-29][i]
    visitor_data = read_csv(file_path)
    month_list = [[], [], [], []]
    for i in range(4):
        for j in range(1, len(visitor_data)):
            country = visitor_data[j][0]
            n = int(visitor_data[j][i + 1])
            month_list[i] += n * [country]
        random.shuffle(month_list[i])
    
    

    month_list[0] = distribute_last_5_percent(month_list[0], 10)
    month_list[1] = distribute_last_5_percent(month_list[1], 29)
    month_list[2] = distribute_last_5_percent(month_list[2], 31)
    month_list[3] = distribute_last_5_percent(month_list[3], 30)

    

    day_list = []
    for i in range(len(month_list)):
        day_list += month_list[i]
    
    passenger_list = list()
    for index in range(len(day_list)):
        passenger_today = list()
        for num in range(len(day_list[index])):
            country = day_list[index][num]
            date = index
            need = False
            fever = False
            cough = False
            if random.randint(0, max(299 - (index * 4) , 0)) == 0:
                need = True

            if random.randint(0, 999) == 0:
                fever = True

            if random.randint(0, 199) == 0:
                cough = True
            new_passenger = util.Passenger(country, need, cough, fever, date)
            new_passenger.infect_rate = new_passenger.count_rate(country_list, country_dict)
            passenger_today.append(new_passenger)
        passenger_list.append(passenger_today)
    return passenger_list

def read_global_time_series(country_dict, file_path = 'time_series_covid19_confirmed_global.csv'):
    with open(file_path, newline='') as datafile:
        data = csv.DictReader(datafile)
        data = list(data)
    n = len(data)
    i = 1
    while i < n:
        if data[i]['Country/Region'] not in country_dict:
            del data[i]
            n -= 1
            i -= 1
        i += 1
   
    global_time_series = dict()
    for i in range(1, len(data)):
        global_time_series[data[i]['Country/Region']] = data[i]

    for name in global_time_series:
        del global_time_series[name]['Country/Region']
        
        global_time_series[name] = {int(k): int(v) for k,v in global_time_series[name].items()}
    

    return global_time_series # global_time_series['country name']['day'] is dict in dict both is string


if __name__ == '__main__':
    quarantine_list, country_dict, country_list ,patient_list, passenger_list, global_time_series = deal_data()
    
