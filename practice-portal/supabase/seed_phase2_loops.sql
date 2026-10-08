-- Phase 2 content expansion: Loops (for, while)
-- topic slug: loops, topic_id = a0000000-0000-0000-0000-000000000005
-- Adds 7 new code questions (3 easy, 3 medium, 1 hard) on top of the existing
-- 3 (order_index 1-3), 5 MCQ questions, 3 fill-in-the-blank questions, and
-- updates the topic's try_it_examples / common_mistakes content.

-- =========================================================================
-- 1. CODE QUESTIONS (order_index 4-10)
-- =========================================================================

-- ---- Question c...029 (easy, order 4): Sum of First N Natural Numbers ----
insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type) values (
  'c0000000-0000-0000-0000-000000000029',
  'a0000000-0000-0000-0000-000000000005',
  $txt$Sum of First N Natural Numbers$txt$,
  $md$Given a positive integer **N**, calculate the sum of all natural numbers from 1 to N (inclusive) using a `for` loop.

**Input Format**

A single integer N.

**Output Format**

A single integer: the sum of the numbers from 1 to N.

**Example**

```
Input:
5

Output:
15
```
$md$,
  'easy',
  10,
  $py$n = int(input())
# write your code here
$py$,
  $txt$Use a for loop with range(1, n + 1) and accumulate a running total.$txt$,
  $py$n = int(input())
total = 0
for i in range(1, n + 1):
    total += i
print(total)
$py$,
  4,
  'code'
);

-- test cases for c...029
insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values
  ('c0000000-0000-0000-0000-000000000029', $txt$5$txt$, $txt$15$txt$, true, 0);

insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values
  ('c0000000-0000-0000-0000-000000000029', $txt$1$txt$, $txt$1$txt$, 0),
  ('c0000000-0000-0000-0000-000000000029', $txt$100$txt$, $txt$5050$txt$, 1);


-- ---- Question c...030 (easy, order 5): Count Even Numbers ----
insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type) values (
  'c0000000-0000-0000-0000-000000000030',
  'a0000000-0000-0000-0000-000000000005',
  $txt$Count Even Numbers$txt$,
  $md$You are given N integers. Using a `for` loop, count how many of them are even.

**Input Format**

The first line contains an integer N. The second line contains N space-separated integers.

**Output Format**

A single integer: the count of even numbers.

**Example**

```
Input:
5
1 2 3 4 5

Output:
2
```
$md$,
  'easy',
  10,
  $py$n = int(input())
nums = list(map(int, input().split()))
# write your code here
$py$,
  $txt$Loop through each number with a for loop and use the modulo operator % to check if it's even (num % 2 == 0). Remember 0 counts as even.$txt$,
  $py$n = int(input())
nums = list(map(int, input().split()))
count = 0
for num in nums:
    if num % 2 == 0:
        count += 1
print(count)
$py$,
  5,
  'code'
);

-- test cases for c...030
insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values
  ('c0000000-0000-0000-0000-000000000030', $txt$5
1 2 3 4 5$txt$, $txt$2$txt$, true, 0);

insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values
  ('c0000000-0000-0000-0000-000000000030', $txt$6
-2 -3 0 7 8 10$txt$, $txt$4$txt$, 0),
  ('c0000000-0000-0000-0000-000000000030', $txt$1
3$txt$, $txt$0$txt$, 1);


-- ---- Question c...031 (easy, order 6): Print Multiplication Table ----
insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type) values (
  'c0000000-0000-0000-0000-000000000031',
  'a0000000-0000-0000-0000-000000000005',
  $txt$Print Multiplication Table$txt$,
  $md$Given an integer N, print its multiplication table from 1 to 10 using a `for` loop. Print one line per row in the exact format `N x i = result`.

**Input Format**

A single integer N.

**Output Format**

10 lines, one for each i from 1 to 10, in the format `N x i = N*i`.

**Example**

```
Input:
3

Output:
3 x 1 = 3
3 x 2 = 6
3 x 3 = 9
3 x 4 = 12
3 x 5 = 15
3 x 6 = 18
3 x 7 = 21
3 x 8 = 24
3 x 9 = 27
3 x 10 = 30
```
$md$,
  'easy',
  10,
  $py$n = int(input())
# write your code here
$py$,
  $txt$Use a for loop with range(1, 11) and print each line using an f-string like f"{n} x {i} = {n * i}".$txt$,
  $py$n = int(input())
for i in range(1, 11):
    print(f"{n} x {i} = {n * i}")
$py$,
  6,
  'code'
);

