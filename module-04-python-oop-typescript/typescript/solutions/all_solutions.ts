/**
 * Solutions — TypeScript OOP Exercises
 * Try solving the exercises first! Only look here when stuck.
 */

// =====================================================================
// 01 — Vehicle Interface
// =====================================================================

interface Vehicle {
  brand: string;
  year: number;
  describe(): string;
  age(currentYear: number): number;
}

class Car implements Vehicle {
  constructor(
    public brand: string,
    public year: number,
    public doors: number
  ) {}

  describe(): string {
    return `${this.year} ${this.brand}`;
  }

  age(currentYear: number): number {
    return currentYear - this.year;
  }
}

class Motorcycle implements Vehicle {
  constructor(
    public brand: string,
    public year: number,
    public hasSidecar: boolean
  ) {}

  describe(): string {
    return `${this.year} ${this.brand}`;
  }

  age(currentYear: number): number {
    return currentYear - this.year;
  }
}

// =====================================================================
// 01 — Generic Repository
// =====================================================================

interface Repository<T extends { id: number }> {
  add(item: T): void;
  getById(id: number): T | undefined;
  getAll(): T[];
  remove(id: number): boolean;
}

class MemoryRepository<T extends { id: number }> implements Repository<T> {
  private items: T[] = [];

  add(item: T): void {
    this.items.push(item);
  }

  getById(id: number): T | undefined {
    return this.items.find((item) => item.id === id);
  }

  getAll(): T[] {
    return [...this.items];
  }

  remove(id: number): boolean {
    const index = this.items.findIndex((item) => item.id === id);
    if (index === -1) return false;
    this.items.splice(index, 1);
    return true;
  }
}

// =====================================================================
// 02 — Generic Stack
// =====================================================================

class Stack<T> {
  private items: T[] = [];

  push(item: T): void {
    this.items.push(item);
  }

  pop(): T {
    if (this.items.length === 0) throw new Error("Stack is empty");
    return this.items.pop()!;
  }

  peek(): T {
    if (this.items.length === 0) throw new Error("Stack is empty");
    return this.items[this.items.length - 1];
  }

  get size(): number {
    return this.items.length;
  }

  isEmpty(): boolean {
    return this.items.length === 0;
  }
}

// =====================================================================
// 02 — Discriminated Union + Type Guards
// =====================================================================

type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number }
  | { kind: "triangle"; base: number; height: number };

function describeShape(shape: Shape): string {
  switch (shape.kind) {
    case "circle":
      return `Circle with radius ${shape.radius}`;
    case "rectangle":
      return `Rectangle ${shape.width}x${shape.height}`;
    case "triangle":
      return `Triangle with base ${shape.base} and height ${shape.height}`;
  }
}

function shapeArea(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "rectangle":
      return shape.width * shape.height;
    case "triangle":
      return 0.5 * shape.base * shape.height;
  }
}

function totalArea(shapes: Shape[]): number {
  return shapes.reduce((sum, s) => sum + shapeArea(s), 0);
}

// =====================================================================
// 02 — Utility Types
// =====================================================================

interface User {
  id: number;
  name: string;
  email: string;
  password: string;
}

type PublicUser = Omit<User, "password">;
type UserUpdate = Partial<Omit<User, "id">>;
type UserSummary = Pick<User, "id" | "name">;

// =====================================================================
// 03 — Abstract Logger (Strategy)
// =====================================================================

abstract class Logger {
  abstract log(message: string): string;

  error(message: string): string {
    return this.log(`[ERROR] ${message}`);
  }
}

class ConsoleLogger extends Logger {
  log(message: string): string {
    return `CONSOLE: ${message}`;
  }
}

class FileLogger extends Logger {
  log(message: string): string {
    return `FILE: ${message}`;
  }
}

class App {
  constructor(private logger: Logger) {}

  run(): string {
    return this.logger.log("App started");
  }
}

// =====================================================================
// 03 — QueryBuilder (Builder Pattern)
// =====================================================================

class QueryBuilder {
  private _select: string[] = [];
  private _from: string = "";
  private _where: string[] = [];
  private _orderBy: string = "";
  private _limit: number | null = null;

  select(...columns: string[]): this {
    this._select = columns;
    return this;
  }

  from(table: string): this {
    this._from = table;
    return this;
  }

  where(condition: string): this {
    this._where.push(condition);
    return this;
  }

  orderBy(column: string): this {
    this._orderBy = column;
    return this;
  }

  limit(n: number): this {
    this._limit = n;
    return this;
  }

  build(): string {
    let query = `SELECT ${this._select.join(", ")} FROM ${this._from}`;
    if (this._where.length > 0) {
      query += ` WHERE ${this._where.join(" AND ")}`;
    }
    if (this._orderBy) {
      query += ` ORDER BY ${this._orderBy}`;
    }
    if (this._limit !== null) {
      query += ` LIMIT ${this._limit}`;
    }
    return query;
  }
}

// =====================================================================
// 03 — TypedEventBus (Observer Pattern)
// =====================================================================

class TypedEventBus<T extends Record<string, any>> {
  private listeners: {
    [K in keyof T]?: Array<(data: T[K]) => void>;
  } = {};

  on<K extends keyof T>(event: K, callback: (data: T[K]) => void): void {
    if (!this.listeners[event]) {
      this.listeners[event] = [];
    }
    this.listeners[event]!.push(callback);
  }

  emit<K extends keyof T>(event: K, data: T[K]): void {
    const callbacks = this.listeners[event];
    if (callbacks) {
      callbacks.forEach((cb) => cb(data));
    }
  }
}

