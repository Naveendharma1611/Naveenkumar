-- Phase 2 content expansion: Variables and Data Types
-- topic_id a0000000-0000-0000-0000-000000000001, slug variables-data-types
-- Adds 7 code questions (order_index 4-10), 5 MCQ (11-15), 3 fill_blank (16-18),
-- and updates the topic's try_it_examples / common_mistakes.

-- ============================================================
-- 1. Code questions
-- ============================================================

insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type) values
(
  'c0000000-0000-0000-0000-000000000001',
  'a0000000-0000-0000-0000-000000000001',
  $txt$Sum of Two Integers$txt$,
  $md$Read two integers and print their sum.

**Input Format**

Two lines, each containing an integer.

**Output Format**

A single line containing the sum of the two integers.

**Example**

```
Input:
3
5

Output:
8
```
$md$,
  'easy',
  10,
  $py$# Read two integers and print their sum
a = input()
b = input()
# TODO: convert a and b to integers, then print their sum
$py$,
  $txt$Remember input() returns a string -- convert both values with int() before adding them.$txt$,
  $py$a = int(input())
b = int(input())
print(a + b)
$py$,
  4,
  'code'
),
(
  'c0000000-0000-0000-0000-000000000002',
  'a0000000-0000-0000-0000-000000000001',
  $txt$Convert String to Integer$txt$,
  $md$Read a number as text, convert it to an integer, then print its type followed by its value, each on its own line.

**Input Format**

One line containing a whole number written as text.

**Output Format**

Two lines: the type of the converted value, then the value itself.

**Example**

```
Input:
42

Output:
<class 'int'>
42
```
$md$,
  'easy',
  10,
  $py$# Read a number as text
s = input()
# TODO: convert s to an int, then print its type and its value
$py$,
  $txt$Use int() to convert, then type() to see the resulting type.$txt$,
  $py$s = input()
n = int(s)
print(type(n))
print(n)
$py$,
  5,
  'code'
),
(
  'c0000000-0000-0000-0000-000000000003',
  'a0000000-0000-0000-0000-000000000001',
  $txt$Swap Two Variables$txt$,
  $md$Read two integers `a` and `b`, swap their values using multiple assignment (no temporary variable), and print the new value of `a` followed by the new value of `b`.

**Input Format**

Two lines, each containing an integer (first `a`, then `b`).

**Output Format**

Two lines: the swapped values.

**Example**

```
Input:
1
2

Output:
2
1
```
$md$,
  'easy',
  10,
  $py$# Read a and b
a = int(input())
b = int(input())
# TODO: swap a and b, then print the new a and new b
$py$,
  $txt$Python lets you swap values in one line: a, b = b, a$txt$,
  $py$a = int(input())
b = int(input())
a, b = b, a
print(a)
print(b)
$py$,
  6,
  'code'
),
(
  'c0000000-0000-0000-0000-000000000004',
  'a0000000-0000-0000-0000-000000000001',
  $txt$Rectangle Area$txt$,
  $md$Read the length and width of a rectangle as floating-point numbers and print its area.

**Input Format**

Two lines: the length, then the width, each a floating-point number.

**Output Format**

One line: the area (length times width).

**Example**

```
Input:
2.5
4.0

Output:
10.0
```
$md$,
  'medium',
  20,
  $py$# Read length and width
length = input()
width = input()
# TODO: convert both to float, multiply them, and print the result
$py$,
  $txt$Convert both inputs with float() before multiplying them.$txt$,
  $py$length = float(input())
width = float(input())
print(length * width)
$py$,
  7,
  'code'
),
(
  'c0000000-0000-0000-0000-000000000005',
  'a0000000-0000-0000-0000-000000000001',
  $txt$Build a Sentence$txt$,
  $md$Read a person's name and age, then print a sentence introducing them. You will need to convert the age to a string before joining it with `+`.

**Input Format**

Two lines: the name, then the age (an integer).

**Output Format**

One line: `My name is <name> and I am <age> years old.`

**Example**

```
Input:
Alice
30

Output:
My name is Alice and I am 30 years old.
```
$md$,
  'medium',
  20,
  $py$name = input()
age = input()
# TODO: convert age to int, then print the introduction sentence
$py$,
  $txt$You can't join a str and an int with + directly -- wrap the age with str() first.$txt$,
  $py$name = input()
age = int(input())
print("My name is " + name + " and I am " + str(age) + " years old.")
$py$,
  8,
  'code'
),
(
  'c0000000-0000-0000-0000-000000000006',
  'a0000000-0000-0000-0000-000000000001',
  $txt$Multiple Conversions$txt$,
  $md$Read a whole number as text, then print its `int` form, its `float` form, and its `bool` form, each on its own line.

**Input Format**

One line containing a whole number as text (it may be negative or zero).

**Output Format**

Three lines: the int value, the float value, and the bool value.

**Example**

```
Input:
7

Output:
7
7.0
True
```
$md$,
  'medium',
  20,
  $py$s = input()
# TODO: convert s to int, then print its int, float, and bool forms
$py$,
  $txt$bool(n) is False only when n is 0; it's True for every other number.$txt$,
  $py$s = input()
n = int(s)
print(n)
print(float(n))
print(bool(n))
$py$,
  9,
  'code'
),
(
  'c0000000-0000-0000-0000-000000000007',
  'a0000000-0000-0000-0000-000000000001',
  $txt$Data Type Report$txt$,
  $md$Read an integer, a floating-point number, and a word (on three separate lines). Compute the sum of the integer and the float, then print, in order: the sum, the name of the sum's type, whether the sum is "truthy" (as a bool), and the word joined with the string form of the integer.

**Input Format**

Three lines: an integer, a floating-point number, and a word (no spaces).

**Output Format**

Four lines:
1. The sum of the integer and the float.
2. The name of the sum's type (e.g. `float`).
3. `True` or `False`, depending on whether the sum is truthy.
4. The word immediately followed by the string form of the integer.

**Example**

```
Input:
3
2.5
hi

Output:
5.5
float
True
hi3
```
$md$,
  'hard',
  30,
  $py$a = input()
b = input()
c = input()
# TODO: convert a to int and b to float, compute their sum,
# and print the sum, its type name, its truthiness, and c + str(int(a))
$py$,
  $txt$Use type(total).__name__ to get the type's name as a string, and bool(total) to check truthiness.$txt$,
  $py$a = int(input())
b = float(input())
c = input()
total = a + b
print(total)
print(type(total).__name__)
print(bool(total))
print(c + str(a))
$py$,
  10,
  'code'
);

