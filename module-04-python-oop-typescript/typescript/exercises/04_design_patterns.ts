/**
 * Exercise 04 — Design Patterns in TypeScript
 * =============================================
 *
 * Five foundational patterns from https://refactoring.guru/design-patterns/catalog
 *
 * | Pattern        | Category    | Core Idea                                      |
 * |----------------|-------------|------------------------------------------------|
 * | Singleton      | Creational  | Only one instance ever; private constructor    |
 * | Factory Method | Creational  | Factory decides which class to instantiate     |
 * | Strategy       | Behavioral  | Swap algorithms at runtime via interface       |
 * | Observer       | Behavioral  | Subject notifies typed observers on change     |
 * | Decorator      | Structural  | Wrap objects to add behavior without subclass  |
 *
 * NOTE vs Exercise 03:
 *   Exercise 03 introduced Strategy (abstract Logger) and Observer (TypedEventBus).
 *   Here each pattern gets a richer, more realistic scenario.
 *
 * TypeScript-specific highlights:
 *   - Singleton uses `private constructor` (more idiomatic than Python's __new__)
 *   - Factory returns a union type; callers use type narrowing
 *   - Strategy/Observer use interfaces (zero runtime cost) instead of abstract classes
 *   - Decorator uses structural typing
 *
 * RUN:
 *   npx ts-node 04_design_patterns.ts
 *   (or: npx tsx 04_design_patterns.ts)
 */

// =========================================================================
// PATTERN 1 — Singleton (Creational)
// =========================================================================
//
// CONCEPT:
//   Ensure only ONE instance of a class exists. In TypeScript, the canonical
//   approach is a PRIVATE constructor + static getInstance() method.
//
//   class Registry {
//     private static instance: Registry;
//     private constructor() {}          // ← blocks `new Registry()`
//
//     static getInstance(): Registry {
//       if (!Registry.instance) Registry.instance = new Registry();
//       return Registry.instance;
//     }
//   }
//
//   const r1 = Registry.getInstance();
//   const r2 = Registry.getInstance();
//   console.assert(r1 === r2);  // same object
//
// TASK: Implement `AppConfig`
//
//   A global key-value config store. Must always return the same instance.
//
//   const cfg1 = AppConfig.getInstance();
//   const cfg2 = AppConfig.getInstance();
//   console.assert(cfg1 === cfg2);
//
//   cfg1.set("debug", true);
//   cfg2.get("debug")                    // true  (shared state)
//   cfg1.get("timeout", 30)              // 30    (returns default if key missing)
//   cfg1.get("missing")                  // undefined
//   cfg1.all()                           // { debug: true }
//
// Rules:
//   1. Use `private constructor` — calling `new AppConfig()` must be a compile error
//   2. set(key, value)  — stores any value
//   3. get(key)         — returns the value or undefined
//   4. get(key, defaultValue) — returns defaultValue if key is missing
//   5. all()            — returns a shallow copy of the entire store
//   6. reset()          — clears the store (needed for test isolation)

// YOUR CODE HERE

class AppConfig {
  // ...
}

// =========================================================================
// PATTERN 2 — Factory Method (Creational)
// =========================================================================
//
// CONCEPT:
//   Define an interface for creating objects, but let a factory function
//   decide the concrete class. Callers work against the interface, never
//   touching concrete constructors.
//
//   interface Serializer {
//     serialize(data: unknown): string;
//   }
//   function createSerializer(format: "json" | "csv"): Serializer { ... }
//
// TASK: Implement a Logger Factory
//
//   All loggers implement the same interface:
//     interface ILogger { log(message: string): string; }
//
//   createLogger("console")              → ConsoleLogger
//   createLogger("file", "app.log")      → FileLogger
//   createLogger("json")                 → JsonLogger
//   createLogger("unknown")              → throws Error
//
//   Output format:
//     ConsoleLogger  → "[CONSOLE] {message}"
//     FileLogger     → "[FILE:app.log] {message}"
//     JsonLogger     → '{"level":"INFO","message":"{message}"}'
//
// Rules:
//   1. `ILogger` is an interface (not abstract class)
//   2. `createLogger` is overloaded so TypeScript knows the return type
//      based on the backend literal — OR use a single signature returning ILogger
//   3. Unknown backend throws Error

