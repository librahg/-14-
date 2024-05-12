import copy

class House:
    address = 0
    def __init__(self):
        self.address = House.address
        self.room = Room()
        self.toilet = Toilet()
        self.balcony = Balcony()

    def clone(self):
        clone = copy.deepcopy(self)
        clone.address = House.address + 1
        return clone

    def printHouse(self):
        print(f"address: {self.address}\nroom: {self.room}\ntoilet: {self.toilet}\nbalcony: {self.balcony}\n")

class HouseFactory:
    def buildHouse(self):
        House.address += 1
        return House()

class Room:
    def __str__(self):
        return "room"
class Toilet:
    def __str__(self):
        return "toilet"
class Balcony:
    def __str__(self):
        return "balcony"

houseFactory = HouseFactory()
houses = [houseFactory.buildHouse() for _ in range(3)] # House 객체 3개 생성

houses.append(houses[0].clone()) # 첫번째 House 객체의 복사본을 append

for house in houses: # address는 clone되지 않고 새로 할당됨
    house.printHouse()