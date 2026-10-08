-- ============================================================
-- Phase 2 content seed: Functions topic
-- topic slug: functions | topic_id: a0000000-0000-0000-0000-000000000008
-- Adds 7 code questions (10 total with existing 3), 5 MCQs, 3 fill-blank
-- questions, plus try_it_examples / common_mistakes on the topic row.
-- ============================================================

-- ------------------------------------------------------------
-- 1. Seven new CODE questions
-- ------------------------------------------------------------

insert into questions
  (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type)
values
(
  'c0000000-0000-0000-0000-000000000050',
  'a0000000-0000-0000-0000-000000000008',
  $txt$Square a Number$txt$,
  $md$Write a function named `square` that takes one parameter `n` and returns the square of `n` (`n * n`).

Your program should read a single integer from standard input, call `square` with that integer, and print the result.

**Input Format**

A single line containing one integer `n`.

**Output Format**

A single line containing the square of `n`.

**Example**
```
Input:
5

Output:
25
```
$md$,
  'easy',
  10,
  $py$def square(n):
    # TODO: return the square of n
    pass

# read input, call square(), and print the result
$py$,
  $txt$Use the `**` operator or multiply n by itself. Remember a function communicates results with `return`, not `print`, inside the function body.$txt$,
  $py$def square(n):
    return n * n

n = int(input())
print(square(n))
$py$,
  4,
  'code'
),
(
  'c0000000-0000-0000-0000-000000000051',
  'a0000000-0000-0000-0000-000000000008',
  $txt$Power With a Default Exponent$txt$,
  $md$Write a function named `power` that takes two parameters, `base` and `exponent`, where `exponent` has a default value of `2`. The function should return `base` raised to the power `exponent` (`base ** exponent`).

Your program should read one line of input containing either one or two integers separated by a space. If only `base` is given, call `power` using the default exponent. If both `base` and `exponent` are given, call `power` with both values. Print the result.

**Input Format**

A single line containing one or two integers separated by spaces: `base` or `base exponent`.

**Output Format**

A single line containing `base` raised to the appropriate power.

**Example**
```
Input:
5

Output:
25
```
$md$,
  'easy',
  10,
  $py$def power(base, exponent=2):
    # TODO: return base raised to exponent
    pass

# read input (one or two numbers), call power(), and print the result
$py$,
  $txt$Split the input line with .split(). If it has one item, call power(base); if it has two, call power(base, exponent).$txt$,
  $py$def power(base, exponent=2):
    return base ** exponent

parts = input().split()
if len(parts) >= 2:
    base, exponent = int(parts[0]), int(parts[1])
    print(power(base, exponent))
else:
    base = int(parts[0])
    print(power(base))
$py$,
  5,
  'code'
),
(
  'c0000000-0000-0000-0000-000000000052',
  'a0000000-0000-0000-0000-000000000008',
  $txt$Smallest and Largest (Multiple Return Values)$txt$,
  $md$Write a function named `min_max` that takes a list of numbers and returns two values: the smallest number and the largest number, in that order (so the caller can unpack them as `smallest, largest = min_max(numbers)`).

Your program should read a single line of space-separated integers, call `min_max`, and print the smallest and largest values separated by a space.

**Input Format**

A single line containing space-separated integers.

**Output Format**

A single line containing the smallest and largest value, separated by a space.

**Example**
```
Input:
4 1 7 3

Output:
1 7
```
$md$,
  'easy',
  10,
  $py$def min_max(numbers):
    # TODO: return a tuple (smallest, largest)
    pass

# read input, unpack the returned tuple, and print "smallest largest"
$py$,
  $txt$A function can "return smallest, largest" - this creates a tuple that can be unpacked with a, b = min_max(...). Use the built-in min() and max() functions.$txt$,
  $py$def min_max(numbers):
    return min(numbers), max(numbers)

numbers = list(map(int, input().split()))
smallest, largest = min_max(numbers)
print(smallest, largest)
$py$,
  6,
  'code'
),
(
  'c0000000-0000-0000-0000-000000000053',
  'a0000000-0000-0000-0000-000000000008',
  $txt$Format a Receipt Line (Keyword Arguments)$txt$,
  $md$Write a function named `format_item` that takes three parameters: `name`, `price`, and `qty` (with a default value of `1`). It should return a string in the format `"{name}: {qty} x {price} = {total}"` where `total` is `qty * price`.

Your program should read a line containing a name, a price, and an optional quantity. If a quantity is given, call `format_item` using keyword arguments, e.g. `format_item(name, price=price, qty=qty)`. If not, call it with just `name` and `price` (using keyword arguments) so the default quantity is used. Print the returned string.

**Input Format**

A single line: `name price` or `name price qty` (space-separated). `price` and `qty` are integers.

**Output Format**

A single line: `name: qty x price = total`

**Example**
```
Input:
Pen 10 3

Output:
Pen: 3 x 10 = 30
```
$md$,
  'medium',
  20,
  $py$def format_item(name, price, qty=1):
    # TODO: return the formatted string
    pass

# read input, call format_item() using keyword arguments, and print the result
$py$,
  $txt$Keyword arguments let you pass values by name, e.g. format_item(name, price=10, qty=3). Use an f-string to build the result.$txt$,
  $py$def format_item(name, price, qty=1):
    total = qty * price
    return f"{name}: {qty} x {price} = {total}"

parts = input().split()
name = parts[0]
price = int(parts[1])
if len(parts) >= 3:
    qty = int(parts[2])
    print(format_item(name, price=price, qty=qty))
else:
    print(format_item(name, price=price))
$py$,
  7,
  'code'
),
(
  'c0000000-0000-0000-0000-000000000054',
  'a0000000-0000-0000-0000-000000000008',
  $txt$Sum Any Number of Values (*args)$txt$,
  $md$Write a function named `total` that accepts any number of positional arguments using `*args` and returns their sum.

Your program should read a single line of space-separated integers (the count can vary), unpack them into `total` using `*`, and print the result.

**Input Format**

A single line containing one or more space-separated integers.

**Output Format**

A single line containing the sum of the integers.

**Example**
```
Input:
1 2 3 4

Output:
10
```
$md$,
  'medium',
  20,
  $py$def total(*args):
    # TODO: return the sum of all values in args
    pass

# read input, unpack the numbers into total() using *, and print the result
$py$,
  $txt$*args collects any number of positional arguments into a tuple. Use sum(args). When calling, unpack a list with total(*numbers).$txt$,
  $py$def total(*args):
    return sum(args)

numbers = list(map(int, input().split()))
print(total(*numbers))
$py$,
  8,
  'code'
),
(
  'c0000000-0000-0000-0000-000000000055',
  'a0000000-0000-0000-0000-000000000008',
  $txt$Global vs Local Scope$txt$,
  $md$Below is a scenario about variable scope. Study it, then complete the program.

A global variable `total` starts at `0`. Write two functions:
- `try_local_change(x)`: assigns `x` to a local variable named `total` (this creates a new local variable and does **not** affect the global `total`). It returns the local value.
- `apply_global_change(x)`: uses the `global` keyword to add `x` to the global `total`, and returns the updated global `total`.

Your program should:
1. Read a single line of space-separated integers.
2. Call `try_local_change(999)` once (its result is discarded - it must not affect the global `total`).
3. Call `apply_global_change(x)` for each number `x` read from the input, updating the global `total`.
4. Print the final value of the global `total`.

**Input Format**

A single line containing space-separated integers.

**Output Format**

A single line containing the final global `total` (the sum of the input integers - the local-scope call in step 2 has no effect on it).

**Example**
```
Input:
1 2 3

Output:
6
```
$md$,
  'medium',
  20,
  $py$total = 0

def try_local_change(x):
    # TODO: assign x to a LOCAL variable named total (no global keyword)
    pass

def apply_global_change(x):
    # TODO: use the global keyword and add x to the global total
    pass

# read input, call try_local_change(999) once, then apply_global_change() for each number, then print total
$py$,
  $txt$Without the global keyword, assigning to a name inside a function creates a brand-new local variable that shadows the outer one - it does not change the outer variable. Declare "global total" before modifying the outer variable.$txt$,
  $py$total = 0

def try_local_change(x):
    total = x
    return total

def apply_global_change(x):
    global total
    total += x
    return total

numbers = list(map(int, input().split()))
try_local_change(999)
for n in numbers:
    apply_global_change(n)
print(total)
$py$,
  9,
  'code'
),
(
  'c0000000-0000-0000-0000-000000000056',
  'a0000000-0000-0000-0000-000000000008',
  $txt$Fibonacci Number (Recursion)$txt$,
  $md$Write a recursive function named `fib` that takes a non-negative integer `n` and returns the `n`-th Fibonacci number, where `fib(0) = 0`, `fib(1) = 1`, and `fib(n) = fib(n-1) + fib(n-2)` for `n >= 2`. Your function must call itself (no loops, and do not use an iterative approach).

Your program should read a single integer `n` from standard input, call `fib(n)`, and print the result.

**Input Format**

A single line containing one non-negative integer `n` (0 <= n <= 25).

**Output Format**

A single line containing `fib(n)`.

**Example**
```
Input:
6

Output:
8
```
$md$,
  'hard',
  30,
  $py$def fib(n):
    # TODO: base cases, then return fib(n - 1) + fib(n - 2)
    pass

# read n, call fib(n), and print the result
$py$,
  $txt$Handle the base cases n == 0 and n == 1 first (return n directly for small n), then return fib(n - 1) + fib(n - 2) for everything else.$txt$,
  $py$def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

n = int(input())
print(fib(n))
$py$,
  10,
  'code'
);

