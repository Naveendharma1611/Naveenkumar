-- NK Practice Portal — seed data
-- Run this once in the Supabase SQL editor, AFTER schema.sql has been run
-- on a fresh Supabase project. Populates 10 topics, 30 practice questions
-- (3 per topic: easy / medium / hard) and their test cases.
--
-- String-quoting convention used throughout this file:
--   $md$ ... $md$   markdown text (topics.explanation, questions.prompt)
--   $py$ ... $py$   python code  (example_code, starter_code, solution_code)
--   $txt$ ... $txt$ plain text   (example_output, hint, stdin, expected_output)
-- Plain '...' quotes are used only for short identifiers with no special
-- characters (slug, title, difficulty).

-- ============================================================================
-- 1. TOPICS
-- ============================================================================
insert into topics (id, slug, title, order_index, explanation, example_code, example_output) values

('a0000000-0000-0000-0000-000000000001', 'variables-data-types', 'Variables and Data Types', 1,
$md$A **variable** is simply a name that points to a value stored in memory. In Python you don't need to declare a type up front — you just assign a value with `=` and Python figures out the type for you. This is called *dynamic typing*.

## Common Data Types

- **int** — whole numbers, e.g. `age = 20`
- **float** — decimal numbers, e.g. `price = 19.99`
- **str** — text, written in quotes, e.g. `name = "Asha"`
- **bool** — `True` or `False`

You can check any variable's type with the built-in `type()` function, e.g. `type(age)` returns `<class 'int'>`.

## Naming Rules

- Names can contain letters, digits and underscores, but can't start with a digit.
- Names are case-sensitive (`score` and `Score` are different variables).
- Use descriptive names (`total_marks` instead of `t`) — it makes your code much easier to read later.

## Type Conversion

Sometimes you need to convert between types, for example when data comes in as text. Python gives you built-in conversion functions:

- `int("25")` → `25`
- `float("3.14")` → `3.14`
- `str(42)` → `"42"`

Getting comfortable with variables and types is the foundation for everything else in Python — every calculation, condition and loop you write depends on values stored in variables.$md$,
$py$name = "Riya"
age = 20
gpa = 8.75
is_enrolled = True

print(name, age, gpa, is_enrolled)
print(type(name), type(age), type(gpa), type(is_enrolled))

age = age + 1
print("Next year age:", age)$py$,
$txt$Riya 20 8.75 True
<class 'str'> <class 'int'> <class 'float'> <class 'bool'>
Next year age: 21
$txt$),

('a0000000-0000-0000-0000-000000000002', 'input-output', 'Input and Output', 2,
$md$Every interactive program needs a way to get data from the user and show results back. Python keeps this simple with two built-in functions: `input()` and `print()`.

## Reading Input

`input()` pauses the program, waits for the user to type something and hit Enter, and returns **whatever was typed, as a string** — even if it looks like a number. That means if you want to do math with it, you must convert it first:

    age_text = input()      # always a string
    age = int(age_text)     # now it's a number

You can also do this in one line: `age = int(input())`.

## Writing Output

`print()` writes text to the screen, and automatically adds a newline at the end. You can pass several values separated by commas, and `print` will join them with a space by default:

    print("Score:", 95)

Two handy keyword arguments let you customize this:

- `sep` — what to put *between* values (default `" "`)
- `end` — what to put *after* everything (default `"\n"`)

## Formatting with f-strings

The cleanest way to mix text and variables is an f-string, written as `f"..."` with `{variable}` placeholders inside:

    print(f"Hello {name}, you scored {marks}!")

Mastering `input()` and `print()` is essential — nearly every practice question on this site reads its data with `input()` and checks your answer against what you `print()`.$md$,
$py$first_name = "Arjun"
marks = 95

print("Welcome", first_name, sep=", ", end="!\n")
print(f"You scored {marks} out of 100")
print("A", "B", "C", sep="-")
print("No newline here", end="")
print(" <- continued on same line")$py$,
$txt$Welcome, Arjun!
You scored 95 out of 100
A-B-C
No newline here <- continued on same line
$txt$),