-- ============================================================
-- 2. Sample test cases (one per code question)
-- ============================================================

insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values
('c0000000-0000-0000-0000-000000000001', $txt$3
5$txt$, $txt$8$txt$, true, 0),
('c0000000-0000-0000-0000-000000000002', $txt$42$txt$, $txt$<class 'int'>
42$txt$, true, 0),
('c0000000-0000-0000-0000-000000000003', $txt$1
2$txt$, $txt$2
1$txt$, true, 0),
('c0000000-0000-0000-0000-000000000004', $txt$2.5
4.0$txt$, $txt$10.0$txt$, true, 0),
('c0000000-0000-0000-0000-000000000005', $txt$Alice
30$txt$, $txt$My name is Alice and I am 30 years old.$txt$, true, 0),
('c0000000-0000-0000-0000-000000000006', $txt$7$txt$, $txt$7
7.0
True$txt$, true, 0),
('c0000000-0000-0000-0000-000000000007', $txt$3
2.5
hi$txt$, $txt$5.5
float
True
hi3$txt$, true, 0);

-- ============================================================
-- 3. Hidden test cases
-- ============================================================

insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values
-- Q1: Sum of Two Integers
('c0000000-0000-0000-0000-000000000001', $txt$0
0$txt$, $txt$0$txt$, 0),
('c0000000-0000-0000-0000-000000000001', $txt$-5
10$txt$, $txt$5$txt$, 1),
-- Q2: Convert String to Integer
('c0000000-0000-0000-0000-000000000002', $txt$0$txt$, $txt$<class 'int'>
0$txt$, 0),
('c0000000-0000-0000-0000-000000000002', $txt$-15$txt$, $txt$<class 'int'>
-15$txt$, 1),
-- Q3: Swap Two Variables
('c0000000-0000-0000-0000-000000000003', $txt$5
10$txt$, $txt$10
5$txt$, 0),
('c0000000-0000-0000-0000-000000000003', $txt$0
-3$txt$, $txt$-3
0$txt$, 1),
-- Q4: Rectangle Area
('c0000000-0000-0000-0000-000000000004', $txt$3.0
3.0$txt$, $txt$9.0$txt$, 0),
('c0000000-0000-0000-0000-000000000004', $txt$0.0
5.5$txt$, $txt$0.0$txt$, 1),
('c0000000-0000-0000-0000-000000000004', $txt$1.5
2.0$txt$, $txt$3.0$txt$, 2),
-- Q5: Build a Sentence
('c0000000-0000-0000-0000-000000000005', $txt$Bob
5$txt$, $txt$My name is Bob and I am 5 years old.$txt$, 0),
('c0000000-0000-0000-0000-000000000005', $txt$Eve
0$txt$, $txt$My name is Eve and I am 0 years old.$txt$, 1),
('c0000000-0000-0000-0000-000000000005', $txt$X
99$txt$, $txt$My name is X and I am 99 years old.$txt$, 2),
-- Q6: Multiple Conversions
('c0000000-0000-0000-0000-000000000006', $txt$0$txt$, $txt$0
0.0
False$txt$, 0),
('c0000000-0000-0000-0000-000000000006', $txt$-3$txt$, $txt$-3
-3.0
True$txt$, 1),
('c0000000-0000-0000-0000-000000000006', $txt$100$txt$, $txt$100
100.0
True$txt$, 2),
-- Q7: Data Type Report
('c0000000-0000-0000-0000-000000000007', $txt$0
0.0
x$txt$, $txt$0.0
float
False
x0$txt$, 0),
('c0000000-0000-0000-0000-000000000007', $txt$-5
2.5
neg$txt$, $txt$-2.5
float
True
neg-5$txt$, 1),
('c0000000-0000-0000-0000-000000000007', $txt$1000
0.5
big$txt$, $txt$1000.5
float
True
big1000$txt$, 2),
('c0000000-0000-0000-0000-000000000007', $txt$2
-2.0
z$txt$, $txt$0.0
float
False
z2$txt$, 3);

