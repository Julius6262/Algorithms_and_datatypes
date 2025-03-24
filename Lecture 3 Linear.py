import sys
import time
 
 # function simply adds one to a count up to n
def main():
    start_time = time.time()
    n = int(sys.argv[1]) # read the input from the command line, and save in n
    total = 0
    for i in range(1, n+1):
        total += 1    
    print("The total:",total)
    print("The execution time:",(time.time() - start_time))

if __name__ == "__main__":
    main()

# run from the terminal and input number of iteration in the command line fx
# python "Lecture 3 Linear.py" 100