('a0000000-0000-0000-0000-000000000003', 'operators', 'Operators', 3,
$md$Operators let you combine values to produce new ones — doing math, comparing things, or building logical conditions.

## Arithmetic Operators

- `+`, `-`, `*` — addition, subtraction, multiplication
- `/` — true division, always returns a float (`7 / 2` → `3.5`)
- `//` — floor division, rounds down to the nearest whole number (`7 // 2` → `3`)
- `%` — modulus, gives the remainder (`7 % 2` → `1`)
- `**` — exponent/power (`2 ** 3` → `8`)

## Comparison Operators

These compare two values and always produce a `bool` (`True`/`False`): `==`, `!=`, `>`, `<`, `>=`, `<=`. Note that `==` checks equality while a single `=` is assignment — mixing these up is one of the most common beginner mistakes.

## Logical Operators

Used to combine boolean expressions:

- `and` — True only if both sides are True
- `or` — True if at least one side is True
- `not` — flips True to False and vice versa

`and` binds tighter than `or`, so in an expression like `a and b or c`, the `a and b` part is evaluated first.

## Assignment Operators

Shortcuts like `+=`, `-=`, `*=`, `/=` update a variable in place: `total += 5` is the same as `total = total + 5`.

Understanding how these operators interact — and their precedence — will save you from subtle bugs later when you write conditions and loops.$md$,
$py$a = 17
b = 5

print(a + b, a - b, a * b)
print(a / b, a // b, a % b)
print(a ** 2)
print(a > b, a == b, a != b)
print(a > 10 and b < 10)
print(a > 10 or b > 10)
print(not (a > 10))$py$,
$txt$22 12 85
3.4 3 2
289
True False True
True
True
False
$txt$),

('a0000000-0000-0000-0000-000000000004', 'conditionals', 'Conditional Statements (if/elif/else)', 4,
$md$Conditional statements let your program make decisions and run different code depending on whether something is true or false.

## The if / elif / else Structure

    if condition1:
        # runs if condition1 is True
    elif condition2:
        # runs if condition1 is False and condition2 is True
    else:
        # runs if none of the above were True

Python checks each condition from top to bottom and runs the **first** block whose condition is True — the rest are skipped, even if they'd also be True. `elif` is short for "else if", and you can chain as many as you need. The `else` block is optional and only runs when every condition above it was False.

## Indentation Matters

Unlike many languages, Python uses indentation (not curly braces) to mark which lines belong to a block. Every line inside an `if`/`elif`/`else` body must be indented consistently, usually with 4 spaces.

## Nesting and Combining Conditions

You can put an `if` inside another `if` for more complex logic, or combine multiple checks with `and`/`or` in a single condition, e.g. `if age >= 18 and has_id:`.

## Truthy and Falsy Values

Besides actual booleans, Python treats `0`, `0.0`, `""`, empty lists, and `None` as "falsy" in a condition, and basically everything else as "truthy".

Conditionals are what take your programs from doing one fixed thing to actually reacting to data.$md$,
$py$marks = 72

if marks >= 90:
    grade = "A"
elif marks >= 75:
    grade = "B"
elif marks >= 60:
    grade = "C"
else:
    grade = "D"

print("Marks:", marks)
print("Grade:", grade)

temperature = 15
if temperature < 0:
    print("Freezing")
elif temperature < 20:
    print("Cool")
else:
    print("Warm")$py$,
$txt$Marks: 72
Grade: C
Cool
$txt$),

('a0000000-0000-0000-0000-000000000005', 'loops', 'Loops (for, while)', 5,
$md$Loops let you repeat a block of code multiple times without copy-pasting it — essential for processing lists of data, counting, or repeating a calculation.

## for Loops

A `for` loop walks through a sequence (like a `range()`, a string, or a list) one item at a time:

    for i in range(1, 6):
        print(i)

`range(start, stop)` produces numbers from `start` up to (but **not including**) `stop`. `range(5)` alone goes from `0` to `4`.

## while Loops

A `while` loop keeps running as long as its condition stays True — useful when you don't know in advance how many times you'll need to repeat:

    n = 5
    while n > 0:
        print(n)
        n -= 1

Be careful: if the condition never becomes False, you get an **infinite loop**. Always make sure something inside the loop eventually changes the condition.

## break and continue

- `break` exits the loop immediately, skipping any remaining iterations.
- `continue` skips the rest of the current iteration and jumps to the next one.

## Choosing Between Them

Use a `for` loop when you know the number of iterations (or are iterating over a collection). Use a `while` loop when you're repeating "until some condition changes," like until a user enters a specific value.

Loops are one of the most powerful tools in programming — most real-world tasks involve repeating something many times.$md$,
$py$squares = []
for i in range(1, 6):
    squares.append(i * i)
print(squares)

total = 0
n = 5
while n > 0:
    total += n
    n -= 1
print("Sum:", total)

result = []
for i in range(10):
    if i == 5:
        break
    if i % 2 == 0:
        continue
    result.append(i)
print(result)$py$,
$txt$[1, 4, 9, 16, 25]
Sum: 15
[1, 3]
$txt$),

('a0000000-0000-0000-0000-000000000006', 'strings', 'Strings', 6,
$md$A string is a sequence of characters, written between single or double quotes. Strings are one of the most-used data types, since almost every program deals with text.

## Indexing and Slicing

Each character has a position (index), starting at `0`. You can grab single characters or ranges:

    word = "Python"
    print(word[0])     # 'P'
    print(word[1:4])   # 'yth'
    print(word[::-1])  # 'nohtyP' (reversed)

Negative indices count from the end, so `word[-1]` is the last character.

## Useful String Methods

- `.upper()` / `.lower()` — change case
- `.strip()` — remove leading/trailing whitespace
- `.split(sep)` — break a string into a list of pieces
- `.replace(old, new)` — swap out a substring
- `.join(list)` — stitch a list of strings together with a separator
- `len(s)` — number of characters

## Strings Are Immutable

You can't change a string in place — every method that "modifies" a string actually returns a brand-new one. So `s.upper()` doesn't change `s`; you need `s = s.upper()` to keep the result.

## Combining Strings

You can join strings with `+`, repeat them with `*` (`"ab" * 3` → `"ababab"`), or — best of all — use an f-string to drop variables directly into text: `f"Hello {name}"`.

Getting comfortable with string methods will make tasks like validating input or formatting output far easier.$md$,
$py$text = "  Hello, Python World!  "

print(text.strip())
print(text.strip().upper())
print(text.strip().lower())
print(len(text.strip()))
print(text.strip()[0:5])
print(text.strip().replace("World", "Students"))
words = text.strip().split(",")
print(words)$py$,
$txt$Hello, Python World!
HELLO, PYTHON WORLD!
hello, python world!
20
Hello
Hello, Python Students!
['Hello', ' Python World!']
$txt$),

('a0000000-0000-0000-0000-000000000007', 'collections', 'Lists, Tuples, Sets & Dictionaries', 7,
$md$Python gives you four built-in ways to store a group of values together, each suited to a different job.

## Lists

A **list** is an ordered, changeable collection, written with square brackets: `fruits = ["apple", "banana"]`. You can add items with `.append()`, access by index (`fruits[0]`), and change them after creation — lists are *mutable*.

## Tuples

A **tuple** looks similar but uses parentheses — `point = (3, 4)` — and is *immutable*: once created, it can't be changed. Tuples are handy for fixed groups of values, like coordinates, that shouldn't accidentally be modified.

## Sets

A **set**, written `{1, 2, 3}`, is an unordered collection that automatically removes duplicates. Sets are great whenever you only care about unique values and don't need a particular order.

## Dictionaries

A **dictionary** stores `key: value` pairs, giving you fast lookup by key instead of by position:

    student = {"name": "Maya", "age": 21}
    print(student["name"])   # "Maya"
    student["grade"] = "A"   # add a new key

## Choosing the Right One

- Need order and duplicates allowed, and might change it? Use a **list**.
- Need a fixed, unchangeable group? Use a **tuple**.
- Only care about unique values? Use a **set**.
- Need to look things up by a name/key? Use a **dictionary**.

Most real programs use a mix of these to organize data cleanly.$md$,
$py$fruits = ["apple", "banana", "cherry"]
fruits.append("date")
print(fruits)
print(fruits[1])
print(len(fruits))

coordinates = (10, 20)
print(coordinates)

unique_numbers = {1, 2, 2, 3, 3, 3}
print(unique_numbers)

student = {"name": "Maya", "age": 21}
student["grade"] = "A"
print(student)
print(student["name"])$py$,
$txt$['apple', 'banana', 'cherry', 'date']
banana
4
(10, 20)
{1, 2, 3}
{'name': 'Maya', 'age': 21, 'grade': 'A'}
Maya
$txt$),

('a0000000-0000-0000-0000-000000000008', 'functions', 'Functions', 8,
$md$A function is a named, reusable block of code that performs a specific task. Instead of repeating the same lines over and over, you define them once and *call* the function whenever you need that logic.

## Defining a Function

    def greet(name):
        return f"Hello, {name}!"

`def` starts the definition, followed by the function name and a parenthesized list of **parameters** — the inputs the function expects. The `return` statement sends a value back to wherever the function was called; without it, the function returns `None`.

## Calling a Function

Once defined, you use the function by writing its name with arguments in parentheses: `greet("Asha")` runs the code inside and gives back `"Hello, Asha!"`.

## Default Arguments

You can give a parameter a default value, making it optional when calling: `def greet(name, greeting="Hello")` lets you call `greet("Sam")` or `greet("Sam", "Hi")`.

## Why Use Functions?

- **Reuse** — write the logic once, call it as many times as you like.
- **Readability** — a well-named function (`is_prime(n)`) documents what the code does.
- **Testing** — small functions are easier to check for correctness in isolation.

## Local Scope

Variables created inside a function only exist inside that function — they don't leak out and overwrite variables with the same name elsewhere in your program.

Functions are the building blocks of larger, well-organized programs.$md$,
$py$def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

def add(a, b):
    return a + b

def is_even(n):
    return n % 2 == 0

print(greet("Sam"))
print(greet("Lee", "Hi"))
print(add(3, 4))
print(is_even(10))
print(is_even(7))$py$,
$txt$Hello, Sam!
Hi, Lee!
7
True
False
$txt$),

('a0000000-0000-0000-0000-000000000009', 'file-handling', 'File Handling', 9,
$md$File handling lets a program save data permanently (or, in this browser-based portal, to an in-memory virtual filesystem) and read it back later.

## Opening a File

Python's `open()` function takes a filename and a **mode**:

- `"w"` — write (creates the file, or overwrites it if it already exists)
- `"r"` — read
- `"a"` — append (adds to the end without erasing existing content)

    with open("notes.txt", "w") as f:
        f.write("Hello\n")

Using `with open(...) as f:` is the recommended pattern — it automatically closes the file for you when the block ends, even if an error occurs.

## Reading Content Back

- `f.read()` — returns the entire file as one string
- `f.readlines()` — returns a list of lines (each one still ending in `"\n"`)
- Looping directly over the file object (`for line in f:`) gives you one line at a time

## A Note on This Portal

The code you write here runs inside a browser-based Python environment (Pyodide), which provides a virtual, in-memory filesystem. `open("data.txt", "w")` works exactly like real file I/O, but the file only exists for the lifetime of that single run — there's no real disk, and nothing persists between runs. So every file-handling question here is self-contained: your script creates the file it needs, writes to it, and reads it back, all in one go.

File handling is how real applications store logs, configuration, and user data between runs.$md$,
$py$with open("notes.txt", "w") as f:
    f.write("Line one\n")
    f.write("Line two\n")

with open("notes.txt", "r") as f:
    content = f.read()
print(content)

with open("notes.txt", "a") as f:
    f.write("Line three\n")

with open("notes.txt", "r") as f:
    lines = f.readlines()
print(len(lines))
for line in lines:
    print(line.strip())$py$,
$txt$Line one
Line two

3
Line one
Line two
Line three
$txt$),

('a0000000-0000-0000-0000-000000000010', 'exception-handling', 'Exception Handling (try/except/finally)', 10,
$md$Even correct-looking code can fail at runtime — a user might type text where a number was expected, or you might divide by zero. Exception handling lets your program respond gracefully instead of crashing.

## try / except

Wrap risky code in a `try` block, and handle the failure in an `except` block:

    try:
        n = int(input())
        print(100 / n)
    except ValueError:
        print("That wasn't a number")
    except ZeroDivisionError:
        print("Can't divide by zero")

Python checks each `except` clause in order and runs the first one that matches the type of exception that was raised. You can catch several different exception types with separate `except` clauses, as shown above.

## else and finally

- An optional `else` block runs only if the `try` block completed **without** raising an exception.
- An optional `finally` block always runs, whether or not an exception occurred — useful for cleanup code (like closing a file) that must happen no matter what.

## Common Built-in Exceptions

- `ValueError` — a value has the right type but an invalid value, e.g. `int("abc")`
- `ZeroDivisionError` — dividing by zero
- `IndexError` — accessing a list index that doesn't exist
- `KeyError` — accessing a dictionary key that doesn't exist

## Why It Matters

Without handling, any of these errors would stop your program immediately. With a `try`/`except`, you decide what should happen instead — show a friendly message, use a default value, or try again.$md$,
$py$def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        return "Cannot divide by zero"
    else:
        return result
    finally:
        print("Division attempted")

print(safe_divide(10, 2))
print(safe_divide(5, 0))

try:
    number = int("abc")
except ValueError as e:
    print("Caught an error:", e)$py$,
$txt$Division attempted
5.0
Division attempted
Cannot divide by zero
Caught an error: invalid literal for int() with base 10: 'abc'
$txt$);

-- ============================================================================
-- 2. QUESTIONS (3 per topic: easy, medium, hard)
-- ============================================================================

-- ---- Topic 1: Variables and Data Types -------------------------------------
insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index) values

