import csv
from os.path import splitext


class CarBase:
    car_type = None

    def __init__(self, brand: str, photo_file_name: str, carrying: float):
        self.photo_file_name = photo_file_name
        self.brand = brand
        self.carrying = float(carrying)
        assert (bool(self.brand.strip()))

    def get_photo_file_ext(self):
        return splitext(self.photo_file_name)[1]


class Car(CarBase):
    car_type = 'car'

    def __init__(self, brand, photo_file_name, carrying,
                 passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    car_type = 'truck'

    def __init__(self, brand, photo_file_name, carrying,
                 body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.body_whl = body_whl.split('x')
        try:
            assert len(self.body_whl) == 3
            self.body_length = float(self.body_whl[0])
            self.body_width = float(self.body_whl[1])
            self.body_height = float(self.body_whl[2])
        except (AssertionError, ValueError):
            self.body_length = 0.0
            self.body_width = 0.0
            self.body_height = 0.0
            self.length = len(body_whl)

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height


class SpecMachine(CarBase):
    car_type = "spec_machine"

    def __init__(self, brand, photo_file_name, carrying,
                 extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra
        assert bool(extra.strip())


def get_car_list(csv_filename: str):
    acceptable_extension = {".jpg", ".jpeg", ".png", ".gif"}
    car_list = []
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)
        for row in reader:
            try:
                assert len(row) == 7
                car = CarBase(row[1], row[3], row[5])
                car.car_type = row[0]
                if car.car_type == 'truck':
                    car = Truck(car.brand, car.photo_file_name, car.carrying,
                                row[4])
                elif car.car_type == 'car':
                    car = Car(car.brand, car.photo_file_name, car.carrying,
                              row[2])
                elif car.car_type == 'spec_machine':
                    car = SpecMachine(car.brand, car.photo_file_name, car.carrying,
                                      row[6])
                else:
                    continue
            except(AssertionError, IndexError, KeyError, ValueError):
                continue
            if car.get_photo_file_ext() in acceptable_extension:
                car_list.append(car)
            else:
                continue
    return car_list
