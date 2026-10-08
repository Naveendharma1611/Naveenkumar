-- ============================================================================
-- Phase 2 content expansion: Conditional Statements (if/elif/else)
-- topic slug: conditionals
-- topic_id:   a0000000-0000-0000-0000-000000000004
--
-- Adds 7 new code questions (order_index 4-10, topic now has 10 code
-- questions total alongside the existing 3), 5 MCQ questions
-- (order_index 11-15), 3 fill-in-the-blank questions (order_index 16-18),
-- and populates topics.try_it_examples / topics.common_mistakes.
-- ============================================================================


-- ----------------------------------------------------------------------------
-- 1. CODE QUESTIONS (7 new: 3 easy, 3 medium, 1 hard)
-- ----------------------------------------------------------------------------

-- Q1 (easy, order 4): Positive, Negative, or Zero
insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type) values (
  'c0000000-0000-0000-0000-000000000022',
  'a0000000-0000-0000-0000-000000000004',
  $txt$Positive, Negative, or Zero$txt$,
  $md$Read a single integer and determine whether it is positive, negative, or zero.

**Input Format**
A single line containing one integer `n`.

**Output Format**
Print `Positive` if `n` is greater than 0, `Negative` if `n` is less than 0, or `Zero` if `n` equals 0.

**Example**
```
Input:
5

Output:
Positive
```$md$,
  'easy',
  10,
  $py$# Read an integer and print whether it is Positive, Negative, or Zero
n = int(input())
# TODO: your code here$py$,
  $txt$Compare n to 0 using an if/elif/else chain. Remember that zero is neither positive nor negative, so it needs its own branch.$txt$,
  $py$n = int(input())
if n > 0:
    print("Positive")
elif n < 0:
    print("Negative")
else:
    print("Zero")$py$,
  4,
  'code'
);

-- Q2 (easy, order 5): Even or Odd
insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type) values (
  'c0000000-0000-0000-0000-000000000023',
  'a0000000-0000-0000-0000-000000000004',
  $txt$Even or Odd$txt$,
  $md$Read a single integer and print whether it is Even or Odd.

**Input Format**
A single line containing one integer `n`.

**Output Format**
Print `Even` if `n` is divisible by 2, otherwise print `Odd`. This also applies to negative numbers.

**Example**
```
Input:
7

Output:
Odd
```$md$,
  'easy',
  10,
  $py$# Read an integer and print Even or Odd
n = int(input())
# TODO: your code here$py$,
  $txt$Use the modulo operator % to check the remainder when n is divided by 2. An if/else is enough here since there are only two outcomes.$txt$,
  $py$n = int(input())
if n % 2 == 0:
    print("Even")
else:
    print("Odd")$py$,
  5,
  'code'
);

-- Q3 (easy, order 6): Vowel or Consonant
insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type) values (
  'c0000000-0000-0000-0000-000000000024',
  'a0000000-0000-0000-0000-000000000004',
  $txt$Vowel or Consonant$txt$,
  $md$Read a single alphabet letter and print whether it is a Vowel or a Consonant.

**Input Format**
A single line containing one letter (uppercase or lowercase).

**Output Format**
Print `Vowel` if the letter is one of a, e, i, o, u (case-insensitive), otherwise print `Consonant`.

**Example**
```
Input:
e

Output:
Vowel
```$md$,
  'easy',
  10,
  $py$# Read a single letter and print Vowel or Consonant
ch = input().strip()
# TODO: your code here$py$,
  $txt$Convert the letter to lowercase first, then check if it is in the string "aeiou" using the in operator inside your if condition.$txt$,
  $py$ch = input().strip().lower()
if ch in "aeiou":
    print("Vowel")
else:
    print("Consonant")$py$,
  6,
  'code'
);