('b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001', 'Swap Two Numbers',
$md$Given two integers, swap their values and print the new values — without using any extra variable besides `a` and `b` themselves.

### Input Format
Two lines, each containing one integer: `a` and `b`.

### Output Format
Two lines: the new value of `a` after swapping, then the new value of `b`.

### Example
```
Input:
5
10

Output:
10
5
```$md$,
'easy', 10,
$py$a = int(input())
b = int(input())
# Write your code here: swap a and b, then print the new values$py$,
$txt$You can swap two variables in Python in a single line using tuple assignment: a, b = b, a.$txt$,
$py$a = int(input())
b = int(input())
a, b = b, a
print(a)
print(b)$py$,
1),

('b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000001', 'Simple Interest Calculator',
$md$Calculate the simple interest earned on a principal amount, given an annual interest rate and a time period, using the formula:

`interest = (principal * rate * time) / 100`

### Input Format
Three lines:
1. `principal` — an integer
2. `rate` — a float (annual interest rate, as a percentage)
3. `time` — an integer (number of years)

### Output Format
A single line with the simple interest, rounded to exactly 2 decimal places.

### Example
```
Input:
1000
5.5
2

Output:
110.00
```$md$,
'medium', 20,
$py$principal = int(input())
rate = float(input())
time = int(input())
# Write your code here: compute simple interest = (principal * rate * time) / 100
# and print it rounded to 2 decimal places$py$,
$txt$Use the formula (P * R * T) / 100 and format the result with :.2f so it always shows two decimal places.$txt$,
$py$principal = int(input())
rate = float(input())
time = int(input())
interest = (principal * rate * time) / 100
print(f"{interest:.2f}")$py$,
2),

('b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000001', 'Student Report Card Summary',
$md$Given a student's name and marks in three subjects, print a short report with their total and average marks.

### Input Format
Four lines:
1. `name` — the student's name
2. Math marks — an integer
3. Science marks — an integer
4. English marks — an integer

### Output Format
Three lines:
```
Name: <name>
Total: <sum of the three marks>
Average: <average of the three marks, rounded to 2 decimal places>
```

### Example
```
Input:
John
80
75
90

Output:
Name: John
Total: 245
Average: 81.67
```$md$,
'hard', 30,
$py$name = input()
math = int(input())
science = int(input())
english = int(input())
# Write your code here: print Name, Total and Average (2 decimal places)
# following the exact format shown in the example$py$,
$txt$Add the three marks together for the total, then divide by 3 for the average — use an f-string with :.2f to format the average to two decimal places.$txt$,
$py$name = input()
math = int(input())
science = int(input())
english = int(input())
total = math + science + english
average = total / 3
print(f"Name: {name}")
print(f"Total: {total}")
print(f"Average: {average:.2f}")$py$,
3);

-- ---- Topic 2: Input and Output ---------------------------------------------
insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index) values

('b0000000-0000-0000-0000-000000000004', 'a0000000-0000-0000-0000-000000000002', 'Greet the User',
$md$Read a user's name and age, and greet them with a single formatted sentence.

### Input Format
Two lines:
1. `name` — a string
2. `age` — an integer

### Output Format
A single line in the exact form: `Hello <name>, you are <age> years old.`

### Example
```
Input:
Alice
25

Output:
Hello Alice, you are 25 years old.
```$md$,
'easy', 10,
$py$name = input()
age = int(input())
# Write your code here: print the greeting in the exact format shown$py$,
$txt$Use an f-string to combine the name and age into a single sentence, following the exact spacing and punctuation shown in the example.$txt$,
$py$name = input()
age = int(input())
print(f"Hello {name}, you are {age} years old.")$py$,
1),

('b0000000-0000-0000-0000-000000000005', 'a0000000-0000-0000-0000-000000000002', 'Sum of Space-Separated Numbers',
$md$Read a single line containing several integers separated by spaces, and print their sum.

### Input Format
One line containing one or more integers, separated by single spaces.

### Output Format
A single integer: the sum of all the numbers.

### Example
```
Input:
3 5 7

Output:
15
```$md$,
'medium', 20,
$py$numbers = input().split()
# Write your code here: convert each piece to int, sum them, and print the total$py$,
$txt$input().split() gives you a list of strings. Convert each one to int before summing, e.g. with a generator expression or map().$txt$,
$py$numbers = input().split()
total = sum(int(x) for x in numbers)
print(total)$py$,
2),

('b0000000-0000-0000-0000-000000000006', 'a0000000-0000-0000-0000-000000000002', 'Formatted Invoice Line',
$md$You're given three purchased items. For each item you're given its name, quantity and unit price. Print a formatted line for every item showing its line total, followed by the grand total of all three.

### Input Format
Nine lines, three per item (name, then quantity as an integer, then unit price as a float), in order for three items.

### Output Format
Four lines — one per item in the form `<name>: <qty> x $<price> = $<total>`, followed by a final line `Grand Total: $<grand total>`. All money values must be shown with exactly 2 decimal places.

### Example
```
Input:
Pen
2
1.50
Notebook
3
2.25
Eraser
1
0.75

Output:
Pen: 2 x $1.50 = $3.00
Notebook: 3 x $2.25 = $6.75
Eraser: 1 x $0.75 = $0.75
Grand Total: $10.50
```$md$,
'hard', 30,
$py$name1 = input()
qty1 = int(input())
price1 = float(input())
name2 = input()
qty2 = int(input())
price2 = float(input())
name3 = input()
qty3 = int(input())
price3 = float(input())
# Write your code here: print each item's line and the grand total,
# following the exact format shown in the example$py$,
$txt$Compute each item's total as quantity * price, format every money value with :.2f, and add all three totals together for the grand total.$txt$,
$py$name1 = input()
qty1 = int(input())
price1 = float(input())
name2 = input()
qty2 = int(input())
price2 = float(input())
name3 = input()
qty3 = int(input())
price3 = float(input())

total1 = qty1 * price1
total2 = qty2 * price2
total3 = qty3 * price3

print(f"{name1}: {qty1} x ${price1:.2f} = ${total1:.2f}")
print(f"{name2}: {qty2} x ${price2:.2f} = ${total2:.2f}")
print(f"{name3}: {qty3} x ${price3:.2f} = ${total3:.2f}")
print(f"Grand Total: ${total1 + total2 + total3:.2f}")$py$,
3);

-- ---- Topic 3: Operators -----------------------------------------------------
insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index) values

('b0000000-0000-0000-0000-000000000007', 'a0000000-0000-0000-0000-000000000003', 'Add, Subtract, Multiply',
$md$Read two integers and print their sum, difference and product.

### Input Format
Two lines, each containing one integer: `a` and `b`.

### Output Format
Three lines in the exact form:
```
Sum: <a + b>
Difference: <a - b>
Product: <a * b>
```

### Example
```
Input:
6
3

Output:
Sum: 9
Difference: 3
Product: 18
```$md$,
'easy', 10,
$py$a = int(input())
b = int(input())
# Write your code here: print Sum, Difference, Product each on its own line$py$,
$txt$Print three lines using the labels exactly as shown: "Sum: ", "Difference: ", "Product: " followed by the computed value.$txt$,
$py$a = int(input())
b = int(input())
print(f"Sum: {a + b}")
print(f"Difference: {a - b}")
print(f"Product: {a * b}")$py$,
1),

('b0000000-0000-0000-0000-000000000008', 'a0000000-0000-0000-0000-000000000003', 'Division Details',
$md$Read two integers and print the results of integer (floor) division, the remainder, and true division between them.

### Input Format
Two lines, each containing one integer: `a` and `b` (`b` is never zero).

### Output Format
Three lines in the exact form:
```
Quotient: <a // b>
Remainder: <a % b>
Division: <a / b, rounded to 3 decimal places>
```

### Example
```
Input:
17
5

Output:
Quotient: 3
Remainder: 2
Division: 3.400
```$md$,
'medium', 20,
$py$a = int(input())
b = int(input())
# Write your code here: print Quotient, Remainder, and Division (3 decimal places)$py$,
$txt$Use // for integer (floor) division, % for remainder, and / for true division — format the true division result with :.3f.$txt$,
$py$a = int(input())
b = int(input())
print(f"Quotient: {a // b}")
print(f"Remainder: {a % b}")
print(f"Division: {a / b:.3f}")$py$,
2),

