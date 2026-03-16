# Module 06 — Java for Data Engineers (FAANG Level)

> You don't need to be a Java developer. You need to be fluent enough to read stack traces, tune JVM memory, debug Spark jobs, and write a UDF when Python is too slow.

---

## Table of Contents

1. [What You Actually Need to Know](#1-what-you-actually-need-to-know)
2. [Install Java](#2-install-java)
3. [Compile & Run a Java File](#3-compile--run-a-java-file)
4. [Core Syntax Cheatsheet](#4-core-syntax-cheatsheet)
5. [JVM Fundamentals](#5-jvm-fundamentals)
6. [OOP in Java (vs Python)](#6-oop-in-java-vs-python)
7. [Build Tools — Maven & sbt](#7-build-tools--maven--sbt)
8. [What a Production Java App Looks Like](#8-what-a-production-java-app-looks-like)
9. [Java UDF in PySpark](#9-java-udf-in-pyspark)
10. [Reading Stack Traces](#10-reading-stack-traces)

---

## 1. What You Actually Need to Know

| Area | Why It Matters for DE | Depth Needed |
|------|----------------------|--------------|
| JVM memory (Heap/Stack/GC) | Spark OOM errors, executor tuning | Deep |
| Reading Java/Scala source | Debugging library internals, stack traces | Medium |
| OOP basics | Understanding Spark internals, writing UDFs | Medium |
| Maven / sbt | Building JARs, adding dependencies | Basic |
| Writing Java UDFs | When Python UDFs are 10x slower | Occasional |
| Full Java app development | Not needed | Skip |

---

## 2. Install Java

### macOS (Homebrew)

```bash
# Install Java 17 (LTS — used by Spark 3.x)
brew install openjdk@17

# Add to PATH
echo 'export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify
java -version
# openjdk version "17.x.x"

javac -version
# javac 17.x.x
```

### Check what Spark expects

```bash
# Spark 3.3+ works with Java 8, 11, or 17
# Always match your cluster's Java version locally
spark-submit --version
```

---

## 3. Compile & Run a Java File

### The basics

```bash
# 1. Write source file
nano Hello.java

# 2. Compile → produces Hello.class (bytecode)
javac Hello.java

# 3. Run the bytecode on the JVM
java Hello
```

### Hello.java

```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello, Data Engineer!");
    }
}
```

### Run with classpath (multiple files / JARs)

```bash
# Add external JAR to classpath
javac -cp .:lib/somelib.jar MyApp.java
java -cp .:lib/somelib.jar MyApp

# Run a JAR directly
java -jar myapp.jar
```

### Useful JVM flags (you'll see these in Spark configs)

```bash
java -Xms512m -Xmx4g -jar myapp.jar
#    ^          ^
#    min heap   max heap

java -XX:+PrintGCDetails -jar myapp.jar   # print GC activity
java -XX:+HeapDumpOnOutOfMemoryError      # dump heap on OOM
```

---

## 4. Core Syntax Cheatsheet

### Variables & Types

```java
// Primitives (lowercase) — stored on Stack
int age = 25;
long bigNum = 10_000_000_000L;
double price = 9.99;
boolean active = true;

// Objects (uppercase) — stored on Heap
String name = "Kanishk";
Integer boxed = 42;          // boxed primitive
List<String> cities = new ArrayList<>();
```

### Control Flow

```java
// if/else
if (age > 18) {
    System.out.println("adult");
} else {
    System.out.println("minor");
}

// for loop
for (int i = 0; i < 10; i++) {
    System.out.println(i);
}

// enhanced for (like Python's for x in list)
for (String city : cities) {
    System.out.println(city);
}

// while
while (active) {
    // do something
}
```

### Methods

```java
// returnType methodName(paramType param)
public static int add(int a, int b) {
    return a + b;
}

// void = no return value
public static void printName(String name) {
    System.out.println("Name: " + name);
}
```

### Collections

```java
import java.util.*;

List<String> list = new ArrayList<>(Arrays.asList("a", "b", "c"));
list.add("d");
list.get(0);          // "a"
list.size();          // 4

Map<String, Integer> map = new HashMap<>();
map.put("delhi", 100);
map.get("delhi");     // 100
map.containsKey("delhi");  // true

Set<String> set = new HashSet<>(Arrays.asList("x", "y", "z"));
```

### Lambda & Streams (functional style — common in Spark)

```java
import java.util.stream.*;

List<Integer> nums = Arrays.asList(1, 2, 3, 4, 5);

// filter + map + collect (like Python list comprehension)
List<Integer> result = nums.stream()
    .filter(n -> n > 2)
    .map(n -> n * 2)
    .collect(Collectors.toList());
// [6, 8, 10]

// reduce
int sum = nums.stream().reduce(0, Integer::sum);  // 15
```

---

## 5. JVM Fundamentals

> This is the most important section for a Data Engineer. Spark runs on the JVM — knowing this saves you hours of debugging OOM errors.

### Memory Layout

```
JVM Memory
├── Heap (managed by GC)
│   ├── Young Generation  → new objects live here first
│   │   ├── Eden Space
│   │   └── Survivor Spaces (S0, S1)
│   └── Old Generation    → long-lived objects promoted here
│
├── Stack (per thread)    → method calls, local variables
│   └── Each thread gets its own stack frame
│
├── Metaspace             → class metadata (replaced PermGen in Java 8+)
└── Off-Heap              → Spark uses this for shuffle/cache (Tungsten)
```

### Garbage Collection

```
Minor GC → cleans Young Generation (fast, frequent)
Major GC → cleans Old Generation (slow, causes pauses)
Full GC  → cleans everything (very slow — avoid in Spark)
```

### Spark OOM Cheatsheet

```bash
# Executor OOM — increase executor memory
spark.executor.memory = 8g
spark.executor.memoryOverhead = 2g   # off-heap buffer

# Driver OOM — increase driver memory
spark.driver.memory = 4g

# GC overhead — tune GC
spark.executor.extraJavaOptions = -XX:+UseG1GC -XX:InitiatingHeapOccupancyPercent=35

# Check GC in Spark UI → Executors tab → GC Time column
```

---

## 6. OOP in Java (vs Python)

```java
// Java class
public class DataPipeline {
    // Fields (instance variables)
    private String name;
    private int batchSize;

    // Constructor
    public DataPipeline(String name, int batchSize) {
        this.name = name;
        this.batchSize = batchSize;
    }

    // Method
    public void run() {
        System.out.println("Running " + name + " with batch=" + batchSize);
    }

    // Getter
    public String getName() { return name; }
}

// Usage
DataPipeline pipeline = new DataPipeline("visa-etl", 1000);
pipeline.run();
```

```python
# Equivalent Python
class DataPipeline:
    def __init__(self, name: str, batch_size: int):
        self.name = name
        self.batch_size = batch_size

    def run(self):
        print(f"Running {self.name} with batch={self.batch_size}")
```

### Key differences from Python

| Concept | Python | Java |
|---------|--------|------|
| Types | Dynamic | Static (declared) |
| Access control | Convention (`_private`) | Enforced (`private`/`public`) |
| Null | `None` | `null` (causes NullPointerException) |
| Interfaces | Duck typing / ABC | `interface` keyword |
| Inheritance | `class Child(Parent)` | `class Child extends Parent` |

---

## 7. Build Tools — Maven & sbt

### Maven (Java projects)

```xml
<!-- pom.xml — defines project and dependencies -->
<project>
  <groupId>com.kanishk</groupId>
  <artifactId>visa-etl</artifactId>
  <version>1.0.0</version>

  <dependencies>
    <dependency>
      <groupId>org.apache.spark</groupId>
      <artifactId>spark-core_2.12</artifactId>
      <version>3.4.0</version>
    </dependency>
  </dependencies>
</project>
```

```bash
mvn compile          # compile source
mvn package          # build JAR → target/visa-etl-1.0.0.jar
mvn test             # run tests
mvn dependency:tree  # show all dependencies
```

### sbt (Scala/Spark projects)

```scala
// build.sbt
name := "visa-etl"
version := "1.0.0"
scalaVersion := "2.12.17"

libraryDependencies += "org.apache.spark" %% "spark-core" % "3.4.0"
```

```bash
sbt compile    # compile
sbt package    # build JAR
sbt assembly   # fat JAR (all deps bundled)
```

---

## 8. What a Production Java App Looks Like

### Project structure (Maven)

```
visa-etl/
├── pom.xml                          # build config + dependencies
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/kanishk/
│   │   │       ├── Main.java        # entry point
│   │   │       ├── pipeline/
│   │   │       │   └── VisaETL.java
│   │   │       └── udf/
│   │   │           └── SlotExtractor.java
│   │   └── resources/
│   │       └── application.properties   # config
│   └── test/
│       └── java/
│           └── com/kanishk/
│               └── VisaETLTest.java
└── target/                          # compiled output (gitignored)
    └── visa-etl-1.0.0.jar
```

### Main.java — entry point

```java
package com.kanishk;

import com.kanishk.pipeline.VisaETL;

public class Main {
    public static void main(String[] args) {
        String inputPath = args[0];
        String outputPath = args[1];

        VisaETL etl = new VisaETL(inputPath, outputPath);
        etl.run();
    }
}
```

### VisaETL.java — business logic

```java
package com.kanishk.pipeline;

import org.apache.spark.sql.*;
import org.apache.spark.sql.functions.*;

public class VisaETL {
    private final String inputPath;
    private final String outputPath;

    public VisaETL(String inputPath, String outputPath) {
        this.inputPath = inputPath;
        this.outputPath = outputPath;
    }

    public void run() {
        SparkSession spark = SparkSession.builder()
            .appName("VisaETL")
            .getOrCreate();

        Dataset<Row> df = spark.read().json(inputPath);

        Dataset<Row> result = df
            .filter(col("city").isNotNull())
            .groupBy("city")
            .count()
            .orderBy(desc("count"));

        result.write().parquet(outputPath);

        spark.stop();
    }
}
```

### Run on a cluster

```bash
spark-submit \
  --class com.kanishk.Main \
  --master yarn \
  --executor-memory 8g \
  --num-executors 10 \
  target/visa-etl-1.0.0.jar \
  s3://bucket/input/ \
  s3://bucket/output/
```

---

## 9. Java UDF in PySpark

Use when a Python UDF is bottlenecked — Java UDFs run natively on the JVM inside Spark executors (no Python serialization overhead).

### Write the UDF in Java

```java
// SlotExtractor.java
package com.kanishk.udf;

import org.apache.spark.sql.api.java.UDF1;

public class SlotExtractor implements UDF1<String, String> {
    @Override
    public String call(String message) {
        // fast string parsing logic
        if (message.contains("slot available")) {
            return message.split("in")[1].trim();
        }
        return null;
    }
}
```

```bash
# Build JAR
mvn package
# → target/visa-etl-1.0.0.jar
```

### Register and use in PySpark

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder \
    .config("spark.jars", "target/visa-etl-1.0.0.jar") \
    .getOrCreate()

# Register Java UDF
spark.udf.registerJavaFunction(
    "extract_slot",
    "com.kanishk.udf.SlotExtractor",
    "string"
)

df.withColumn("slot", expr("extract_slot(message)")).show()
```

---

## 10. Reading Stack Traces

The most common Java skill you'll use day-to-day in Spark.

```
org.apache.spark.SparkException: Job aborted due to stage failure:
  at org.apache.spark.scheduler.DAGScheduler.failJobAndIndependentStages(DAGScheduler.scala:2258)
  ...
Caused by: java.lang.OutOfMemoryError: GC overhead limit exceeded
  at org.apache.spark.sql.execution.UnsafeFixedWidthAggregationMap.getAggregationBufferFromUnsafeRow(...)
```

### How to read it

```
1. Start at the BOTTOM — "Caused by" is the root cause
2. OutOfMemoryError: GC overhead → executor running out of heap
3. The line with your code (com.yourpackage.*) is where to fix
4. Lines with org.apache.spark.* are Spark internals — usually not your bug

Fix: increase spark.executor.memory or reduce partition size
```

### Common exceptions

| Exception | Cause | Fix |
|-----------|-------|-----|
| `OutOfMemoryError: Java heap space` | Executor heap full | Increase `spark.executor.memory` |
| `OutOfMemoryError: GC overhead limit` | GC spending >98% time collecting | Increase memory or repartition |
| `NullPointerException` | Accessing null object | Add null checks, use `Option` in Scala |
| `ClassNotFoundException` | JAR not on classpath | Add to `--jars` in spark-submit |
| `TaskNotSerializableException` | Non-serializable object in closure | Make class `Serializable` or use broadcast |

---

## Quick Reference

```bash
# Install
brew install openjdk@17

# Compile + run
javac Hello.java && java Hello

# Run JAR
java -jar app.jar

# JVM memory flags
-Xms512m          # initial heap
-Xmx4g            # max heap
-XX:+UseG1GC      # use G1 garbage collector

# Spark submit with JAR
spark-submit --class com.pkg.Main --executor-memory 8g app.jar

# Maven build
mvn package       # → target/*.jar
```
