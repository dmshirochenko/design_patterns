"""Factory Method pattern.

Reference: https://refactoring.guru/design-patterns/factory-method

Intent
------
Define an interface for creating an object, but let subclasses decide which
class to instantiate. Factory Method lets a class defer instantiation to
subclasses.

Example
-------
A logistics app starts out only handling road delivery (Trucks). Later it must
also support sea delivery (Ships). Instead of scattering ``Truck()`` calls all
over the code, the creation of the transport object is moved behind a single
"factory method". Subclasses override that method to decide which concrete
transport to build, while the rest of the logic stays unchanged.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


# --- Product -----------------------------------------------------------------
# The common interface that every object the factory method produces must
# implement. Client code works with this interface, never the concrete classes.
class Transport(ABC):
    @abstractmethod
    def deliver(self) -> str:
        """Carry the cargo to its destination."""
        raise NotImplementedError


# --- Concrete Products -------------------------------------------------------
class Truck(Transport):
    def deliver(self) -> str:
        return "Delivering by land in a box."


class Ship(Transport):
    def deliver(self) -> str:
        return "Delivering by sea in a container."


# --- Creator -----------------------------------------------------------------
# Declares the factory method that returns a Product. It may also contain core
# business logic that relies on the Product, without knowing the concrete type.
class Logistics(ABC):
    @abstractmethod
    def create_transport(self) -> Transport:
        """The factory method. Subclasses decide the concrete Transport."""
        raise NotImplementedError

    def plan_delivery(self) -> str:
        # Note: the Creator does NOT depend on a concrete product. It only
        # knows it gets *some* Transport and can call deliver() on it.
        transport = self.create_transport()
        return f"Logistics: planning a route. {transport.deliver()}"


# --- Concrete Creators -------------------------------------------------------
# Each subclass overrides the factory method to change the resulting product.
class RoadLogistics(Logistics):
    def create_transport(self) -> Transport:
        return Truck()


class SeaLogistics(Logistics):
    def create_transport(self) -> Transport:
        return Ship()


# --- Client ------------------------------------------------------------------
# Client code works with a Logistics instance through its base interface. You
# can pass it any concrete creator and it keeps working.
def client_code(logistics: Logistics) -> None:
    print(logistics.plan_delivery())


if __name__ == "__main__":
    print("App: launched with RoadLogistics.")
    client_code(RoadLogistics())

    print("\nApp: launched with SeaLogistics.")
    client_code(SeaLogistics())