-- Q4 (medium, order 7): Grade Classifier
insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type) values (
  'c0000000-0000-0000-0000-000000000025',
  'a0000000-0000-0000-0000-000000000004',
  $txt$Grade Classifier$txt$,
  $md$Read an integer score between 0 and 100 and print the letter grade using the following bands:

- 90 and above: `A`
- 80 to 89: `B`
- 70 to 79: `C`
- 60 to 69: `D`
- below 60: `F`

**Input Format**
A single line containing one integer `score`.

**Output Format**
Print a single letter grade: `A`, `B`, `C`, `D`, or `F`.

**Example**
```
Input:
85

Output:
B
```$md$,
  'medium',
  20,
  $py$# Read an integer score and print the letter grade (A/B/C/D/F)
score = int(input())
# TODO: your code here$py$,
  $txt$Use an if/elif/else chain and check the highest band first (score >= 90), falling through to lower bands. Order matters here.$txt$,
  $py$score = int(input())
if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
elif score >= 60:
    print("D")
else:
    print("F")$py$,
  7,
  'code'
);

-- Q5 (medium, order 8): Leap Year Checker
insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type) values (
  'c0000000-0000-0000-0000-000000000026',
  'a0000000-0000-0000-0000-000000000004',
  $txt$Leap Year Checker$txt$,
  $md$Read a year and determine whether it is a leap year.

A year is a leap year if it is divisible by 4, except that years divisible by 100 are not leap years unless they are also divisible by 400.

**Input Format**
A single line containing one integer `year`.

**Output Format**
Print `Leap Year` if the year is a leap year, otherwise print `Not a Leap Year`.

**Example**
```
Input:
2024

Output:
Leap Year
```$md$,
  'medium',
  20,
  $py$# Read a year and print Leap Year or Not a Leap Year
year = int(input())
# TODO: your code here$py$,
  $txt$Combine the three rules with and/or inside a single condition: divisible by 4 AND (not divisible by 100 OR divisible by 400).$txt$,
  $py$year = int(input())
if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
    print("Leap Year")
else:
    print("Not a Leap Year")$py$,
  8,
  'code'
);

-- Q6 (medium, order 9): Triangle Type Checker
insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type) values (
  'c0000000-0000-0000-0000-000000000027',
  'a0000000-0000-0000-0000-000000000004',
  $txt$Triangle Type Checker$txt$,
  $md$Read three integers representing the side lengths of a triangle and classify it.

First check whether the three sides can actually form a valid triangle (the sum of any two sides must be strictly greater than the third side). If they cannot, print `Not a triangle`. Otherwise, classify the triangle as `Equilateral` (all three sides equal), `Isosceles` (exactly two sides equal), or `Scalene` (no sides equal).

**Input Format**
A single line containing three space-separated integers `a b c`.

**Output Format**
Print `Not a triangle`, `Equilateral`, `Isosceles`, or `Scalene`.

**Example**
```
Input:
3 3 3

Output:
Equilateral
```$md$,
  'medium',
  20,
  $py$# Read three side lengths and classify the triangle
a, b, c = map(int, input().split())
# TODO: your code here$py$,
  $txt$First check the triangle inequality with a top-level if before deciding the type. Use elif branches for the equal-sides checks, and remember "all equal" should be checked before "two equal".$txt$,
  $py$a, b, c = map(int, input().split())
if a + b <= c or a + c <= b or b + c <= a:
    print("Not a triangle")
elif a == b == c:
    print("Equilateral")
elif a == b or b == c or a == c:
    print("Isosceles")
else:
    print("Scalene")$py$,
  9,
  'code'
);

