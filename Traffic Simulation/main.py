import csv
from collections import OrderedDict

import math
import matplotlib.pyplot as plt


class Parser:

    def __init__(self, path):
        self.reader = None
        self.raw = None
        self.path = None
        self.headers = []

        self.path = path
        self.reader = csv.reader(open(self.path, 'r'), delimiter=';')

    def logic(self, value):
        pass

    def parse(self):
        for item in self.reader:
            self.logic(item)


class Car:

    def __init__(self, id):
        self.id = str(id)
        self.log = OrderedDict()
        self.calculated_speed = []
        self.speed = []
        self.position = []

    def add_speed(self, speed_dict):
        self.speed.append(speed_dict)

    def calculate_speeds(self):
        speed_prev = 0
        for k, v in self.speed:
            iter_speed = float(v)
            current_speed = abs(iter_speed - speed_prev)

            speed_prev = iter_speed
            self.calculated_speed.append([k, current_speed])

    def add_position(self, position_dict):
        self.position.append(position_dict)

    def get_max_speed(self):
        max_speed = 0.0  # The highest speed we've found
        previous_distance = 0  # So we can account for the zero index.

        for time, current_distance in self.speed:

            iter_distance = float(current_distance)  # The current distance
            current_speed = abs(
                iter_distance - previous_distance)  # Our speed is the iteration speed minus the previous

            if current_speed > max_speed:
                max_speed = current_speed
            previous_distance = iter_distance
        return max_speed  # returning the highest found speed

    def calculate_speeds(self):
        """ Function that stores all the speeds we've come across """
        speed_prev = float(self.speed[0][0])
        for k, v in self.speed:
            iter_speed = float(v)
            current_speed = abs(iter_speed - speed_prev)

            self.calculated_speed.append([k, current_speed])
            speed_prev = iter_speed

    def get_min_speed(self):
        min_speed = math.inf
        speed_prev = float(self.speed[0][0])  # So we can account for the zero index.

        for k, v in self.speed[1:]:

            iter_speed = float(v)
            current_speed = abs(iter_speed - speed_prev)

            if current_speed < min_speed:
                min_speed = current_speed
            speed_prev = iter_speed
        return min_speed

    def plot_position(self, p):
        """Receiving the plot and writing our time and positional data on it. """
        times = []
        positions = []

        for time, position in self.position:
            times.append(round(float(time), 2))
            positions.append(round(float(position), 2))

        p.plot(times, positions, label='Car ' + self.id)

    def get_position_by_time(self, tm):

        for time, pos in self.position:
            if time == tm:
                return pos
        return None

    def get_time_by_position(self, position):
        if float(position) < float(self.position[0][1]):
            return False
        temp_time = None
        temp_pos = None
        for time, pos in self.position:
            if pos == position:
                return time
            if float(pos) > float(position):
                temp_time = time
                temp_pos = float(pos)
                break
        return temp_time

    def plot_speed(self, plot):
        """Receiving the plot and writing our time and speed data on it. """
        self.calculate_speeds()

        lists = sorted(self.calculated_speed)
        x, y = zip(*lists)  # unpack a list of pairs into two tuples

        plot.plot(x, y, label='Car ' + self.id)


class Cars:

    def __init__(self, inserted_cars):
        self.cars = inserted_cars

    def set_speed(self, car, value):
        self.cars[car].add_speed(value)

    def set_position(self, car, value):
        self.cars[car].add_position(value)

    def get_speed_at_times(self):
        p = plt
        for car in self.cars:  # Asking all our cars to plot their speed
            car.plot_speed(p)
        p.xlabel('Speed')
        p.ylabel('Time')
        p.legend(loc='lower right')
        p.show()

    def get_position_at_times(self):
        p = plt
        for car in self.cars[:-1]:
            car.plot_position(p)  # Asking all our cars to plot their position
        p.title('Positions')
        p.xlabel('Time')
        p.ylabel('Position')

        p.legend(loc='lower right')
        p.show()

    def get_max_speeds(self):
        ls = []
        for car in self.cars:
            ls.append(car.get_max_speed())  # Redirecting the function call to the individual cars
        return ls

    def get_min_speeds(self):
        ls = []
        for car in self.cars:
            ls.append(car.get_min_speed())  # Redirecting the function call to the individual cars
        return ls

    def get_collision(self):
        start_car = self.cars[0]
        collision_time = start_car.get_time_by_position(0.0)
        for car in self.cars[1:-1]:
            car_at_collision_time = car.get_position_by_time(collision_time)
            if car_at_collision_time:
                if -1 < float() < 1:
                    print(
                        "Auto : " + str(car.id) + " zal crashen met auto " + str(start_car.id) + " op tijdstip " + str(
                            collision_time))
                return

        print("Er vindt geen crash plaats")

    def get_speed_ranges(self):
        for car in self.cars:
            print(
                " Auto " + str(car.id) + " heeft een minimumsnelheid van " + str(
                    car.get_min_speed()) + " en een maxiumumsnelheid van " + str(car.get_max_speed()))


class DirectionParser(Parser):
    def __init__(self, path, cars):
        super().__init__(path)

    def logic(self, value):
        time = value[0]
        car_1 = value[1]
        car_2 = value[2]


class PositionParser(Parser):
    def __init__(self, path, cars):
        super().__init__(path)

    def logic(self, value):
        time = value[0]

        car_1 = value[1]
        car_2 = value[2]

        cars.set_position(0, [time, car_1])
        cars.set_position(1, [time, car_2])


class SpeedParser(Parser):
    def __init__(self, path, cars):
        super().__init__(path)
        self.cars = cars

    def logic(self, value):
        time = value[0]
        car_1 = value[1]
        car_2 = value[2]
        car_3 = value[3]

        self.cars.set_speed(0, [time, car_1])
        self.cars.set_speed(1, [time, car_2])
        self.cars.set_speed(2, [time, car_3])


cars = Cars([Car(1), Car(2), Car(3)])

SpeedParser('verkeerssimulatie-rechteweg-snelheden.csv', cars).parse()
PositionParser('verkeerssimulatie-rechteweg-posities.csv', cars).parse()
DirectionParser('verkeerssimulatie-richting.csv', cars).parse()

# Voor elk voertuig de maximum en minimum snelheid.
cars.get_speed_ranges()

# Een grafiek (in python code met matplotlib) van de snelheden van alle voertuigen over de gegeven tijdsperiode (van minimum tijdstip tot maximum tijdstip in het bestand).
cars.get_speed_at_times()

# Een grafiek (in python code met matplotlib) van de posities van de voertuigen over de gegeven tijdsperiode (van minimum tijdstip tot maximum tijdstip in het bestand).
cars.get_position_at_times()

# Het tijdstip van de eerste botsing en welke voertuigen dit zijn
cars.get_collision()
