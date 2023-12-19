import threading
import time

# Define the first function
def function_one():
    for i in range(1, 6):
        print(f"Function One: {i}")
        time.sleep(1)

# Define the second function
def function_two():
    for i in range(1, 6):
        print(f"Function Two: {i}")
        time.sleep(1)

# Create threads for each function
thread_one = threading.Thread(target=function_one)
thread_two = threading.Thread(target=function_two)

# Start the threads
thread_one.start()
thread_two.start()

# Wait for both threads to complete
thread_one.join()
thread_two.join()

print("Both functions are complete.")
