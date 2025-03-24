import random as ran
import matplotlib.pyplot as plt
def random_permutation(n):
    list_num = [i for i in range(n)]
    ran.shuffle(list_num)
    return list_num


def count_circles(random_permutation):
    # an array with false in each element
    mark = [False for i in range(len(random_permutation))] 
    count = 0
    for i in range(len(random_permutation)):
        if i == random_permutation[i]:
            mark[i] = True
            count += 1
        if i != random_permutation[i] and mark[random_permutation[i]] == False:
            while i != random_permutation[i] and mark[random_permutation[i]] == False:
                mark[random_permutation[i]] = True
                i = random_permutation[i]
                
            count += 1
    return count

# Generate 100.000 random permutations with 16 elements and calculate the number of cycles for each
num_trials = 100000
num_elements = 16
data_circles = [count_circles(random_permutation(num_elements)) for _ in range(num_trials)]

# collect what the probility is for each number of cycles to occur
probabilities = {}
for i in data_circles:
    if i not in probabilities:
        probabilities[i] = data_circles.count(i)/num_trials


# calculate the average based on the experiment and the theory 
avg_num_cirlces_exp = sum(data_circles)/num_trials
avg_num_cirlces_th = sum([1/i for i in range(1,num_elements +1)])



# Plot histogram
plt.bar(probabilities.keys(), probabilities.values(), color='blue', alpha=0.6)
plt.xlabel("Number of Cycles")
plt.ylabel("Probability")
plt.title("Probability of k cycles in a random permutation (n=16)")
plt.show()

print("The average number of cycles calculated based on the experiment is:", avg_num_cirlces_exp)
print("The average number of cycles calculated based on the formula is:", avg_num_cirlces_th)