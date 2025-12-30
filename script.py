import datetime
import logging
import queue
import threading
from multiprocessing import Process, Queue

tickets_list = [104583, 729416, 560982, 381704, 948215, 672093, 815460, 294781, 703649, 186295,
                459870, 820361, 937104, 568492, 241980, 694728, 305816, 781954, 462137, 950682,
                178309, 634705, 820947, 496218, 753061, 189574, 602839, 945370, 318496, 770152,
                584209, 931678, 246805, 709431, 865294, 190748, 437860, 658123, 904571, 312689]


def count_lucky_tickets_thread(start_range, end_range, tickets, thread_num, q):
    lucky_counter = 0
    for ticket in tickets[start_range:end_range]:
        sum_1 = sum(int(digit) for digit in str(ticket)[:3])
        sum_2 = sum(int(digit) for digit in str(ticket)[3:])
        if sum_1 == sum_2:
            lucky_counter += 1
    print(f" Number of lucky tickets: {lucky_counter} (thread - {thread_num})")
    q.put((thread_num, lucky_counter))
    q.task_done()


def count_lucky_tickets_process(start_range, end_range, tickets, proc_num, q):
    lucky_counter = 0
    for ticket in tickets[start_range:end_range]:
        sum_1 = sum(int(digit) for digit in str(ticket)[:3])
        sum_2 = sum(int(digit) for digit in str(ticket)[3:])
        if sum_1 == sum_2:
            lucky_counter += 1
    print(f" Number of lucky tickets: {lucky_counter} (process - {proc_num})")
    q.put((proc_num, lucky_counter))


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    t1 = datetime.datetime.now()
    q = queue.Queue()
    x1 = threading.Thread(target=count_lucky_tickets_thread, args=(1, 19, tickets_list, "thread_1", q))
    x2 = threading.Thread(target=count_lucky_tickets_thread, args=(20, 40, tickets_list, "thread_2", q))
    logging.info("Main    : before running thread")
    x1.start()
    x2.start()
    logging.info("Main    : wait for the thread to finish")
    # x.join()
    x1.join()
    x2.join()
    q.join()
    t2 = datetime.datetime.now()
    logging.info("Main    : all done")
    logging.info(f"Time taken    : {t2 - t1}")

    total_lucky_tickets = 0
    while not q.empty():
        thead_name, sum_count = q.get()
        total_lucky_tickets += sum_count
    logging.info(f"Total number of lucky tickets in thread - {total_lucky_tickets}")

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : before creating process")
    t1 = datetime.datetime.now()
    q = Queue()
    p1 = Process(target=count_lucky_tickets_process, args=(1, 19, tickets_list, "process_1", q))
    p2 = Process(target=count_lucky_tickets_process, args=(20, 40, tickets_list, "process_2", q))
    logging.info("Main    : before running process")
    p1.start()
    p2.start()
    logging.info("Main    : wait for the process to finish")
    # x.join()
    p1.join()
    p2.join()
    t2 = datetime.datetime.now()
    logging.info("Main    : all done")
    logging.info(f"Time taken    : {t2 - t1}")
    total_lucky_tickets = 0
    while not q.empty():
        proc_name, sum_count = q.get()
        total_lucky_tickets += sum_count
    logging.info(f"Total number of lucky tickets in process - {total_lucky_tickets}")