-- ------------------------------------------------------------
-- Sample test_cases (order_index 0) for the 7 new code questions
-- ------------------------------------------------------------

insert into test_cases (question_id, stdin, expected_output, is_sample, order_index)
values
  ('c0000000-0000-0000-0000-000000000050', $txt$5$txt$, $txt$25$txt$, true, 0),
  ('c0000000-0000-0000-0000-000000000051', $txt$5$txt$, $txt$25$txt$, true, 0),
  ('c0000000-0000-0000-0000-000000000052', $txt$4 1 7 3$txt$, $txt$1 7$txt$, true, 0),
  ('c0000000-0000-0000-0000-000000000053', $txt$Pen 10 3$txt$, $txt$Pen: 3 x 10 = 30$txt$, true, 0),
  ('c0000000-0000-0000-0000-000000000054', $txt$1 2 3 4$txt$, $txt$10$txt$, true, 0),
  ('c0000000-0000-0000-0000-000000000055', $txt$1 2 3$txt$, $txt$6$txt$, true, 0),
  ('c0000000-0000-0000-0000-000000000056', $txt$6$txt$, $txt$8$txt$, true, 0);

-- ------------------------------------------------------------
-- Hidden test cases
-- ------------------------------------------------------------

insert into hidden_test_cases (question_id, stdin, expected_output, order_index)
values
  -- c050 square (easy, 2 hidden)
  ('c0000000-0000-0000-0000-000000000050', $txt$0$txt$, $txt$0$txt$, 0),
  ('c0000000-0000-0000-0000-000000000050', $txt$-4$txt$, $txt$16$txt$, 1),

  -- c051 power with default exponent (easy, 2 hidden)
  ('c0000000-0000-0000-0000-000000000051', $txt$2 3$txt$, $txt$8$txt$, 0),
  ('c0000000-0000-0000-0000-000000000051', $txt$10$txt$, $txt$100$txt$, 1),

  -- c052 min_max (easy, 2 hidden)
  ('c0000000-0000-0000-0000-000000000052', $txt$5$txt$, $txt$5 5$txt$, 0),
  ('c0000000-0000-0000-0000-000000000052', $txt$-3 -1 -7 -2$txt$, $txt$-7 -1$txt$, 1),

  -- c053 format_item keyword args (medium, 3 hidden)
  ('c0000000-0000-0000-0000-000000000053', $txt$Book 50$txt$, $txt$Book: 1 x 50 = 50$txt$, 0),
  ('c0000000-0000-0000-0000-000000000053', $txt$Eraser 5 0$txt$, $txt$Eraser: 0 x 5 = 0$txt$, 1),
  ('c0000000-0000-0000-0000-000000000053', $txt$Marker 20 10$txt$, $txt$Marker: 10 x 20 = 200$txt$, 2),

  -- c054 total *args (medium, 3 hidden)
  ('c0000000-0000-0000-0000-000000000054', $txt$0$txt$, $txt$0$txt$, 0),
  ('c0000000-0000-0000-0000-000000000054', $txt$100$txt$, $txt$100$txt$, 1),
  ('c0000000-0000-0000-0000-000000000054', $txt$-1 -2 -3$txt$, $txt$-6$txt$, 2),

  -- c055 global vs local scope (medium, 3 hidden)
  ('c0000000-0000-0000-0000-000000000055', $txt$10 20$txt$, $txt$30$txt$, 0),
  ('c0000000-0000-0000-0000-000000000055', $txt$-5 5$txt$, $txt$0$txt$, 1),
  ('c0000000-0000-0000-0000-000000000055', $txt$0$txt$, $txt$0$txt$, 2),

  -- c056 fib recursion (hard, 4 hidden)
  ('c0000000-0000-0000-0000-000000000056', $txt$0$txt$, $txt$0$txt$, 0),
  ('c0000000-0000-0000-0000-000000000056', $txt$1$txt$, $txt$1$txt$, 1),
  ('c0000000-0000-0000-0000-000000000056', $txt$10$txt$, $txt$55$txt$, 2),
  ('c0000000-0000-0000-0000-000000000056', $txt$20$txt$, $txt$6765$txt$, 3);

