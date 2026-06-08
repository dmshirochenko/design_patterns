"""Abstract Factory pattern.

Reference: https://refactoring.guru/design-patterns/abstract-factory

Intent
------
Provide an interface for creating families of related or dependent objects
without specifying their concrete classes.

Example
-------
A furniture shop sells chairs, sofas, and coffee tables in two style variants:
Modern and Victorian. Each variant forms a compatible family — you never want
a Modern chair paired with a Victorian sofa. The Abstract Factory guarantees
that every product returned by the same factory belongs to the same family.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


# --- Abstract Products -------------------------------------------------------
# One interface per product type. All concrete variants must implement it.

class Chair(ABC):
    @abstractmethod
    def sit_on(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def has_legs(self) -> bool:
        raise NotImplementedError


class Sofa(ABC):
    @abstractmethod
    def lie_on(self) -> str:
        raise NotImplementedError


class CoffeeTable(ABC):
    @abstractmethod
    def place_cup(self) -> str:
        raise NotImplementedError


# --- Concrete Products: Modern variant ---------------------------------------

class ModernChair(Chair):
    def sit_on(self) -> str:
        return "Sitting on a sleek Modern chair."

    def has_legs(self) -> bool:
        return False  # Modern chairs often use a pedestal base


class ModernSofa(Sofa):
    def lie_on(self) -> str:
        return "Lying on a low-profile Modern sofa."


class ModernCoffeeTable(CoffeeTable):
    def place_cup(self) -> str:
        return "Placing cup on a glass-top Modern coffee table."


# --- Concrete Products: Victorian variant ------------------------------------

class VictorianChair(Chair):
    def sit_on(self) -> str:
        return "Sitting on an ornate Victorian chair."

    def has_legs(self) -> bool:
        return True  # Victorian chairs always have four carved legs


class VictorianSofa(Sofa):
    def lie_on(self) -> str:
        return "Lying on a tufted Victorian sofa."


class VictorianCoffeeTable(CoffeeTable):
    def place_cup(self) -> str:
        return "Placing cup on a dark-wood Victorian coffee table."


# --- Abstract Factory --------------------------------------------------------
# Declares creation methods for every product in the family.

class FurnitureFactory(ABC):
    @abstractmethod
    def create_chair(self) -> Chair:
        raise NotImplementedError

    @abstractmethod
    def create_sofa(self) -> Sofa:
        raise NotImplementedError

    @abstractmethod
    def create_coffee_table(self) -> CoffeeTable:
        raise NotImplementedError


# --- Concrete Factories ------------------------------------------------------
# Each factory produces only its own variant — compatibility is guaranteed.

class ModernFurnitureFactory(FurnitureFactory):
    def create_chair(self) -> Chair:
        return ModernChair()

    def create_sofa(self) -> Sofa:
        return ModernSofa()

    def create_coffee_table(self) -> CoffeeTable:
        return ModernCoffeeTable()


class VictorianFurnitureFactory(FurnitureFactory):
    def create_chair(self) -> Chair:
        return VictorianChair()

    def create_sofa(self) -> Sofa:
        return VictorianSofa()

    def create_coffee_table(self) -> CoffeeTable:
        return VictorianCoffeeTable()


# --- Client ------------------------------------------------------------------
# Works only with abstract types. The factory variant can be swapped freely
# without touching this code.

def client_code(factory: FurnitureFactory) -> None:
    chair = factory.create_chair()
    sofa = factory.create_sofa()
    table = factory.create_coffee_table()

    print(chair.sit_on())
    print(f"  Chair has legs: {chair.has_legs()}")
    print(sofa.lie_on())
    print(table.place_cup())


if __name__ == "__main__":
    print("App: using ModernFurnitureFactory.")
    client_code(ModernFurnitureFactory())

    print("\nApp: using VictorianFurnitureFactory.")
    client_code(VictorianFurnitureFactory())
