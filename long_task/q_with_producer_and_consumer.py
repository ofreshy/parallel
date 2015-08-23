__author__ = 'osharabi'

"""
As the previous approach of workers with q work, it does not handle the case when there are exceptions in the workers.
In this case, the task will not be marked as done by the worker and we may end up hanging forever

Here, we surround each worker with a try/catch block and signal to signal queue if we failed or not.
Terminating the job is done by closing all remaining live processes
"""

import logging
from multiprocessing import JoinableQueue, Queue, Process
import sys
import time


def process_task(num_consumers):
    logging.info("Started")

    task_queue = Queue()
    signal_queue = Queue()
    num_tasks = num_consumers * 5

    def producer(name):
        logging.info("Started process : %s" % name)

        try:
            for i in range(num_tasks):
                task_queue.put(i)
            for i in range(num_consumers):
                task_queue.put("Stop")
        except Exception:
            signal_queue.put('fatal : %s' % name)
            logging.exception("In producer : %s" % name)

        logging.info("Done process : %s" % name)

    def consumer(name):
        """
        represents an 'expensive' task
        """
        logging.info("Started process : %s" % name)

        try:
            for _ in iter(task_queue.get, 'Stop'):
                time.sleep(1)
        except Exception:
            signal_queue.put('fail : %s' % name)
            logging.exception("In consumer : %s" % name)
        else:
            signal_queue.put('success : %s' % name)

        logging.info("Done process : %s" % name)

    # First we create the consumers and start them
    # Note that here we keep the reference to these guys
    consumers = [Process(target=consumer, args=("C-%s" % (i+1), )) for i in range(num_consumers)]
    [c.start() for c in consumers]

    # Now we can start the producer
    Process(target=producer, args=("Producer", )).start()

    num_failed = num_success = 0
    while (num_failed + num_success) < num_consumers:
        signal = signal_queue.get()
        if signal.startswith('success'):
            num_success += 1
        elif signal.startswith('fail'):
            num_failed += 1
        else:
            logging.error("Problem with producer, closing all consumers and aborting")
            [c.terminate() for c in consumers if c.is_alive()]

    if num_success == 0:
        logging.error("All workers died before finishing work")
    else:
        logging.info("Work is done, %s workers failed and %s finished successfully" % (num_failed, num_success))


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    process_task(20)