('b0000000-0000-0000-0000-000000000009', 'a0000000-0000-0000-0000-000000000003', 'Eligibility Checker with Logical Operators',
$md$A person qualifies for a scheme either if they are at least 18 years old **and** have an ID, or if their income is at least 50000, whichever applies. Read their details and print each individual check plus the final eligibility result.

### Input Format
Three lines:
1. `age` — an integer
2. `has_id` — the string `yes` or `no`
3. `income` — a float

### Output Format
Four lines in the exact form:
```
Age OK: <True/False>
Has ID: <True/False>
High Income: <True/False>
Eligible: <True/False>
```

### Example
```
Input:
20
yes
30000

Output:
Age OK: True
Has ID: True
High Income: False
Eligible: True
```$md$,
'hard', 30,
$py$age = int(input())
has_id = input()
income = float(input())
# Write your code here: print the four lines shown in the example,
# using comparison and logical operators (and, or)$py$,
$txt$Build boolean values with comparison operators (>=, ==) and combine them using "and" / "or". Remember "and" binds tighter than "or", so (age >= 18 and has_id == "yes") or income >= 50000 checks either condition.$txt$,
$py$age = int(input())
has_id = input()
income = float(input())

age_ok = age >= 18
has_id_ok = has_id == "yes"
high_income = income >= 50000

eligible = (age_ok and has_id_ok) or high_income

print(f"Age OK: {age_ok}")
print(f"Has ID: {has_id_ok}")
print(f"High Income: {high_income}")
print(f"Eligible: {eligible}")$py$,
3);

-- ---- Topic 4: Conditional Statements ----------------------------------------
insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index) values

('b0000000-0000-0000-0000-000000000010', 'a0000000-0000-0000-0000-000000000004', 'Positive, Negative or Zero',
$md$Read an integer and print whether it is positive, negative, or zero.

### Input Format
One line containing an integer `n`.

### Output Format
A single word: `Positive`, `Negative`, or `Zero`.

### Example
```
Input:
7

Output:
Positive
```$md$,
'easy', 10,
$py$n = int(input())
# Write your code here: print "Positive", "Negative", or "Zero"$py$,
$txt$Use if / elif / else, checking n > 0 first, then n < 0, with an else for zero.$txt$,
$py$n = int(input())
if n > 0:
    print("Positive")
elif n < 0:
    print("Negative")
else:
    print("Zero")$py$,
1),

('b0000000-0000-0000-0000-000000000011', 'a0000000-0000-0000-0000-000000000004', 'Grade Calculator',
$md$Read a student's marks (0 to 100) and print their letter grade using this scale:

- `90` and above → `A`
- `75` to `89` → `B`
- `60` to `74` → `C`
- `40` to `59` → `D`
- below `40` → `F`

### Input Format
One line containing an integer `marks`.

### Output Format
A single letter: the grade.

### Example
```
Input:
82

Output:
B
```$md$,
'medium', 20,
$py$marks = int(input())
# Write your code here: print the grade using if/elif/else$py$,
$txt$Check the highest threshold first (marks >= 90) and work downward with elif, ending with an else for F.$txt$,
$py$marks = int(input())
if marks >= 90:
    print("A")
elif marks >= 75:
    print("B")
elif marks >= 60:
    print("C")
elif marks >= 40:
    print("D")
else:
    print("F")$py$,
2),

('b0000000-0000-0000-0000-000000000012', 'a0000000-0000-0000-0000-000000000004', 'Triangle Type Classifier',
$md$Given the three side lengths of a triangle, first check if they can actually form a valid triangle (each side must be shorter than the sum of the other two). If not, print `Not a triangle`. Otherwise, classify the triangle as `Equilateral` (all sides equal), `Isosceles` (exactly two sides equal), or `Scalene` (all sides different), and also report whether it's a right triangle (using the Pythagorean theorem).

### Input Format
Three lines, each an integer side length: `a`, `b`, `c`.

### Output Format
If invalid: a single line `Not a triangle`.
If valid: two lines — the triangle type, then `Right triangle` or `Not a right triangle`.

### Example
```
Input:
3
4
5

Output:
Scalene
Right triangle
```$md$,
'hard', 30,
$py$a = int(input())
b = int(input())
c = int(input())
# Write your code here: classify the triangle as shown in the example$py$,
$txt$First check the triangle inequality (each side must be less than the sum of the other two). Then compare the three sides for equality to classify the type, and use the Pythagorean theorem on the sorted sides to check for a right angle.$txt$,
$py$a = int(input())
b = int(input())
c = int(input())

if a + b <= c or a + c <= b or b + c <= a:
    print("Not a triangle")
else:
    if a == b == c:
        print("Equilateral")
    elif a == b or b == c or a == c:
        print("Isosceles")
    else:
        print("Scalene")

    sides = sorted([a, b, c])
    if sides[0] ** 2 + sides[1] ** 2 == sides[2] ** 2:
        print("Right triangle")
    else:
        print("Not a right triangle")$py$,
3);

-- ---- Topic 5: Loops ----------------------------------------------------------
insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index) values

('b0000000-0000-0000-0000-000000000013', 'a0000000-0000-0000-0000-000000000005', 'Print Numbers 1 to N',
$md$Read an integer `n` and print every integer from `1` to `n`, one per line.

### Input Format
One line containing an integer `n` (`n` may be `0`).

### Output Format
`n` lines, each containing the next integer starting from `1`. If `n` is `0`, print nothing.

### Example
```
Input:
5

Output:
1
2
3
4
5
```$md$,
'easy', 10,
$py$n = int(input())
# Write your code here: print numbers from 1 to n, each on its own line$py$,
$txt$Use a for loop with range(1, n + 1).$txt$,
$py$n = int(input())
for i in range(1, n + 1):
    print(i)$py$,
1),

('b0000000-0000-0000-0000-000000000014', 'a0000000-0000-0000-0000-000000000005', 'Sum of Digits',
$md$Read a non-negative integer and print the sum of its digits.

### Input Format
One line containing an integer `n`.

### Output Format
A single integer: the sum of the digits of `n`.

### Example
```
Input:
12345

Output:
15
```$md$,
'medium', 20,
$py$n = int(input())
# Write your code here: compute the sum of digits of n using a while loop$py$,
$txt$Repeatedly use n % 10 to get the last digit and n //= 10 to remove it, accumulating the sum until n becomes 0.$txt$,
$py$n = int(input())
total = 0
while n > 0:
    total += n % 10
    n //= 10
print(total)$py$,
2),

('b0000000-0000-0000-0000-000000000015', 'a0000000-0000-0000-0000-000000000005', 'Prime Check and Factor Sum',
$md$Read a positive integer `n`. Find every divisor of `n` (from `1` to `n`), and use them to determine whether `n` is prime and what the sum of all its divisors is.

### Input Format
One line containing an integer `n` (`n >= 1`).

### Output Format
Two lines in the exact form:
```
Prime: <True/False>
Divisor Sum: <sum of all divisors of n>
```

### Example
```
Input:
6

Output:
Prime: False
Divisor Sum: 12
```$md$,
'hard', 30,
$py$n = int(input())
# Write your code here: use a loop to find all divisors of n,
# determine if n is prime, and print both results as shown$py$,
$txt$Loop i from 1 to n (inclusive) with a for loop, check n % i == 0 to find divisors, add qualifying i to a running sum, and count them — a count of exactly 2 means n is prime (this works correctly even for n = 1).$txt$,
$py$n = int(input())
divisor_sum = 0
divisor_count = 0
for i in range(1, n + 1):
    if n % i == 0:
        divisor_sum += i
        divisor_count += 1

is_prime = divisor_count == 2
print(f"Prime: {is_prime}")
print(f"Divisor Sum: {divisor_sum}")$py$,
3);

-- ---- Topic 6: Strings ---------------------------------------------------------
insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index) values

('b0000000-0000-0000-0000-000000000016', 'a0000000-0000-0000-0000-000000000006', 'Reverse a String',
$md$Read a line of text and print it reversed.

### Input Format
One line containing a string `s`.

### Output Format
The string `s` reversed.

### Example
```
Input:
hello

Output:
olleh
```$md$,
'easy', 10,
$py$s = input()
# Write your code here: print the reverse of s$py$,
$txt$Python slicing s[::-1] reverses a string in one step.$txt$,
$py$s = input()
print(s[::-1])$py$,
1),

('b0000000-0000-0000-0000-000000000017', 'a0000000-0000-0000-0000-000000000006', 'Count Vowels and Consonants',
$md$Read a line of text and count how many letters in it are vowels and how many are consonants. Ignore spaces and any non-letter characters.

### Input Format
One line containing a string `s`.

### Output Format
Two lines in the exact form:
```
Vowels: <count>
Consonants: <count>
```

### Example
```
Input:
Hello World

Output:
Vowels: 3
Consonants: 7
```$md$,
'medium', 20,
$py$s = input()
# Write your code here: count vowels and consonants in s (letters only)$py$,
$txt$Loop through each character, use .lower() and check membership in "aeiou" for vowels, and use .isalpha() to decide whether a non-vowel letter counts as a consonant.$txt$,
$py$s = input()
vowels = 0
consonants = 0
for ch in s:
    if ch.isalpha():
        if ch.lower() in "aeiou":
            vowels += 1
        else:
            consonants += 1
print(f"Vowels: {vowels}")
print(f"Consonants: {consonants}")$py$,
2),