-- ============================================================
-- 4. MCQ questions
-- ============================================================

insert into questions (id, topic_id, title, prompt, difficulty, points, order_index, question_type, options, correct_option) values
(
  'd0000000-0000-0000-0000-000000000001',
  'a0000000-0000-0000-0000-000000000001',
  $txt$Mutable vs Immutable$txt$,
  $md$Which of the following is an **immutable** data type in Python?$md$,
  'easy',
  5,
  11,
  'mcq',
  $json$["list", "dictionary", "tuple", "set"]$json$::jsonb,
  2
),
(
  'd0000000-0000-0000-0000-000000000002',
  'a0000000-0000-0000-0000-000000000001',
  $txt$Type Conversion Result$txt$,
  $md$What does `int('42')` return?$md$,
  'easy',
  5,
  12,
  'mcq',
  $json$["The string 42", "The integer 42", "A float 42.0", "A TypeError"]$json$::jsonb,
  1
),
(
  'd0000000-0000-0000-0000-000000000003',
  'a0000000-0000-0000-0000-000000000001',
  $txt$Floor Division Result Type$txt$,
  $md$What is the data type of the result of `7 // 2` in Python?$md$,
  'medium',
  5,
  13,
  'mcq',
  $json$["int", "float", "str", "bool"]$json$::jsonb,
  0
),
(
  'd0000000-0000-0000-0000-000000000004',
  'a0000000-0000-0000-0000-000000000001',
  $txt$Boolean Conversion$txt$,
  $md$Which built-in function converts a value to a boolean in Python?$md$,
  'medium',
  5,
  14,
  'mcq',
  $json$["str()", "bool()", "int()", "type()"]$json$::jsonb,
  1
),
(
  'd0000000-0000-0000-0000-000000000005',
  'a0000000-0000-0000-0000-000000000001',
  $txt$The bool Subtype$txt$,
  $md$In Python, `bool` is actually a subtype of which other data type?$md$,
  'hard',
  5,
  15,
  'mcq',
  $json$["str", "int", "float", "list"]$json$::jsonb,
  1
);

