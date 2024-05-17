import copy

# HousePart와 Floor Bridge
class HousePart: # Floor 클래스의 parts 멤버에 담길 집의 part
    def __init__(self):
        self.light = False

    def __str__(self):
        raise NotImplementedError

    def light_on_off(self):
        self.light = not self.light


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

    def get_house_part(self, part_name):  # 해당 파츠가 있다면 그 파츠를 반환
        found_parts = []
        for part in self.parts:
            if str(part) == part_name:
                found_parts.append(part)

        return found_parts

    def __str__(self):
        parts_str = ', '.join(str(part) for part in self.parts)
        return f"Floor {self.level}: {parts_str}"


# House
class House:
    address = 0

    def __init__(self):
        self.address = House.address
        self.floors = [] # floor는 현재 층과 그 층의 parts를 담는 Floor 객체 리스트

    def add_floor(self, floor):
        self.floors.append(floor)

    def clone(self): # Prototype Pattern
        clone = copy.deepcopy(self)
        clone.address = House.address + 1
        return clone

    def printHouse(self):
        floors_str = '\n'.join(str(floor) for floor in self.floors)
        print(f"Address: {self.address}\n{floors_str}\n")




# Factory Pattern
class HouseFactory:
    def buildHouse(self, floor_plans):
        House.address += 1
        house = House()
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
        return self.factory.buildHouse(floor_plans)

    def build_luxury_house(self):
        floor_plans = [
            [Room(), Kitchen(), Balcony()],
            [Room(), Room(), Toilet()],
            [Kitchen(), Toilet(), Balcony()]
        ]
        return self.factory.buildHouse(floor_plans)

    def build_custom_house(self, floor_plans): # 사용자의 입력에 따라 자유롭게 집 구성
        return self.factory.buildHouse(floor_plans)


# Facade
builder = HouseBuilderFacade()
houses = [
    builder.build_standard_house(),
    builder.build_luxury_house(),
    builder.build_custom_house([
        [Room(), Toilet()],
        [Room(), Kitchen(), Balcony()],
        [Room(), Room(), Toilet(), Balcony()]
    ])
]

houses.append(houses[0].clone())
for house in houses:
    house.printHouse()

print(houses[2].floors[2].get_house_part("Room")[0].light) # 3번째 집의 3층 첫째 방의 조명 상태 출력
houses[2].floors[2].get_house_part("Room")[0].light_on_off()
print(houses[2].floors[2].get_house_part("Room")[0].light)