('b0000000-0000-0000-0000-000000000018', 'a0000000-0000-0000-0000-000000000006', 'Palindrome and Anagram Checker',
$md$Read two lines of text. Check whether the first one is a palindrome, and whether the two are anagrams of each other — in both cases, ignore letter case and spaces.

### Input Format
Two lines: `s1`, then `s2`.

### Output Format
Two lines in the exact form:
```
Palindrome: <True/False>
Anagram: <True/False>
```

### Example
```
Input:
Madam
madam

Output:
Palindrome: True
Anagram: True
```$md$,
'hard', 30,
$py$s1 = input()
s2 = input()
# Write your code here: check if s1 is a palindrome and if s1/s2 are anagrams
# (ignore case and spaces for both checks)$py$,
$txt$Clean each string first with .lower().replace(" ", ""), then compare the cleaned s1 to its reverse for the palindrome check, and compare sorted(cleaned s1) to sorted(cleaned s2) for the anagram check.$txt$,
$py$s1 = input()
s2 = input()

clean1 = s1.lower().replace(" ", "")
clean2 = s2.lower().replace(" ", "")

is_palindrome = clean1 == clean1[::-1]
is_anagram = sorted(clean1) == sorted(clean2)

print(f"Palindrome: {is_palindrome}")
print(f"Anagram: {is_anagram}")$py$,
3);

-- ---- Topic 7: Collections -------------------------------------------------------
insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index) values

('b0000000-0000-0000-0000-000000000019', 'a0000000-0000-0000-0000-000000000007', 'List Statistics',
$md$Read a line of space-separated integers and print their sum, maximum, and minimum.

### Input Format
One line of one or more integers, separated by spaces.

### Output Format
Three lines in the exact form:
```
Sum: <sum>
Max: <maximum value>
Min: <minimum value>
```

### Example
```
Input:
4 8 2 9 5

Output:
Sum: 28
Max: 9
Min: 2
```$md$,
'easy', 10,
$py$numbers = list(map(int, input().split()))
# Write your code here: print Sum, Max, and Min$py$,
$txt$Use Python's built-in sum(), max(), and min() functions on the list.$txt$,
$py$numbers = list(map(int, input().split()))
print(f"Sum: {sum(numbers)}")
print(f"Max: {max(numbers)}")
print(f"Min: {min(numbers)}")$py$,
1),

('b0000000-0000-0000-0000-000000000020', 'a0000000-0000-0000-0000-000000000007', 'Remove Duplicates and Sort',
$md$Read a line of space-separated integers, remove any duplicates, and print the remaining values sorted in ascending order, space-separated.

### Input Format
One line of one or more integers, separated by spaces.

### Output Format
The unique values, sorted ascending, separated by single spaces.

### Example
```
Input:
5 3 5 1 3 2

Output:
1 2 3 5
```$md$,
'medium', 20,
$py$numbers = list(map(int, input().split()))
# Write your code here: print unique values, sorted ascending, space-separated$py$,
$txt$Convert the list to a set to remove duplicates, then sort it and join the values with " ".join() (remember to convert each number back to a string first).$txt$,
$py$numbers = list(map(int, input().split()))
unique_sorted = sorted(set(numbers))
print(" ".join(str(x) for x in unique_sorted))$py$,
2),

('b0000000-0000-0000-0000-000000000021', 'a0000000-0000-0000-0000-000000000007', 'Word Frequency Counter',
$md$Read a line of space-separated words, and print how many times each unique word (case-insensitive) appears, listed in alphabetical order.

### Input Format
One line of one or more words, separated by spaces.

### Output Format
One line per unique word (lowercased), in alphabetical order, in the form `<word>: <count>`.

### Example
```
Input:
the cat sat on the mat the cat ran

Output:
cat: 2
mat: 1
on: 1
ran: 1
sat: 1
the: 3
```$md$,
'hard', 30,
$py$words = input().lower().split()
# Write your code here: count occurrences of each word and print them
# alphabetically as "word: count", one per line$py$,
$txt$Build a dictionary by looping through the words and incrementing a counter for each one (counts.get(word, 0) + 1 works well), then use sorted() on the dictionary's keys to print them in alphabetical order.$txt$,
$py$words = input().lower().split()
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1

for word in sorted(counts):
    print(f"{word}: {counts[word]}")$py$,
3);

-- ---- Topic 8: Functions -----------------------------------------------------------
insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index) values

('b0000000-0000-0000-0000-000000000022', 'a0000000-0000-0000-0000-000000000008', 'Function to Check Even/Odd',
$md$Write a function `is_even(n)` that returns whether `n` is even, then use it to print the result for a given number.

### Input Format
One line containing an integer `n`.

### Output Format
A single word: `Even` or `Odd`.

### Example
```
Input:
4

Output:
Even
```$md$,
'easy', 10,
$py$def is_even(n):
    # Write your code here: return True if n is even, False otherwise
    pass

n = int(input())
if is_even(n):
    print("Even")
else:
    print("Odd")$py$,
$txt$A number is even if n % 2 == 0 — return that expression directly.$txt$,
$py$def is_even(n):
    return n % 2 == 0

n = int(input())
if is_even(n):
    print("Even")
else:
    print("Odd")$py$,
1),

('b0000000-0000-0000-0000-000000000023', 'a0000000-0000-0000-0000-000000000008', 'Factorial Function',
$md$Write a function `factorial(n)` that computes `n!` (the product of all integers from `1` to `n`, with `0! = 1`), then print the result for a given number.

### Input Format
One line containing an integer `n` (`0 <= n <= 12`).

### Output Format
A single integer: `n!`.

### Example
```
Input:
5

Output:
120
```$md$,
'medium', 20,
$py$def factorial(n):
    # Write your code here: return n! (factorial of n)
    pass

n = int(input())
print(factorial(n))$py$,
$txt$Factorial of 0 is 1 by definition; for n > 0, build the product iteratively by multiplying all integers from 2 up to and including n.$txt$,
$py$def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

n = int(input())
print(factorial(n))$py$,
2),

('b0000000-0000-0000-0000-000000000024', 'a0000000-0000-0000-0000-000000000008', 'Function Toolkit: GCD and LCM',
$md$Write two functions, `gcd(a, b)` and `lcm(a, b)`, to compute the greatest common divisor and least common multiple of two positive integers, then print both.

### Input Format
Two lines, each a positive integer: `a`, then `b`.

### Output Format
Two lines in the exact form:
```
GCD: <gcd of a and b>
LCM: <lcm of a and b>
```

### Example
```
Input:
12
18

Output:
GCD: 6
LCM: 36
```$md$,
'hard', 30,
$py$def gcd(a, b):
    # Write your code here: return the greatest common divisor of a and b
    pass

def lcm(a, b):
    # Write your code here: return the least common multiple of a and b
    # (hint: use the gcd function above)
    pass

a = int(input())
b = int(input())
print(f"GCD: {gcd(a, b)}")
print(f"LCM: {lcm(a, b)}")$py$,
$txt$Implement gcd with the Euclidean algorithm (while b: a, b = b, a % b), then compute lcm as (a * b) // gcd(a, b).$txt$,
$py$def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return (a * b) // gcd(a, b)

a = int(input())
b = int(input())
print(f"GCD: {gcd(a, b)}")
print(f"LCM: {lcm(a, b)}")$py$,
3);

-- ---- Topic 9: File Handling --------------------------------------------------------
insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index) values

('b0000000-0000-0000-0000-000000000025', 'a0000000-0000-0000-0000-000000000009', 'Write and Count Lines',
$md$Read a number of lines of text, write them into a file, then read that file back and print how many lines it contains.

### Input Format
First line: an integer `n`. Then `n` more lines of text.

### Output Format
A single integer: the number of lines found in the file after reading it back.

### Example
```
Input:
3
apple
banana
cherry

Output:
3
```$md$,
'easy', 10,
$py$n = int(input())
lines = []
for _ in range(n):
    lines.append(input())

# Write your code here: write the lines to a file named "data.txt"
# (one per line), then read the file back and print how many lines it has$py$,
$txt$Open the file with mode "w" and write each line followed by "\n", then reopen it with mode "r" and use readlines() to count the lines.$txt$,
$py$n = int(input())
lines = []
for _ in range(n):
    lines.append(input())

with open("data.txt", "w") as f:
    for line in lines:
        f.write(line + "\n")

with open("data.txt", "r") as f:
    file_lines = f.readlines()

print(len(file_lines))$py$,
1),

('b0000000-0000-0000-0000-000000000026', 'a0000000-0000-0000-0000-000000000009', 'Word Count in File',
$md$Read a number of lines of text, write them into a file, then read the file back and count the total number of words across all lines.

### Input Format
First line: an integer `n`. Then `n` more lines of text.

### Output Format
A single integer: the total word count.

### Example
```
Input:
2
The quick brown fox
jumps over the lazy dog

Output:
9
```$md$,
'medium', 20,
$py$n = int(input())
lines = []
for _ in range(n):
    lines.append(input())

# Write your code here: write the lines to "essay.txt", read the file back,
# and print the total number of words across all lines$py$,
$txt$After writing each line (with a newline) to the file, read the whole file back with read(), then use .split() on the full text — it splits on any whitespace, including newlines — and count the resulting list.$txt$,
$py$n = int(input())
lines = []
for _ in range(n):
    lines.append(input())

with open("essay.txt", "w") as f:
    for line in lines:
        f.write(line + "\n")

with open("essay.txt", "r") as f:
    content = f.read()

word_count = len(content.split())
print(word_count)$py$,
2),

