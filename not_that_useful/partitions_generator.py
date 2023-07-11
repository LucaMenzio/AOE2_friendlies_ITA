import numpy as np
from itertools import combinations

elos = [1200,1245,2184, 1100, 1760, 1550, 1640, 1320]
#elos = [1200,1245,2184, 1760, 1100] # 1550, 1640, 1320]

teams = [[]]
good_i = -1
n = 8
n_combinations = np.math.factorial(n)/(np.math.factorial(n/2)*np.math.factorial(n/2))/2
difference = 1000
sum_elo = np.sum(np.array(elos))

possible_combinations = list(combinations(range(n),int(n/2)))

for i in range(len(possible_combinations)):
    sum = 0
    for j in range(int(n/2)):
        sum += elos[possible_combinations[i][j]]

    if difference > np.abs(sum - sum_elo/2):
        good_i = i
        difference = np.abs(sum - sum_elo/2)
        print(str(i) + "\t" + str(difference))
    
print("best configuration found with team ")
print(possible_combinations[good_i])
print("corresponding to iteration "+str(good_i))
