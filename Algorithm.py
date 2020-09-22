import os
from util import *
from input import *
import random
import numpy as np
from io import StringIO
from read_csv import read_csv

if __name__ == '__main__':
	date = 0	 #距離1/22天數
	flag = False #是否所以旅館都爆滿
	quarantine_list, country_dict, country_list, patient_list, passenger_list, country_confirmed_case = deal_data() #讀資料
	country_abroad_case = np.zeros(len(country_list))
	confirmed_num = 0 #台灣境外移入確診人數
	cost = 0	#當前消耗
	MAX_INT = float('inf')
	
	while(passenger_list and not flag):
		country_abroad_case = np.zeros(len(country_list)) #歸零各國當日在台灣新增之確診人數
		
		while(patient_list[0].confirm_date <= date): #計算各國當日在台灣新增之確診人數
			confirmed_num = confirmed_num + 1
			new = patient_list.pop(0)
			for i in range(len(new.country)):
				if new.country[i] in country_dict:
					country_abroad_case[country_dict[new.country[i]]] = country_abroad_case[country_dict[new.country[i]]] + 1
		
		for country in country_list:	#新增各國國內新增確診人數
			country.increase(country_confirmed_case[country.name][date], country_abroad_case[country.id], confirmed_num)
		
		for location in quarantine_list:	#更新防疫旅館人員
			location.kick_out(date, country_list, country_dict)
		
		entry_list = passenger_list.pop(0)	#pop當天旅客名單

		used_hotel =[] #hotel that have patients inside, to indicate we have taxi there

		while(entry_list and not flag):
			next_passenger = entry_list.pop()	#pop下一名旅客
			if(next_passenger.need):	#旅客需要住宿
				dest = -1
				# 決定送旅客去哪
				# 距離計算方式更改：假設一台防疫計程車一天可以載送 location.cap_per_taxi 的人
				# 一台防疫計程車補助3500，因此希望花越少台計程車越好
				# 因此當決定要不要送去旅館時，需考慮那間旅館今天已經送去多少人，旅館感染率，以及價格
				# 如何決定：argmin x: 116000 * location.infect_rate + 3500 * 運送人次是否為y的倍數
				full_list = []
				for i in range(len(quarantine_list)):
					if not quarantine_list[i].full:
						quarantine_list[i].increase(next_passenger, country_list, country_dict)
					else:
						full_list.append(i)

				if not used_hotel:
					risk_temp = MAX_INT
					for i in range(len(quarantine_list)):
						if (not i in full_list and quarantine_list[i].infect_rate < risk_temp):
							dest = i
					used_hotel.append(dest)

				else:
					ok = 1
					for used in used_hotel:
						for hotel in quarantine_list:
							risk_difference = quarantine_list[used].infect_rate - hotel.infect_rate #determine whether the risk difference > 30%
							if (risk_difference >= 0.03):
								ok = 0

					if ok: #if the risk difference still < 30%, just use the used hotel (to minimize the taxi fees)
						idx = -1
						risk_temp = MAX_INT
						for i in used_hotel: 
							if (i not in full_list and quarantine_list[i].infect_rate < risk_temp): 
								risk_temp = quarantine_list[i].infect_rate
								idx = i

						if idx != -1:
							dest = idx
						else: # if the used hotel capacity already full, search for the new place that has lower risk in quarantine list
							
							for i in range(len(quarantine_list)):
								if (i not in full_list and quarantine_list[i].infect_rate < risk_temp):
									risk_temp = quarantine_list[i].infect_rate
									idx = i

							dest = idx

					else:  #if the risk difference of some hotels > 30%, send the customer to the new hotel with lower risk ( so the risk difference not really high)
						idx = -1
						risk_temp = MAX_INT

						for i in range(len(quarantine_list)):
								if (i not in full_list and quarantine_list[i].infect_rate < risk_temp):
									risk_temp = quarantine_list[i].infect_rate
									idx = i


						dest = idx



				if dest != -1:
					if dest not in used_hotel:
						used_hotel.append(dest)
					for i in range(len(quarantine_list)):
						if i != dest and i not in full_list:
							quarantine_list[i].decrease(quarantine_list[i].inhabited - 1, country_list, country_dict)
					space = quarantine_list[dest].customer_today % quarantine_list[dest].cap_per_taxi #我是這臺車的第幾個人 0代表滿了
					cost = cost + 3500 * (space == 1)
					if space == 0:
						used_hotel.remove(dest)
				else:
					flag = True
					print("Quarantine FULL Error!")
		#cost = cost + add_cost(quarantine_list)	
		print_result(date, quarantine_list, cost)
		date = date + 1