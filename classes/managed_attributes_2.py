# You want to add extra processing (e.g., type checking or validation) to the getting or
# setting of an instance attribute.

import logging

from abc import abstractmethod


logging.basicConfig(level=logging.INFO)


class VehicleAttributeManager:

    def __set_name__(self, owner, name):
        logging.info(f'Setting attribute name "{name}" of owner class "{owner}"')
        self.public_name = name
        self.private_name = '_' + name

    def __get__(self, instance, objtype=None):
        value = getattr(instance, self.private_name)
        logging.info(f'Accessing "{self.public_name}" attribute of {instance}: {value}')
        return value

    def __set__(self, instance, value):
        self.validate(value)
        logging.info(f'Updating "{self.public_name}" attribute of {instance} to new value: {value}')
        setattr(instance, self.private_name, value)

    @abstractmethod
    def validate(self, value):
        pass


class CarFuel(VehicleAttributeManager):

    def __init__(self, compatible_fuel_types):
        self.compatible_fuel_types = compatible_fuel_types

    def validate(self, value):
        if value not in self.compatible_fuel_types:
            raise ValueError(f'Fuel type "{value}" is not one of the compatible fuel types: {self.compatible_fuel_types}')


class Car:

    number_plate: VehicleAttributeManager = VehicleAttributeManager()
    series: VehicleAttributeManager = VehicleAttributeManager()
    fuel_type: CarFuel = CarFuel(['diesel'])

    def __init__(self, brand, series, number_plate, fuel_type):
        logging.info(f'Instantiating object {self}')
        self.brand = brand               # regular instance attribute
        self.series = series             # calls __set__() of the descriptor
        self.number_plate = number_plate
        self.fuel_type = fuel_type

    def switch_number_plate(self, number_plate):
        self.number_plate = number_plate


class Rocket:

    engine_type: VehicleAttributeManager = VehicleAttributeManager()

    def __init__(self, engine_type):
        logging.info(f'Instantiating object {self}')
        self.engine_type = engine_type # calls __set__() of the descriptor


car = Car('BMW', 'M5', 'X201Y', 'diesel')
_ = car.number_plate # calls __get__()
car.switch_number_plate('X222Y')

logging.info(f'vars of {car}: {vars(car)} contains the private attribute "_number_plate"')
logging.info(f'The class {Car} contains the "public_name" and "private_name" attributes that are used to manage '
             f'the "number_plate" attribute: {vars(vars(Car)["number_plate"])}')

rocket = Rocket('hydrogen')

# this throws ValueError due to incompatible fuel
car = Car('BMW', 'M5', 'X201Y', 'petrol')
