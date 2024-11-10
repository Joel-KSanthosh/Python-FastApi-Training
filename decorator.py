from functools import wraps
import time

def timer(f):
    @wraps(f)
    def wrapper():
        start_time = time.process_time_ns()
        f()
        print(f"Total Time Taken : {round(time.process_time_ns() - start_time,2)} nano seconds")
    return wrapper

@timer
def loop():
    sum = 0
    for i in range(1000):
        sum+= i
    print(sum) 
    

loop()