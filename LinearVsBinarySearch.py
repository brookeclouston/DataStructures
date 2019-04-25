"""
Author: Brooke Clouston
Date Created: January 18 2019

This script compares the running time for two different searching algorithms against lists of varying sizes.
Algorithm A (linear search) traverses the list element by element (O(n)) and algorithm B (binary search) sorts the list
using merge sort (O(nlogn) then searches the list. The relationship between runtime and search set is then plotted.
This script was created in response to Assignment 1.2 of CISC235 Winter 2019.
"""
import random
import time
import matplotlib.plot as plt
import matplotlib.patches as mpatches


def generate_list(n):
    # generates and returns a list of size n containing even integers between 0 and 10000
    unsorted_list = []
    while len(unsorted_list) < n:
        element = random.randint(0, 10000)
        if (element % 2) == 0:
            unsorted_list.append(element)
    return unsorted_list


def generate_search_list(k):
    # generates and returns a list of even size greater than 10, containing half even integers and half odd integers
    search_list = []
    list_size = k

    while len(search_list) < int(list_size / 2): # filling list with even integers
        even_element = random.randint(0, 10000)
        if (even_element % 2) == 0:
            search_list.append(even_element)

    while len(search_list) < list_size: # filling list with odd integers
        odd_element = random.randint(0, 10000)
        if (odd_element % 2) != 0:
            search_list.append(odd_element)

    return search_list


def merge(left, right):
    # merging the left list and the right list  together
    result = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result += left[i:]
    result += right[j:]
    return result


def merge_sort(unsorted_list):
    # using merge sort to sort list, recursively splits list in half, sorts, then recursively merges together again
    if len(unsorted_list) < 2:
        return unsorted_list
    mid = len(unsorted_list) // 2
    left = merge_sort(unsorted_list[:mid])
    right = merge_sort(unsorted_list[mid:])
    return merge(left, right)


def algorithm_a(unsorted_list, target_element):
    # algorithm works by comparing each and every element until a match is found (or not)
    for item in unsorted_list:
        if item == target_element:
            return True
    return False


def algorithm_b(sorted_list, target_element):
    # algorithm uses binary search to search for target element in a sorted list
    low = 0
    high = len(sorted_list)-1
    while high > low:
        mid = (low + high) // 2
        if target_element < sorted_list[mid]:
            high = mid-1
        elif target_element > sorted_list[mid]:
            low = mid + 1
        elif target_element == sorted_list[mid]:
            return True
    return False


def run_algorithm_a(unsorted_list, search_list):
    # executes and times the runtime of algorithm A
    a_start = time.time()
    for element in search_list:
        algorithm_a(unsorted_list, element)
    a_end = time.time()
    a_time = a_end - a_start  # calculating algorithm A's runtime
    return a_time


def run_algorithm_b(unsorted_list, search_list):
    # executes and times the sorting of the list and the runtime of algorithm B
    b_start = time.time()
    sorted_list = merge_sort(unsorted_list)
    for element in search_list:
        algorithm_b(sorted_list, element)
    b_end = time.time()
    b_time = b_end - b_start  # calculating algorithm B's runtime
    return b_time


def find_avg(time_list):
    # finds the average of a list passed in
    counter = 0
    for element in time_list:
        counter += element
    return counter/len(time_list)


def run(n):
    # generates a list of size n, calls the functions to time each algorithm and calls function to display results
    unsorted_list = generate_list(n)
    a_time_list, b_time_list, k_plot_list, =  [], [],[]
    f_of_n = 0
    for k in range(10, n):
        search_list = generate_search_list(k)
        a_time = run_algorithm_a(unsorted_list, search_list)
        b_time = run_algorithm_b(unsorted_list, search_list)

        if f_of_n == 0:  # determines the smallest value of k where algorithm B is faster than algorithm A
            if b_time < a_time:
                f_of_n = k

        a_time_list.append(a_time)
        b_time_list.append(b_time)
        k_plot_list.append(k)

    a_avg = find_avg(a_time_list)
    b_avg = find_avg(b_time_list)

    plot_results(a_time_list, b_time_list, k_plot_list, n)   # calls the graphing function

    return [f_of_n, a_avg, b_avg]


def plot_results(a_plot_list, b_plot_list, k_plot_list, n):
    # plotting the results of the two algorithms against k value and runtime
    plt.plot(k_plot_list, a_plot_list, "r-")
    plt.plot(k_plot_list, b_plot_list, "k-")
    plt.xlabel("Searching Set Size (k value)")
    plt.ylabel("Time (seconds)")
    plt.title(str("Time complexity with data set of size n=" + str(n)))
    red = mpatches.Patch(color="red", label="Linear Search")
    black = mpatches.Patch(color="black", label="Binary Search")
    plt.legend(handles=[red, black])
    plt.grid(True)
    plt.show()


def main():
    # calls the run function for the required size of list and displays information
    n_list = [1000, 2000, 5000, 10000]
    for size in n_list:
        values = run(size)
        print("\n\nF(n) for a list of size ", size, "is: ", values[0])
        print("Average runtime for linear search: ", values[1])
        print("Average runtime for binary search: ", values[2])


if __name__ == "__main__":
    main()

