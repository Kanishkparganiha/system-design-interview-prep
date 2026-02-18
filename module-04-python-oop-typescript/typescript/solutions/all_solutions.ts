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