console.log("✓ All solutions compile and run correctly");

// =====================================================================
// 04 — AppConfig (Singleton)
// =====================================================================

class AppConfig {
  private static _instance: AppConfig | undefined;
  private store: Record<string, unknown> = {};

  private constructor() {}

  static getInstance(): AppConfig {
    if (!AppConfig._instance) {
      AppConfig._instance = new AppConfig();
    }
    return AppConfig._instance;
  }

  set(key: string, value: unknown): void {
    this.store[key] = value;
  }

  get(key: string, defaultValue?: unknown): unknown {
    return key in this.store ? this.store[key] : defaultValue;
  }

  all(): Record<string, unknown> {
    return { ...this.store };
  }

  reset(): void {
    this.store = {};
  }
}

// =====================================================================
// 04 — Logger Factory (Factory Method)
// =====================================================================

interface ILogger {
  log(message: string): string;
}

class ConsoleLogHandler implements ILogger {
  log(message: string): string {
    return `[CONSOLE] ${message}`;
  }
}

class FileLogHandler implements ILogger {
  constructor(private path: string) {}

  log(message: string): string {
    return `[FILE:${this.path}] ${message}`;
  }
}

class JsonLogHandler implements ILogger {
  log(message: string): string {
    return JSON.stringify({ level: "INFO", message });
  }
}

function createLogger(backend: string, ...args: string[]): ILogger {
  switch (backend) {
    case "console":
      return new ConsoleLogHandler();
    case "file":
      return new FileLogHandler(args[0]);
    case "json":
      return new JsonLogHandler();
    default:
      throw new Error(`Unknown logger backend: ${backend}`);
  }
}

// =====================================================================
// 04 — ShoppingCart (Strategy Pattern)
// =====================================================================

interface DiscountStrategy {
  apply(prices: number[]): number;
}

class NoDiscount implements DiscountStrategy {
  apply(prices: number[]): number {
    return prices.reduce((sum, p) => sum + p, 0);
  }
}

class PercentageDiscount implements DiscountStrategy {
  constructor(private percent: number) {}

  apply(prices: number[]): number {
    const total = prices.reduce((sum, p) => sum + p, 0);
    return total * (1 - this.percent / 100);
  }
}

class BuyOneGetOne implements DiscountStrategy {
  apply(prices: number[]): number {
    if (prices.length === 0) return 0;
    const total = prices.reduce((sum, p) => sum + p, 0);
    return total - Math.min(...prices);
  }
}

class ThresholdDiscount implements DiscountStrategy {
  constructor(private threshold: number, private saving: number) {}

  apply(prices: number[]): number {
    const total = prices.reduce((sum, p) => sum + p, 0);
    return total >= this.threshold ? total - this.saving : total;
  }
}

class ShoppingCart {
  private items: { name: string; price: number }[] = [];
  private strategy: DiscountStrategy = new NoDiscount();

  addItem(name: string, price: number): void {
    this.items.push({ name, price });
  }

  setStrategy(strategy: DiscountStrategy): void {
    this.strategy = strategy;
  }

  total(): number {
    return this.strategy.apply(this.items.map((i) => i.price));
  }
}

// =====================================================================
// 04 — StockMarket (Observer Pattern)
// =====================================================================

interface StockObserver {
  update(ticker: string, price: number): void;
}

class StockMarket {
  private observers: StockObserver[] = [];

  subscribe(observer: StockObserver): void {
    this.observers.push(observer);
  }

  unsubscribe(observer: StockObserver): void {
    this.observers = this.observers.filter((o) => o !== observer);
  }

  setPrice(ticker: string, price: number): void {
    this.observers.forEach((o) => o.update(ticker, price));
  }
}

class PriceLogger implements StockObserver {
  history: { ticker: string; price: number }[] = [];

  update(ticker: string, price: number): void {
    this.history.push({ ticker, price });
  }
}

class PriceAlert implements StockObserver {
  alerts: string[] = [];

  constructor(private threshold: number) {}

  update(ticker: string, price: number): void {
    if (price > this.threshold) {
      this.alerts.push(`ALERT: ${ticker} exceeded ${this.threshold} at ${price}`);
    }
  }
}

class Portfolio implements StockObserver {
  value: number = 0;

  constructor(private ticker: string, private shares: number) {}

  update(ticker: string, price: number): void {
    if (ticker === this.ticker) {
      this.value = this.shares * price;
    }
  }
}

// =====================================================================
// 04 — Coffee Order (Decorator Pattern)
// =====================================================================

interface Beverage {
  cost(): number;
  description(): string;
}

class Espresso implements Beverage {
  cost(): number { return 2.00; }
  description(): string { return "Espresso"; }
}

abstract class CondimentDecorator implements Beverage {
  constructor(protected beverage: Beverage) {}
  abstract cost(): number;
  abstract description(): string;
}

class MilkDecorator extends CondimentDecorator {
  cost(): number { return this.beverage.cost() + 0.50; }
  description(): string { return this.beverage.description() + ", Milk"; }
}

class SugarDecorator extends CondimentDecorator {
  cost(): number { return this.beverage.cost() + 0.25; }
  description(): string { return this.beverage.description() + ", Sugar"; }
}

class WhipDecorator extends CondimentDecorator {
  cost(): number { return this.beverage.cost() + 0.75; }
  description(): string { return this.beverage.description() + ", Whip"; }
}

console.log("✓ All 04 solutions compile correctly");