('b0000000-0000-0000-0000-000000000027', 'a0000000-0000-0000-0000-000000000009', 'CSV-like Record Processor',
$md$You're given a number of student records, each in the form `name,score`. Write all the records to a file, then read the file back and determine which student has the highest score and what the average score is.

### Input Format
First line: an integer `n`. Then `n` more lines, each in the form `name,score` (score is an integer).

### Output Format
Two lines in the exact form:
```
Top: <name of the student with the highest score>
Average: <average score, rounded to 2 decimal places>
```

### Example
```
Input:
3
Alice,85
Bob,92
Cara,78

Output:
Top: Bob
Average: 85.00
```$md$,
'hard', 30,
$py$n = int(input())
records = []
for _ in range(n):
    records.append(input())

# Write your code here:
# 1. Write each record line to a file named "scores.txt"
# 2. Read the file back and parse each "name,score" line
# 3. Print the name with the highest score, and the average score (2 decimals)$py$,
$txt$Write each raw line as-is to the file. When reading it back, use line.strip().split(",") to separate the name and score, convert the score to int, and track the running maximum and sum as you go through each record.$txt$,
$py$n = int(input())
records = []
for _ in range(n):
    records.append(input())

with open("scores.txt", "w") as f:
    for record in records:
        f.write(record + "\n")

with open("scores.txt", "r") as f:
    file_lines = f.readlines()

top_name = ""
top_score = None
total = 0

for line in file_lines:
    name, score_str = line.strip().split(",")
    score = int(score_str)
    total += score
    if top_score is None or score > top_score:
        top_score = score
        top_name = name

average = total / n
print(f"Top: {top_name}")
print(f"Average: {average:.2f}")$py$,
3);

-- ---- Topic 10: Exception Handling -------------------------------------------------
insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index) values

('b0000000-0000-0000-0000-000000000028', 'a0000000-0000-0000-0000-000000000010', 'Safe Integer Conversion',
$md$Read a line of text. If it's a valid integer, print double its value. Otherwise, print an error message.

### Input Format
One line containing a string `s`.

### Output Format
If `s` can be converted to an integer: a single integer, double its value.
Otherwise: the line `Invalid integer`.

### Example
```
Input:
21

Output:
42
```$md$,
'easy', 10,
$py$s = input()
# Write your code here: try to convert s to int and print it doubled;
# if it's not a valid integer, print "Invalid integer"$py$,
$txt$Wrap the int(s) conversion in a try/except block, catching ValueError specifically.$txt$,
$py$s = input()
try:
    n = int(s)
    print(n * 2)
except ValueError:
    print("Invalid integer")$py$,
1),

('b0000000-0000-0000-0000-000000000029', 'a0000000-0000-0000-0000-000000000010', 'Safe Division with Multiple Exceptions',
$md$Read two values and attempt to divide the first by the second. Handle two kinds of problems separately: the values might not be valid integers, or the second value might be zero.

### Input Format
Two lines: `a`, then `b` (both read as text).

### Output Format
- If either value isn't a valid integer: `Error: Invalid number`
- Otherwise, if `b` is `0`: `Error: Division by zero`
- Otherwise: `a / b`, rounded to 2 decimal places

### Example
```
Input:
10
2

Output:
5.00
```$md$,
'medium', 20,
$py$a_str = input()
b_str = input()
# Write your code here: try converting both to int and dividing a/b.
# Catch ValueError -> print "Error: Invalid number"
# Catch ZeroDivisionError -> print "Error: Division by zero"
# Otherwise print the result rounded to 2 decimals$py$,
$txt$Put the int() conversions and the division inside the same try block, then use two except clauses — one for ValueError, one for ZeroDivisionError — in that order.$txt$,
$py$a_str = input()
b_str = input()
try:
    a = int(a_str)
    b = int(b_str)
    result = a / b
    print(f"{result:.2f}")
except ValueError:
    print("Error: Invalid number")
except ZeroDivisionError:
    print("Error: Division by zero")$py$,
2),

('b0000000-0000-0000-0000-000000000030', 'a0000000-0000-0000-0000-000000000010', 'Robust List Indexer with Finally',
$md$Read a list of integers and an index. Try to access the list at that index, handling both an invalid (non-integer) index and an out-of-range index — and always report that the operation finished, no matter what happened.

### Input Format
Two lines:
1. A line of space-separated integers (the list)
2. A line containing the index to access (read as text, since it might not be a valid integer)

### Output Format
First, one of:
```
Value: <the value at that index>
Error: Index must be an integer
Error: Index out of range
```
Then, on the next line, always:
```
Operation complete
```

### Example
```
Input:
10 20 30 40
2

Output:
Value: 30
Operation complete
```$md$,
'hard', 30,
$py$numbers = list(map(int, input().split()))
index_str = input()
# Write your code here: try to convert index_str to int and access
# numbers[index]. Handle ValueError and IndexError with the messages
# described, and use finally to always print "Operation complete".$py$,
$txt$Structure it as try / except ValueError / except IndexError / finally — the finally block runs no matter which branch executes, so put the "Operation complete" print there.$txt$,
$py$numbers = list(map(int, input().split()))
index_str = input()

try:
    index = int(index_str)
    value = numbers[index]
    print(f"Value: {value}")
except ValueError:
    print("Error: Index must be an integer")
except IndexError:
    print("Error: Index out of range")
finally:
    print("Operation complete")$py$,
3);

-- ============================================================================
-- 3. TEST CASES
-- ============================================================================

-- ---- Topic 1 test cases -------------------------------------------------------
insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values
-- Swap Two Numbers (b...0001)
('b0000000-0000-0000-0000-000000000001', $txt$5
10$txt$, $txt$10
5$txt$, true, 0),
('b0000000-0000-0000-0000-000000000001', $txt$-3
7$txt$, $txt$7
-3$txt$, false, 1),
('b0000000-0000-0000-0000-000000000001', $txt$0
0$txt$, $txt$0
0$txt$, false, 2),
-- Simple Interest Calculator (b...0002)
('b0000000-0000-0000-0000-000000000002', $txt$1000
5.5
2$txt$, $txt$110.00$txt$, true, 0),
('b0000000-0000-0000-0000-000000000002', $txt$2500
3.25
4$txt$, $txt$325.00$txt$, false, 1),
('b0000000-0000-0000-0000-000000000002', $txt$0
10
5$txt$, $txt$0.00$txt$, false, 2),
('b0000000-0000-0000-0000-000000000002', $txt$100
7
1$txt$, $txt$7.00$txt$, false, 3),
-- Student Report Card Summary (b...0003)
('b0000000-0000-0000-0000-000000000003', $txt$John
80
75
90$txt$, $txt$Name: John
Total: 245
Average: 81.67$txt$, true, 0),
('b0000000-0000-0000-0000-000000000003', $txt$Priya
100
100
100$txt$, $txt$Name: Priya
Total: 300
Average: 100.00$txt$, false, 1),
('b0000000-0000-0000-0000-000000000003', $txt$Zero
0
0
0$txt$, $txt$Name: Zero
Total: 0
Average: 0.00$txt$, false, 2),
('b0000000-0000-0000-0000-000000000003', $txt$Ana
50
60
70$txt$, $txt$Name: Ana
Total: 180
Average: 60.00$txt$, false, 3),
('b0000000-0000-0000-0000-000000000003', $txt$Max
99
1
1$txt$, $txt$Name: Max
Total: 101
Average: 33.67$txt$, false, 4);

