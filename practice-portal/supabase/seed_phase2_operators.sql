-- Phase 2 content seed: Operators topic (a0000000-0000-0000-0000-000000000003)
-- Adds 7 code questions, 5 MCQs, 3 fill-in-the-blank questions, and topic
-- try_it_examples / common_mistakes content.

-- =========================================================================
-- 1. CODE QUESTIONS (7 new: 3 easy, 3 medium, 1 hard)
-- =========================================================================

insert into questions
  (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type)
values

-- Easy #1 ---------------------------------------------------------------
(
  'c0000000-0000-0000-0000-000000000015',
  'a0000000-0000-0000-0000-000000000003',
  $txt$Sum, Difference and Product$txt$,
  $md$Read two integers `a` and `b` from a single line of input, separated by a space, and print their sum, difference, and product -- each separated by a single space -- on one line.

**Input Format**
A single line containing two integers `a` and `b`, separated by a space.

**Output Format**
A single line containing `a + b`, `a - b`, and `a * b`, separated by spaces.

**Example**
```
Input:
5 3

Output:
8 2 15
```
$md$,
  'easy',
  10,
  $py$# Read two integers a and b separated by a space
# Print a + b, a - b, a * b separated by spaces

$py$,
  $txt$Use input().split() to read both numbers on one line, convert each to int, then use +, -, and *.$txt$,
  $py$a, b = map(int, input().split())
print(a + b, a - b, a * b)
$py$,
  4,
  'code'
),