-- Q7 (hard, order 10): Password Strength Checker
insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type) values (
  'c0000000-0000-0000-0000-000000000028',
  'a0000000-0000-0000-0000-000000000004',
  $txt$Password Strength Checker$txt$,
  $md$Read a password string (no spaces) and classify its strength.

If the password has fewer than 8 characters, it is always `Weak`. Otherwise, count how many of the following four criteria it satisfies: contains an uppercase letter, contains a lowercase letter, contains a digit, contains a special character from `!@#$%^&*`. Based on that count, print:

- all 4 criteria met: `Very Strong`
- exactly 3 criteria met: `Strong`
- exactly 2 criteria met: `Medium`
- 0 or 1 criteria met: `Weak`

**Input Format**
A single line containing one password string with no spaces.

**Output Format**
Print one of `Weak`, `Medium`, `Strong`, or `Very Strong`.

**Example**
```
Input:
Abcdef1!

Output:
Very Strong
```$md$,
  'hard',
  30,
  $py$# Read a password and print its strength: Weak, Medium, Strong, or Very Strong
pw = input().strip()
# TODO: your code here$py$,
  $txt$First handle the length < 8 case on its own. Then compute four booleans (upper, lower, digit, special), add them up, and use an if/elif/elif/else chain on the count.$txt$,
  $py$pw = input().strip()
if len(pw) < 8:
    print("Weak")
else:
    has_upper = any(c.isupper() for c in pw)
    has_lower = any(c.islower() for c in pw)
    has_digit = any(c.isdigit() for c in pw)
    special_chars = "!@#$%^&*"
    has_special = any(c in special_chars for c in pw)
    count = has_upper + has_lower + has_digit + has_special
    if count == 4:
        print("Very Strong")
    elif count == 3:
        print("Strong")
    elif count == 2:
        print("Medium")
    else:
        print("Weak")$py$,
  10,
  'code'
);


-- ----------------------------------------------------------------------------
-- 2. TEST CASES (sample, is_sample = true, order_index 0)
-- ----------------------------------------------------------------------------

insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values ('c0000000-0000-0000-0000-000000000022', $txt$5$txt$, $txt$Positive$txt$, true, 0);
insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values ('c0000000-0000-0000-0000-000000000023', $txt$7$txt$, $txt$Odd$txt$, true, 0);
insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values ('c0000000-0000-0000-0000-000000000024', $txt$e$txt$, $txt$Vowel$txt$, true, 0);
insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values ('c0000000-0000-0000-0000-000000000025', $txt$85$txt$, $txt$B$txt$, true, 0);
insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values ('c0000000-0000-0000-0000-000000000026', $txt$2024$txt$, $txt$Leap Year$txt$, true, 0);
insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values ('c0000000-0000-0000-0000-000000000027', $txt$3 3 3$txt$, $txt$Equilateral$txt$, true, 0);
insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values ('c0000000-0000-0000-0000-000000000028', $txt$Abcdef1!$txt$, $txt$Very Strong$txt$, true, 0);


-- ----------------------------------------------------------------------------
-- 3. HIDDEN TEST CASES
-- ----------------------------------------------------------------------------

-- Q1: Positive, Negative, or Zero (2 hidden)
insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values ('c0000000-0000-0000-0000-000000000022', $txt$-3$txt$, $txt$Negative$txt$, 0);
insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values ('c0000000-0000-0000-0000-000000000022', $txt$0$txt$, $txt$Zero$txt$, 1);

-- Q2: Even or Odd (2 hidden)
insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values ('c0000000-0000-0000-0000-000000000023', $txt$10$txt$, $txt$Even$txt$, 0);
insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values ('c0000000-0000-0000-0000-000000000023', $txt$-7$txt$, $txt$Odd$txt$, 1);

-- Q3: Vowel or Consonant (2 hidden)
insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values ('c0000000-0000-0000-0000-000000000024', $txt$b$txt$, $txt$Consonant$txt$, 0);
insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values ('c0000000-0000-0000-0000-000000000024', $txt$U$txt$, $txt$Vowel$txt$, 1);

-- Q4: Grade Classifier (3 hidden)
insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values ('c0000000-0000-0000-0000-000000000025', $txt$90$txt$, $txt$A$txt$, 0);
insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values ('c0000000-0000-0000-0000-000000000025', $txt$65$txt$, $txt$D$txt$, 1);
insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values ('c0000000-0000-0000-0000-000000000025', $txt$50$txt$, $txt$F$txt$, 2);

-- Q5: Leap Year Checker (3 hidden)
insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values ('c0000000-0000-0000-0000-000000000026', $txt$1900$txt$, $txt$Not a Leap Year$txt$, 0);
insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values ('c0000000-0000-0000-0000-000000000026', $txt$2000$txt$, $txt$Leap Year$txt$, 1);
insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values ('c0000000-0000-0000-0000-000000000026', $txt$2023$txt$, $txt$Not a Leap Year$txt$, 2);