-- test cases for c...031
insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values
  ('c0000000-0000-0000-0000-000000000031', $txt$3$txt$, $txt$3 x 1 = 3
3 x 2 = 6
3 x 3 = 9
3 x 4 = 12
3 x 5 = 15
3 x 6 = 18
3 x 7 = 21
3 x 8 = 24
3 x 9 = 27
3 x 10 = 30$txt$, true, 0);

insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values
  ('c0000000-0000-0000-0000-000000000031', $txt$1$txt$, $txt$1 x 1 = 1
1 x 2 = 2
1 x 3 = 3
1 x 4 = 4
1 x 5 = 5
1 x 6 = 6
1 x 7 = 7
1 x 8 = 8
1 x 9 = 9
1 x 10 = 10$txt$, 0),
  ('c0000000-0000-0000-0000-000000000031', $txt$0$txt$, $txt$0 x 1 = 0
0 x 2 = 0
0 x 3 = 0
0 x 4 = 0
0 x 5 = 0
0 x 6 = 0
0 x 7 = 0
0 x 8 = 0
0 x 9 = 0
0 x 10 = 0$txt$, 1);


-- ---- Question c...032 (medium, order 7): Sum of Digits ----
insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type) values (
  'c0000000-0000-0000-0000-000000000032',
  'a0000000-0000-0000-0000-000000000005',
  $txt$Sum of Digits$txt$,
  $md$Given a non-negative integer N, find the sum of its digits using a `while` loop.

**Input Format**

A single non-negative integer N.

**Output Format**

A single integer: the sum of the digits of N.

**Example**

```
Input:
1234

Output:
10
```
$md$,
  'medium',
  20,
  $py$n = int(input())
# write your code here
$py$,
  $txt$Use a while loop: repeatedly take n % 10 to get the last digit, add it to a running total, then use n //= 10 to remove that digit. Stop when n becomes 0.$txt$,
  $py$n = int(input())
total = 0
while n > 0:
    total += n % 10
    n //= 10
print(total)
$py$,
  7,
  'code'
);

-- test cases for c...032
insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values
  ('c0000000-0000-0000-0000-000000000032', $txt$1234$txt$, $txt$10$txt$, true, 0);

insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values
  ('c0000000-0000-0000-0000-000000000032', $txt$0$txt$, $txt$0$txt$, 0),
  ('c0000000-0000-0000-0000-000000000032', $txt$999999$txt$, $txt$54$txt$, 1),
  ('c0000000-0000-0000-0000-000000000032', $txt$500$txt$, $txt$5$txt$, 2);


-- ---- Question c...033 (medium, order 8): Reverse a Number ----
insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type) values (
  'c0000000-0000-0000-0000-000000000033',
  'a0000000-0000-0000-0000-000000000005',
  $txt$Reverse a Number$txt$,
  $md$Given a non-negative integer N, reverse its digits using a `while` loop and print the result as an integer (so any trailing zeros in the original number simply disappear from the front of the reversed result).

**Input Format**

A single non-negative integer N.

**Output Format**

A single integer: N with its digits reversed.

**Example**

```
Input:
1234

Output:
4321
```
$md$,
  'medium',
  20,
  $py$n = int(input())
# write your code here
$py$,
  $txt$Use a while loop with n % 10 to peel off the last digit and build up the reversed number as reversed_num = reversed_num * 10 + digit, then shrink n with n //= 10.$txt$,
  $py$n = int(input())
reversed_num = 0
while n > 0:
    digit = n % 10
    reversed_num = reversed_num * 10 + digit
    n //= 10
print(reversed_num)
$py$,
  8,
  'code'
);

-- test cases for c...033
insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values
  ('c0000000-0000-0000-0000-000000000033', $txt$1234$txt$, $txt$4321$txt$, true, 0);

insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values
  ('c0000000-0000-0000-0000-000000000033', $txt$0$txt$, $txt$0$txt$, 0),
  ('c0000000-0000-0000-0000-000000000033', $txt$1200$txt$, $txt$21$txt$, 1),
  ('c0000000-0000-0000-0000-000000000033', $txt$7$txt$, $txt$7$txt$, 2);


-- ---- Question c...034 (medium, order 9): First N Fibonacci Numbers ----
insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type) values (
  'c0000000-0000-0000-0000-000000000034',
  'a0000000-0000-0000-0000-000000000005',
  $txt$First N Fibonacci Numbers$txt$,
  $md$Given an integer N (N >= 0), print the first N Fibonacci numbers (starting 0, 1, 1, 2, 3, ...) on one line, separated by single spaces. If N is 0, print an empty line.

**Input Format**

A single integer N.

**Output Format**

The first N Fibonacci numbers, space-separated, on one line.

**Example**

```
Input:
7

Output:
0 1 1 2 3 5 8
```
$md$,
  'medium',
  20,
  $py$n = int(input())
# write your code here
$py$,
  $txt$Keep two variables for the previous two Fibonacci numbers and update both of them inside a for loop that runs n times, collecting each value before updating.$txt$,
  $py$n = int(input())
a, b = 0, 1
result = []
for _ in range(n):
    result.append(a)
    a, b = b, a + b
print(" ".join(map(str, result)))
$py$,
  9,
  'code'
);