-- ------------------------------------------------------------
-- 2. Five MCQ questions
-- ------------------------------------------------------------

insert into questions
  (id, topic_id, title, prompt, difficulty, points, order_index, question_type, options, correct_option)
values
(
  'd0000000-0000-0000-0000-000000000036',
  'a0000000-0000-0000-0000-000000000008',
  $txt$What Does This Function Return?$txt$,
  $md$What does the following code print?

```python
def mystery(a, b=5):
    return a + b

print(mystery(3))
```
$md$,
  'easy',
  5,
  11,
  'mcq',
  '["8", "3", "5", "Error, missing argument"]'::jsonb,
  0
),
(
  'd0000000-0000-0000-0000-000000000037',
  'a0000000-0000-0000-0000-000000000008',
  $txt$Local vs Global Variables$txt$,
  $md$What does the following code print?

```python
x = 10

def foo():
    x = 20
    return x

print(foo())
print(x)
```
$md$,
  'medium',
  5,
  12,
  'mcq',
  '["Prints 20, then 10", "Prints 20, then 20", "Prints 10, then 10", "Prints 10, then 20"]'::jsonb,
  0
),
(
  'd0000000-0000-0000-0000-000000000038',
  'a0000000-0000-0000-0000-000000000008',
  $txt$Understanding *args and **kwargs$txt$,
  $md$In the function definition `def f(*args, **kwargs):`, what do `args` and `kwargs` represent respectively?
$md$,
  'medium',
  5,
  13,
  'mcq',
  '["A tuple of positional arguments and a dict of keyword arguments", "A list of keyword arguments and a tuple of positional arguments", "Both are dictionaries of named arguments", "args is a dict and kwargs is a tuple"]'::jsonb,
  0
),
(
  'd0000000-0000-0000-0000-000000000039',
  'a0000000-0000-0000-0000-000000000008',
  $txt$Calling With a Keyword Argument$txt$,
  $md$What is printed by the following code?

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Alex", greeting="Hi"))
```
$md$,
  'easy',
  5,
  14,
  'mcq',
  '["Hi, Alex!", "Hello, Alex!", "Alex, Hi!", "TypeError"]'::jsonb,
  0
),
(
  'd0000000-0000-0000-0000-000000000040',
  'a0000000-0000-0000-0000-000000000008',
  $txt$Functions Without a Return Statement$txt$,
  $md$A function uses `print()` to display a value but has no `return` statement. What does it produce when called in an expression like `result = my_func()`?
$md$,
  'easy',
  5,
  15,
  'mcq',
  '["None", "The printed value", "0", "An empty string"]'::jsonb,
  0
);

-- ------------------------------------------------------------
-- 3. Three fill-in-the-blank questions
-- ------------------------------------------------------------

insert into questions
  (id, topic_id, title, prompt, difficulty, points, order_index, question_type, correct_answer)
values
(
  'e0000000-0000-0000-0000-000000000022',
  'a0000000-0000-0000-0000-000000000008',
  $txt$The Return Keyword$txt$,
  $md$The `___` keyword is used inside a function to send a value back to the caller.$md$,
  'easy',
  5,
  16,
  'fill_blank',
  $txt$return$txt$
),
(
  'e0000000-0000-0000-0000-000000000023',
  'a0000000-0000-0000-0000-000000000008',
  $txt$Modifying a Global Variable$txt$,
  $md$To modify a global variable from inside a function, you must first declare it using the `___` keyword.$md$,
  'medium',
  5,
  17,
  'fill_blank',
  $txt$global$txt$
),
(
  'e0000000-0000-0000-0000-000000000024',
  'a0000000-0000-0000-0000-000000000008',
  $txt$Default Return Value$txt$,
  $md$A function that does not explicitly return a value returns `___` by default.$md$,
  'easy',
  5,
  18,
  'fill_blank',
  $txt$None$txt$
);

-- ------------------------------------------------------------
-- 4. Topic content: try_it_examples + common_mistakes
-- ------------------------------------------------------------

update topics
set
  try_it_examples = '[{"description": "Define and call a simple function with a return value", "code": "def add(a, b):\n    return a + b\n\nresult = add(3, 4)\nprint(result)", "output": "7"}, {"description": "Default parameter values", "code": "def greet(name, greeting=\"Hello\"):\n    return f\"{greeting}, {name}!\"\n\nprint(greet(\"Maya\"))\nprint(greet(\"Maya\", greeting=\"Hi\"))", "output": "Hello, Maya!\nHi, Maya!"}, {"description": "Variable-length arguments with *args", "code": "def total(*numbers):\n    return sum(numbers)\n\nprint(total(1, 2, 3))\nprint(total(10, 20))", "output": "6\n30"}]'::jsonb,
  common_mistakes = $md$## Common Mistakes with Functions

**1. Confusing `print()` with `return`.** A function that prints a value but has no `return` statement still returns `None` to the caller. For example, if `calculate_total(items)` prints the total but doesn't return it, then `result = calculate_total(items)` sets `result` to `None`, and any later code that uses `result` breaks silently. *Fix:* if you need to use a value later, `return` it - use `print()` only when you want to display something immediately.

**2. Forgetting the parentheses when calling a function.** Writing `my_function` instead of `my_function()` refers to the function object itself, not its result - it won't raise an error, which makes the mistake easy to miss. *Fix:* always include parentheses (with any required arguments) to actually call a function.

**3. Mutable default arguments.** Writing `def add_item(item, basket=[])` is dangerous: the same list object is reused across every call that doesn't supply `basket`, so items silently pile up between unrelated calls. *Fix:* use `def add_item(item, basket=None)` and set `basket = basket if basket is not None else []` inside the function.

**4. Assuming a function can freely change an outer variable.** Assigning to a name inside a function creates a new *local* variable by default, leaving the outer one untouched - which surprises beginners expecting the outer value to update. *Fix:* use the `global` keyword to explicitly modify a global variable, or better, return the new value and reassign it at the call site.

**5. Overusing `global` instead of parameters and return values.** Relying on global variables for communication between functions makes code harder to test and reason about. *Fix:* prefer passing data in through parameters and getting results out through `return`.
$md$
where id = 'a0000000-0000-0000-0000-000000000008';
