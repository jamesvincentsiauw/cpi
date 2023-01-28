from threading import Thread
from adapter.rabbitmq import RabbitPublisher
from time import perf_counter
from main import main

# Initiate Rabbit MQ Connection
publisher = RabbitPublisher()
publisher.run()

new_thread = Thread(target=main)
start_time = perf_counter()

# create and start 10 threads
threads = []
for n in range(1, 11):
    t = Thread(target=main, args=(n, publisher))
    threads.append(t)
    t.start()

# wait for the threads to complete
for t in threads:
    t.join()

end_time = perf_counter()

print(f'It took {end_time- start_time: 0.2f} second(s) to complete.')