// YOUR CODE HERE

interface ILogger {
  log(message: string): string;
}

class ConsoleLogger implements ILogger {
  // ...
  log(message: string): string { return ""; }
}

class FileLogger implements ILogger {
  // ...
  log(message: string): string { return ""; }
}

class JsonLogger implements ILogger {
  // ...
  log(message: string): string { return ""; }
}

function createLogger(backend: string, ...args: any[]): ILogger {
  throw new Error("Not implemented");
}

// =========================================================================
// PATTERN 3 — Strategy (Behavioral)
// =========================================================================
//
// CONCEPT:
//   Encapsulate a family of algorithms behind a common interface so they
//   can be swapped at runtime. The context holds a reference to the
//   strategy and delegates work to it.
//
// TASK: Implement a Discount System
//
//   interface DiscountStrategy {
//     apply(prices: number[]): number;  // returns final total
//   }
//
//   class ShoppingCart {
//     addItem(name: string, price: number): void
//     setStrategy(strategy: DiscountStrategy): void
//     total(): number
//   }
//
//   const cart = new ShoppingCart();
//   cart.addItem("apple",  1.50);
//   cart.addItem("banana", 2.00);
//   cart.addItem("cherry", 3.50);  // subtotal = 7.00
//
//   cart.setStrategy(new NoDiscount());           // 7.00
//   cart.setStrategy(new PercentageDiscount(10)); // 6.30  (10% off)
//   cart.setStrategy(new BuyOneGetOne());         // 5.50  (cheapest item free)
//   cart.setStrategy(new ThresholdDiscount(50,5));// 7.00  (threshold not met)
//
// Rules:
//   1. `DiscountStrategy` is an interface
//   2. Default strategy is `NoDiscount`
//   3. `BuyOneGetOne` makes the single cheapest item free
//   4. `ThresholdDiscount(threshold, saving)` deducts `saving` only when
//      subtotal >= threshold

// YOUR CODE HERE

interface DiscountStrategy {
  apply(prices: number[]): number;
}

class NoDiscount implements DiscountStrategy {
  apply(prices: number[]): number { return 0; }
}

class PercentageDiscount implements DiscountStrategy {
  constructor(private percent: number) {}
  apply(prices: number[]): number { return 0; }
}

class BuyOneGetOne implements DiscountStrategy {
  apply(prices: number[]): number { return 0; }
}

class ThresholdDiscount implements DiscountStrategy {
  constructor(private threshold: number, private saving: number) {}
  apply(prices: number[]): number { return 0; }
}

class ShoppingCart {
  // ...
  addItem(name: string, price: number): void {}
  setStrategy(strategy: DiscountStrategy): void {}
  total(): number { return 0; }
}

// =========================================================================
// PATTERN 4 — Observer (Behavioral)
// =========================================================================
//
// CONCEPT:
//   One-to-many dependency. When a subject changes state it notifies all
//   registered observers. Observers are typed with generics for safety.
//
//   interface Observer<T> {
//     update(data: T): void;
//   }
//
// TASK: Implement a Stock Ticker
//
//   interface StockObserver {
//     update(ticker: string, price: number): void;
//   }
//
//   class StockMarket {
//     subscribe(observer: StockObserver): void
//     unsubscribe(observer: StockObserver): void
//     setPrice(ticker: string, price: number): void   ← triggers all observers
//   }
//
//   class PriceLogger   → stores { ticker, price } objects in .history
//   class PriceAlert    → fires when price > threshold; stores strings in .alerts
//                         format: "ALERT: AAPL exceeded 150 at 160"
//   class Portfolio     → tracks .value = shares * latestPrice for its ticker only
//
//   const market = new StockMarket();
//   const logger = new PriceLogger();
//   const alert  = new PriceAlert(150);
//   const port   = new Portfolio("AAPL", 10);
//
//   market.subscribe(logger);
//   market.subscribe(alert);
//   market.subscribe(port);
//   market.setPrice("AAPL", 140);
//   // logger.history → [{ ticker: "AAPL", price: 140 }]
//   // alert.alerts   → []
//   // port.value     → 1400

