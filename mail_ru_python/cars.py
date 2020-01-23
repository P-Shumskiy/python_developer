import csv
from os.path import splitext


class CarBase:  # TODO Add car_type attribute
    def __init__(self, brand: str, photo_file_name: str, carrying: str):
        self.photo_file_name = photo_file_name
        self.brand = brand
        self.carrying = carrying

    def get_photo_file_ext(self):
        return splitext(self.photo_file_name)


class Car(CarBase):  # TODO Add car_type attribute
    def __init__(self, brand, photo_file_name, carrying,
                 passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):  # TODO Add car_type attribute
    def __init__(self, brand, photo_file_name, carrying,
                 body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.body_whl = body_whl.split('x')
        try:
            self.body_length = float(self.body_whl[0])
            self.body_width = float(self.body_whl[1])
            self.body_height = float(self.body_whl[2])
        except ValueError:
            self.body_length = 0.0
            self.body_width = 0.0
            self.body_height = 0.0

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height


class SpecMachine(CarBase):  # TODO Add car_type attribute
    def __init__(self, brand, photo_file_name, carrying,
                 extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra


def get_car_list(csv_filename: str):
    car_list = []
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=',')
        next(reader)
        cnt = 1
        for row in reader:
            cnt += 1
            try:
                if row[0] == 'truck':
                    car = Truck(row[1], row[3], row[5], row[4])
                elif row[0] == 'car':
                    car = Car(row[1], row[3], row[5], row[2])
                elif row[0] == 'spec_machine':
                    car = SpecMachine(row[1], row[3], row[5], row[6])
                else:
                    continue
            except(IndexError, KeyError, ValueError):
                continue
            if car.get_photo_file_ext()[1]:
                car_list.append(car)
            else:
                continue
    return car_list
