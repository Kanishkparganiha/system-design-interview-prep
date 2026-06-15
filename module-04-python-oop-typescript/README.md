# Module 04 — Python OOP & TypeScript Practice

Hands-on exercises to master Object-Oriented Programming in both Python and TypeScript. Each exercise explains the concept first, then gives you a problem with built-in tests to self-check.

---

## Python OOP (Jupyter Notebooks)

Progress through these in order — each builds on the previous:

| # | Notebook | Concepts | Exercises |
|---|----------|----------|-----------|
| 01 | [Classes & Objects](python_oop/exercises/01_classes_and_objects.ipynb) | `__init__`, `self`, instance vs class attributes, `@classmethod` | `BankAccount` |
| 02 | [Inheritance & Polymorphism](python_oop/exercises/02_inheritance_and_polymorphism.ipynb) | `super()`, method overriding, `isinstance()`, MRO | Shape hierarchy, `total_area()` |
| 03 | [Encapsulation & Properties](python_oop/exercises/03_encapsulation_and_properties.ipynb) | `_private`, `@property`, `@setter`, data hiding | `Temperature`, `Stack` |
| 04 | [Dunder Methods](python_oop/exercises/04_dunder_methods.ipynb) | `__add__`, `__eq__`, `__lt__`, `__len__`, `__iter__`, `__getitem__` | `Money`, `LinkedList` |
| 05 | [Abstract Classes & Patterns](python_oop/exercises/05_abstract_classes_and_patterns.ipynb) | `ABC`, `@abstractmethod`, Strategy, Observer, Singleton | Notification system, `EventBus` |

**Solutions:** [all_solutions.ipynb](python_oop/solutions/all_solutions.ipynb) — try first, check later!

---

## TypeScript OOP

| # | File | Concepts | Exercises |
|---|------|----------|-----------|
| 01 | [Interfaces & Classes](typescript/exercises/01_interfaces_and_classes.ts) | `interface`, `implements`, `readonly`, generics | `Vehicle`, `Repository<T>` |
| 02 | [Generics & Type System](typescript/exercises/02_generics_and_type_system.ts) | `<T>`, constraints, union types, discriminated unions, utility types | `Stack<T>`, `Shape`, `Partial/Pick/Omit` |
| 03 | [Abstract & Patterns](typescript/exercises/03_abstract_and_patterns.ts) | `abstract class`, Strategy, Builder, typed Observer | `Logger`, `QueryBuilder`, `TypedEventBus` |

**Solutions:** [all_solutions.ts](typescript/solutions/all_solutions.ts)

---

## CDK (Infrastructure as Code)

Practice writing AWS CDK stack definitions in TypeScript — modeled on a real
Kafka/Glue/Step-Functions ETL pipeline. Each exercise mirrors one stack from
that project so you can confidently answer "how did you write the stack
definition / app.ts?" in an interview.

| # | File | Concepts | Exercise |
|---|------|----------|----------|
| 01 | [Storage Stack](typescript/cdk/exercises/01_storage_stack.ts) | `cdk.Stack`, `StackProps`, `readonly` exports, `s3.Bucket`, `RemovalPolicy`, `CfnOutput` | `StorageStack` (3 buckets, lifecycle rule) |
| 02 | [Glue Stack](typescript/cdk/exercises/02_glue_stack.ts) | L1 constructs (`CfnDatabase`/`CfnJob`/`CfnCrawler`), `iam.Role`, `grantRead`/`grantReadWrite`, cross-stack props | `GlueStack` (catalog DB, ETL job, crawler) |
| 03 | [Orchestration Stack](typescript/cdk/exercises/03_orchestration_stack.ts) | `sfn.Succeed`/`Fail`, `tasks.GlueStartJobRun`, `.addCatch()`, Wait/Choice polling loop, `DefinitionBody.fromChainable` | `OrchestrationStack` (Step Functions state machine) |
| 04 | [App Wiring](typescript/cdk/exercises/04_app_wiring.ts) | `cdk.App`, `cdk.Environment`, cross-stack references (`Fn::ImportValue`), `app.synth()` | bin/app.ts pattern across 3 stacks |

**Solutions:** [all_solutions.ts](typescript/cdk/solutions/all_solutions.ts)

```bash
cd typescript/cdk
npm install   # one-time — installs aws-cdk-lib + constructs
npx tsx exercises/01_storage_stack.ts
```

---

## How to Use

### Python
```bash
# Open in Jupyter / VS Code
jupyter notebook python_oop/exercises/01_classes_and_objects.ipynb

# Or run from terminal
jupyter execute python_oop/exercises/01_classes_and_objects.ipynb
```

### TypeScript
```bash
# Install ts runner (one time)
npm install -g tsx

# Run exercises
npx tsx typescript/exercises/01_interfaces_and_classes.ts
```

---

## Python vs TypeScript OOP — Quick Comparison

| Feature | Python | TypeScript |
|---------|--------|-----------|
| Interface | `ABC` + `@abstractmethod` | `interface` keyword |
| Access control | Convention (`_private`) | `private` / `protected` keywords |
| Generics | Duck typing (no syntax) | `<T>` syntax |
| Operator overloading | Dunder methods (`__add__`) | Not supported |
| Properties | `@property` decorator | `get` / `set` keywords |
| Multiple inheritance | Yes (with MRO) | No (use interfaces) |
| Type checking | Runtime (`isinstance`) | Compile-time (erased at runtime) |
