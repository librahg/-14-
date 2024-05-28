import copy

# HousePart와 Floor Bridge
class HousePart: # Floor 클래스의 parts 멤버에 담길 집의 part
    def __str__(self):
        raise NotImplementedError


class Room(HousePart):
    def __str__(self):
        return "Room"


class Toilet(HousePart):
    def __str__(self):
        return "Toilet"


class Balcony(HousePart):
    def __str__(self):
        return "Balcony"


class Kitchen(HousePart):
    def __str__(self):
        return "Kitchen"


# Floor와 House Bridge
class Floor: # House 클래스의 멤버
    def __init__(self, level, parts=None):
        self.level = level
        self.parts = parts if parts is not None else []

    def add_part(self, part):
        self.parts.append(part)

    def get_house_part(self, part_name):
        found_parts = [part for part in self.parts if str(part) == part_name]
        return found_parts

    def has_part(self, part_name):
        return any(str(part) == part_name for part in self.parts)

    def __str__(self):
        parts_str = ', '.join(str(part) for part in self.parts)
        return f"Floor {self.level}: {parts_str}"

# House
class House:
    address = 0

    def __init__(self, price):
        self.price = price
        self.is_sold = False
        self.address = House.address
        self.floors = [] # floor는 현재 층과 그 층의 parts를 담는 Floor 객체 리스트
        self.owner = None
        
    def buy_house(self, balance, owner_name):
        if not self.is_sold:
            if balance >= self.price:
                balance -= self.price
                self.is_sold = True
                self.owner = owner_name
                print(f"House at Address {self.address} has been purchased by {owner_name}.")
                return balance
            else:
                print("Your balance is not enough.")
                return balance
        else:
            print(f"This house is already purchased by {self.owner}.")
            return balance

    def cancel_purchase(self, balance):
        if self.is_sold:
            print(f"Purchase of House at Address {self.address} by {self.owner} has been canceled.")
            self.is_sold = False
            self.owner = None
            balance += self.price
            return balance
        else:
            print("No purchase record for this house.")
    
    
    def add_floor(self, floor):
        self.floors.append(floor)

    def clone(self): # Prototype Pattern
        clone = copy.deepcopy(self)
        clone.is_sold = False
        House.address += 1
        clone.address = House.address
        return clone

    def printHouse(self):
        owner_status = f", owned by {self.owner}" if self.is_sold else ", available for purchase"
        floors_str = '\n'.join(str(floor) for floor in self.floors)
        print(f"Address: {self.address}{owner_status}\nPrice: {self.price}\n{floors_str}\n")


# Factory Pattern
class HouseFactory:
    def buildHouse(self, floor_plans, price):
        House.address += 1
        house = House(price)
        for level, parts in enumerate(floor_plans):
            floor = Floor(level + 1, parts)
            house.add_floor(floor)
        return house


# Facade Pattern
class HouseBuilderFacade: # 하나의 메서드로 복잡한 집 생성 인터페이스를 간소화
    def __init__(self):
        self.factory = HouseFactory()

    def build_standard_house(self):
        floor_plans = [
            [Room(), Toilet(), Balcony()],
            [Room(), Room(), Toilet()]
        ]
        return self.factory.buildHouse(floor_plans, 10000)

    def build_luxury_house(self):
        floor_plans = [
            [Room(), Kitchen(), Balcony()],
            [Room(), Room(), Toilet()],
            [Kitchen(), Toilet(), Balcony()]
        ]
        return self.factory.buildHouse(floor_plans, 50000)

    def build_custom_house(self, floor_plans, price): # 사용자의 입력에 따라 자유롭게 집 구성
        return self.factory.buildHouse(floor_plans, price)

def search_house(condition, house_list):
    from collections import Counter

    def is_condition_met(condition_counter, house_counter):
        for part, count in condition_counter.items():
            if house_counter[part] < count:
                return False
        return True

    search_result = []
    condition_counter = Counter(str(part) for part in condition)
    
    for house in house_list:
        flattened_house_parts = [str(part) for floor in house.floors for part in floor.parts]
        house_counter = Counter(flattened_house_parts)
        
        if is_condition_met(condition_counter, house_counter):
            search_result.append(house)
    
    return search_result

# Client Code
builder = HouseBuilderFacade()
houses = []

name = input("Input your name: ")
balance = int(input("Input balance: "))
while True:
    command = input("\nInput command: ").split()
    if command[0] == "exit":
        break
    
    elif command[0] == "print_houses":
        print()
        for house in houses:
            house.printHouse()
    
    elif command[0] == "build_standard_house":
        houses.append(builder.build_standard_house())
    
    elif command[0] == "build_luxury_house":
        houses.append(builder.build_luxury_house())
    
    elif command[0] == "build_custom_house":
        floor_plans = []
        price = int(input("Input price: "))
        floor = int(input("Input height: "))
        for i in range(floor):
            parts_ = []
            parts = input(f"Input house parts of floor {i+1}: ").split()
            for part in parts:
                if part == "Room":
                    parts_.append(Room())
                elif part == "Toilet":
                    parts_.append(Toilet())
                elif part == "Balcony":
                    parts_.append(Balcony())
                elif part == "Kitchen":
                    parts_.append(Kitchen())
            floor_plans.append(parts_)
        
        houses.append(builder.build_custom_house(floor_plans, price))
        
    elif command[0] == "clone_house":
        houses.append(houses[int(command[1])-1].clone())
    
    elif command[0] == "buy_house":
        balance = houses[int(command[1])-1].buy_house(balance, name)
        print("Balance Remaining:", balance)
        
    elif command[0] == "cancel_purchase":
        balance = houses[int(command[1])-1].cancel_purchase(balance)
        print("Balance Remaining:", balance)
        
    elif command[0] == "search_house":
        condition = []
        for part in command[1:]:
            if part == "Room":
                condition.append(Room())
            elif part == "Toilet":
                condition.append(Toilet())
            elif part == "Balcony":
                condition.append(Balcony())
            elif part == "Kitchen":
                condition.append(Kitchen())
        
        print()      
        for house in search_house(condition, houses):
            house.printHouse()
    
    else:
        print("Invalid Command!")