-- ============================================================
-- 5. Fill-in-the-blank questions
-- ============================================================

insert into questions (id, topic_id, title, prompt, difficulty, points, order_index, question_type, correct_answer) values
(
  'e0000000-0000-0000-0000-000000000001',
  'a0000000-0000-0000-0000-000000000001',
  $txt$String to Integer$txt$,
  $md$The function `___()` converts a string to an integer in Python.$md$,
  'easy',
  5,
  16,
  'fill_blank',
  $txt$int$txt$
),
(
  'e0000000-0000-0000-0000-000000000002',
  'a0000000-0000-0000-0000-000000000001',
  $txt$input() Return Type$txt$,
  $md$In Python, `input()` always returns a value of type `___`.$md$,
  'easy',
  5,
  17,
  'fill_blank',
  $txt$str$txt$
),
(
  'e0000000-0000-0000-0000-000000000003',
  'a0000000-0000-0000-0000-000000000001',
  $txt$Checking a Variable's Type$txt$,
  $md$The function `___()` returns the data type of a variable, e.g. `___(5)` returns `<class 'int'>`.$md$,
  'medium',
  5,
  18,
  'fill_blank',
  $txt$type$txt$
);

-- ============================================================
-- 6. Topic content: try_it_examples and common_mistakes
-- ============================================================

update topics set
  try_it_examples = $json$[
  {"description": "Assigning different data types to variables", "code": "x = 5\ny = 3.14\nz = 'hello'\nprint(x, y, z)\nprint(type(x), type(y), type(z))", "output": "5 3.14 hello\n<class 'int'> <class 'float'> <class 'str'>"},
  {"description": "Converting between data types", "code": "num_str = '25'\nnum_int = int(num_str)\nnum_float = float(num_int)\nprint(num_int + 5)\nprint(num_float)", "output": "30\n25.0"},
  {"description": "Multiple assignment and checking types", "code": "a, b, c = 1, 2, 3\nprint(a, b, c)\na, b = b, a\nprint(a, b)\nis_valid = True\nprint(type(is_valid))", "output": "1 2 3\n2 1\n<class 'bool'>"}
]$json$::jsonb,
  common_mistakes = $md$## Common Mistakes

**Confusing `=` with `==`.** A single `=` assigns a value; `==` compares two values. Writing `if x = 5:` is a syntax error -- use `if x == 5:` for comparisons.

**Forgetting that `input()` always returns a string.** `age = input()` makes `age` a string even if the user typed `25`, so `age + 1` raises a `TypeError`. Fix: `age = int(input())`.

**Mixing strings and numbers with `+`.** `"Score: " + 90` raises a `TypeError` because Python won't silently convert the number. Fix: wrap the number with `str()`, e.g. `"Score: " + str(90)`.

**Expecting floats to print with exact decimals.** Operations like `0.1 + 0.2` can produce `0.30000000000000004` due to binary floating-point rounding. Avoid comparing floats with `==`; round when displaying results.

**Thinking `int()` rounds.** `int(4.9)` truncates down to `4`, it does not round to `5`. Use `round()` if you want proper rounding.

**Overwriting a variable with an unrelated value.** Python happily lets you reuse a name for a completely different type, e.g. `total = 10` later becoming `total = "done"`. Nothing stops this, but it quickly turns readable code into a guessing game about what a variable currently holds. Pick a fresh, descriptive name instead of recycling one for something unrelated, and keep a variable's type consistent for its whole lifetime whenever possible.
$md$
where id = 'a0000000-0000-0000-0000-000000000001';
