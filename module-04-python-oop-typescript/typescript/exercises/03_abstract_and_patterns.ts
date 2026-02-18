/**
 * Exercise 03 — Abstract Classes & Patterns in TypeScript
 * =========================================================
 *
 * CONCEPTS:
 *   - abstract class    → like Python's ABC, can't be instantiated, can have default methods
 *   - abstract method   → subclass MUST implement it
 *   - interface vs abstract class:
 *       interface = pure contract, no implementation at all
 *       abstract  = partial implementation + contract
 *
 * PATTERNS:
 *   - Strategy  → swap algorithms via dependency injection
 *   - Observer  → event-driven notification
 *   - Builder   → step-by-step object construction
 *
 * RUN:
 *   npx ts-node 03_abstract_and_patterns.ts
 */

// ---- TASK 1: Abstract Logger (Strategy Pattern) ----
//
// abstract class Logger {
//   abstract log(message: string): string;
//
//   // Default method — subclasses inherit this for free
//   error(message: string): string {
//     return this.log(`[ERROR] ${message}`);
//   }
// }
//
// class ConsoleLogger extends Logger { ... }  → returns "CONSOLE: {message}"
// class FileLogger extends Logger { ... }     → returns "FILE: {message}"
//
// class App {
//   constructor(private logger: Logger) {}
//   run(): string { return this.logger.log("App started"); }
// }

// YOUR CODE HERE

abstract class Logger {
  // ...
}

class ConsoleLogger {
  // ...
}

class FileLogger {
  // ...
}

class App {
  // ...
}

// ---- TASK 2: Builder Pattern ----
//
// Implement a QueryBuilder that constructs SQL-like query strings:
//
//   const query = new QueryBuilder()
//     .select("name", "age")
//     .from("users")
//     .where("age > 18")
//     .where("name LIKE '%a%'")
//     .orderBy("name")
//     .limit(10)
//     .build();
//
//   → "SELECT name, age FROM users WHERE age > 18 AND name LIKE '%a%' ORDER BY name LIMIT 10"
//
// Each method returns `this` (method chaining).

// YOUR CODE HERE

class QueryBuilder {
  // ...

  build(): string {
    return ""; // replace
  }
}

// ---- TASK 3: Observer Pattern (typed) ----
//
// interface EventMap {
//   login: { userId: string };
//   logout: { userId: string };
//   purchase: { userId: string; amount: number };
// }
//
// class TypedEventBus<T extends Record<string, any>> {
//   on<K extends keyof T>(event: K, callback: (data: T[K]) => void): void;
//   emit<K extends keyof T>(event: K, data: T[K]): void;
// }
//
// This gives you type-safe events:
//   bus.emit("login", { userId: "abc" })  // ✓
//   bus.emit("login", { amount: 5 })       // ✗ type error!

// YOUR CODE HERE

class TypedEventBus<T extends Record<string, any>> {
  // ...
}

// ---- TESTS ---- (uncomment after implementing)

/*
// Task 1
const consoleApp = new App(new ConsoleLogger());
console.assert(consoleApp.run() === "CONSOLE: App started");

const fileApp = new App(new FileLogger());
console.assert(fileApp.run() === "FILE: App started");

const cl = new ConsoleLogger();
console.assert(cl.error("disk full") === "CONSOLE: [ERROR] disk full");

// Can't instantiate abstract class
// new Logger();  // ← TypeScript compiler error

// Task 2
const query = new QueryBuilder()
  .select("name", "age")
  .from("users")
  .where("age > 18")
  .where("name LIKE '%a%'")
  .orderBy("name")
  .limit(10)
  .build();

console.assert(
  query ===
    "SELECT name, age FROM users WHERE age > 18 AND name LIKE '%a%' ORDER BY name LIMIT 10"
);

const simple = new QueryBuilder().select("*").from("products").build();
console.assert(simple === "SELECT * FROM products");

// Task 3
interface EventMap {
  login: { userId: string };
  purchase: { userId: string; amount: number };
}

const bus = new TypedEventBus<EventMap>();
const log: string[] = [];

bus.on("login", (data) => log.push(`login:${data.userId}`));
bus.on("purchase", (data) => log.push(`buy:${data.userId}:${data.amount}`));

bus.emit("login", { userId: "alice" });
bus.emit("purchase", { userId: "bob", amount: 99 });

console.assert(log[0] === "login:alice");
console.assert(log[1] === "buy:bob:99");

console.log("✓ 03_abstract_and_patterns — all tests passed");
*/
