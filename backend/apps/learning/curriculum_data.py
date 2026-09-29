# -*- coding: utf-8 -*-
"""Full Python Masterclass Curriculum: Syllabus, HTML generator, and Django database seeder."""

import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.db import transaction
from apps.learning.models import StudyCategory, Course, Lesson, StudyMaterial, InterviewQuestion, Level

# -----------------------------------------------------------------------------
# 1. CURRICULUM DATA DEFINITIONS
# -----------------------------------------------------------------------------

COURSES_DATA = [
    {
        "title": "Python Core & Fundamentals",
        "slug": "python-core-fundamentals",
        "level": Level.BEGINNER,
        "description": "Master Python from scratch: syntax, variables, operators, input/output, strings, conditionals, and loops with hands-on practice.",
        "order": 1,
        "lessons": [
            {
                "title": "Python Introduction & Setup",
                "slug": "python-intro-setup",
                "summary": "Understand Python features, architecture, interpreter vs compiler, environment setup, indentation, and naming conventions.",
                "estimated_minutes": 25,
                "order": 1,
                "content": """# Module 1 — Python Introduction

Python is a high-level, interpreted, dynamically-typed, garbage-collected programming language created by **Guido van Rossum** in 1991. It emphasizes code readability with its notable use of significant indentation.

---

### 1. Key Features of Python
- **Simple & Readable:** Clean English-like syntax; minimal boilerplate compared to C/C++/Java.
- **Interpreted:** Executes code line-by-line via the CPython virtual machine (PVM).
- **Dynamically Typed:** Variable types are resolved at runtime without explicit type declarations.
- **Cross-Platform:** Runs on Windows, macOS, Linux, and embedded systems.
- **Extensive Standard Library:** "Batteries included" philosophy covering math, networking, JSON, databases, and more.
- **Multi-Paradigm:** Supports Procedural, Object-Oriented, and Functional programming.

---

### 2. Python vs C / C++ / Java
| Feature | Python | C / C++ | Java |
| :--- | :--- | :--- | :--- |
| **Typing** | Dynamic | Static | Static |
| **Execution** | Interpreted (Bytecode -> PVM) | Compiled (Machine binary) | Compiled to Bytecode (JVM) |
| **Syntax** | Minimal, indentation-based | Braces `{}` & semicolons `;` | Verbose, Class-mandatory |
| **Memory** | Automatic Garbage Collection | Manual (`malloc`/`free`) | Automatic Garbage Collection |
| **Speed** | Moderate (optimizable via C-extensions) | Extremely fast | Fast (JIT compiled) |

---

### 3. Execution Model & Architecture
When you run a script `script.py`:
1. **Source Code (`.py`)** is parsed into an Abstract Syntax Tree (AST).
2. The compiler translates the AST into **Bytecode** cached in `__pycache__/*.pyc`.
3. The **Python Virtual Machine (PVM)** executes the bytecode instructions on the underlying CPU/OS.

---

### 4. Syntax Fundamentals: Indentation, Comments & Identifiers

#### Indentation
Python uses whitespace (standard: 4 spaces) rather than curly braces to define scope:
```python
# Valid indentation
if True:
    print("Indented by 4 spaces")
    if 5 > 2:
        print("Nested block")
```

#### Comments
```python
# Single-line comment

\"\"\"
Multi-line docstring / block comment.
Often used for documentation of modules, functions, and classes.
\"\"\"
```

#### Identifiers & Naming Conventions (PEP 8)
- **Variables & Functions:** `snake_case` (e.g., `user_name`, `calculate_total()`)
- **Constants:** `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES`, `PI = 3.14159`)
- **Classes:** `PascalCase` (e.g., `StudentProfile`, `NeuralNetwork`)
- **Private Attributes:** Single leading underscore `_internal_var` or double `__mangled_var`.
"""
            },
            {
                "title": "Python Basics & Variables",
                "slug": "python-basics-variables",
                "summary": "Understand variables, dynamic typing, memory references, id(), type(), and standard type conversions.",
                "estimated_minutes": 25,
                "order": 2,
                "content": """# Module 2 — Python Basics & Variables

In Python, variables are **labels (references)** pointing to objects in memory, not fixed memory buckets.

---

### 1. Variables & Dynamic Typing
You don't declare types; Python deduces the type from the assigned value:
```python
name = "Naveen"          # str
age = 25                 # int
salary = 25000.50        # float
active = True            # bool
data = None              # NoneType

# Dynamic reassignment
x = 100
print(type(x))           # <class 'int'>
x = "Hello"
print(type(x))           # <class 'str'>
```

### 2. Multiple Assignment & Constants
```python
# Multiple assignment in one line
a, b, c = 10, 20, 30

# Same value to multiple variables
x = y = z = 0

# Python constants (convention by PEP 8)
DATABASE_PORT = 5432
MAX_CONNECTIONS = 100
```

### 3. Inspecting Memory: `id()` and `type()`
Every object has an identity (memory address integer returned by `id()`) and a type (`type()`):
```python
a = 256
b = 256
print(id(a) == id(b))  # True (small integer caching in CPython [-5 to 256])

x = [1, 2, 3]
y = [1, 2, 3]
print(x == y)          # True (same values)
print(x is y)          # False (distinct objects in memory)
```

### 4. Type Conversion (Type Casting)
```python
# Explicit casting
s_num = "123"
i_num = int(s_num)     # 123
f_num = float(i_num)   # 123.0
b_val = bool(1)        # True
c_val = complex(5, 2)  # (5+2j)

# Type errors to watch out for:
# int("abc") -> ValueError: invalid literal for int()
```
"""
            },
            {
                "title": "Operators & Expressions",
                "slug": "operators-expressions",
                "summary": "Arithmetic, comparison, logical, assignment, bitwise, membership, identity operators, and operator precedence.",
                "estimated_minutes": 30,
                "order": 3,
                "content": """# Module 3 — Operators & Expressions

Python provides an expressive set of operators to manipulate values and variables.

---

### 1. Operator Categories

#### Arithmetic Operators
```python
a, b = 15, 4

print(a + b)   # 19 (Addition)
print(a - b)   # 11 (Subtraction)
print(a * b)   # 60 (Multiplication)
print(a / b)   # 3.75 (Float division)
print(a // b)  # 3 (Floor / Integer division)
print(a % b)   # 3 (Modulus / Remainder)
print(a ** b)  # 50625 (Exponentiation 15^4)
```

#### Comparison (Relational) Operators
Always evaluate to a boolean (`True` or `False`):
```python
x, y = 10, 20
print(x == y)  # False
print(x != y)  # True
print(x > y)   # False
print(x < y)   # True
print(x >= 10) # True
print(x <= 20) # True
```

#### Logical Operators (`and`, `or`, `not`)
Short-circuit evaluation:
```python
age = 22
has_id = True

# and: True only if both conditions are True
can_enter = (age >= 18) and has_id

# or: True if at least one condition is True
discount = (age < 18) or (age > 60)

# not: inverts boolean value
is_busy = False
print(not is_busy)  # True
```

#### Membership (`in`, `not in`) & Identity (`is`, `is not`)
```python
languages = ["Python", "SQL", "JavaScript"]

# Membership
print("Python" in languages)      # True
print("Java" not in languages)    # True

# Identity (compares memory location id())
x = [1, 2]
y = [1, 2]
z = x
print(x is z)      # True (same reference)
print(x is y)      # False (distinct objects)
print(x == y)      # True (identical content)
```

#### Bitwise Operators
```python
x, y = 5, 3  # 5 = 0b0101, 3 = 0b0011
print(x & y)   # 1 (0b0001 AND)
print(x | y)   # 7 (0b0111 OR)
print(x ^ y)   # 6 (0b0110 XOR)
print(~x)      # -6 (NOT / Two's complement)
print(x << 1)  # 10 (Left shift: multiply by 2)
print(x >> 1)  # 2 (Right shift: integer divide by 2)
```

---

### 2. Operator Precedence (PEMDAS / BODMAS)
1. `()` Parentheses
2. `**` Exponentiation
3. `+x`, `-x`, `~x` Unary plus, minus, bitwise NOT
4. `*`, `/`, `//`, `%` Multiplication, division, floor division, modulo
5. `+`, `-` Addition, subtraction
6. `<<`, `>>` Bitwise shifts
7. `&` Bitwise AND
8. `^` Bitwise XOR
9. `|` Bitwise OR
10. `==`, `!=`, `<`, `<=`, `>`, `>=`, `is`, `is not`, `in`, `not in` Comparisons & Identity
11. `not` Logical NOT
12. `and` Logical AND
13. `or` Logical OR
"""
            },
            {
                "title": "Input, Output & String Formatting",
                "slug": "input-output-formatting",
                "summary": "Master print(), input(), escape characters, sep, end, f-strings, and .format().",
                "estimated_minutes": 20,
                "order": 4,
                "content": """# Module 4 — Input, Output & String Formatting

Handling user interaction and presenting formatted data cleanly.

---

### 1. `print()` Parameters: `sep` and `end`
```python
# Default sep=' ', end='\\n'
print("Python", "Data Science", "AI")
# Output: Python Data Science AI

# Custom separator
print("2026", "09", "25", sep="-")
# Output: 2026-09-25

# Custom ending (prevent newline or add punctuation)
print("Loading", end="...")
print("Done!")
# Output: Loading...Done!
```

---

### 2. Reading Input with `input()`
The `input()` function **always** returns a string (`str`). Cast explicitly when reading numbers:
```python
name = input("Enter your name: ")
age = int(input("Enter your age: "))
score = float(input("Enter your test score: "))

print(f"Candidate {name} (Age: {age}) scored {score:.1f}%")
```

---

### 3. String Formatting Approaches

#### A. Modern f-strings (Python 3.6+ Recommended)
Fastest, cleanest, and most readable:
```python
name = "Naveen"
salary = 75250.758

print(f"Developer: {name}")
print(f"Monthly Salary: ${salary:,.2f}")  # Comma grouped with 2 decimals ($75,250.76)
print(f"Next Year Age: {25 + 1}")        # Expressions directly inside { }

# Alignment and padding
print(f"{name:>15}")  # Right-aligned width 15
print(f"{name:<15}")  # Left-aligned width 15
print(f"{name:^15}")  # Centered width 15
```

#### B. The `.format()` Method
```python
template = "Hello {name}, you have {count} unread notifications."
print(template.format(name="Naveen", count=3))
```
"""
            },
            {
                "title": "Strings & In-Depth Operations",
                "slug": "strings-in-depth",
                "summary": "String indexing, slicing, immutability, built-in methods, searching, validation, and regular string techniques.",
                "estimated_minutes": 35,
                "order": 5,
                "content": """# Module 5 — Strings & In-Depth Operations

Strings in Python are **immutable sequences of Unicode characters**.

---

### 1. String Indexing & Slicing
```
 Index:   0   1   2   3   4   5
 Char:    P   Y   T   H   O   N
-Index:  -6  -5  -4  -3  -2  -1
```

```python
s = "PYTHON"

# Positive & Negative Indexing
print(s[0])    # 'P'
print(s[-1])   # 'N'

# Slicing: s[start:stop:step]
print(s[0:4])   # 'PYTH' (stop is exclusive)
print(s[:3])    # 'PYT' (starts from 0)
print(s[2:])    # 'THON' (runs to end)
print(s[::2])   # 'PTO' (step 2)
print(s[::-1])  # 'NOHTYP' (reverse string!)
```

---

### 2. String Immutability
You cannot alter individual characters in place:
```python
text = "Python"
# text[0] = 'J'  -> TypeError: 'str' object does not support item assignment

# Correct approach: construct a new string
new_text = "J" + text[1:]  # 'Jython'
```

---

### 3. Essential String Methods
```python
msg = "  Machine Learning with Python  "

# Case transformations
print(msg.upper())       # "  MACHINE LEARNING WITH PYTHON  "
print(msg.lower())       # "  machine learning with python  "
print(msg.title())       # "  Machine Learning With Python  "
print(msg.swapcase())    # "  mACHINE lEARNING WITH pYTHON  "

# Trimming whitespace
clean = msg.strip()      # "Machine Learning with Python"
print(msg.lstrip())      # Removes left spaces
print(msg.rstrip())      # Removes right spaces

# Search & Replace
print(clean.replace("Machine", "Deep"))  # "Deep Learning with Python"
print(clean.find("with"))               # 17 (index of match, -1 if not found)
print(clean.count("i"))                 # 3

# Splitting and Joining
tokens = clean.split(" ")               # ['Machine', 'Learning', 'with', 'Python']
rejoined = "-".join(tokens)             # 'Machine-Learning-with-Python'

# Checking Prefix & Suffix
print(clean.startswith("Machine"))      # True
print(clean.endswith("Python"))         # True
```

---

### 4. Validation Methods
```python
print("12345".isdigit())      # True
print("Alpha".isalpha())      # True
print("Alpha123".isalnum())   # True
print("   ".isspace())        # True
print("python".islower())     # True
print("PYTHON".isupper())     # True
```
"""
            },
            {
                "title": "Conditional Statements & Decision Making",
                "slug": "conditional-statements",
                "summary": "if, if-else, if-elif-else, nested conditionals, and ternary conditional expressions.",
                "estimated_minutes": 25,
                "order": 6,
                "content": """# Module 6 — Conditional Statements

Conditional statements let your code make decisions based on runtime conditions.

---

### 1. `if`, `if-else`, and `if-elif-else`
```python
score = 85

if score >= 90:
    grade = "A+"
elif score >= 80:
    grade = "A"
elif score >= 70:
    grade = "B"
elif score >= 60:
    grade = "C"
else:
    grade = "F"

print(f"Final Grade: {grade}")
```

---

### 2. Nested Conditionals
```python
age = 20
has_license = True

if age >= 18:
    if has_license:
        print("Eligible to drive.")
    else:
        print("Must obtain a driving license first.")
else:
    print("Underage; cannot drive.")
```

---

### 3. Ternary Operator (Conditional Expression)
Syntax: `[value_if_true] if [condition] else [value_if_false]`
```python
mark = 72
status = "Pass" if mark >= 40 else "Fail"

# Nested ternary (use sparingly for readability)
age = 15
category = "Child" if age < 13 else ("Teenager" if age < 20 else "Adult")
```
"""
            },
            {
                "title": "Loops, Controls & Pattern Programs",
                "slug": "loops-control-patterns",
                "summary": "for and while loops, range(), break, continue, pass, loop else, infinite loops, and pattern printing.",
                "estimated_minutes": 35,
                "order": 7,
                "content": """# Module 7 — Loops & Iterations

Loops repeat a block of code until a condition is satisfied or an iterable is exhausted.

---

### 1. `for` Loop and `range()`
```python
# range(start, stop, step)
for i in range(1, 6):
    print(i, end=" ")
# Output: 1 2 3 4 5

# Stepping in reverse
for i in range(10, 0, -2):
    print(i, end=" ")
# Output: 10 8 6 4 2
```

---

### 2. `while` Loop
```python
count = 3
while count > 0:
    print(f"Countdown: {count}")
    count -= 1
print("Blast off!")
```

---

### 3. Loop Control Statements: `break`, `continue`, `pass`
- `break`: Terminates the innermost loop immediately.
- `continue`: Skips the remainder of the current iteration and jumps to the next.
- `pass`: A placeholder statement that performs no operation.

```python
# Example of break and continue
for n in range(1, 10):
    if n % 2 == 0:
        continue  # skip even numbers
    if n == 7:
        break     # stop loop when 7 is reached
    print(n, end=" ")
# Output: 1 3 5
```

---

### 4. `else` Clause on Loops
The `else` block runs **only if the loop finishes naturally** without encountering a `break`:
```python
def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            print(f"{num} is divisible by {i}")
            break
    else:
        print(f"{num} is a Prime Number!")

is_prime(29)  # 29 is a Prime Number!
```

---

### 5. Classic Pattern Programs

#### Right-Angled Triangle Pattern
```python
n = 5
for i in range(1, n + 1):
    print("*" * i)
\"\"\"
*
**
***
****
*****
\"\"\"
```

#### Number Pyramid Pattern
```python
n = 4
for i in range(1, n + 1):
    print(" " * (n - i) + " ".join(str(i) for _ in range(i)))
\"\"\"
   1
  2 2
 3 3 3
4 4 4 4
\"\"\"
```
"""
            }
        ]
    },
    {
        "title": "Python Data Types & Data Structures Masterclass",
        "slug": "python-data-types-masterclass",
        "level": Level.INTERMEDIATE,
        "description": "Comprehensive, deep dive into Python's built-in data types: mutability, collections, hashing, comprehensions, and data science foundations.",
        "order": 2,
        "lessons": [
            {
                "title": "Introduction to Python Data Types & Memory",
                "slug": "intro-data-types-memory",
                "summary": "Dynamic vs static typing, strong typing, id(), type(), isinstance(), and memory classification.",
                "estimated_minutes": 25,
                "order": 1,
                "content": """# Module 8 — Data Types Architecture & Memory

Every value in Python is an object stored in heap memory. Variables are reference pointers pointing to these objects.

---

### 1. Classification of Built-in Data Types
- **Numeric:** `int`, `float`, `complex`
- **Sequence:** `str`, `list`, `tuple`, `range`, `bytes`, `bytearray`
- **Set Types:** `set`, `frozenset`
- **Mapping:** `dict`
- **Boolean:** `bool`
- **NoneType:** `None`

---

### 2. Type Checking: `type()` vs `isinstance()`
Always prefer `isinstance()` in production code because it respects inheritance:
```python
class Animal: pass
class Dog(Animal): pass

d = Dog()
print(type(d) == Animal)        # False (exact match required)
print(isinstance(d, Animal))    # True (supports polymorphism)

# Checking multiple allowed types
x = 10.5
print(isinstance(x, (int, float)))  # True
```

---

### 3. Summary Comparison Table
| Data Type | Ordered? | Mutable? | Allows Duplicates? | Syntax Example |
| :--- | :--- | :--- | :--- | :--- |
| **`int` / `float`** | N/A | No (Immutable) | N/A | `10`, `3.14` |
| **`str`** | Yes | No (Immutable) | Yes | `"hello"` |
| **`list`** | Yes | Yes (Mutable) | Yes | `[1, 2, 2]` |
| **`tuple`** | Yes | No (Immutable) | Yes | `(1, 2, 2)` |
| **`set`** | No | Yes (Mutable) | No (Unique) | `{1, 2, 3}` |
| **`dict`** | Yes (Insertion order) | Yes (Mutable) | Keys: No; Values: Yes | `{"a": 1}` |
"""
            },
            {
                "title": "Numeric, Boolean & None Types",
                "slug": "numeric-boolean-none",
                "summary": "Deep dive into int, float, complex, boolean truthy/falsy evaluation, and the None singleton.",
                "estimated_minutes": 30,
                "order": 2,
                "content": """# Module 9 — Numeric, Boolean & None Types

---

### 1. Numeric Types: `int`, `float`, `complex`

#### Integers (`int`)
In Python 3, integers have **arbitrary precision** (limited only by available system RAM):
```python
huge = 10 ** 100  # A googol! No overflow error.

# Radix conversions
val = 42
print(bin(val))  # '0b101010'
print(oct(val))  # '0o52'
print(hex(val))  # '0x2a'
```

#### Floats (`float`)
Implemented as IEEE 754 64-bit double precision floats:
```python
price = 99.99
exp = 1.5e-3  # Scientific notation: 0.0015
print(round(2.675, 2))
```

#### Complex Numbers (`complex`)
```python
z = 3 + 4j
print(z.real)       # 3.0
print(z.imag)       # 4.0
print(abs(z))       # 5.0 (Magnitude: sqrt(3^2 + 4^2))
print(z.conjugate())# (3-4j)
```

---

### 2. Boolean (`bool`) & Truthiness
In Python, `bool` is a subclass of `int` (`True == 1`, `False == 0`).

#### Truthy vs Falsy Values
Every object evaluates to a boolean in conditional contexts. **Falsy values:**
- Constants: `None`, `False`
- Numeric zeros: `0`, `0.0`, `0j`
- Empty sequences and collections: `""`, `()`, `[]`, `{}`, `set()`, `range(0)`

```python
def check_data(items):
    if not items:
        print("Collection is empty!")
    else:
        print(f"Found {len(items)} elements.")

check_data([])  # Falsy
```

---

### 3. The `None` Singleton
`None` denotes the absence of a value. Always compare using the identity operator `is None`:
```python
val = None

if val is None:
    print("Value not set")

# Avoid: if val == None (can be overridden by __eq__)
```
"""
            },
            {
                "title": "Lists in Depth (CRUD, Methods, Unpacking)",
                "slug": "lists-in-depth",
                "summary": "List creation, indexing, slicing, methods, list comprehension, unpacking, and multi-dimensional matrices.",
                "estimated_minutes": 35,
                "order": 3,
                "content": """# Module 10 — List Data Type

Lists are **mutable, ordered sequences** that can hold heterogeneous items.

---

### 1. Creating and Modifying Lists
```python
nums = [10, 20, 30, 40]

# Insertion
nums.append(50)        # Adds to the end: [10, 20, 30, 40, 50]
nums.insert(1, 15)     # Insert at index 1: [10, 15, 20, 30, 40, 50]
nums.extend([60, 70])  # Appends multiple elements

# Deletion
nums.remove(20)        # Removes first occurrence of value 20
popped = nums.pop()    # Removes and returns last element (70)
del nums[0]            # Removes element at index 0
# nums.clear()         # Empties the list
```

---

### 2. List Slicing & Striding
```python
items = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print(items[2:6])    # [2, 3, 4, 5]
print(items[:4])     # [0, 1, 2, 3]
print(items[6:])     # [6, 7, 8, 9]
print(items[::2])    # [0, 2, 4, 6, 8]
print(items[::-1])   # Reversed list
```

---

### 3. List Sorting: `sort()` vs `sorted()`
- `list.sort()` sorts the list **in-place** and returns `None`.
- `sorted(iterable)` returns a **new sorted list**, leaving the original untouched.
```python
scores = [88, 42, 95, 71]
sorted_scores = sorted(scores, reverse=True)
print(scores)         # [88, 42, 95, 71] (unchanged)
print(sorted_scores)  # [95, 88, 71, 42]

scores.sort()
print(scores)         # [42, 71, 88, 95] (modified in-place)
```

---

### 4. Advanced Unpacking (`*` operator)
```python
first, *middle, last = [10, 20, 30, 40, 50]
print(first)   # 10
print(middle)  # [20, 30, 40]
print(last)    # 50
```

---

### 5. List Comprehension
```python
# Standard comprehension
squares = [x**2 for x in range(1, 6)]  # [1, 4, 9, 16, 25]

# With condition
evens = [x for x in range(10) if x % 2 == 0]

# Nested comprehension (flattening a 2D matrix)
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [num for row in matrix for num in row]
print(flat)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
```
"""
            },
            {
                "title": "Tuples (Packing, Unpacking & Immutability)",
                "slug": "tuples-packing-unpacking",
                "summary": "Tuple characteristics, single-element tuples, immutability, packing/unpacking, and use cases.",
                "estimated_minutes": 25,
                "order": 4,
                "content": """# Module 11 — Tuple Data Type

Tuples are **immutable, ordered sequences**. Once created, their elements cannot be changed, added, or removed.

---

### 1. Creating Tuples & The Comma Rule
```python
# A single-element tuple REQUIRES a trailing comma!
not_a_tuple = ("Naveen")  # type: str
is_a_tuple = ("Naveen",)  # type: tuple

coords = (12.9716, 77.5946)
empty = ()
```

---

### 2. Why Use Tuples Over Lists?
1. **Data Integrity:** Protects constants and fixed records from unintentional mutation.
2. **Performance:** Slight memory and allocation speed optimization over lists.
3. **Dictionary Keys:** Because tuples are immutable (provided their elements are also immutable), they are **hashable** and can serve as dictionary keys or set members.

```python
location_cache = {
    (12.97, 77.59): "Bengaluru",
    (11.01, 76.95): "Coimbatore"
}
```

---

### 3. Tuple Packing and Unpacking
```python
# Packing
student = "Naveen", 25, "AI Engineer"

# Unpacking
name, age, role = student
print(f"{name} is {age} years old working as {role}.")

# Swapping variables using tuple packing/unpacking
x, y = 10, 20
x, y = y, x  # Clean variable swap without temporary variable
```
"""
            },
            {
                "title": "Sets & Mathematical Set Operations",
                "slug": "sets-mathematical-operations",
                "summary": "Set characteristics, hashing requirement, deduplication, union, intersection, difference, and symmetric difference.",
                "estimated_minutes": 25,
                "order": 5,
                "content": """# Module 12 — Set Data Type

A `set` is an **unordered, mutable collection of unique, hashable objects**.

---

### 1. Creating Sets
```python
# Notice: {} creates an empty dict; use set() for empty set!
empty_set = set()

# Deduplication from list
raw_tags = ["python", "ai", "python", "ml", "ai"]
unique_tags = set(raw_tags)
print(unique_tags)  # {'python', 'ai', 'ml'}
```

---

### 2. Adding & Removing Elements
```python
s = {10, 20, 30}
s.add(40)
s.update([50, 60])

# Discard vs Remove:
s.remove(20)   # Removes 20; raises KeyError if not found
s.discard(99)  # Removes 99 if present; does NOT raise error if missing
```

---

### 3. Mathematical Set Operations
```python
A = {1, 2, 3, 4}
B = {3, 4, 5, 6}

# Union (all items from both)
print(A | B)                    # {1, 2, 3, 4, 5, 6}
print(A.union(B))

# Intersection (common elements)
print(A & B)                    # {3, 4}
print(A.intersection(B))

# Difference (items in A but not in B)
print(A - B)                    # {1, 2}
print(A.difference(B))

# Symmetric Difference (items in A or B, but not both)
print(A ^ B)                    # {1, 2, 5, 6}
print(A.symmetric_difference(B))
```

---

### 4. Relationship Tests
```python
small = {1, 2}
big = {1, 2, 3, 4}

print(small.issubset(big))      # True
print(big.issuperset(small))    # True
print(small.isdisjoint({5, 6})) # True (no common elements)
```
"""
            },
            {
                "title": "Dictionaries (Key-Value Mastery)",
                "slug": "dictionaries-mastery",
                "summary": "Hash map implementation, keys/values/items, safe retrieval with get(), default dicts, and comprehensions.",
                "estimated_minutes": 35,
                "order": 6,
                "content": """# Module 13 — Dictionary Data Type

Dictionaries represent **hash maps / key-value mappings**. In Python 3.7+, dictionaries preserve key insertion order.

---

### 1. Dictionary Creation & Access
```python
student = {
    "name": "Naveen",
    "role": "AI Engineer",
    "skills": ["Python", "PyTorch", "Django"],
    "experience_years": 3
}

# Accessing
print(student["name"])          # "Naveen"
# student["salary"]             # KeyError!

# Safe access with .get()
salary = student.get("salary", 0.0)  # Returns default 0.0 without throwing error
```

---

### 2. Modifying & Removing Entries
```python
student["location"] = "Coimbatore"     # Add or update
student.update({"level": "Senior", "active": True})

# Removal
popped_val = student.pop("level")       # Removes 'level' and returns value
del student["active"]                   # Deletes 'active'
# student.clear()                       # Empties the dictionary
```

---

### 3. Iterating Over Dictionaries
```python
# Iterating keys
for key in student:
    print(key)

# Iterating values
for val in student.values():
    print(val)

# Iterating key-value pairs (preferred)
for key, val in student.items():
    print(f"{key}: {val}")
```

---

### 4. Dictionary Comprehension
```python
# Inverting a dictionary
original = {"a": 1, "b": 2, "c": 3}
inverted = {val: key for key, val in original.items()}
print(inverted)  # {1: 'a', 2: 'b', 3: 'c'}

# Filtering items
scores = {"Alice": 85, "Bob": 35, "Charlie": 90, "David": 55}
passed_students = {k: v for k, v in scores.items() if v >= 50}
```
"""
            },
            {
                "title": "Binary Types, Range & Memoryview",
                "slug": "binary-types-range",
                "summary": "bytes, bytearray, memoryview buffer protocol, and the range sequence generator.",
                "estimated_minutes": 25,
                "order": 7,
                "content": """# Module 14 — Binary Types & Range

Low-level memory and buffer manipulation types essential for file I/O, networking, and data processing.

---

### 1. `bytes` vs `bytearray`
- `bytes`: **Immutable** sequence of raw bytes (integers in range 0-255).
- `bytearray`: **Mutable** sequence of bytes.

```python
# Creating bytes
b1 = b"Hello Python"
print(type(b1))        # <class 'bytes'>
print(b1[0])           # 72 (ASCII for 'H')

# Creating mutable bytearray
ba = bytearray(b"Hello")
ba[0] = ord("J")       # Replaces 'H' with 'J'
print(ba.decode())     # "Jello"
```

---

### 2. `memoryview`
A `memoryview` allows Python code to access the internal data of an object that supports the buffer protocol without copying memory.
```python
data = bytearray(b"ImageDataBuffer")
mv = memoryview(data)

# Slice without copying the underlying buffer!
sub_view = mv[5:9]
print(sub_view.tobytes())  # b'Data'
```

---

### 3. `range` Object
`range` is a memory-efficient sequence type representing arithmetic progressions:
```python
# range takes O(1) memory regardless of size!
r = range(1, 1000000, 2)
print(r[10])       # Direct indexing supported: 21
print(len(r))      # 500000
```
"""
            },
            {
                "title": "Mutable vs Immutable & Memory References",
                "slug": "mutable-vs-immutable-memory",
                "summary": "Understand object identity, aliasing, shallow vs deep copying, and why hashability matters.",
                "estimated_minutes": 30,
                "order": 8,
                "content": """# Module 15 — Mutability, Copying & Hashing

Understanding how Python handles object references in memory is critical to preventing subtle bugs.

---

### 1. Mutability Overview
- **Immutable:** `int`, `float`, `complex`, `bool`, `str`, `tuple`, `frozenset`, `bytes`. Modifying results in a new object.
- **Mutable:** `list`, `dict`, `set`, `bytearray`. Can be modified in-place without changing memory address (`id()`).

```python
# Aliasing: both variables reference the SAME memory address
a = [1, 2, 3]
b = a
b.append(4)
print(a)  # [1, 2, 3, 4]! (a is affected because a and b point to same list)
```

---

### 2. Shallow Copy vs Deep Copy
```python
import copy

nested = [[1, 2], [3, 4]]

# Shallow copy: outer list copied, inner objects shared
shallow = copy.copy(nested)
# Deep copy: recursive duplicate of all nested objects
deep = copy.deepcopy(nested)

nested[0][0] = 999
print(shallow[0][0])  # 999 (affected!)
print(deep[0][0])     # 1 (isolated and unaffected!)
```

---

### 3. Hashability & Dictionary Keys
An object is **hashable** if it has a hash value (`__hash__()`) that never changes during its lifetime and can be compared to other objects (`__eq__()`).
- Immutable types (`int`, `str`, `tuple` containing immutable items) are hashable.
- Mutable types (`list`, `dict`, `set`) are **unhashable** (`TypeError: unhashable type: 'list'`).
- Only hashable objects can be stored as dictionary keys or set elements!
"""
            }
        ]
    },
    {
        "title": "Functions, OOP & Advanced Python",
        "slug": "functions-oop-advanced-python",
        "level": Level.ADVANCED,
        "description": "Functional programming, recursive techniques, file handling, exception safety, OOP 4 pillars, iterators, generators, decorators, and regex.",
        "order": 3,
        "lessons": [
            {
                "title": "Functions, Scopes, *args & **kwargs",
                "slug": "functions-scopes-args-kwargs",
                "summary": "Defining functions, default arguments, variable length arguments (*args, **kwargs), closures, and lambda expressions.",
                "estimated_minutes": 35,
                "order": 1,
                "content": """# Module 16 — Functions & Parameter Handling

Functions are first-class citizens in Python: they can be assigned to variables, passed as arguments, and returned from other functions.

---

### 1. Function Syntax & Defaults
```python
def greet(name: str, greeting: str = "Hello") -> str:
    \"\"\"Return a personalized greeting.\"\"\"
    return f"{greeting}, {name}!"

print(greet("Naveen"))
print(greet("Naveen", greeting="Good Morning"))
```

> **Warning: Avoid Mutable Default Arguments!**
> ```python
> # BUGGY:
> def append_item(val, target=[]):
>     target.append(val)
>     return target
>
> # CORRECT:
> def append_item(val, target=None):
>     if target is None:
>         target = []
>     target.append(val)
>     return target
> ```

---

### 2. `*args` and `**kwargs`
- `*args`: Collects extra positional arguments into a **tuple**.
- `**kwargs`: Collects extra keyword arguments into a **dictionary**.

```python
def make_api_request(endpoint, *flags, **headers):
    print(f"Calling: {endpoint}")
    print(f"Flags (tuple): {flags}")
    print(f"Headers (dict): {headers}")

make_api_request("/users", "v2", "secure", timeout=30, auth="Bearer token123")
```

---

### 3. Lambda (Anonymous) Functions
Short one-line expressions:
```python
square = lambda x: x * x
print(square(5))  # 25

# Frequently used in sorting:
students = [("Alice", 88), ("Bob", 95), ("Charlie", 72)]
students.sort(key=lambda item: item[1], reverse=True)
```
"""
            },
            {
                "title": "Recursion & Recursive Algorithms",
                "slug": "recursion-algorithms",
                "summary": "Recursive call stack, base conditions, factorial, fibonacci, and string reversal.",
                "estimated_minutes": 25,
                "order": 2,
                "content": """# Module 17 — Recursion & Stack Anatomy

A recursive function calls itself to solve a smaller sub-instance of the same problem.

---

### 1. The Two Rules of Recursion
1. **Base Case:** The terminating condition that returns a value without further recursion.
2. **Recursive Step:** Moves the problem state closer to the base case.

---

### 2. Classic Examples

#### Factorial Calculation: $n! = n \times (n-1)!$
```python
def factorial(n: int) -> int:
    if n <= 1:
        return 1  # Base case
    return n * factorial(n - 1)  # Recursive case

print(factorial(5))  # 120
```

#### Fibonacci with Memoization
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

print([fib(i) for i in range(10)])  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```
"""
            },
            {
                "title": "Modules, Packages & Imports",
                "slug": "modules-packages-imports",
                "summary": "Module creation, __name__ == '__main__', packages with __init__.py, and standard library modules.",
                "estimated_minutes": 25,
                "order": 3,
                "content": """# Module 18 — Modules & Packages

---

### 1. Modules & `if __name__ == '__main__':`
A module is simply a Python file (`.py`).
When a script is run directly, its `__name__` is set to `"__main__"`. When imported, `__name__` equals the module's file name.

```python
# math_utils.py
def add(a, b):
    return a + b

if __name__ == "__main__":
    print("Self-test: add(2, 3) =", add(2, 3))
```

---

### 2. Important Standard Library Modules
- `os` / `pathlib`: Operating system interactions and file paths.
- `sys`: Interpreter arguments and runtime configuration.
- `json`: Parsing and serializing JSON data.
- `math` / `statistics`: Mathematical constants and statistical functions.
- `random`: Pseudo-random number generation.
- `collections`: `defaultdict`, `Counter`, `namedtuple`, `deque`.
```python
from collections import Counter

words = ["apple", "banana", "apple", "orange", "apple"]
counts = Counter(words)
print(counts["apple"])  # 3
```
"""
            },
            {
                "title": "File Handling & Context Managers",
                "slug": "file-handling-context-managers",
                "summary": "Reading, writing, appending files, binary files, and the with statement (context managers).",
                "estimated_minutes": 30,
                "order": 4,
                "content": """# Module 19 — File Handling & Context Managers

Always use the `with` statement: it guarantees that files are properly closed even if exceptions occur.

---

### 1. File Modes
- `'r'`: Read (default). Raises `FileNotFoundError` if missing.
- `'w'`: Write (truncates existing content or creates new file).
- `'a'`: Append (writes to end of file).
- `'x'`: Exclusive creation (fails if file already exists).
- `'rb'` / `'wb'`: Binary read / write (for images, audio, pickle).

---

### 2. Reading & Writing Text Files
```python
# Writing
with open("sample.txt", "w", encoding="utf-8") as f:
    f.write("Line 1: Python Data Science\\n")
    f.writelines(["Line 2: Machine Learning\\n", "Line 3: Artificial Intelligence\\n"])

# Reading line-by-line (memory-efficient for large files)
with open("sample.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
```
"""
            },
            {
                "title": "Exception Handling (Robust Code)",
                "slug": "exception-handling-robust",
                "summary": "try, except, else, finally blocks, raising exceptions, and building custom exception classes.",
                "estimated_minutes": 25,
                "order": 5,
                "content": """# Module 20 — Exception Handling

Gracefully recover from runtime errors without crashing your application.

---

### 1. Complete `try-except-else-finally` Anatomy
```python
try:
    num = int("42")
    result = 100 / num
except ValueError as e:
    print(f"Invalid integer: {e}")
except ZeroDivisionError:
    print("Cannot divide by zero!")
except Exception as e:
    print(f"Unexpected error: {e}")
else:
    # Executes ONLY if NO exception was raised in try
    print(f"Calculation succeeded: {result}")
finally:
    # ALWAYS executes (cleanup operations, closing DB connections)
    print("Execution completed.")
```

---

### 2. Custom Exceptions
Inherit from `Exception`:
```python
class InsufficientFundsError(Exception):
    \"\"\"Raised when a withdrawal amount exceeds account balance.\"\"\"
    def __init__(self, balance, amount):
        super().__init__(f"Attempted to withdraw ${amount} with balance ${balance}.")
        self.balance = balance
        self.amount = amount

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError(balance, amount)
    return balance - amount
```
"""
            },
            {
                "title": "Object-Oriented Programming (The 4 Pillars)",
                "slug": "oop-four-pillars",
                "summary": "Classes, objects, constructors, __init__, self, Encapsulation, Inheritance, Polymorphism, Abstraction, and super().",
                "estimated_minutes": 40,
                "order": 6,
                "content": """# Module 21 — Object-Oriented Programming (OOP)

OOP organizes code around **data (attributes)** and **behaviors (methods)**.

---

### 1. Class & Instance Definition
```python
class Developer:
    # Class variable (shared across all instances)
    community = "Antigravity Devs"

    def __init__(self, name: str, primary_language: str):
        # Instance variables (unique to each object)
        self.name = name
        self.primary_language = primary_language

    def describe(self) -> str:
        return f"{self.name} builds with {self.primary_language} ({self.community})"

dev1 = Developer("Naveen", "Python")
print(dev1.describe())
```

---

### 2. The Four Pillars of OOP

#### A. Encapsulation
Protect internal state using private variables and public getters/setters:
```python
class BankAccount:
    def __init__(self, balance: float):
        self.__balance = balance  # Private attribute (name mangling)

    @property
    def balance(self) -> float:
        return self.__balance

    def deposit(self, amount: float):
        if amount > 0:
            self.__balance += amount
```

#### B. Inheritance
Code reuse across parent and child classes:
```python
class Employee:
    def __init__(self, name: str, salary: float):
        self.name = name
        self.salary = salary

class DataScientist(Employee):
    def __init__(self, name: str, salary: float, model_stack: list):
        super().__init__(name, salary)  # Delegate to parent constructor
        self.model_stack = model_stack
```

#### C. Polymorphism
Different classes implementing the same method interface:
```python
class Square:
    def area(self): return 16

class Circle:
    def area(self): return 3.14 * 16

for shape in [Square(), Circle()]:
    print(shape.area())
```

#### D. Abstraction
Hiding complex implementation details using Abstract Base Classes (`abc` module):
```python
from abc import ABC, abstractmethod

class MLModel(ABC):
    @abstractmethod
    def fit(self, X, y):
        pass

    @abstractmethod
    def predict(self, X):
        pass
```
"""
            },
            {
                "title": "Advanced OOP: Dunder Methods & Decorators",
                "slug": "advanced-oop-dunder-methods",
                "summary": "Magic methods (__str__, __repr__, __len__, __getitem__), @staticmethod, @classmethod, and @property.",
                "estimated_minutes": 30,
                "order": 7,
                "content": """# Module 22 — Advanced OOP & Dunder Methods

Special "dunder" (double underscore) methods allow user-defined classes to hook into Python's core language operators.

---

### 1. Magic Methods
```python
class Vector2D:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    # String representation for end-users
    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    # Unambiguous string representation for developers / debugging
    def __repr__(self):
        return f"Vector2D(x={self.x}, y={self.y})"

    # Operator overloading: + operator
    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    # Equality: == operator
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

v1 = Vector2D(2, 4)
v2 = Vector2D(3, 1)
v3 = v1 + v2
print(v3)  # Vector(5, 5)
```

---

### 2. Method Types: `@staticmethod` vs `@classmethod`
```python
class DateUtils:
    format_pattern = "%Y-%m-%d"

    @classmethod
    def from_string(cls, date_str):
        # Receives class 'cls', useful for alternative constructors
        parts = date_str.split("-")
        return cls()

    @staticmethod
    def is_leap_year(year: int) -> bool:
        # Independent utility; has no access to 'self' or 'cls'
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
```
"""
            },
            {
                "title": "Iterators, Generators & Custom Decorators",
                "slug": "iterators-generators-decorators",
                "summary": "iter(), next(), generator functions with yield, pipeline streams, closures, and custom function decorators.",
                "estimated_minutes": 35,
                "order": 8,
                "content": """# Module 23 — Iterators, Generators & Decorators

---

### 1. Iterators vs Generators
- **Iterator:** Object implementing `__iter__()` and `__next__()`.
- **Generator:** Elegant syntax using `yield` that pauses state execution and resumes upon `next()`.

```python
# Custom generator streaming infinite numbers
def count_stream(start=1):
    while True:
        yield start
        start += 1

gen = count_stream()
print(next(gen))  # 1
print(next(gen))  # 2

# Generator expression (memory efficient vs list comprehension)
large_squares = (x * x for x in range(1_000_000))
print(next(large_squares))  # 0
print(next(large_squares))  # 1
```

---

### 2. Decorators & Closures
A decorator wraps a function to modify or extend its behavior without altering its source code.

```python
import time
from functools import wraps

def time_tracker(func):
    @wraps(func)  # Preserves function metadata (__name__, __doc__)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        print(f"Function '{func.__name__}' executed in {duration:.6f}s")
        return result
    return wrapper

@time_tracker
def heavy_calculation(n):
    return sum(i * i for i in range(n))

heavy_calculation(100_000)
```
"""
            },
            {
                "title": "Regular Expressions (re module)",
                "slug": "regular-expressions-re",
                "summary": "Pattern matching, character classes, quantifiers, search, match, findall, sub, and email/phone validation.",
                "estimated_minutes": 30,
                "order": 9,
                "content": """# Module 24 — Regular Expressions (`re`)

Regular expressions match and manipulate textual patterns.

---

### 1. Core Regex Functions
- `re.search(pattern, text)`: Finds first match anywhere in string.
- `re.match(pattern, text)`: Matches only at the start of string.
- `re.findall(pattern, text)`: Returns all non-overlapping matches as list.
- `re.sub(pattern, replacement, text)`: Replaces matches.

---

### 2. Practical Pattern Validations
```python
import re

# Email validation
email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
email = "developer@antigravity.ai"
print(bool(re.match(email_pattern, email)))  # True

# Phone number extraction
text = "Contact us at 9876543210 or office at +91-9123456789."
phones = re.findall(r"\\+?\\d{1,3}?[-.\\s]?\\d{10}", text)
print("Extracted phones:", phones)

# Sanitizing text
raw = "Hello   world!  Multiple   spaces."
clean = re.sub(r"\\s+", " ", raw)
print(clean)  # "Hello world! Multiple spaces."
```
"""
            },
            {
                "title": "Date and Time Mastery",
                "slug": "datetime-mastery",
                "summary": "Working with datetime, date, time, timedelta, parsing strptime, and formatting strftime.",
                "estimated_minutes": 25,
                "order": 10,
                "content": """# Module 25 — Date and Time Handling

The `datetime` module provides classes for manipulating dates and times.

---

### 1. Creating & Inspecting Dates
```python
from datetime import datetime, date, timedelta

now = datetime.now()
print(f"Current Timestamp: {now}")
print(f"Year: {now.year}, Month: {now.month}, Day: {now.day}")

# Time differences with timedelta
yesterday = now - timedelta(days=1)
next_week = now + timedelta(weeks=1)
```

---

### 2. Formatting (`strftime`) & Parsing (`strptime`)
- `strftime` (String Format Time): Object -> String.
- `strptime` (String Parse Time): String -> Object.

```python
# Format to readable string
formatted = now.strftime("%A, %d %B %Y - %I:%M %p")
print(formatted)  # e.g., 'Friday, 25 September 2026 - 02:30 PM'

# Parse string into datetime object
log_time_str = "2026-09-25 14:30:00"
dt_obj = datetime.strptime(log_time_str, "%Y-%m-%d %H:%M:%S")
print(dt_obj.year)  # 2026
```
"""
            }
        ]
    },
    {
        "title": "Python for Data Science & Interview Prep",
        "slug": "python-data-science-interview-prep",
        "level": Level.INTERVIEW,
        "description": "Transition from Python built-in collections to NumPy & Pandas, plus detailed answers to the top 25 technical interview questions.",
        "order": 4,
        "lessons": [
            {
                "title": "Transitioning Collections to NumPy & Pandas",
                "slug": "collections-to-numpy-pandas",
                "summary": "Bridging Python lists, dicts, and tuples to NumPy ndarrays, Pandas Series, and DataFrames.",
                "estimated_minutes": 30,
                "order": 1,
                "content": """# Module 26 — Python to Data Science Bridge

Python collections (`list`, `dict`) are heterogeneous and flexible, but slow for large-scale mathematical computations. Libraries like NumPy and Pandas provide vectorized, contiguous C-memory structures.

---

### 1. Python List -> NumPy `ndarray`
- Python lists store pointers to objects scattered across memory.
- NumPy arrays store **homogenous data contiguously**, enabling CPU cache line utilization and SIMD vectorization.

```python
import numpy as np

# Creating an array from Python list
py_list = [10, 20, 30, 40]
np_arr = np.array(py_list)

# Vectorized arithmetic (without for-loops!)
print(np_arr * 2)  # array([20, 40, 60, 80])
```

---

### 2. Python Dict -> Pandas DataFrame
```python
import pandas as pd

# Creating a DataFrame from a dictionary of lists
data = {
    "Name": ["Naveen", "Aravind", "Priya"],
    "Role": ["AI Engineer", "Data Scientist", "ML Engineer"],
    "Score": [92, 88, 95]
}

df = pd.DataFrame(data)
print(df)

# Vectorized filtering
high_scorers = df[df["Score"] >= 90]
print(high_scorers)
```
"""
            },
            {
                "title": "Top 25 Python Interview Questions & Solutions",
                "slug": "top-25-interview-questions",
                "summary": "Complete, rigorous answers and code illustrations for the 25 essential Python interview questions.",
                "estimated_minutes": 45,
                "order": 2,
                "content": """# Module 27 — Top 25 Python Interview Questions & Solutions

Master these 25 essential questions asked in technical interviews.

---

### 1. What are Python's built-in data types?
Python includes:
- **Numeric:** `int`, `float`, `complex`
- **Sequence:** `str`, `list`, `tuple`, `range`, `bytes`, `bytearray`
- **Mapping:** `dict`
- **Set:** `set`, `frozenset`
- **Boolean:** `bool`
- **NoneType:** `None`

---

### 2. Difference between List and Tuple?
- **List:** Mutable (`list.append()`), slower allocation, uses more memory. Syntax: `[1, 2]`.
- **Tuple:** Immutable (cannot be changed after creation), faster, memory efficient, hashable (can be used as dictionary keys). Syntax: `(1, 2)`.

---

### 3. List vs Set?
- **List:** Ordered sequence, allows duplicate values, supports integer indexing and slicing `list[0]`.
- **Set:** Unordered collection of unique items, does not allow duplicates, does not support indexing, optimized for $O(1)$ membership checks (`x in my_set`).

---

### 4. Set vs Dictionary?
- **Set:** Stores distinct single keys (`{1, 2, 3}`).
- **Dictionary:** Stores key-value mappings (`{"key": "value"}`). Keys must be unique and hashable.

---

### 5. Mutable vs Immutable?
- **Mutable:** Object can be modified in-place without altering its memory identity `id()`. Examples: `list`, `dict`, `set`, `bytearray`.
- **Immutable:** Object state cannot be changed once created. Any modification creates a new object in memory. Examples: `int`, `float`, `str`, `tuple`, `frozenset`, `bytes`.

---

### 6. Why are strings immutable?
1. **Security:** Strings are used as network URLs, file paths, and database credentials; immutability prevents tampering.
2. **Hashability:** Strings can safely serve as dictionary keys because their hash code never changes.
3. **Memory Optimization:** Python interns strings (String Interning) so identical string literals share the exact same memory location.
4. **Thread Safety:** Multiple threads can access string data simultaneously without race conditions.

---

### 7. Why can't a list be a dictionary key?
Dictionary keys must be **hashable** (their hash value must remain invariant throughout their lifetime). Since lists are mutable, their contents can change, which would corrupt the hash table bucket location.

---

### 8. Why can a tuple be a dictionary key?
A tuple is immutable, meaning its hash value is fixed—**provided all elements within the tuple are also immutable**. A tuple containing a mutable item like `([1, 2], 3)` is unhashable.

---

### 9. Difference between `==` and `is`?
- `==`: Equality operator. Compares **values / contents** of two objects (via `__eq__()`).
- `is`: Identity operator. Checks whether both variables point to the **exact same object in memory** (`id(a) == id(b)`).

```python
a = [1, 2, 3]
b = [1, 2, 3]
print(a == b)  # True (same values)
print(a is b)  # False (different objects)
```

---

### 10. Difference between `remove()` and `pop()`?
- `list.remove(value)`: Removes the **first occurrence of the specified value**. Returns `None`. Raises `ValueError` if value is missing.
- `list.pop([index])`: Removes and **returns** the element at the specified index (default: last element `-1`). Raises `IndexError` on empty list.

---

### 11. Difference between `append()` and `extend()`?
- `list.append(x)`: Adds `x` as a **single element** to the end of the list.
- `list.extend(iterable)`: Iterates over the iterable and appends each element individually.

```python
a = [1, 2]
a.append([3, 4])  # [1, 2, [3, 4]]

b = [1, 2]
b.extend([3, 4])  # [1, 2, 3, 4]
```

---

### 12. Difference between `discard()` and `remove()` in sets?
- `set.remove(val)`: Deletes `val` if found; raises `KeyError` if `val` is not in the set.
- `set.discard(val)`: Deletes `val` if found; quietly does nothing without raising any error if `val` is absent.

---

### 13. Difference between `sort()` and `sorted()`?
- `list.sort()`: In-place method that sorts the list directly and returns `None`. Only works on lists.
- `sorted(iterable)`: Built-in function that takes any iterable and returns a **new sorted list**, preserving the original iterable.

---

### 14. Difference between Shallow Copy and Deep Copy?
- **Shallow Copy (`copy.copy()`):** Creates a new container object, but populates it with references to the child objects contained in the original. Modifications to nested mutable objects reflect in both.
- **Deep Copy (`copy.deepcopy()`):** Recursively creates copies of all nested objects. Completely isolates the copy from the original.

---

### 15. What is List Comprehension?
A concise, syntactic construct for creating a new list from an existing iterable based on an expression and optional condition:
`[expression for item in iterable if condition]`

---

### 16. What is Dictionary Comprehension?
A compact way to build dictionaries from iterables:
`{key_expr: val_expr for item in iterable if condition}`

---

### 17. What is Tuple Packing?
Assigning multiple values separated by commas to a single variable without explicit parentheses:
`data = 10, "Python", True`

---

### 18. What is Tuple Unpacking?
Extracting the values from a tuple directly into individual variables:
`a, b, c = data`

---

### 19. What is `*` Unpacking?
Using the asterisk `*` operator to capture multiple positional elements into a list:
`first, *rest = [1, 2, 3, 4, 5]`  # first = 1, rest = [2, 3, 4, 5]

---

### 20. What are hashable objects?
An object is hashable if:
1. It implements a `__hash__()` method returning an integer constant over its lifetime.
2. It implements `__eq__()` for equality comparison.
All immutable built-in types in Python are hashable.

---

### 21. Why are dictionary keys unique?
Dictionaries are built upon hash tables. Each key is hashed to an array index. If duplicate keys were permitted, retrieving a key would result in ambiguity. Writing to an existing key simply overwrites its current value.

---

### 22. Why doesn't a set allow duplicates?
Like dictionaries, sets use hash tables under the hood. When adding an element, Python hashes the object. If an entry with an identical hash and equality already exists, the addition is skipped.

---

### 23. What is `None`?
`None` is a special constant in Python that represents the absence of a value or a null value. It is the sole instance of the `NoneType` class. Functions that do not explicitly return a value implicitly return `None`.

---

### 24. What is Type Conversion?
The process of converting a value from one data type to another:
- **Implicit Conversion:** Performed automatically by Python (e.g., adding `int` and `float` produces a `float`).
- **Explicit Conversion (Type Casting):** Performed manually using constructor functions like `int()`, `float()`, `str()`, `list()`.

---

### 25. Difference between `type()` and `isinstance()`?
- `type(obj)` returns the exact class type of the object. It does not account for class inheritance.
- `isinstance(obj, class_or_tuple)` returns `True` if the object is an instance of the class **or any subclass derived from it**. It supports checking against multiple types via tuples.
"""
            }
        ]
    }
]

