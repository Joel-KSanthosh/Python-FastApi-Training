# import threading

# def square(n: int) -> None:
#     print(f'The square of the number = {n*n}')

# def cube(n: int) -> None:
#     print(f'The cube of the number = {n*n*n}')


# thread1 = threading.Thread(target=square,args=(10,))
# thread2 = threading.Thread(target=cube,args=(10,))

# thread1.start()
# print("Break")
# thread2.start()

# thread2.join()
# thread1.join()

# import threading
# import os

# def task1():
#     print("Task 1 assigned to thread: {}".format(threading.current_thread().name))
#     print("ID of process running task 1: {}".format(os.getpid()))

# def task2():
#     print("Task 2 assigned to thread: {}".format(threading.current_thread().name))
#     print("ID of process running task 2: {}".format(os.getpid()))

# if __name__ == "__main__":

#     print("ID of process running main program: {}".format(os.getpid()))

#     print("Main thread name: {}".format(threading.current_thread().name))

#     t1 = threading.Thread(target=task1, name='t1')
#     t2 = threading.Thread(target=task2, name='t2')

#     t1.start()
#     t2.start()

#     t1.join()
#     t2.join()

# import concurrent.futures

# def worker():
#     print("Worker thread running")

# pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)

# pool.submit(worker)
# pool.submit(worker)

# pool.shutdown(wait=True)

# print("Main thread continuing to run")

import threading

def even():#creating second function
    for i in range(0,20,2):
        print(i)
def odd():
    for i in range(1,20,2):
        print(i)

# creating a thread for each function
trd1 = threading.Thread(target=even)
trd2 = threading.Thread(target=odd)

trd1.start() # starting the thread 1 

trd2.start() # starting the thread 2
print(threading.enumerate())

print("Count =", threading.active_count())
print(threading.current_thread())

trd1.join()
trd2.join()

print('End')

print("Count =",threading.active_count())