// YOUR CODE HERE

interface StockObserver {
  update(ticker: string, price: number): void;
}

class StockMarket {
  // ...
  subscribe(observer: StockObserver): void {}
  unsubscribe(observer: StockObserver): void {}
  setPrice(ticker: string, price: number): void {}
}

class PriceLogger implements StockObserver {
  history: { ticker: string; price: number }[] = [];
  update(ticker: string, price: number): void {}
}

class PriceAlert implements StockObserver {
  alerts: string[] = [];
  constructor(private threshold: number) {}
  update(ticker: string, price: number): void {}
}

class Portfolio implements StockObserver {
  value: number = 0;
  constructor(private ticker: string, private shares: number) {}
  update(ticker: string, price: number): void {}
}

// =========================================================================
// PATTERN 5 — Decorator (Structural)
// =========================================================================
//
// CONCEPT:
//   Wrap an object in another object that shares the same interface,
//   adding behavior before/after delegating to the wrapped object.
//   Decorators can be stacked.
//
//   interface Component { operation(): string; }
//   class ConcreteComponent implements Component { ... }
//   class WrapperA implements Component {
//     constructor(private wrapped: Component) {}
//     operation() { return "A(" + this.wrapped.operation() + ")"; }
//   }
//
// TASK: Implement a Coffee Order Builder
//
//   interface Beverage {
//     cost(): number;
//     description(): string;
//   }
//
//   class Espresso implements Beverage     → cost: 2.00, desc: "Espresso"
//
//   abstract class CondimentDecorator implements Beverage {
//     constructor(protected beverage: Beverage) {}
//   }
//
//   class MilkDecorator  extends CondimentDecorator  → +0.50, appends ", Milk"
//   class SugarDecorator extends CondimentDecorator  → +0.25, appends ", Sugar"
//   class WhipDecorator  extends CondimentDecorator  → +0.75, appends ", Whip"
//
//   let order: Beverage = new Espresso();
//   order = new MilkDecorator(order);    // cost: 2.50, desc: "Espresso, Milk"
//   order = new SugarDecorator(order);   // cost: 2.75, desc: "Espresso, Milk, Sugar"
//   order = new WhipDecorator(order);    // cost: 3.25, desc: "Espresso, Milk, Sugar, Whip"

// YOUR CODE HERE

interface Beverage {
  cost(): number;
  description(): string;
}

class Espresso implements Beverage {
  cost(): number { return 0; }
  description(): string { return ""; }
}

abstract class CondimentDecorator implements Beverage {
  constructor(protected beverage: Beverage) {}
  abstract cost(): number;
  abstract description(): string;
}

class MilkDecorator extends CondimentDecorator {
  cost(): number { return 0; }
  description(): string { return ""; }
}

class SugarDecorator extends CondimentDecorator {
  cost(): number { return 0; }
  description(): string { return ""; }
}

class WhipDecorator extends CondimentDecorator {
  cost(): number { return 0; }
  description(): string { return ""; }
}

// =========================================================================
// TESTS — uncomment after implementing
// =========================================================================