-- ---- Topic 2 test cases -------------------------------------------------------
insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values
-- Greet the User (b...0004)
('b0000000-0000-0000-0000-000000000004', $txt$Alice
25$txt$, $txt$Hello Alice, you are 25 years old.$txt$, true, 0),
('b0000000-0000-0000-0000-000000000004', $txt$Bob
30$txt$, $txt$Hello Bob, you are 30 years old.$txt$, false, 1),
('b0000000-0000-0000-0000-000000000004', $txt$Zed
0$txt$, $txt$Hello Zed, you are 0 years old.$txt$, false, 2),
-- Sum of Space-Separated Numbers (b...0005)
('b0000000-0000-0000-0000-000000000005', $txt$3 5 7$txt$, $txt$15$txt$, true, 0),
('b0000000-0000-0000-0000-000000000005', $txt$10 -2 -3 5$txt$, $txt$10$txt$, false, 1),
('b0000000-0000-0000-0000-000000000005', $txt$0$txt$, $txt$0$txt$, false, 2),
('b0000000-0000-0000-0000-000000000005', $txt$1 2 3 4 5 6 7 8 9 10$txt$, $txt$55$txt$, false, 3),
-- Formatted Invoice Line (b...0006)
('b0000000-0000-0000-0000-000000000006', $txt$Pen
2
1.50
Notebook
3
2.25
Eraser
1
0.75$txt$, $txt$Pen: 2 x $1.50 = $3.00
Notebook: 3 x $2.25 = $6.75
Eraser: 1 x $0.75 = $0.75
Grand Total: $10.50$txt$, true, 0),
('b0000000-0000-0000-0000-000000000006', $txt$A
0
0
B
0
0
C
0
0$txt$, $txt$A: 0 x $0.00 = $0.00
B: 0 x $0.00 = $0.00
C: 0 x $0.00 = $0.00
Grand Total: $0.00$txt$, false, 1),
('b0000000-0000-0000-0000-000000000006', $txt$Book
5
9.99
Pen
10
0.50
Bag
1
25.00$txt$, $txt$Book: 5 x $9.99 = $49.95
Pen: 10 x $0.50 = $5.00
Bag: 1 x $25.00 = $25.00
Grand Total: $79.95$txt$, false, 2),
('b0000000-0000-0000-0000-000000000006', $txt$X
2
10.00
Y
2
10.00
Z
2
10.00$txt$, $txt$X: 2 x $10.00 = $20.00
Y: 2 x $10.00 = $20.00
Z: 2 x $10.00 = $20.00
Grand Total: $60.00$txt$, false, 3),
('b0000000-0000-0000-0000-000000000006', $txt$Milk
1
2.49
Bread
2
1.99
Eggs
1
3.49$txt$, $txt$Milk: 1 x $2.49 = $2.49
Bread: 2 x $1.99 = $3.98
Eggs: 1 x $3.49 = $3.49
Grand Total: $9.96$txt$, false, 4);

-- ---- Topic 3 test cases -------------------------------------------------------
insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values
-- Add, Subtract, Multiply (b...0007)
('b0000000-0000-0000-0000-000000000007', $txt$6
3$txt$, $txt$Sum: 9
Difference: 3
Product: 18$txt$, true, 0),
('b0000000-0000-0000-0000-000000000007', $txt$-4
10$txt$, $txt$Sum: 6
Difference: -14
Product: -40$txt$, false, 1),
('b0000000-0000-0000-0000-000000000007', $txt$0
0$txt$, $txt$Sum: 0
Difference: 0
Product: 0$txt$, false, 2),
-- Division Details (b...0008)
('b0000000-0000-0000-0000-000000000008', $txt$17
5$txt$, $txt$Quotient: 3
Remainder: 2
Division: 3.400$txt$, true, 0),
('b0000000-0000-0000-0000-000000000008', $txt$-17
5$txt$, $txt$Quotient: -4
Remainder: 3
Division: -3.400$txt$, false, 1),
('b0000000-0000-0000-0000-000000000008', $txt$9
3$txt$, $txt$Quotient: 3
Remainder: 0
Division: 3.000$txt$, false, 2),
('b0000000-0000-0000-0000-000000000008', $txt$7
2$txt$, $txt$Quotient: 3
Remainder: 1
Division: 3.500$txt$, false, 3),
-- Eligibility Checker with Logical Operators (b...0009)
('b0000000-0000-0000-0000-000000000009', $txt$20
yes
30000$txt$, $txt$Age OK: True
Has ID: True
High Income: False
Eligible: True$txt$, true, 0),
('b0000000-0000-0000-0000-000000000009', $txt$16
yes
10000$txt$, $txt$Age OK: False
Has ID: True
High Income: False
Eligible: False$txt$, false, 1),
('b0000000-0000-0000-0000-000000000009', $txt$16
no
60000$txt$, $txt$Age OK: False
Has ID: False
High Income: True
Eligible: True$txt$, false, 2),
('b0000000-0000-0000-0000-000000000009', $txt$25
no
20000$txt$, $txt$Age OK: True
Has ID: False
High Income: False
Eligible: False$txt$, false, 3),
('b0000000-0000-0000-0000-000000000009', $txt$18
yes
49999$txt$, $txt$Age OK: True
Has ID: True
High Income: False
Eligible: True$txt$, false, 4);

-- ---- Topic 4 test cases -------------------------------------------------------
insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values
-- Positive, Negative or Zero (b...0010)
('b0000000-0000-0000-0000-000000000010', $txt$7$txt$, $txt$Positive$txt$, true, 0),
('b0000000-0000-0000-0000-000000000010', $txt$-5$txt$, $txt$Negative$txt$, false, 1),
('b0000000-0000-0000-0000-000000000010', $txt$0$txt$, $txt$Zero$txt$, false, 2),
-- Grade Calculator (b...0011)
('b0000000-0000-0000-0000-000000000011', $txt$82$txt$, $txt$B$txt$, true, 0),
('b0000000-0000-0000-0000-000000000011', $txt$95$txt$, $txt$A$txt$, false, 1),
('b0000000-0000-0000-0000-000000000011', $txt$55$txt$, $txt$D$txt$, false, 2),
('b0000000-0000-0000-0000-000000000011', $txt$30$txt$, $txt$F$txt$, false, 3),
-- Triangle Type Classifier (b...0012)
('b0000000-0000-0000-0000-000000000012', $txt$3
4
5$txt$, $txt$Scalene
Right triangle$txt$, true, 0),
('b0000000-0000-0000-0000-000000000012', $txt$1
1
5$txt$, $txt$Not a triangle$txt$, false, 1),
('b0000000-0000-0000-0000-000000000012', $txt$5
5
5$txt$, $txt$Equilateral
Not a right triangle$txt$, false, 2),
('b0000000-0000-0000-0000-000000000012', $txt$5
5
8$txt$, $txt$Isosceles
Not a right triangle$txt$, false, 3),
('b0000000-0000-0000-0000-000000000012', $txt$6
8
10$txt$, $txt$Scalene
Right triangle$txt$, false, 4);

-- ---- Topic 5 test cases -------------------------------------------------------
insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values
-- Print Numbers 1 to N (b...0013)
('b0000000-0000-0000-0000-000000000013', $txt$5$txt$, $txt$1
2
3
4
5$txt$, true, 0),
('b0000000-0000-0000-0000-000000000013', $txt$1$txt$, $txt$1$txt$, false, 1),
('b0000000-0000-0000-0000-000000000013', $txt$0$txt$, '', false, 2),
-- Sum of Digits (b...0014)
('b0000000-0000-0000-0000-000000000014', $txt$12345$txt$, $txt$15$txt$, true, 0),
('b0000000-0000-0000-0000-000000000014', $txt$0$txt$, $txt$0$txt$, false, 1),
('b0000000-0000-0000-0000-000000000014', $txt$9$txt$, $txt$9$txt$, false, 2),
('b0000000-0000-0000-0000-000000000014', $txt$100$txt$, $txt$1$txt$, false, 3),
-- Prime Check and Factor Sum (b...0015)
('b0000000-0000-0000-0000-000000000015', $txt$6$txt$, $txt$Prime: False
Divisor Sum: 12$txt$, true, 0),
('b0000000-0000-0000-0000-000000000015', $txt$7$txt$, $txt$Prime: True
Divisor Sum: 8$txt$, false, 1),
('b0000000-0000-0000-0000-000000000015', $txt$1$txt$, $txt$Prime: False
Divisor Sum: 1$txt$, false, 2),
('b0000000-0000-0000-0000-000000000015', $txt$28$txt$, $txt$Prime: False
Divisor Sum: 56$txt$, false, 3),
('b0000000-0000-0000-0000-000000000015', $txt$2$txt$, $txt$Prime: True
Divisor Sum: 3$txt$, false, 4);

-- ---- Topic 6 test cases -------------------------------------------------------
insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values
-- Reverse a String (b...0016)
('b0000000-0000-0000-0000-000000000016', $txt$hello$txt$, $txt$olleh$txt$, true, 0),
('b0000000-0000-0000-0000-000000000016', $txt$Python$txt$, $txt$nohtyP$txt$, false, 1),
('b0000000-0000-0000-0000-000000000016', $txt$
$txt$, '', false, 2),
-- Count Vowels and Consonants (b...0017)
('b0000000-0000-0000-0000-000000000017', $txt$Hello World$txt$, $txt$Vowels: 3
Consonants: 7$txt$, true, 0),
('b0000000-0000-0000-0000-000000000017', $txt$Python Programming$txt$, $txt$Vowels: 4
Consonants: 13$txt$, false, 1),
('b0000000-0000-0000-0000-000000000017', $txt$
$txt$, $txt$Vowels: 0
Consonants: 0$txt$, false, 2),
('b0000000-0000-0000-0000-000000000017', $txt$xyz XYZ$txt$, $txt$Vowels: 0
Consonants: 6$txt$, false, 3),
-- Palindrome and Anagram Checker (b...0018)
('b0000000-0000-0000-0000-000000000018', $txt$Madam
madam$txt$, $txt$Palindrome: True
Anagram: True$txt$, true, 0),
('b0000000-0000-0000-0000-000000000018', $txt$Hello
World$txt$, $txt$Palindrome: False
Anagram: False$txt$, false, 1),
('b0000000-0000-0000-0000-000000000018', $txt$Was it a car or a cat I saw
x$txt$, $txt$Palindrome: True
Anagram: False$txt$, false, 2),
('b0000000-0000-0000-0000-000000000018', $txt$Listen
Silent$txt$, $txt$Palindrome: False
Anagram: True$txt$, false, 3),
('b0000000-0000-0000-0000-000000000018', $txt$

$txt$, $txt$Palindrome: True
Anagram: True$txt$, false, 4);

