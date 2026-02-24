# Arac Kiralama ve Takip Uygulamasi
from abc import ABC, abstractmethod
import json

# ================= ABSTRACT VEHICLE =================

class Vehicle(ABC):
    def __init__(self, brand, model, daily_price):
        self.brand = brand
        self.model = model
        self.__daily_price = daily_price
        self.__is_rented = False

    def rent(self):
        if self.__is_rented:
            raise Exception("Bu araç zaten kirada!")
        self.__is_rented = True

    def return_vehicle(self):
        self.__is_rented = False

    def is_rented(self):
        return self.__is_rented

    def get_price(self):
        return self.__daily_price

    @abstractmethod
    def calculate_price(self, days):
        pass

    def __str__(self):
        return f"{self.brand} {self.model}"


# ================= CAR =================

class Car(Vehicle):
    def __init__(self, brand, model, daily_price, door_count, trunk_volume):
        super().__init__(brand, model, daily_price)
        self.door_count = door_count
        self.trunk_volume = trunk_volume

    def calculate_price(self, days):
        return self.get_price() * days


# ================= MOTORCYCLE =================

class Motorcycle(Vehicle):
    def __init__(self, brand, model, daily_price, helmet_included):
        super().__init__(brand, model, daily_price)
        self.helmet_included = helmet_included

    def calculate_price(self, days):
        price = self.get_price() * days
        if self.helmet_included:
            return price * 0.9
        return price


# ================= ELECTRIC CAR =================

class ElectricCar(Vehicle):
    def __init__(self, brand, model, daily_price, battery_capacity, charge_time):
        super().__init__(brand, model, daily_price)
        self.battery_capacity = battery_capacity
        self.charge_time = charge_time

    def calculate_price(self, days):
        return (self.get_price() * days) + (days * 500)

    def battery_warning(self):
        if self.battery_capacity < 50:
            print("⚠ Düşük batarya kapasitesi!")


# ================= CUSTOMER =================

class Customer:
    def __init__(self, name, tc_no):
        self.name = name
        self.__tc_no = tc_no
        self.rented_vehicles = []

    def add_vehicle(self, vehicle):
        self.rented_vehicles.append(vehicle)

    def __len__(self):
        return len(self.rented_vehicles)

    def __str__(self):
        return f"Müşteri: {self.name}"


# ================= RENTAL =================

class Rental:
    def __init__(self, customer, vehicle, days):
        if days <= 0:
            raise ValueError("Gün sayısı negatif veya sıfır olamaz!")

        if vehicle.is_rented():
            raise Exception("Araç zaten kiralanmış!")

        self.customer = customer
        self.vehicle = vehicle
        self.days = days
        self.total_price = vehicle.calculate_price(days)

        vehicle.rent()
        customer.add_vehicle(vehicle)

    def __eq__(self, other):
        return self.customer == other.customer and self.vehicle == other.vehicle

    def __add__(self, other):
        if self.vehicle != other.vehicle:
            raise Exception("Farklı araçlar birleştirilemez!")
        return self.days + other.days

    def __repr__(self):
        return (f"Rental(customer={self.customer}, "
                f"vehicle={self.vehicle}, days={self.days}, "
                f"total={self.total_price})")


# ================= FLEET MANAGEMENT =================

class Fleet:
    def __init__(self):
        self.vehicles = []

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def total_fleet_value(self):
        return sum(vehicle.get_price() for vehicle in self.vehicles)


# ================= JSON SAVE =================

def save_rental_to_json(rental):
    data = {
        "customer": rental.customer.name,
        "vehicle": str(rental.vehicle),
        "days": rental.days,
        "total_price": rental.total_price
    }

    with open("rental_history.json", "a") as file:
        json.dump(data, file)
        file.write("\n")


# ================= TEST SCENARIO =================

def main():

    fleet = Fleet()

    car1 = Car("BMW", "320i", 2000, 4, 480)
    moto1 = Motorcycle("Yamaha", "R25", 1000, True)
    electric1 = ElectricCar("Tesla", "Model 3", 5000, 75, 8)

    fleet.add_vehicle(car1)
    fleet.add_vehicle(moto1)
    fleet.add_vehicle(electric1)

    customer1 = Customer("Ahmet Yılmaz", "12345678901")

    rental1 = Rental(customer1, electric1, 3)

    print(rental1)
    print("Toplam filo günlük değeri:", fleet.total_fleet_value())

    save_rental_to_json(rental1)


if __name__ == "__main__":
    main()