/*
// ---- Singleton ----
AppConfig["_instance"] = undefined as any;  // reset for test isolation

const cfg1 = AppConfig.getInstance();
const cfg2 = AppConfig.getInstance();
console.assert(cfg1 === cfg2, "Must be the same instance");

cfg1.set("debug", true);
console.assert(cfg2.get("debug") === true);
console.assert(cfg1.get("timeout", 30) === 30);  // default
console.assert(cfg1.get("missing") === undefined);

const snap = cfg1.all();
console.assert(snap["debug"] === true);
snap["debug"] = false;
console.assert(cfg1.get("debug") === true);  // copy, original unchanged

cfg1.reset();
console.assert(Object.keys(cfg1.all()).length === 0);

// ---- Factory Method ----
const cl = createLogger("console");
console.assert(cl.log("hello") === "[CONSOLE] hello");

const fl = createLogger("file", "app.log");
console.assert(fl.log("hello") === "[FILE:app.log] hello");

const jl = createLogger("json");
const parsed = JSON.parse(jl.log("hello"));
console.assert(parsed.level === "INFO" && parsed.message === "hello");

try {
  createLogger("unknown");
  console.assert(false, "Should have thrown");
} catch (e) {}

// All loggers implement ILogger (polymorphism)
const loggers: ILogger[] = [createLogger("console"), createLogger("file", "x.log"), createLogger("json")];
for (const lg of loggers) {
  console.assert(typeof lg.log("test") === "string");
}

// ---- Strategy ----
const cart = new ShoppingCart();
cart.addItem("apple",  1.50);
cart.addItem("banana", 2.00);
cart.addItem("cherry", 3.50);  // subtotal = 7.00

cart.setStrategy(new NoDiscount());
console.assert(Math.abs(cart.total() - 7.00) < 1e-9);

cart.setStrategy(new PercentageDiscount(10));
console.assert(Math.abs(cart.total() - 6.30) < 1e-9);

cart.setStrategy(new BuyOneGetOne());
console.assert(Math.abs(cart.total() - 5.50) < 1e-9);

cart.setStrategy(new ThresholdDiscount(50, 5));
console.assert(Math.abs(cart.total() - 7.00) < 1e-9);  // threshold not met

const bigCart = new ShoppingCart();
bigCart.addItem("item", 60.00);
bigCart.setStrategy(new ThresholdDiscount(50, 5));
console.assert(Math.abs(bigCart.total() - 55.00) < 1e-9);

// Strategy swap
cart.setStrategy(new PercentageDiscount(50));
console.assert(Math.abs(cart.total() - 3.50) < 1e-9);

// ---- Observer ----
const market    = new StockMarket();
const logger    = new PriceLogger();
const alertObs  = new PriceAlert(150);
const portfolio = new Portfolio("AAPL", 10);

market.subscribe(logger);
market.subscribe(alertObs);
market.subscribe(portfolio);

market.setPrice("AAPL", 140);
console.assert(logger.history.length === 1);
console.assert(logger.history[0].ticker === "AAPL" && logger.history[0].price === 140);
console.assert(alertObs.alerts.length === 0);
console.assert(Math.abs(portfolio.value - 1400) < 1e-9);

market.setPrice("AAPL", 160);
console.assert(logger.history.length === 2);
console.assert(alertObs.alerts.length === 1);
console.assert(alertObs.alerts[0].includes("AAPL") && alertObs.alerts[0].includes("160"));
console.assert(Math.abs(portfolio.value - 1600) < 1e-9);

market.unsubscribe(logger);
market.setPrice("AAPL", 170);
console.assert(logger.history.length === 2);        // logger unsubscribed
console.assert(Math.abs(portfolio.value - 1700) < 1e-9);

market.subscribe(logger);
market.setPrice("GOOG", 200);                       // different ticker
console.assert(Math.abs(portfolio.value - 1700) < 1e-9);  // AAPL portfolio unchanged

// ---- Decorator ----
let order: Beverage = new Espresso();
console.assert(Math.abs(order.cost() - 2.00) < 1e-9);
console.assert(order.description() === "Espresso");

order = new MilkDecorator(order);
console.assert(Math.abs(order.cost() - 2.50) < 1e-9);
console.assert(order.description() === "Espresso, Milk");

order = new SugarDecorator(order);
console.assert(Math.abs(order.cost() - 2.75) < 1e-9);
console.assert(order.description() === "Espresso, Milk, Sugar");

order = new WhipDecorator(order);
console.assert(Math.abs(order.cost() - 3.25) < 1e-9);
console.assert(order.description() === "Espresso, Milk, Sugar, Whip");

const doubleMilk = new MilkDecorator(new MilkDecorator(new Espresso()));
console.assert(Math.abs(doubleMilk.cost() - 3.00) < 1e-9);
console.assert(doubleMilk.description() === "Espresso, Milk, Milk");

const altOrder = new SugarDecorator(new WhipDecorator(new Espresso()));
console.assert(Math.abs(altOrder.cost() - 3.00) < 1e-9);
console.assert(altOrder.description() === "Espresso, Whip, Sugar");

console.log("✓ 04_design_patterns — all tests passed");
*/
