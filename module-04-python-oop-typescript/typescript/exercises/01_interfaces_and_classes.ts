/**
 * Exercise 01 — Interfaces & Classes in TypeScript
 * ==================================================
 *
 * CONCEPTS:
 *   - interface  → defines a contract (shape of an object). No runtime code.
 *   - class      → blueprint with implementation. Exists at runtime.
 *   - implements → a class promises to fulfill an interface's contract.
 *   - readonly   → property can only be set in the constructor.
 *   - access modifiers → public (default), private, protected.
 *
 * RUN:
 *   npx ts-node 01_interfaces_and_classes.ts
 *   (or: npx tsx 01_interfaces_and_classes.ts)
 */

// ---- EXAMPLE (for reference) ----

interface Printable {
  toString(): string;
}

class Document implements Printable {
  constructor(public title: string) {}
  toString(): string {
    return `Document: ${this.title}`;
  }
}

// ---- TASK 1: Implement the `Vehicle` interface and two classes ----
//
// interface Vehicle {
//   brand: string;
//   year: number;
//   describe(): string;       → "2020 Tesla Model S"
//   age(currentYear: number): number;
// }
//
// class Car implements Vehicle { ... }
// class Motorcycle implements Vehicle { ... }
//
// Car has an additional property: `doors: number`
// Motorcycle has: `hasSidecar: boolean`

// YOUR CODE HERE

interface Vehicle {
  // ...
}

class Car {
  // ...
}

class Motorcycle {
  // ...
}

// ---- TASK 2: Generic interface ----
//
// Implement a generic `Repository<T>` interface and a `MemoryRepository<T>` class.
//
// interface Repository<T> {
//   add(item: T): void;
//   getById(id: number): T | undefined;
//   getAll(): T[];
//   remove(id: number): boolean;
// }
//
// Each item must have at least { id: number }.
// Use a constraint: <T extends { id: number }>

// YOUR CODE HERE

interface Repository<T extends { id: number }> {
  // ...
}

class MemoryRepository<T extends { id: number }> {
  // ...
}

// ---- TESTS ---- (uncomment after implementing)

/*
// Task 1 tests
const car = new Car("Tesla", 2020, 4);
console.assert(car.brand === "Tesla");
console.assert(car.year === 2020);
console.assert(car.doors === 4);
console.assert(car.describe() === "2020 Tesla");
console.assert(car.age(2026) === 6);

const moto = new Motorcycle("Harley", 2018, true);
console.assert(moto.describe() === "2018 Harley");
console.assert(moto.hasSidecar === true);

// Task 2 tests
interface User {
  id: number;
  name: string;
}

const repo = new MemoryRepository<User>();
repo.add({ id: 1, name: "Alice" });
repo.add({ id: 2, name: "Bob" });

console.assert(repo.getAll().length === 2);
console.assert(repo.getById(1)?.name === "Alice");
console.assert(repo.getById(99) === undefined);
console.assert(repo.remove(1) === true);
console.assert(repo.remove(1) === false);
console.assert(repo.getAll().length === 1);

console.log("✓ 01_interfaces_and_classes — all tests passed");
*/