-- test cases for c...034
insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values
  ('c0000000-0000-0000-0000-000000000034', $txt$7$txt$, $txt$0 1 1 2 3 5 8$txt$, true, 0);

insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values
  ('c0000000-0000-0000-0000-000000000034', $txt$0$txt$, $txt$$txt$, 0),
  ('c0000000-0000-0000-0000-000000000034', $txt$1$txt$, $txt$0$txt$, 1),
  ('c0000000-0000-0000-0000-000000000034', $txt$10$txt$, $txt$0 1 1 2 3 5 8 13 21 34$txt$, 2);


-- ---- Question c...035 (hard, order 10): Sum Until Sentinel (Skip Negatives) ----
insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type) values (
  'c0000000-0000-0000-0000-000000000035',
  'a0000000-0000-0000-0000-000000000005',
  $txt$Sum Until Sentinel (Skip Negatives)$txt$,
  $md$You will receive a sequence of integers, one per line, that always ends with the sentinel value **0**. Read the integers one at a time using a `while` loop:

- When you read **0**, stop reading immediately using `break` (the 0 itself is not counted).
- For every other number, if it is **negative**, skip it using `continue` (do not add it to the total).
- Otherwise, add it to a running total.

After the loop ends, print the total sum of all non-negative numbers read before the sentinel.

**Input Format**

Several lines, each containing one integer. The sequence always ends with a line containing 0.

**Output Format**

A single integer: the sum of the non-negative numbers read before the sentinel.

**Example**

```
Input:
5
-3
10
0

Output:
15
```
$md$,
  'hard',
  30,
  $py$# write your code here
$py$,
  $txt$Use `while True:` to read lines one at a time with input(). Use break when you read 0, and continue to skip negative numbers without adding them to the total.$txt$,
  $py$total = 0
while True:
    n = int(input())
    if n == 0:
        break
    if n < 0:
        continue
    total += n
print(total)
$py$,
  10,
  'code'
);

-- test cases for c...035
insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values
  ('c0000000-0000-0000-0000-000000000035', $txt$5
-3
10
0$txt$, $txt$15$txt$, true, 0);

insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values
  ('c0000000-0000-0000-0000-000000000035', $txt$0$txt$, $txt$0$txt$, 0),
  ('c0000000-0000-0000-0000-000000000035', $txt$-1
-2
-3
0$txt$, $txt$0$txt$, 1),
  ('c0000000-0000-0000-0000-000000000035', $txt$1
2
3
4
5
0$txt$, $txt$15$txt$, 2),
  ('c0000000-0000-0000-0000-000000000035', $txt$100
-50
-25
200
0
999$txt$, $txt$300$txt$, 3);


-- =========================================================================
-- 2. MCQ QUESTIONS (order_index 11-15)
-- =========================================================================

insert into questions (id, topic_id, title, prompt, difficulty, points, order_index, question_type, options, correct_option) values (
  'd0000000-0000-0000-0000-000000000021',
  'a0000000-0000-0000-0000-000000000005',
  $txt$Loop Iteration Count$txt$,
  $md$How many times does the loop below execute?

```python
for i in range(5):
    print(i)
```
$md$,
  'easy',
  5,
  11,
  'mcq',
  '["4", "5", "6", "It depends on i"]'::jsonb,
  1
);

insert into questions (id, topic_id, title, prompt, difficulty, points, order_index, question_type, options, correct_option) values (
  'd0000000-0000-0000-0000-000000000022',
  'a0000000-0000-0000-0000-000000000005',
  $txt$range() with a Step$txt$,
  $md$What values does the loop below print?

```python
for i in range(2, 10, 3):
    print(i, end=" ")
```
$md$,
  'medium',
  5,
  12,
  'mcq',
  '["2 5 8", "2 5 8 9", "2 4 6 8", "2 5 8 11"]'::jsonb,
  0
);

insert into questions (id, topic_id, title, prompt, difficulty, points, order_index, question_type, options, correct_option) values (
  'd0000000-0000-0000-0000-000000000023',
  'a0000000-0000-0000-0000-000000000005',
  $txt$What Does This while Loop Print?$txt$,
  $md$What does the code below print (each value on its own line, in order)?

```python
i = 0
while i < 3:
    print(i)
    i += 1
```
$md$,
  'easy',
  5,
  13,
  'mcq',
  '["0 1 2", "1 2 3", "0 1 2 3", "Infinite loop"]'::jsonb,
  0
);

