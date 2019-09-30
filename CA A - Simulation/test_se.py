import math

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

list_num = [170.5, 160, 161, 170, 150.5]
print(calculate_standard_error(list_num))