# -----------------------------------------------------------------------------
# 2. INTERVIEW QUESTIONS (25 SEEDED ENTRIES)
# -----------------------------------------------------------------------------

INTERVIEW_QUESTIONS_DATA = [
    {
        "question": "What are Python's built-in data types?",
        "difficulty": InterviewQuestion.Difficulty.EASY,
        "short_answer": "Python includes Numeric (int, float, complex), Sequence (str, list, tuple, range, bytes, bytearray), Mapping (dict), Set (set, frozenset), Boolean (bool), and NoneType.",
        "detailed_answer": "Python's data types are categorized by their underlying memory structure and behaviors: Numeric types represent scalar numbers; sequences represent ordered collections; mappings store key-value associations; and sets represent unordered collections of unique elements.",
        "example": "x = 10 (int), y = 3.14 (float), s = 'hello' (str), l = [1, 2] (list), d = {'a': 1} (dict)",
        "code": "types = [10, 3.14, 2+3j, True, 'Python', [1], (1,), {1}, {'k': 'v'}, None]\nfor t in types:\n    print(f'{str(t):<10} -> {type(t).__name__}')",
        "interview_tip": "Mention the distinction between mutable (list, dict, set) and immutable (int, str, tuple) types when answering."
    },
    {
        "question": "What is the difference between list and tuple in Python?",
        "difficulty": InterviewQuestion.Difficulty.EASY,
        "short_answer": "Lists are mutable and defined with square brackets []; tuples are immutable and defined with parentheses ().",
        "detailed_answer": "Lists are dynamic arrays that support adding, removing, and changing elements in-place. Tuples are fixed-size immutable arrays. Because of immutability, tuples are faster, use less memory, and can be used as dictionary keys.",
        "example": "l = [1, 2]; l.append(3) # Allowed\nt = (1, 2); t[0] = 9 # TypeError: 'tuple' object does not support item assignment",
        "code": "import sys\nl = [1, 2, 3, 4, 5]\nt = (1, 2, 3, 4, 5)\nprint('List size:', sys.getsizeof(l))\nprint('Tuple size:', sys.getsizeof(t))",
        "interview_tip": "Highlight that tuples provide write-protection for constants and explain why they can be hashed."
    },
    {
        "question": "What is the difference between List and Set?",
        "difficulty": InterviewQuestion.Difficulty.EASY,
        "short_answer": "Lists are ordered and allow duplicates; sets are unordered collections of unique, hashable items.",
        "detailed_answer": "Lists preserve element insertion order and allow indexing list[0]. Sets use hash tables to guarantee element uniqueness and provide O(1) average lookup time compared to O(N) linear search in lists.",
        "example": "[1, 2, 2, 3] maintains both 2s. {1, 2, 2, 3} deduplicates to {1, 2, 3}.",
        "code": "nums = [1, 2, 2, 3, 4, 4]\nunique_nums = set(nums)\nprint(unique_nums)  # {1, 2, 3, 4}\nprint(3 in unique_nums)  # O(1) membership check",
        "interview_tip": "Always mention the computational complexity difference for membership testing: O(1) for set vs O(N) for list."
    },
    {
        "question": "What is the difference between Set and Dictionary?",
        "difficulty": InterviewQuestion.Difficulty.EASY,
        "short_answer": "Sets store only unique keys; dictionaries store key-value pairs.",
        "detailed_answer": "Both data structures rely on hash tables for rapid lookups. However, a set represents a mathematical collection of single unique elements, while a dictionary maps unique keys to corresponding value objects.",
        "example": "s = {'python', 'sql'} vs d = {'python': 3.12, 'sql': 'postgres'}",
        "code": "s = {1, 2, 3}\nd = {1: 'one', 2: 'two', 3: 'three'}\nprint(type(s), type(d))",
        "interview_tip": "Point out that empty {} in Python creates a dictionary; an empty set must be instantiated using set()."
    },
    {
        "question": "What is the difference between Mutable and Immutable objects in Python?",
        "difficulty": InterviewQuestion.Difficulty.MEDIUM,
        "short_answer": "Mutable objects can change their state in-place without changing memory address; immutable objects cannot.",
        "detailed_answer": "When you modify a mutable object (like appending to a list), the id() stays the same. When you modify an immutable object (like modifying a string or int), Python allocates a new object in memory with a new id().",
        "example": "x = 10; id_before = id(x); x += 1; id_after = id(x) # id_before != id_after",
        "code": "# Mutable:\nl = [1, 2]\nprint(id(l))\nl.append(3)\nprint(id(l))  # Identical id\n\n# Immutable:\ns = 'abc'\nprint(id(s))\ns += 'd'\nprint(id(s))  # Different id",
        "interview_tip": "Demonstrate this using the id() function in your answer to prove mastery of Python memory."
    },
    {
        "question": "Why are strings immutable in Python?",
        "difficulty": InterviewQuestion.Difficulty.MEDIUM,
        "short_answer": "For security, hashability as dictionary keys, thread safety, and string interning memory optimization.",
        "detailed_answer": "Strings are extensively used in file paths, network sockets, and database queries. If strings were mutable, another thread could mutate a verified path. Immutability also allows strings to cache their hash and share memory via string interning.",
        "example": "a = 'hello'; b = 'hello'; print(a is b) yields True due to string interning.",
        "code": "s1 = 'antigravity'\ns2 = 'antigravity'\nprint(s1 is s2)  # True: Same cached memory reference",
        "interview_tip": "Mention 'String Interning' and 'Thread Safety' for extra points in senior developer rounds."
    },
    {
        "question": "Why can't a list be a dictionary key in Python?",
        "difficulty": InterviewQuestion.Difficulty.MEDIUM,
        "short_answer": "Lists are mutable, meaning their contents can change, making them unhashable.",
        "detailed_answer": "Python dictionaries are hash tables. A key must have an invariant hash code throughout its lifecycle to ensure it can always be retrieved from its bucket. Because lists are mutable, their contents and hash would change, breaking the lookup contract.",
        "example": "d = {[1, 2]: 'val'} raises TypeError: unhashable type: 'list'.",
        "code": "try:\n    d = {[1, 2]: 'value'}\nexcept TypeError as e:\n    print('Caught error:', e)",
        "interview_tip": "Explain that objects used as dictionary keys must implement both __hash__() and __eq__()."
    },
    {
        "question": "Why can a tuple be used as a dictionary key?",
        "difficulty": InterviewQuestion.Difficulty.MEDIUM,
        "short_answer": "Tuples are immutable sequences, so their hash values remain constant.",
        "detailed_answer": "Because tuples cannot be modified once instantiated, their hash value is deterministic and stable, allowing the hash table to reliably index them. Note: A tuple is only hashable if all elements inside it are also hashable.",
        "example": "d = {(1, 2): 'coordinates'} is valid; d = {([1], 2): 'err'} fails because list is unhashable.",
        "code": "valid = (1, 'two', 3.0)\nprint('Hash:', hash(valid))\nd = {valid: 'success'}\nprint(d[valid])",
        "interview_tip": "Highlight the catch: a tuple containing a list is NOT hashable."
    },
    {
        "question": "What is the difference between == and is in Python?",
        "difficulty": InterviewQuestion.Difficulty.EASY,
        "short_answer": "'==' compares equality of values; 'is' compares identity (memory addresses).",
        "detailed_answer": "The == operator invokes the object's __eq__() method to test whether two objects hold equivalent contents. The 'is' operator checks whether both operands point to the exact same object in memory (id(a) == id(b)).",
        "example": "a = [1, 2]; b = [1, 2]; a == b is True, but a is b is False.",
        "code": "a = [10, 20]\nb = [10, 20]\nc = a\nprint('a == b:', a == b)  # True\nprint('a is b:', a is b)  # False\nprint('a is c:', a is c)  # True",
        "interview_tip": "Mention that you should always use 'is' when checking for None (e.g. 'if x is None')."
    },
    {
        "question": "What is the difference between remove() and pop() on a list?",
        "difficulty": InterviewQuestion.Difficulty.EASY,
        "short_answer": "remove() deletes the first matching value; pop() removes and returns an element at a given index.",
        "detailed_answer": "remove(x) searches for the first occurrence of value x and removes it without returning anything. pop([index]) removes and returns the element at the specified index (defaults to index -1, the last item).",
        "example": "l = [10, 20, 30]; l.remove(20) -> [10, 30]; popped = l.pop() -> popped is 30, l is [10].",
        "code": "nums = [10, 20, 30, 40]\nnums.remove(20)  # Value removal\nprint(nums)      # [10, 30, 40]\nlast = nums.pop()# Index removal with return\nprint('Popped:', last, 'Remaining:', nums)",
        "interview_tip": "Note that pop() on an empty list or remove() on a missing item raises an exception (IndexError vs ValueError)."
    },
    {
        "question": "What is the difference between append() and extend() on a list?",
        "difficulty": InterviewQuestion.Difficulty.EASY,
        "short_answer": "append() adds its argument as a single element; extend() iterates over its argument and adds each item.",
        "detailed_answer": "If you pass a list [3, 4] to append(), you create a nested list. If you pass it to extend(), the elements are unpacked and appended individually.",
        "example": "a = [1, 2]; a.append([3, 4]) -> [1, 2, [3, 4]]. a.extend([3, 4]) -> [1, 2, 3, 4].",
        "code": "l1 = [1, 2]\nl1.append([3, 4])\nprint('append:', l1)\n\nl2 = [1, 2]\nl2.extend([3, 4])\nprint('extend:', l2)",
        "interview_tip": "Mention that extend() works with any iterable (strings, tuples, sets, generators), not just lists."
    },
    {
        "question": "What is the difference between discard() and remove() on a set?",
        "difficulty": InterviewQuestion.Difficulty.EASY,
        "short_answer": "remove() raises a KeyError if the element does not exist; discard() silently does nothing.",
        "detailed_answer": "Both methods remove an element from a set. However, discard() provides safe deletion without requiring a pre-check (x in my_set) or try-except block.",
        "example": "s = {1, 2}; s.discard(99) # Safe; s.remove(99) # KeyError: 99",
        "code": "s = {'a', 'b'}\ns.discard('z')  # No error\nprint('Discarded safely:', s)\ntry:\n    s.remove('z')\nexcept KeyError:\n    print('remove() raised KeyError as expected')",
        "interview_tip": "Use discard() when you don't care if the element was originally present or not."
    },
    {
        "question": "What is the difference between sort() and sorted()?",
        "difficulty": InterviewQuestion.Difficulty.EASY,
        "short_answer": "list.sort() modifies the list in-place and returns None; sorted() returns a new sorted list from any iterable.",
        "detailed_answer": "sort() is a method belonging strictly to the list class. sorted() is a built-in function that accepts any iterable (list, tuple, string, dictionary keys) and always returns a new list containing the sorted elements.",
        "example": "l = [3, 1]; res = l.sort() # l is [1, 3], res is None. sorted([3, 1]) returns [1, 3].",
        "code": "original = [5, 2, 9, 1]\nnew_list = sorted(original)\nprint('Original:', original)\nprint('New list:', new_list)\noriginal.sort()\nprint('After sort():', original)",
        "interview_tip": "Both methods use Timsort (an adaptive merge/insertion hybrid) with O(N log N) worst-case time complexity."
    },
    {
        "question": "What is the difference between Shallow Copy and Deep Copy?",
        "difficulty": InterviewQuestion.Difficulty.HARD,
        "short_answer": "Shallow copy creates a new container but references child objects; deep copy recursively clones all nested objects.",
        "detailed_answer": "In a shallow copy (copy.copy() or list.copy()), the outer object is newly created, but nested objects point to the same references. In a deep copy (copy.deepcopy()), Python recursively creates copies of all child and nested objects.",
        "example": "orig = [[1]]; sc = copy.copy(orig); sc[0][0] = 99 -> alters orig[0][0] too!",
        "code": "import copy\norig = [[10, 20], [30, 40]]\nshallow = copy.copy(orig)\ndeep = copy.deepcopy(orig)\norig[0][0] = 999\nprint('Shallow reflects change:', shallow[0][0])\nprint('Deep remains untouched:', deep[0][0])",
        "interview_tip": "Draw or describe memory pointers to show the interviewer you understand compound object references."
    },
    {
        "question": "What is List Comprehension and why is it preferred?",
        "difficulty": InterviewQuestion.Difficulty.MEDIUM,
        "short_answer": "A concise syntax for creating lists from iterables, faster than for-loops because it executes at C-speed in bytecode.",
        "detailed_answer": "List comprehension provides a readable, declarative syntax: [expr for item in iterable if condition]. It optimizes performance because the loop and list append operations run inside C-level bytecode (LIST_APPEND) without python method call overhead.",
        "example": "evens = [x for x in range(10) if x % 2 == 0]",
        "code": "squares = [x**2 for x in range(1, 6)]\nprint('Squares:', squares)\nnames = ['naveen', 'kumar']\ntitled = [n.capitalize() for n in names]\nprint('Titled:', titled)",
        "interview_tip": "Warn against overusing deeply nested comprehensions that sacrifice code readability."
    },
    {
        "question": "What is Dictionary Comprehension?",
        "difficulty": InterviewQuestion.Difficulty.MEDIUM,
        "short_answer": "A declarative syntax to transform or filter data into a dictionary: {k: v for item in iterable}.",
        "detailed_answer": "Dictionary comprehension creates dictionaries dynamically from lists, tuples, or other dictionaries with optional conditional filtering.",
        "example": "{x: x**2 for x in range(5)} creates {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}.",
        "code": "prices_usd = {'laptop': 1000, 'mouse': 25, 'monitor': 300}\nusd_to_inr = 83.5\nprices_inr = {item: price * usd_to_inr for item, price in prices_usd.items()}\nprint(prices_inr)",
        "interview_tip": "Show how dictionary comprehension is great for reversing/inverting dictionaries: {v: k for k, v in d.items()}."
    },
    {
        "question": "What is Tuple Packing in Python?",
        "difficulty": InterviewQuestion.Difficulty.EASY,
        "short_answer": "Packing multiple values into a single tuple object without needing parentheses.",
        "detailed_answer": "In Python, any comma-separated sequence of values without surrounding brackets automatically packs into a tuple.",
        "example": "data = 1, 2, 'three' results in type(data) being tuple.",
        "code": "packed = 'Naveen', 25, 'AI/ML'\nprint(packed, type(packed))",
        "interview_tip": "Mention that functions returning multiple values are actually returning a packed tuple."
    },
    {
        "question": "What is Tuple Unpacking in Python?",
        "difficulty": InterviewQuestion.Difficulty.EASY,
        "short_answer": "Assigning individual elements of a tuple directly to multiple variables in a single statement.",
        "detailed_answer": "Unpacking extracts elements from a sequence into separate variables. The number of variables on the left must exactly match the number of elements unless extended unpacking is used.",
        "example": "point = (10, 20); x, y = point",
        "code": "coords = (12.97, 77.59)\nlat, lon = coords\nprint(f'Lat: {lat}, Lon: {lon}')",
        "interview_tip": "Demonstrate variable swapping: a, b = b, a uses tuple packing and unpacking."
    },
    {
        "question": "What is * (Asterisk / Star) Unpacking in Python?",
        "difficulty": InterviewQuestion.Difficulty.MEDIUM,
        "short_answer": "Extended unpacking that captures surplus elements into a list: first, *rest = items.",
        "detailed_answer": "Introduced in PEP 3132, the star operator allows unpacking sequences of arbitrary length, collecting zero or more remaining elements into a list.",
        "example": "first, *middle, last = [1, 2, 3, 4, 5] -> middle is [2, 3, 4].",
        "code": "scores = [98, 85, 92, 74, 89]\nhighest, *other_scores = sorted(scores, reverse=True)\nprint('Highest:', highest)\nprint('Others:', other_scores)",
        "interview_tip": "Mention that * can also be used in function arguments (*args) and to merge dictionaries (**kwargs or {**d1, **d2})."
    },
    {
        "question": "What are Hashable objects in Python?",
        "difficulty": InterviewQuestion.Difficulty.HARD,
        "short_answer": "Objects whose hash value never changes during their lifetime and can be compared for equality.",
        "detailed_answer": "An object is hashable if it has an integer hash value returned by __hash__() and can be compared via __eq__(). Hashability is required for objects to be stored in sets or used as dictionary keys. By default, immutable types are hashable.",
        "example": "hash('hello') returns an integer; hash([1, 2]) raises TypeError.",
        "code": "print(hash(42))\nprint(hash('Python'))\nprint(hash((1, 2, 3)))\ntry:\n    hash([1, 2])\nexcept TypeError as e:\n    print('Lists cannot be hashed:', e)",
        "interview_tip": "Explain that user-defined classes are hashable by default (using id() for hash and identity for equality) unless __eq__ is overridden."
    },
    {
        "question": "Why are Dictionary keys unique?",
        "difficulty": InterviewQuestion.Difficulty.MEDIUM,
        "short_answer": "Dictionaries use hash tables where each key maps to a distinct bucket index; duplicates would cause ambiguity.",
        "detailed_answer": "When a key is added, Python computes its hash to find the bucket index. If the same key is added again, Python finds the existing key and overwrites its value rather than creating a duplicate entry.",
        "example": "d = {'x': 1, 'x': 2} results in {'x': 2}.",
        "code": "profile = {'name': 'Naveen', 'name': 'Naveen Kumar'}\nprint(profile)  # Only the latest value is preserved",
        "interview_tip": "Note that values can be duplicated, but keys must remain strictly unique."
    },
    {
        "question": "Why doesn't a Set allow duplicate elements?",
        "difficulty": InterviewQuestion.Difficulty.MEDIUM,
        "short_answer": "Sets represent mathematical sets and use a hash table backend that skips identical hash/equality items.",
        "detailed_answer": "Sets are implemented similarly to dictionaries with dummy values. When you insert an item, Python hashes it and checks for an existing entry. If an item matches both hash() and == equality, insertion is ignored.",
        "example": "s = {1, 2, 2, 3} becomes {1, 2, 3}.",
        "code": "raw = [1, 1, 2, 3, 5, 8, 5]\nclean_set = set(raw)\nprint('Deduplicated set:', clean_set)",
        "interview_tip": "A classic interview problem is deduplicating a list in O(N) time using set(my_list)."
    },
    {
        "question": "What is None in Python?",
        "difficulty": InterviewQuestion.Difficulty.EASY,
        "short_answer": "A singleton constant representing the absence of a value or null state.",
        "detailed_answer": "None is the sole instance of the NoneType class. It evaluates to False in a boolean context. Functions without an explicit return statement return None by default. Always compare using 'is None'.",
        "example": "res = print('hi') # res is None",
        "code": "x = None\nprint('Type:', type(x))\nprint('Is None?', x is None)\nprint('Boolean value:', bool(x))",
        "interview_tip": "Remind interviewers never to check 'if x == None' because == can be overloaded by classes, while 'is None' checks memory identity."
    },
    {
        "question": "What is Type Conversion in Python? (Implicit vs Explicit)",
        "difficulty": InterviewQuestion.Difficulty.EASY,
        "short_answer": "Converting data from one type to another; implicit is automatic by Python, explicit is cast by the programmer.",
        "detailed_answer": "Implicit conversion avoids data loss by automatically promoting smaller types (e.g. int + float -> float). Explicit conversion (type casting) uses built-in constructor functions like int(), float(), str(), list() to force a conversion.",
        "example": "Implicit: 5 + 2.0 = 7.0. Explicit: int('100') -> 100.",
        "code": "# Implicit\nx = 10\ny = 2.5\nz = x + y\nprint(z, type(z))  # 12.5 <class 'float'>\n\n# Explicit\ns = '456'\ni = int(s)\nprint(i, type(i))  # 456 <class 'int'>",
        "interview_tip": "Mention potential runtime errors with explicit conversion, such as ValueError when casting non-numeric strings to int."
    },
    {
        "question": "What is the difference between type() and isinstance()?",
        "difficulty": InterviewQuestion.Difficulty.MEDIUM,
        "short_answer": "type() checks for exact class match; isinstance() checks class and supports inheritance.",
        "detailed_answer": "type(obj) returns the exact type and does not consider inheritance hierarchies. isinstance(obj, ClassInfo) checks whether the object is an instance of the class or any derived subclass, making it the standard for polymorphic type checking.",
        "example": "class Dog(Animal): pass; d = Dog(); type(d) == Animal is False, but isinstance(d, Animal) is True.",
        "code": "class Base: pass\nclass Derived(Base): pass\n\nobj = Derived()\nprint('type() == Base:', type(obj) == Base)         # False\nprint('isinstance(Base):', isinstance(obj, Base))   # True\nprint('isinstance tuple:', isinstance(10, (int, str))) # True",
        "interview_tip": "PEP 8 explicitly recommends isinstance() over type() comparisons for clean object-oriented Python."
    }
]

print("Definitions loaded. Starting seeding process...")