insert into questions (id, topic_id, title, prompt, difficulty, points, order_index, question_type, options, correct_option) values (
  'd0000000-0000-0000-0000-000000000024',
  'a0000000-0000-0000-0000-000000000005',
  $txt$Exiting a Loop Early$txt$,
  $md$Inside a loop, which keyword immediately exits the loop entirely, skipping any remaining iterations?$md$,
  'easy',
  5,
  14,
  'mcq',
  '["continue", "break", "pass", "return"]'::jsonb,
  1
);

insert into questions (id, topic_id, title, prompt, difficulty, points, order_index, question_type, options, correct_option) values (
  'd0000000-0000-0000-0000-000000000025',
  'a0000000-0000-0000-0000-000000000005',
  $txt$Tracing continue$txt$,
  $md$What does the code below print (each printed value on its own line, in order)?

```python
for i in range(3):
    if i == 1:
        continue
    print(i)
```
$md$,
  'medium',
  5,
  15,
  'mcq',
  '["0 1 2", "0 2", "1 2", "0 1"]'::jsonb,
  1
);


-- =========================================================================
-- 3. FILL-IN-THE-BLANK QUESTIONS (order_index 16-18)
-- =========================================================================

insert into questions (id, topic_id, title, prompt, difficulty, points, order_index, question_type, correct_answer) values (
  'e0000000-0000-0000-0000-000000000013',
  'a0000000-0000-0000-0000-000000000005',
  $txt$Exiting a Loop$txt$,
  $md$The `___` statement immediately exits the nearest enclosing loop in Python.$md$,
  'easy',
  5,
  16,
  'fill_blank',
  $txt$break$txt$
);

insert into questions (id, topic_id, title, prompt, difficulty, points, order_index, question_type, correct_answer) values (
  'e0000000-0000-0000-0000-000000000014',
  'a0000000-0000-0000-0000-000000000005',
  $txt$Skipping an Iteration$txt$,
  $md$The `___` statement skips the rest of the current loop iteration and moves on to the next one.$md$,
  'easy',
  5,
  17,
  'fill_blank',
  $txt$continue$txt$
);

insert into questions (id, topic_id, title, prompt, difficulty, points, order_index, question_type, correct_answer) values (
  'e0000000-0000-0000-0000-000000000015',
  'a0000000-0000-0000-0000-000000000005',
  $txt$range() Starting Point$txt$,
  $md$`range(5)` generates the sequence of integers starting at ___ and ending just before 5.$md$,
  'medium',
  5,
  18,
  'fill_blank',
  $txt$0$txt$
);


-- =========================================================================
-- 4. TOPIC CONTENT UPDATE (try_it_examples + common_mistakes)
-- =========================================================================

update topics set
  try_it_examples = '[
    {"description": "Sum of numbers 1 to 5 using a for loop", "code": "total = 0\nfor i in range(1, 6):\n    total += i\nprint(total)", "output": "15"},
    {"description": "Print numbers 0 to 4 using a while loop", "code": "i = 0\nwhile i < 5:\n    print(i)\n    i += 1", "output": "0\n1\n2\n3\n4"},
    {"description": "Using break to stop a loop early when a target number is found", "code": "numbers = [4, 9, 2, 7, 5]\nfor n in numbers:\n    if n == 2:\n        print(\"Found 2!\")\n        break\n    print(n)", "output": "4\n9\nFound 2!"}
  ]'::jsonb,
  common_mistakes = $md$### Common Mistakes with Loops

- **Off-by-one errors with `range()` endpoints.** `range(1, n)` stops *before* n, so it excludes n. If you want to include n, use `range(1, n + 1)`. Always double-check whether your loop should run n times or up to-and-including n.

- **Infinite `while` loops.** A `while` loop only stops when its condition becomes false. If you forget to update the variable the condition depends on (e.g. forgetting `i += 1`), the loop never ends. Always make sure something inside the loop body moves you closer to the exit condition.

- **Modifying a list while iterating over it.** Removing or adding items to a list inside a `for item in my_list:` loop can silently skip elements or cause unexpected results, because the loop tracks a changing index into a changing list. Iterate over a copy instead (`for item in list(my_list):`) or build a new list rather than mutating the original mid-loop.

- **Confusing `break` and `continue`.** `break` exits the loop entirely — no more iterations run. `continue` only skips the rest of the *current* iteration and moves on to the next one. Mixing these up is a common source of bugs when filtering values inside a loop.

- **Forgetting `range(n)` starts at 0.** `range(n)` produces `0, 1, 2, ..., n-1` — n values total, not including n itself. This trips up beginners translating 1-based counting into code.
$md$
where id = 'a0000000-0000-0000-0000-000000000005';