-- Q6: Triangle Type Checker (3 hidden)
insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values ('c0000000-0000-0000-0000-000000000027', $txt$3 4 5$txt$, $txt$Scalene$txt$, 0);
insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values ('c0000000-0000-0000-0000-000000000027', $txt$5 5 8$txt$, $txt$Isosceles$txt$, 1);
insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values ('c0000000-0000-0000-0000-000000000027', $txt$1 2 10$txt$, $txt$Not a triangle$txt$, 2);

-- Q7: Password Strength Checker (4 hidden)
insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values ('c0000000-0000-0000-0000-000000000028', $txt$abcdefgh$txt$, $txt$Weak$txt$, 0);
insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values ('c0000000-0000-0000-0000-000000000028', $txt$Abcdefgh$txt$, $txt$Medium$txt$, 1);
insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values ('c0000000-0000-0000-0000-000000000028', $txt$Abcdef12$txt$, $txt$Strong$txt$, 2);
insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values ('c0000000-0000-0000-0000-000000000028', $txt$abc$txt$, $txt$Weak$txt$, 3);


-- ----------------------------------------------------------------------------
-- 4. MCQ QUESTIONS (5)
-- ----------------------------------------------------------------------------

insert into questions (id, topic_id, title, prompt, difficulty, points, order_index, question_type, options, correct_option) values (
  'd0000000-0000-0000-0000-000000000016',
  'a0000000-0000-0000-0000-000000000004',
  $txt$Trace an if/elif/else Chain$txt$,
  $md$What does the following code print?

```python
x = 5
if x > 10:
    print("A")
elif x > 3:
    print("B")
else:
    print("C")
```$md$,
  'easy',
  5,
  11,
  'mcq',
  '["A","B","C","Nothing is printed"]'::jsonb,
  1
);

insert into questions (id, topic_id, title, prompt, difficulty, points, order_index, question_type, options, correct_option) values (
  'd0000000-0000-0000-0000-000000000017',
  'a0000000-0000-0000-0000-000000000004',
  $txt$The elif Keyword$txt$,
  $md$Which keyword is used in Python to check an additional condition after an if statement fails, before an optional else runs?$md$,
  'easy',
  5,
  12,
  'mcq',
  '["elseif","elif","else if","otherwise"]'::jsonb,
  1
);

insert into questions (id, topic_id, title, prompt, difficulty, points, order_index, question_type, options, correct_option) values (
  'd0000000-0000-0000-0000-000000000018',
  'a0000000-0000-0000-0000-000000000004',
  $txt$Trace Nested Conditions$txt$,
  $md$What does the following code print?

```python
x = -5
if x >= 0:
    if x == 0:
        print("zero")
    else:
        print("positive")
else:
    print("negative")
```$md$,
  'medium',
  5,
  13,
  'mcq',
  '["zero","positive","negative","This code raises an error"]'::jsonb,
  2
);

insert into questions (id, topic_id, title, prompt, difficulty, points, order_index, question_type, options, correct_option) values (
  'd0000000-0000-0000-0000-000000000019',
  'a0000000-0000-0000-0000-000000000004',
  $txt$Boolean Logic in a Condition$txt$,
  $md$What does the following code print?

```python
a = 4
b = 7
if a > 2 and b < 5:
    print("Yes")
else:
    print("No")
```$md$,
  'medium',
  5,
  14,
  'mcq',
  '["Yes","No","YesNo","This code raises an error"]'::jsonb,
  1
);

insert into questions (id, topic_id, title, prompt, difficulty, points, order_index, question_type, options, correct_option) values (
  'd0000000-0000-0000-0000-000000000020',
  'a0000000-0000-0000-0000-000000000004',
  $txt$One-Line Conditional Expression$txt$,
  $md$What value is stored in result after this line runs?

```python
result = "Even" if 7 % 2 == 0 else "Odd"
```$md$,
  'medium',
  5,
  15,
  'mcq',
  '["Even","Odd","7","0"]'::jsonb,
  1
);


