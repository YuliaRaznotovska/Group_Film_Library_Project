# Написати программу яка буде обчислювати кылькысть щасливих білетів.
#
# Використати multiprocessing та multithreading
#
# обов'язково додати відмітки про час щоб можна було побачити який з підходів скільки виконується
#
# Щасливий білет це такий білет у якого сума першиз трьох цифр номеру доравнює суммі другої трійки цифр
#
# 123042 -> 1+2+3 = 0+4+2
#
# не обов'язкове завдання:
#
# розібратись і забрати результати виконання функцій які виконувалась у thread/subprocess
#
# ну і відповідно просумувати результати
# ticket1 = 554988
# sum_1 = sum(int(digit) for digit in str(ticket1)[:3])
# sum_2 = sum(int(digit) for digit in str(ticket1)[3:])
# # str_ticket1 = str(ticket1)
# # digit_list = list(map(int, str_ticket1))
# # sum_1 = sum()
# print(sum_1)
# print(sum_2)
import threading
import datetime
import logging
from multiprocessing import Process

tickets_list = [104583, 729416, 560982, 381704, 948215, 672093, 815460, 294781, 703649, 186295,
                459870, 820361, 937104, 568492, 241980, 694728, 305816, 781954, 462137, 950682,
                178309, 634705, 820947, 496218, 753061, 189574, 602839, 945370, 318496, 770152,
                584209, 931678, 246805, 709431, 865294, 190748, 437860, 658123, 904571, 312689]


def count_lucky_tickets(start_range, end_range, tickets, thread_num):
    lucky_counter = 0
    for ticket in tickets[start_range:end_range]:
        sum_1 = sum(int(digit) for digit in str(ticket)[:3])
        sum_2 = sum(int(digit) for digit in str(ticket)[3:])
        if sum_1 == sum_2:
            lucky_counter += 1
    print(f" Number of lucky tickets: {lucky_counter} (thread - {thread_num})")


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    t1 = datetime.datetime.now()
    x1 = threading.Thread(target=count_lucky_tickets, args=(1, 19, tickets_list, "thread_1"))
    x2 = threading.Thread(target=count_lucky_tickets, args=(20, 40, tickets_list, "thread_2"))
    logging.info("Main    : before running thread")
    x1.start()
    x2.start()
    logging.info("Main    : wait for the thread to finish")
    # x.join()
    x1.join()
    x2.join()
    t2 = datetime.datetime.now()
    logging.info("Main    : all done")
    logging.info(f"Time taken    : {t2 - t1}")


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    t1 = datetime.datetime.now()
    p1 = Process(target=count_lucky_tickets, args=(1, 19, tickets_list, "process_1"))
    p2 = Process(target=count_lucky_tickets, args=(20, 40, tickets_list, "process_2"))
    logging.info("Main    : before running thread")
    p1.start()
    p2.start()
    logging.info("Main    : wait for the thread to finish")
    # x.join()
    p1.join()
    p2.join()
    t2 = datetime.datetime.now()
    logging.info("Main    : all done")
    logging.info(f"Time taken    : {t2 - t1}")