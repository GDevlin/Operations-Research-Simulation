
# Get 1000 random numbers and their frequencies
from scipy.stats import chisquare
import random
import math

def populate_dictionary(num_range):
	num_count = {}
	i = 0
	while i < num_range:	
		num_count[str(i)] = 0
		i += 1
	return num_count

def chi_sqaure_test(num_count):
	num_frequencies = list(num_count.values())
	chi_sqaure_stat = chisquare(num_frequencies)
	return chi_sqaure_stat

def language_random(num_integers, num_range, num_count):
	num_count = populate_dictionary(num_range)

	for i in range(num_integers):
		rand_num = random.randint(0, num_range - 1)
		if str(rand_num) in num_count:
			num_count[str(rand_num)] += 1
		else:
			num_count[str(rand_num)] = 1
	return num_count

def mult_congru(num_count, num_integers, seed, a, b, m):
	while num_integers >  0:
		rand_num = ((a * seed) + b) % m
		if str(rand_num) in num_count:
			num_count[str(rand_num)] += 1
		else:
			num_count[str(rand_num)] = 1
		seed = rand_num
		num_integers -= 1
	return num_count


#Returns percentage of chi-squared stats that are in good range
def results_check(list_chisq_stats, num_range):
	in_good_range = 2*(math.sqrt(num_range))#2SqrootR
	count = 0
	for chisq in  list_chisq_stats:
		if not ((num_range - in_good_range) <= chisq and chisq <=  (num_range + in_good_range)):
			count += 1

	amount_in_range = len(list_chisq_stats) - count
	percentage_good_range = (100 * amount_in_range)/ len(list_chisq_stats)
	print("percentage in good range", percentage_good_range)

	good_range = "Acceptable number range: " + str(num_range - in_good_range) + " - " + str(num_range + in_good_range)
	return good_range

def main():
	print("Which random number generator would you like to use?")
	generator_decision = input("Language(l) or Muliplicative Congruential Method(m): ")

	repeitions = int(input("How many repeitions: "))
	list_chisq_stats = []

	num_count = {}#Dict of random numbers and their occurences
	num_integers = int(input("Enter number of integers: "))
	
	if generator_decision == 'l':
		num_range = int(input("Enter Upper Range, (lower range = 0): "))
		num_count = language_random(num_integers, num_range, num_count)
	elif generator_decision == 'm':
		seed = int(input("Seed(u0): "))#u0
		a = int(input("a: "))
		b = int(input("b: "))
		m = int(input("m: "))
		num_count = mult_congru(num_count, num_integers, seed, a, b, m)

	while repeitions > 0:
		num_count.clear()
		if generator_decision == 'l':
			num_count = language_random(num_integers, num_range, num_count)
		elif generator_decision == 'm':
			num_count = mult_congru(num_count, num_integers, seed, a, b, m)

		print("Frequencies of numbers: ", num_count)
		chisq_stat = chi_sqaure_test(num_count)
		print("Chi-Sqaure stat: ", chisq_stat[0])
		list_chisq_stats.append(chisq_stat[0])

		repeitions -= 1
		print()

	if generator_decision == 'l':
		print(list_chisq_stats)
		print(results_check(list_chisq_stats, num_range))
	elif generator_decision == 'm':
		print("List of chi squared stats: ", list_chisq_stats)
		print(results_check(list_chisq_stats, m-1))

if __name__ == '__main__':
	main()