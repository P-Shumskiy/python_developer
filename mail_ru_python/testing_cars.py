from cars import *
cars = get_car_list('test.csv')
print(len(cars))

for car in cars:
    print(type(car[0]))

print(cars[0][0].passenger_seats_count)

print(cars[1][0].get_body_volume())

from cars import *

cars = get_car_list('test.csv')
print(len(cars))

for car in cars:
    print(type(car[0]))

print(cars[0][0].passenger_seats_count)

print(cars[1][0].get_body_volume())


