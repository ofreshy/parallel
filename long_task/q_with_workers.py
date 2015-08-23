__author__ = 'osharabi'

"""
In this implementation, I used the notion of a task q and several workers consuming the q
The task queue represents tasks that are 'cheap' to create,
for example, reading a line from a file,
and the workers represents a more 'expensive' task such as writing this line to DB or sending it as a request.
"""

import logging
from multiprocessing import JoinableQueue, Queue, Process
import sys
import time


def process_task(num_workers):
    logging.info("Started")

    task_queue = JoinableQueue()
    done_queue = Queue()

    def worker(name):
        """
        represents an 'expensive' task
        """
        logging.info("Started process : %s" % name)
        for task in iter(task_queue.get, 'Stop'):
            done_queue.put(task)
            time.sleep(1)
            task_queue.task_done()
        # This is for the poison pill task
        task_queue.task_done()
        logging.info("Done process : %s" % name)

    # First we start the workers, and give them a list that we can look at after
    for i in range(num_workers):
        Process(target=worker, args=("P-%s" % (i+1), )).start()

    # Now the main thread populates the Queue
    num_tasks = num_workers * 5
    for i in range(num_tasks):
        task_queue.put(i)

    # Now, administer the poison pill which tells processes that we are done populating the Q
    for i in range(num_workers):
        task_queue.put('Stop')

    # Now wait for workers to finish their work
    task_queue.close()
    task_queue.join()

    logging.info("Workers are done")

    # Now verify that all tasks are done by seeing them in the done queue
    done_queue.put('Stop')
    done_tasks = [task for task in iter(done_queue.get, 'Stop')]
    assert len(done_tasks) == num_tasks
    logging.info("Verified work - done!")


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    process_task(20)