-- Easy #2 ---------------------------------------------------------------
(
  'c0000000-0000-0000-0000-000000000016',
  'a0000000-0000-0000-0000-000000000003',
  $txt$Quotient and Remainder$txt$,
  $md$Read two integers `a` (dividend) and `b` (divisor) from a single line of input, separated by a space. Print the quotient of integer division `a // b` and the remainder `a % b`, separated by a space.

**Input Format**
A single line containing two integers `a` and `b`, separated by a space. `b` is never zero.

**Output Format**
A single line containing `a // b` and `a % b`, separated by a space.

**Example**
```
Input:
17 5

Output:
3 2
```
$md$,
  'easy',
  10,
  $py$# Read two integers a and b separated by a space
# Print a // b and a % b separated by a space

$py$,
  $txt$Python's // gives the floor-divided quotient and % gives the remainder; use both on the same two values.$txt$,
  $py$a, b = map(int, input().split())
print(a // b, a % b)
$py$,
  5,
  'code'
),

-- Easy #3 ---------------------------------------------------------------
(
  'c0000000-0000-0000-0000-000000000017',
  'a0000000-0000-0000-0000-000000000003',
  $txt$Comparing Two Numbers$txt$,
  $md$Read two integers `a` and `b` from a single line of input, separated by a space. Print the results of three comparisons -- `a == b`, `a != b`, and `a < b` -- separated by spaces, exactly as Python prints boolean values (`True`/`False`).

**Input Format**
A single line containing two integers `a` and `b`, separated by a space.

**Output Format**
A single line containing the three boolean results, separated by spaces.

**Example**
```
Input:
4 7

Output:
False True True
```
$md$,
  'easy',
  10,
  $py$# Read two integers a and b separated by a space
# Print a == b, a != b, a < b separated by spaces

$py$,
  $txt$print() can take multiple comma-separated values -- pass the three comparison expressions directly to it.$txt$,
  $py$a, b = map(int, input().split())
print(a == b, a != b, a < b)
$py$,
  6,
  'code'
),

-- Medium #1 ---------------------------------------------------------------
(
  'c0000000-0000-0000-0000-000000000018',
  'a0000000-0000-0000-0000-000000000003',
  $txt$Even or Odd$txt$,
  $md$Read a single integer `n`. Using the modulo operator, determine whether it is even or odd, and print `Even` or `Odd` accordingly.

**Input Format**
A single line containing one integer `n`.

**Output Format**
Print `Even` if `n % 2 == 0`, otherwise print `Odd`.

**Example**
```
Input:
7

Output:
Odd
```
$md$,
  'medium',
  20,
  $py$# Read an integer n
# Print "Even" or "Odd" using the modulo operator

$py$,
  $txt$A number is even exactly when dividing it by 2 leaves no remainder -- check n % 2.$txt$,
  $py$n = int(input())
print("Even" if n % 2 == 0 else "Odd")
$py$,
  7,
  'code'
),

-- Medium #2 ---------------------------------------------------------------
(
  'c0000000-0000-0000-0000-000000000019',
  'a0000000-0000-0000-0000-000000000003',
  $txt$Last Digit and Remaining Number$txt$,
  $md$Read a positive integer `n`. Using the `%` and `//` operators, print its last digit and the number formed by removing that last digit, separated by a space.

**Input Format**
A single line containing one positive integer `n`.

**Output Format**
A single line containing `n % 10` and `n // 10`, separated by a space.

**Example**
```
Input:
4567

Output:
7 456
```
$md$,
  'medium',
  20,
  $py$# Read a positive integer n
# Print n % 10 and n // 10 separated by a space

$py$,
  $txt$%10 isolates the last digit of a base-10 number; //10 drops it.$txt$,
  $py$n = int(input())
print(n % 10, n // 10)
$py$,
  8,
  'code'
),

-- Medium #3 ---------------------------------------------------------------
(
  'c0000000-0000-0000-0000-000000000020',
  'a0000000-0000-0000-0000-000000000003',
  $txt$Compound Assignment Chain$txt$,
  $md$Read an integer `n`. Apply the following compound-assignment updates to it, in order:

1. `n += 5`
2. `n -= 2`
3. `n *= 3`
4. `n //= 4`

Print the final value of `n`.

**Input Format**
A single line containing one integer `n`.

**Output Format**
A single line containing the final value of `n` after all four updates.

**Example**
```
Input:
10

Output:
9
```
$md$,
  'medium',
  20,
  $py$# Read an integer n
# Apply: n += 5, n -= 2, n *= 3, n //= 4
# Print the final value of n

$py$,
  $txt$Apply each compound-assignment operator one at a time, in the exact order given, to the same variable.$txt$,
  $py$n = int(input())
n += 5
n -= 2
n *= 3
n //= 4
print(n)
$py$,
  9,
  'code'
),

-- Hard #1 ---------------------------------------------------------------
(
  'c0000000-0000-0000-0000-000000000021',
  'a0000000-0000-0000-0000-000000000003',
  $txt$Triangle Classifier$txt$,
  $md$Read three integers `a`, `b`, and `c` -- the lengths of a triangle's three sides. First decide whether they can form a valid triangle, using the triangle inequality: the sum of any two sides must be strictly greater than the third side.

- If they cannot form a valid triangle, print `Invalid`.
- If they can, classify the triangle using comparison and logical operators and print one of:
  - `Equilateral` -- all three sides equal
  - `Isosceles` -- exactly two sides equal
  - `Scalene` -- all three sides different

**Input Format**
A single line containing three integers `a`, `b`, and `c`, separated by spaces.

**Output Format**
One word: `Invalid`, `Equilateral`, `Isosceles`, or `Scalene`.

**Example**
```
Input:
3 4 5

Output:
Scalene
```
$md$,
  'hard',
  30,
  $py$# Read three integers a, b, c
# Check the triangle inequality, then classify as
# Equilateral, Isosceles, Scalene, or Invalid

$py$,
  $txt$Combine and/or with comparison operators: check the triangle inequality first, then compare the three sides to each other.$txt$,
  $py$a, b, c = map(int, input().split())
if a + b > c and a + c > b and b + c > a:
    if a == b == c:
        print("Equilateral")
    elif a == b or b == c or a == c:
        print("Isosceles")
    else:
        print("Scalene")
else:
    print("Invalid")
$py$,
  10,
  'code'
);

-- =========================================================================
-- Sample test_cases (1 per code question)
-- =========================================================================

insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values
('c0000000-0000-0000-0000-000000000015', $txt$5 3$txt$, $txt$8 2 15$txt$, true, 0),
('c0000000-0000-0000-0000-000000000016', $txt$17 5$txt$, $txt$3 2$txt$, true, 0),
('c0000000-0000-0000-0000-000000000017', $txt$4 7$txt$, $txt$False True True$txt$, true, 0),
('c0000000-0000-0000-0000-000000000018', $txt$7$txt$, $txt$Odd$txt$, true, 0),
('c0000000-0000-0000-0000-000000000019', $txt$4567$txt$, $txt$7 456$txt$, true, 0),
('c0000000-0000-0000-0000-000000000020', $txt$10$txt$, $txt$9$txt$, true, 0),
('c0000000-0000-0000-0000-000000000021', $txt$3 4 5$txt$, $txt$Scalene$txt$, true, 0);

-- =========================================================================
-- Hidden test_cases
-- =========================================================================

insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values
-- Q1: Sum, Difference and Product (easy, 2 hidden)
('c0000000-0000-0000-0000-000000000015', $txt$-4 6$txt$, $txt$2 -10 -24$txt$, 0),
('c0000000-0000-0000-0000-000000000015', $txt$100 100$txt$, $txt$200 0 10000$txt$, 1),

-- Q2: Quotient and Remainder (easy, 2 hidden)
('c0000000-0000-0000-0000-000000000016', $txt$-17 5$txt$, $txt$-4 3$txt$, 0),
('c0000000-0000-0000-0000-000000000016', $txt$9 1$txt$, $txt$9 0$txt$, 1),

-- Q3: Comparing Two Numbers (easy, 2 hidden)
('c0000000-0000-0000-0000-000000000017', $txt$-3 -3$txt$, $txt$True False False$txt$, 0),
('c0000000-0000-0000-0000-000000000017', $txt$10 2$txt$, $txt$False True False$txt$, 1),

-- Q4: Even or Odd (medium, 3 hidden)
('c0000000-0000-0000-0000-000000000018', $txt$4$txt$, $txt$Even$txt$, 0),
('c0000000-0000-0000-0000-000000000018', $txt$-10$txt$, $txt$Even$txt$, 1),
('c0000000-0000-0000-0000-000000000018', $txt$-7$txt$, $txt$Odd$txt$, 2),

-- Q5: Last Digit and Remaining Number (medium, 3 hidden)
('c0000000-0000-0000-0000-000000000019', $txt$5$txt$, $txt$5 0$txt$, 0),
('c0000000-0000-0000-0000-000000000019', $txt$100$txt$, $txt$0 10$txt$, 1),
('c0000000-0000-0000-0000-000000000019', $txt$999999$txt$, $txt$9 99999$txt$, 2),

-- Q6: Compound Assignment Chain (medium, 3 hidden)
('c0000000-0000-0000-0000-000000000020', $txt$0$txt$, $txt$2$txt$, 0),
('c0000000-0000-0000-0000-000000000020', $txt$-10$txt$, $txt$-6$txt$, 1),
('c0000000-0000-0000-0000-000000000020', $txt$100$txt$, $txt$77$txt$, 2),

-- Q7: Triangle Classifier (hard, 4 hidden)
('c0000000-0000-0000-0000-000000000021', $txt$5 5 5$txt$, $txt$Equilateral$txt$, 0),
('c0000000-0000-0000-0000-000000000021', $txt$5 5 8$txt$, $txt$Isosceles$txt$, 1),
('c0000000-0000-0000-0000-000000000021', $txt$2 3 4$txt$, $txt$Scalene$txt$, 2),
('c0000000-0000-0000-0000-000000000021', $txt$1 1 5$txt$, $txt$Invalid$txt$, 3);

-- =========================================================================
-- 2. MCQ QUESTIONS (5)
-- =========================================================================

insert into questions
  (id, topic_id, title, prompt, difficulty, points, order_index, question_type, options, correct_option)
values
(
  'd0000000-0000-0000-0000-000000000011',
  'a0000000-0000-0000-0000-000000000003',
  $txt$Floor Division Result$txt$,
  $md$What is the value of `7 // 2` in Python?$md$,
  'easy',
  5,
  11,
  'mcq',
  '["3", "3.5", "4", "Error"]'::jsonb,
  0
),
(
  'd0000000-0000-0000-0000-000000000012',
  'a0000000-0000-0000-0000-000000000003',
  $txt$Operator Precedence$txt$,
  $md$What is the value of the expression `2 + 3 * 4 ** 2`?$md$,
  'medium',
  5,
  12,
  'mcq',
  '["50", "100", "38", "44"]'::jsonb,
  0
),
(
  'd0000000-0000-0000-0000-000000000013',
  'a0000000-0000-0000-0000-000000000003',
  $txt$Modulo with a Negative Divisor$txt$,
  $md$What is the value of `7 % -2` in Python?$md$,
  'hard',
  5,
  13,
  'mcq',
  '["-1", "1", "-1.0", "3"]'::jsonb,
  0
),
(
  'd0000000-0000-0000-0000-000000000014',
  'a0000000-0000-0000-0000-000000000003',
  $txt$Chained Comparison$txt$,
  $md$What does `1 < 2 < 3` evaluate to in Python?$md$,
  'medium',
  5,
  14,
  'mcq',
  '["True", "False", "TypeError", "3"]'::jsonb,
  0
),
(
  'd0000000-0000-0000-0000-000000000015',
  'a0000000-0000-0000-0000-000000000003',
  $txt$Highest Precedence Operator$txt$,
  $md$Which of these operators has the highest precedence in Python?$md$,
  'easy',
  5,
  15,
  'mcq',
  '["**", "*", "+", "=="]'::jsonb,
  0
);

-- =========================================================================
-- 3. FILL-IN-THE-BLANK QUESTIONS (3)
-- =========================================================================

insert into questions
  (id, topic_id, title, prompt, difficulty, points, order_index, question_type, correct_answer)
values
(
  'e0000000-0000-0000-0000-000000000007',
  'a0000000-0000-0000-0000-000000000003',
  $txt$Modulo Operator$txt$,
  $md$The `___` operator returns the remainder of integer division in Python.$md$,
  'easy',
  5,
  16,
  'fill_blank',
  $txt$%$txt$
),
(
  'e0000000-0000-0000-0000-000000000008',
  'a0000000-0000-0000-0000-000000000003',
  $txt$Floor Division Operator$txt$,
  $md$The `___` operator performs floor (integer) division in Python, discarding any fractional part.$md$,
  'easy',
  5,
  17,
  'fill_blank',
  $txt$//$txt$
),
(
  'e0000000-0000-0000-0000-000000000009',
  'a0000000-0000-0000-0000-000000000003',
  $txt$Equality vs Assignment$txt$,
  $md$To check whether two values are equal (without assigning), you use the `___` operator, as opposed to a single `=` which assigns a value.$md$,
  'medium',
  5,
  18,
  'fill_blank',
  $txt$==$txt$
);

-- =========================================================================
-- 4. TOPIC CONTENT (try_it_examples, common_mistakes)
-- =========================================================================

update topics
set
  try_it_examples = '[
    {
      "description": "Operator precedence changes the result",
      "code": "a = 10\nb = 3\nprint(a + b * 2)\nprint((a + b) * 2)",
      "output": "16\n26"
    },
    {
      "description": "Integer division vs true division vs modulo",
      "code": "print(7 / 2)\nprint(7 // 2)\nprint(7 % 2)",
      "output": "3.5\n3\n1"
    },
    {
      "description": "Chained comparisons and logical operators",
      "code": "x = 5\nprint(1 < x < 10)\nprint(x > 0 and x % 2 == 1)\nprint(not x == 5)",
      "output": "True\nTrue\nFalse"
    }
  ]'::jsonb,
  common_mistakes = $md$### Common Mistakes with Operators

- **Confusing `=` with `==`.** A single `=` assigns a value to a variable, while `==` compares two values for equality. Writing `if x = 5:` is a syntax error in Python, but the slip is still easy to make out of habit. *Fix:* use `==` whenever you are comparing, and reserve `=` for assignment.

- **Expecting `/` to behave like `//`.** In Python 3, `/` always performs true division and returns a `float`, even when both operands are integers that divide evenly (`6 / 2` is `3.0`, not `3`). Beginners who want a whole-number result reach for `/` and are surprised by the decimal point. *Fix:* use `//` for floor (integer) division.

- **Misjudging operator precedence.** Expressions like `2 + 3 * 2` evaluate the `*` before the `+` (giving `8`, not `10`), and `**` binds even tighter than unary minus, so `-2 ** 2` is `-4`, not `4`. *Fix:* when in doubt, add parentheses to make the intended order explicit.

- **Misreading chained comparisons.** `1 < x < 10` is not a typo -- Python evaluates it as `(1 < x) and (x < 10)`, not left to right like arithmetic. *Fix:* read a chained comparison as an implicit `and`.

- **Comparing floats with `==`.** Because of floating-point rounding, `0.1 + 0.2 == 0.3` evaluates to `False`. *Fix:* compare with a small tolerance, e.g. `abs(a - b) < 1e-9`, instead of exact equality.
$md$
where id = 'a0000000-0000-0000-0000-000000000003';
