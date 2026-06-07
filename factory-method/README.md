# Factory Method

**Category:** Creational
**Reference:** https://refactoring.guru/design-patterns/factory-method

## Intent
Provide an interface for creating objects in a superclass, but let subclasses
alter the type of objects that will be created.

## Problem
A logistics app first handles only **Trucks**. The whole codebase ends up
coupled to the `Truck` class. Adding **Ships** later means changing code
everywhere a `Truck` was created — and you'd repeat that pain for every new
transport type.

## Solution
Replace direct constructor calls (`Truck()`) with calls to a special **factory
method**. Subclasses override that method to return a different product. The
objects returned are often called *products*.

## Structure
| Role | In this example | Job |
|------|-----------------|-----|
| **Product** | `Transport` | Common interface for all created objects |
| **Concrete Products** | `Truck`, `Ship` | Specific implementations |
| **Creator** | `Logistics` | Declares the factory method; holds business logic that uses the product |
| **Concrete Creators** | `RoadLogistics`, `SeaLogistics` | Override the factory method to pick the product |

The key move: the `Creator` (`Logistics.plan_delivery`) never references a
concrete product. It only knows it receives *some* `Transport`.

## When to use it
- You don't know the exact types/dependencies of objects your code works with ahead of time.
- You want to let users of a library/framework extend its internal components.
- You want to reuse existing objects instead of rebuilding them (pooling/caching).

## Pros & Cons
**Pros**
- Avoids tight coupling between creator and concrete products.
- Single Responsibility: creation code lives in one place.
- Open/Closed: add new products by adding new subclasses — no edits to existing code.

**Cons**
- More classes/subclasses → more complexity.

## Run it
```bash
python factory_method.py
```
