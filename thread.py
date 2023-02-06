from threading import Thread
from adapter.rabbitmq import RabbitPublisher
from time import perf_counter
from main import main
import schedule
import time

# Initiate Rabbit MQ Connection
publisher = RabbitPublisher()
publisher.run()

new_thread = Thread(target=main)
start_time = perf_counter()

def run_thread():
    # create and start 100 threads
    threads = []
    for n in range(1, 101):
        t = Thread(target=main, args=(n, publisher))
        threads.append(t)
        t.start()

    # wait for the threads to complete
    for t in threads:
        t.join()

    end_time = perf_counter()

    print(f'It took {end_time- start_time: 0.2f} second(s) to complete.')

schedule.every().day.at('22:00').do(run_thread)

while True:
    schedule.run_pending()
    time.sleep(1)