-- ----------------------------------------------------------------------------
-- 5. FILL-IN-THE-BLANK QUESTIONS (3)
-- ----------------------------------------------------------------------------

insert into questions (id, topic_id, title, prompt, difficulty, points, order_index, question_type, correct_answer) values (
  'e0000000-0000-0000-0000-000000000010',
  'a0000000-0000-0000-0000-000000000004',
  $txt$Fill in the Blank: elif Keyword$txt$,
  $md$The keyword `___` is used to check an additional condition after an `if` fails but before an `else` runs.$md$,
  'easy',
  5,
  16,
  'fill_blank',
  $txt$elif$txt$
);

insert into questions (id, topic_id, title, prompt, difficulty, points, order_index, question_type, correct_answer) values (
  'e0000000-0000-0000-0000-000000000011',
  'a0000000-0000-0000-0000-000000000004',
  $txt$Fill in the Blank: Equality Operator$txt$,
  $md$Inside a condition, the operator `___` is used to check whether two values are equal (a single `=` is assignment, not comparison).$md$,
  'easy',
  5,
  17,
  'fill_blank',
  $txt$==$txt$
);

insert into questions (id, topic_id, title, prompt, difficulty, points, order_index, question_type, correct_answer) values (
  'e0000000-0000-0000-0000-000000000012',
  'a0000000-0000-0000-0000-000000000004',
  $txt$Fill in the Blank: Boolean Expressions$txt$,
  $md$A condition inside an `if` statement must evaluate to a ___ value, meaning either True or False.$md$,
  'medium',
  5,
  18,
  'fill_blank',
  $txt$boolean$txt$
);


-- ----------------------------------------------------------------------------
-- 6. TOPIC CONTENT: try_it_examples + common_mistakes
-- ----------------------------------------------------------------------------

update topics set
  try_it_examples = '[
    {"description": "Check if a number is positive, negative, or zero", "code": "n = -3\nif n > 0:\n    print(\"Positive\")\nelif n < 0:\n    print(\"Negative\")\nelse:\n    print(\"Zero\")", "output": "Negative"},
    {"description": "A nested if inside an elif branch for a simple grade check", "code": "score = 72\nif score >= 90:\n    print(\"A\")\nelif score >= 70:\n    print(\"C or better\")\nelse:\n    print(\"Needs improvement\")", "output": "C or better"},
    {"description": "A one-line conditional expression (the ternary form of if/else)", "code": "age = 15\nstatus = \"Minor\" if age < 18 else \"Adult\"\nprint(status)", "output": "Minor"}
  ]'::jsonb,
  common_mistakes = $md$### Common Mistakes with Conditionals

**Using `=` instead of `==`.** A single `=` is assignment, while `==` compares two values. Writing `if x = 5:` is actually a syntax error in Python, but the habit is still worth breaking early: always use `==` inside a condition, and `=` only to assign.

**Forgetting `elif` and writing separate `if` statements.** If you write `if x > 10: ...` followed by a second, unrelated `if x > 5: ...` instead of `elif`, both blocks can run even when only one should. Chain related conditions with `elif` so only the first matching branch executes, and the rest are skipped.

**Indentation errors.** Python uses indentation, not braces, to decide what belongs inside an `if`, `elif`, or `else` block. A line indented at the wrong level silently attaches to the wrong branch (or raises an `IndentationError`), so keep every statement in a branch aligned consistently.

**Expecting a switch/case statement.** Python has no built-in switch/case statement, so a long `if`/`elif`/.../`else` chain (or a dictionary lookup, for more advanced cases) is the normal, idiomatic way to handle many branches. Do not look for syntax that is not there.

**Truthy/falsy surprises.** Values like `0`, `""`, `None`, and empty lists are all falsy, so `if my_list:` behaves differently than `if my_list is not None:`. Be explicit about what you are checking when the distinction between "empty" and "missing" matters.$md$
where id = 'a0000000-0000-0000-0000-000000000004';
