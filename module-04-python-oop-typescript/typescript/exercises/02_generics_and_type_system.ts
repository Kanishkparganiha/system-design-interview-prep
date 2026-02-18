/**
 * Exercise 02 — Generics & the Type System
 * ==========================================
 *
 * CONCEPTS:
 *   - Generics <T>       → write code that works with any type
 *   - Constraints         → <T extends SomeType> limits what T can be
 *   - Union types         → string | number (one of several types)
 *   - Type guards         → narrow a union at runtime (typeof, instanceof, "in")
 *   - Utility types       → Partial<T>, Pick<T,K>, Omit<T,K>, Readonly<T>
 *   - Discriminated unions → tagged objects for exhaustive checking
 *
 * RUN:
 *   npx ts-node 02_generics_and_type_system.ts
 */

// ---- TASK 1: Generic Stack ----
//
// Implement a Stack<T> class with:
//   push(item: T): void
//   pop(): T            (throw Error if empty)
//   peek(): T           (throw Error if empty)
//   get size(): number  (getter)
//   isEmpty(): boolean

// YOUR CODE HERE

class Stack<T> {
  // ...
}

// ---- TASK 2: Type Guards ----
//
// Given this union type, implement a function that formats it:
//
//   type Shape =
//     | { kind: "circle"; radius: number }
//     | { kind: "rectangle"; width: number; height: number }
//     | { kind: "triangle"; base: number; height: number }
//
//   function describeShape(shape: Shape): string
//     → "Circle with radius 5"
//     → "Rectangle 4x3"
//     → "Triangle with base 6 and height 4"
//
//   function totalArea(shapes: Shape[]): number
//     → sum of all areas

// YOUR CODE HERE

type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number }
  | { kind: "triangle"; base: number; height: number };

function describeShape(shape: Shape): string {
  // Hint: use a switch on shape.kind (discriminated union)
  return ""; // replace
}

function totalArea(shapes: Shape[]): number {
  return 0; // replace
}

// ---- TASK 3: Utility Types ----
//
// Given:
//   interface User {
//     id: number;
//     name: string;
//     email: string;
//     password: string;
//   }
//
// Create these types using utility types:
//   type PublicUser    = ...  // User without "password"        (use Omit)
//   type UserUpdate    = ...  // All fields optional            (use Partial + Omit to exclude id)
//   type UserSummary   = ...  // Only id and name               (use Pick)

// YOUR CODE HERE

interface User {
  id: number;
  name: string;
  email: string;
  password: string;
}

// type PublicUser = ...
// type UserUpdate = ...
// type UserSummary = ...

// ---- TESTS ---- (uncomment after implementing)

/*
// Task 1
const stack = new Stack<number>();
console.assert(stack.isEmpty() === true);
stack.push(10);
stack.push(20);
stack.push(30);
console.assert(stack.size === 3);
console.assert(stack.peek() === 30);
console.assert(stack.pop() === 30);
console.assert(stack.pop() === 20);
console.assert(stack.size === 1);

// Works with strings too (generic)
const strStack = new Stack<string>();
strStack.push("hello");
console.assert(strStack.peek() === "hello");

// Task 2
console.assert(
  describeShape({ kind: "circle", radius: 5 }) === "Circle with radius 5"
);
console.assert(
  describeShape({ kind: "rectangle", width: 4, height: 3 }) === "Rectangle 4x3"
);
console.assert(
  describeShape({ kind: "triangle", base: 6, height: 4 }) ===
    "Triangle with base 6 and height 4"
);

const area = totalArea([
  { kind: "rectangle", width: 2, height: 3 },
  { kind: "circle", radius: 1 },
  { kind: "triangle", base: 4, height: 3 },
]);
console.assert(Math.abs(area - (6 + Math.PI + 6)) < 0.001);

// Task 3 — compile-time checks (if these compile, they pass)
const pub: PublicUser = { id: 1, name: "A", email: "a@b" };
const upd: UserUpdate = { name: "B" };  // partial, no id
const sum: UserSummary = { id: 1, name: "A" };

console.log("✓ 02_generics_and_type_system — all tests passed");
*/
