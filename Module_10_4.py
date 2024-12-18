import threading
import random
import time
from queue import Queue


class Table:
    def __init__(self, number):
        """
        Инициализация стола.
        :param number: Номер стола (целое число).
        """
        self.number = number  # Номер стола
        self.guest = None  # Гость за столом (по умолчанию None)


class Guest(threading.Thread):
    def __init__(self, name):
        """
        Инициализация гостя.
        :param name: Имя гостя (строка).
        """
        super().__init__()  # Инициализация родительского класса Thread
        self.name = name  # Имя гостя

    def run(self):
        """
        Метод, который выполняется при запуске потока.
        Гость ожидает случайное время от 3 до 10 секунд.
        """
        wait_time = random.randint(3, 10)  # Случайное время ожидания от 3 до 10 секунд
        time.sleep(wait_time)  # Имитация времени, проведенного в кафе


class Cafe:
    def __init__(self, *tables):
        """
        Инициализация кафе.
        :param tables: Столы в кафе (любая коллекция).
        """
        self.queue = Queue()  # Очередь для гостей
        self.tables = tables  # Список столов в кафе

    def guest_arrival(self, *guests):
        """
        Метод для прибытия гостей.
        :param guests: Гости (объекты класса Guest).
        """
        for guest in guests:  # Проходим по каждому гостю
            free_table = next((table for table in self.tables if table.guest is None), None)  # Находим свободный стол

            if free_table:  # Если есть свободный стол
                free_table.guest = guest  # Сажаем гостя за стол
                guest.start()  # Запускаем поток гостя
                print(f"{guest.name} сел(-а) за стол номер {free_table.number}")  # Сообщение о посадке
            else:  # Если свободных столов нет
                self.queue.put(guest)  # Добавляем гостя в очередь
                print(f"{guest.name} в очереди")  # Сообщение о том, что гость в очереди

    def discuss_guests(self):
        """
        Метод для обслуживания гостей.
        Обслуживание продолжается пока очередь не пустая или хотя бы один стол занят.
        """
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:  # Проходим по всем столам
                if table.guest and not table.guest.is_alive():  # Если за столом есть гость и он покинул кафе
                    print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")  # Сообщение о том, что гость ушел
                    print(f"Стол номер {table.number} свободен")  # Сообщение о том, что стол свободен
                    table.guest = None  # Освобождаем стол

                    if not self.queue.empty():  # Если очередь не пуста
                        next_guest = self.queue.get()  # Берем следующего гостя из очереди
                        table.guest = next_guest  # Сажаем его за стол
                        next_guest.start()  # Запускаем поток нового гостя
                        print(f"{next_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")

            time.sleep(0.5)  # Задержка для имитации времени обслуживания


# Создание столов
tables = [Table(number) for number in range(1, 6)]

# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]

# Создание гостей
guests = [Guest(name) for name in guests_names]

# Заполнение кафе столами
cafe = Cafe(*tables)

# Приём гостей
cafe.guest_arrival(*guests)

# Обслуживание гостей
cafe.discuss_guests()