-- ---- Topic 7 test cases -------------------------------------------------------
insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values
-- List Statistics (b...0019)
('b0000000-0000-0000-0000-000000000019', $txt$4 8 2 9 5$txt$, $txt$Sum: 28
Max: 9
Min: 2$txt$, true, 0),
('b0000000-0000-0000-0000-000000000019', $txt$10$txt$, $txt$Sum: 10
Max: 10
Min: 10$txt$, false, 1),
('b0000000-0000-0000-0000-000000000019', $txt$-5 -1 -10 0$txt$, $txt$Sum: -16
Max: 0
Min: -10$txt$, false, 2),
-- Remove Duplicates and Sort (b...0020)
('b0000000-0000-0000-0000-000000000020', $txt$5 3 5 1 3 2$txt$, $txt$1 2 3 5$txt$, true, 0),
('b0000000-0000-0000-0000-000000000020', $txt$1 1 1 1$txt$, $txt$1$txt$, false, 1),
('b0000000-0000-0000-0000-000000000020', $txt$-3 -1 -3 0 2$txt$, $txt$-3 -1 0 2$txt$, false, 2),
('b0000000-0000-0000-0000-000000000020', $txt$7$txt$, $txt$7$txt$, false, 3),
-- Word Frequency Counter (b...0021)
('b0000000-0000-0000-0000-000000000021', $txt$the cat sat on the mat the cat ran$txt$, $txt$cat: 2
mat: 1
on: 1
ran: 1
sat: 1
the: 3$txt$, true, 0),
('b0000000-0000-0000-0000-000000000021', $txt$a a a a$txt$, $txt$a: 4$txt$, false, 1),
('b0000000-0000-0000-0000-000000000021', $txt$Apple banana apple Banana APPLE$txt$, $txt$apple: 3
banana: 2$txt$, false, 2),
('b0000000-0000-0000-0000-000000000021', $txt$one$txt$, $txt$one: 1$txt$, false, 3),
('b0000000-0000-0000-0000-000000000021', $txt$z y x z y z$txt$, $txt$x: 1
y: 2
z: 3$txt$, false, 4);

-- ---- Topic 8 test cases -------------------------------------------------------
insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values
-- Function to Check Even/Odd (b...0022)
('b0000000-0000-0000-0000-000000000022', $txt$4$txt$, $txt$Even$txt$, true, 0),
('b0000000-0000-0000-0000-000000000022', $txt$7$txt$, $txt$Odd$txt$, false, 1),
('b0000000-0000-0000-0000-000000000022', $txt$0$txt$, $txt$Even$txt$, false, 2),
-- Factorial Function (b...0023)
('b0000000-0000-0000-0000-000000000023', $txt$5$txt$, $txt$120$txt$, true, 0),
('b0000000-0000-0000-0000-000000000023', $txt$0$txt$, $txt$1$txt$, false, 1),
('b0000000-0000-0000-0000-000000000023', $txt$1$txt$, $txt$1$txt$, false, 2),
('b0000000-0000-0000-0000-000000000023', $txt$7$txt$, $txt$5040$txt$, false, 3),
-- Function Toolkit: GCD and LCM (b...0024)
('b0000000-0000-0000-0000-000000000024', $txt$12
18$txt$, $txt$GCD: 6
LCM: 36$txt$, true, 0),
('b0000000-0000-0000-0000-000000000024', $txt$7
13$txt$, $txt$GCD: 1
LCM: 91$txt$, false, 1),
('b0000000-0000-0000-0000-000000000024', $txt$100
75$txt$, $txt$GCD: 25
LCM: 300$txt$, false, 2),
('b0000000-0000-0000-0000-000000000024', $txt$1
1$txt$, $txt$GCD: 1
LCM: 1$txt$, false, 3),
('b0000000-0000-0000-0000-000000000024', $txt$6
6$txt$, $txt$GCD: 6
LCM: 6$txt$, false, 4);

-- ---- Topic 9 test cases -------------------------------------------------------
insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values
-- Write and Count Lines (b...0025)
('b0000000-0000-0000-0000-000000000025', $txt$3
apple
banana
cherry$txt$, $txt$3$txt$, true, 0),
('b0000000-0000-0000-0000-000000000025', $txt$0$txt$, $txt$0$txt$, false, 1),
('b0000000-0000-0000-0000-000000000025', $txt$1
hello$txt$, $txt$1$txt$, false, 2),
-- Word Count in File (b...0026)
('b0000000-0000-0000-0000-000000000026', $txt$2
The quick brown fox
jumps over the lazy dog$txt$, $txt$9$txt$, true, 0),
('b0000000-0000-0000-0000-000000000026', $txt$1
Hello World$txt$, $txt$2$txt$, false, 1),
('b0000000-0000-0000-0000-000000000026', $txt$3
One
Two three
Four five six$txt$, $txt$6$txt$, false, 2),
('b0000000-0000-0000-0000-000000000026', $txt$0$txt$, $txt$0$txt$, false, 3),
-- CSV-like Record Processor (b...0027)
('b0000000-0000-0000-0000-000000000027', $txt$3
Alice,85
Bob,92
Cara,78$txt$, $txt$Top: Bob
Average: 85.00$txt$, true, 0),
('b0000000-0000-0000-0000-000000000027', $txt$1
Solo,100$txt$, $txt$Top: Solo
Average: 100.00$txt$, false, 1),
('b0000000-0000-0000-0000-000000000027', $txt$4
A,50
B,50
C,90
D,90$txt$, $txt$Top: C
Average: 70.00$txt$, false, 2),
('b0000000-0000-0000-0000-000000000027', $txt$2
X,0
Y,0$txt$, $txt$Top: X
Average: 0.00$txt$, false, 3),
('b0000000-0000-0000-0000-000000000027', $txt$5
P,10
Q,20
R,30
S,40
T,50$txt$, $txt$Top: T
Average: 30.00$txt$, false, 4);

-- ---- Topic 10 test cases -------------------------------------------------------
insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values
-- Safe Integer Conversion (b...0028)
('b0000000-0000-0000-0000-000000000028', $txt$21$txt$, $txt$42$txt$, true, 0),
('b0000000-0000-0000-0000-000000000028', $txt$abc$txt$, $txt$Invalid integer$txt$, false, 1),
('b0000000-0000-0000-0000-000000000028', $txt$-15$txt$, $txt$-30$txt$, false, 2),
-- Safe Division with Multiple Exceptions (b...0029)
('b0000000-0000-0000-0000-000000000029', $txt$10
2$txt$, $txt$5.00$txt$, true, 0),
('b0000000-0000-0000-0000-000000000029', $txt$10
0$txt$, $txt$Error: Division by zero$txt$, false, 1),
('b0000000-0000-0000-0000-000000000029', $txt$abc
2$txt$, $txt$Error: Invalid number$txt$, false, 2),
('b0000000-0000-0000-0000-000000000029', $txt$7
xyz$txt$, $txt$Error: Invalid number$txt$, false, 3),
-- Robust List Indexer with Finally (b...0030)
('b0000000-0000-0000-0000-000000000030', $txt$10 20 30 40
2$txt$, $txt$Value: 30
Operation complete$txt$, true, 0),
('b0000000-0000-0000-0000-000000000030', $txt$10 20 30 40
10$txt$, $txt$Error: Index out of range
Operation complete$txt$, false, 1),
('b0000000-0000-0000-0000-000000000030', $txt$10 20 30 40
abc$txt$, $txt$Error: Index must be an integer
Operation complete$txt$, false, 2),
('b0000000-0000-0000-0000-000000000030', $txt$5
-1$txt$, $txt$Value: 5
Operation complete$txt$, false, 3),
('b0000000-0000-0000-0000-000000000030', $txt$1 2 3
-5$txt$, $txt$Error: Index out of range
Operation complete$txt$, false, 4);

-- ============================================================================
-- 4. SANITY CHECK
-- ============================================================================
select
  (select count(*) from topics) as topics_count,
  (select count(*) from questions) as questions_count,
  (select count(*) from test_cases) as test_cases_count,
  (select count(*) from questions where difficulty = 'easy') as easy_count,
  (select count(*) from questions where difficulty = 'medium') as medium_count,
  (select count(*) from questions where difficulty = 'hard') as hard_count,
  (select count(*) from test_cases where is_sample = true) as sample_test_case_count;
-- Expected: topics_count = 10, questions_count = 30, test_cases_count = 120,
-- easy_count = 10, medium_count = 10, hard_count = 10, sample_test_case_count = 30
