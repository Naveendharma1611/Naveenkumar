-- Phase 2 content seed: topic 'input-output' (Input and Output)
-- Adds 7 code questions, 5 MCQs, 3 fill-in-the-blank questions, and topic enrichment content.

insert into questions
  (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type)
values
  ('c0000000-0000-0000-0000-000000000008', 'a0000000-0000-0000-0000-000000000002',
   $txt$Greet the User$txt$,
   $md$Read a person's name from the input and print a friendly greeting.

**Input Format**

A single line containing the person's name.

**Output Format**

A single line: `Hello, <name>!`

**Example**

```
Input:
Alice

Output:
Hello, Alice!
```$md$,
   'easy', 10,
   $py$# Read the user's name from input and print a greeting.
# Example: if the input is "Alice", print "Hello, Alice!"

name = input()
# TODO: print the greeting
$py$,
   $txt$Use an f-string (or string concatenation) to build the greeting, then pass it to print().$txt$,
   $py$name = input()
print(f"Hello, {name}!")
$py$,
   4, 'code'),
  ('c0000000-0000-0000-0000-000000000009', 'a0000000-0000-0000-0000-000000000002',
   $txt$Add Two Numbers$txt$,
   $md$Read two integers, each given on its own line, and print their sum.

**Input Format**

Two lines, each containing one integer.

**Output Format**

A single line containing the sum of the two integers.

**Example**

```
Input:
3
5

Output:
8
```$md$,
   'easy', 10,
   $py$# Read two integers, each on its own line, and print their sum.

# TODO: read the first integer
# TODO: read the second integer
# TODO: print the sum
$py$,
   $txt$input() always returns a string — convert each value with int() before adding them.$txt$,
   $py$a = int(input())
b = int(input())
print(a + b)
$py$,
   5, 'code'),
  ('c0000000-0000-0000-0000-000000000010', 'a0000000-0000-0000-0000-000000000002',
   $txt$Sum on One Line$txt$,
   $md$Read two integers given on the same line, separated by a single space, and print their sum.

**Input Format**

One line containing two integers separated by a space, e.g. "4 6".

**Output Format**

A single line containing the sum of the two integers.

**Example**

```
Input:
4 6

Output:
10
```$md$,
   'easy', 10,
   $py$# Read two integers from a single line separated by a space.
# Example: "4 6" should print 10

# TODO: split the line into two parts and convert each to an integer
$py$,
   $txt$input().split() gives you a list of strings — convert each piece with int() before adding.$txt$,
   $py$a, b = input().split()
print(int(a) + int(b))
$py$,
   6, 'code'),
  ('c0000000-0000-0000-0000-000000000011', 'a0000000-0000-0000-0000-000000000002',
   $txt$Average to Two Decimals$txt$,
   $md$Read three integers given on one line, separated by spaces, and print their average formatted to exactly 2 decimal places.

**Input Format**

One line containing three integers separated by spaces, e.g. "1 2 3".

**Output Format**

A single line containing the average, formatted with exactly 2 digits after the decimal point.

**Example**

```
Input:
1 2 3

Output:
2.00
```$md$,
   'medium', 20,
   $py$# Read three integers from one line separated by spaces.
# Print their average rounded to exactly 2 decimal places.

# TODO: read and convert the three integers
# TODO: compute the average
# TODO: print it formatted to 2 decimal places
$py$,
   $txt$Use an f-string format spec like f'{value:.2f}' to control the number of decimal places.$txt$,
   $py$a, b, c = map(int, input().split())
avg = (a + b + c) / 3
print(f"{avg:.2f}")
$py$,
   7, 'code'),
  ('c0000000-0000-0000-0000-000000000012', 'a0000000-0000-0000-0000-000000000002',
   $txt$Custom Separators$txt$,
   $md$Read three words, each on its own line, and print them on a single line separated by `" - "` using a single print() call with the `sep` parameter.

**Input Format**

Three lines, each containing one word.

**Output Format**

A single line: `word1 - word2 - word3`.

**Example**

```
Input:
red
green
blue

Output:
red - green - blue
```$md$,
   'medium', 20,
   $py$# Read three words, each on its own line.
# Print them on a single line separated by " - " using one print() call.

# TODO: read the three words
# TODO: print them with sep=" - "
$py$,
   $txt$print() accepts multiple positional arguments and a sep= keyword argument that controls what goes between them.$txt$,
   $py$a = input()
b = input()
c = input()
print(a, b, c, sep=" - ")
$py$,
   8, 'code'),
  ('c0000000-0000-0000-0000-000000000013', 'a0000000-0000-0000-0000-000000000002',
   $txt$Student Report$txt$,
   $md$Read a student's name, age, and GPA, each on its own line, and print a formatted report line.

**Input Format**

Three lines: the student's name (text), age (integer), and GPA (decimal number).

**Output Format**

A single line: `Name: <name>, Age: <age>, GPA: <gpa to 1 decimal place>`.

**Example**

```
Input:
John
20
3.567

Output:
Name: John, Age: 20, GPA: 3.6
```$md$,
   'medium', 20,
   $py$# Read a student's name, age, and GPA (each on its own line).
# Print: Name: <name>, Age: <age>, GPA: <gpa to 1 decimal place>

# TODO: read the name, and convert age/gpa to the right types
# TODO: print the formatted report
$py$,
   $txt$Convert age with int() and gpa with float(), then use an f-string with a :.1f format spec for the GPA.$txt$,
   $py$name = input()
age = int(input())
gpa = float(input())
print(f"Name: {name}, Age: {age}, GPA: {gpa:.1f}")
$py$,
   9, 'code'),
  ('c0000000-0000-0000-0000-000000000014', 'a0000000-0000-0000-0000-000000000002',
   $txt$Formatted Score Table$txt$,
   $md$Read an integer `n`, the number of students, followed by `n` lines each containing a student's name and integer score separated by a space. Print one line per student, with the name left-aligned in a field of width 10 and the score right-aligned in a field of width 5, in the same order as the input.

**Input Format**

The first line contains an integer `n`. Each of the next `n` lines contains a name and an integer score separated by a space.

**Output Format**

`n` lines, each formatted as the name left-aligned in 10 characters immediately followed by the score right-aligned in 5 characters.

**Example**

```
Input:
2
Alice 90
Bob 85

Output:
Alice        90
Bob          85
```$md$,
   'hard', 30,
   $py$# Read an integer n, then n lines of "name score".
# Print each as: name left-aligned in 10 characters, score right-aligned in 5 characters.

# TODO: read n
# TODO: loop n times, reading and formatting each line
$py$,
   $txt$Format specs like f'{name:<10}{score:>5}' control alignment and field width.$txt$,
   $py$n = int(input())
for _ in range(n):
    name, score = input().split()
    print(f"{name:<10}{int(score):>5}")
$py$,
   10, 'code');

insert into test_cases (question_id, stdin, expected_output, is_sample, order_index)
values
  ('c0000000-0000-0000-0000-000000000008',
   $txt$Alice$txt$,
   $txt$Hello, Alice!$txt$,
   true, 0),
  ('c0000000-0000-0000-0000-000000000009',
   $txt$3
5$txt$,
   $txt$8$txt$,
   true, 0),
  ('c0000000-0000-0000-0000-000000000010',
   $txt$4 6$txt$,
   $txt$10$txt$,
   true, 0),
  ('c0000000-0000-0000-0000-000000000011',
   $txt$1 2 3$txt$,
   $txt$2.00$txt$,
   true, 0),
  ('c0000000-0000-0000-0000-000000000012',
   $txt$red
green
blue$txt$,
   $txt$red - green - blue$txt$,
   true, 0),
  ('c0000000-0000-0000-0000-000000000013',
   $txt$John
20
3.567$txt$,
   $txt$Name: John, Age: 20, GPA: 3.6$txt$,
   true, 0),
  ('c0000000-0000-0000-0000-000000000014',
   $txt$2
Alice 90
Bob 85$txt$,
   $txt$Alice        90
Bob          85$txt$,
   true, 0);

insert into hidden_test_cases (question_id, stdin, expected_output, order_index)
values
  ('c0000000-0000-0000-0000-000000000008',
   $txt$Bob$txt$,
   $txt$Hello, Bob!$txt$,
   0),
  ('c0000000-0000-0000-0000-000000000008',
   $txt$Zoe Smith$txt$,
   $txt$Hello, Zoe Smith!$txt$,
   1),
  ('c0000000-0000-0000-0000-000000000009',
   $txt$0
0$txt$,
   $txt$0$txt$,
   0),
  ('c0000000-0000-0000-0000-000000000009',
   $txt$-5
10$txt$,
   $txt$5$txt$,
   1),
  ('c0000000-0000-0000-0000-000000000010',
   $txt$0 0$txt$,
   $txt$0$txt$,
   0),
  ('c0000000-0000-0000-0000-000000000010',
   $txt$-3 -7$txt$,
   $txt$-10$txt$,
   1),
  ('c0000000-0000-0000-0000-000000000011',
   $txt$0 0 0$txt$,
   $txt$0.00$txt$,
   0),
  ('c0000000-0000-0000-0000-000000000011',
   $txt$-1 -2 -3$txt$,
   $txt$-2.00$txt$,
   1),
  ('c0000000-0000-0000-0000-000000000011',
   $txt$7 8 10$txt$,
   $txt$8.33$txt$,
   2),
  ('c0000000-0000-0000-0000-000000000012',
   $txt$cat
dog
fish$txt$,
   $txt$cat - dog - fish$txt$,
   0),
  ('c0000000-0000-0000-0000-000000000012',
   $txt$1
2
3$txt$,
   $txt$1 - 2 - 3$txt$,
   1),
  ('c0000000-0000-0000-0000-000000000012',
   $txt$one
two
three$txt$,
   $txt$one - two - three$txt$,
   2),
  ('c0000000-0000-0000-0000-000000000013',
   $txt$Mary
19
3.5$txt$,
   $txt$Name: Mary, Age: 19, GPA: 3.5$txt$,
   0),
  ('c0000000-0000-0000-0000-000000000013',
   $txt$Zoe
0
0.0$txt$,
   $txt$Name: Zoe, Age: 0, GPA: 0.0$txt$,
   1),
  ('c0000000-0000-0000-0000-000000000013',
   $txt$Alexander The Great
100
9.999$txt$,
   $txt$Name: Alexander The Great, Age: 100, GPA: 10.0$txt$,
   2),
  ('c0000000-0000-0000-0000-000000000014',
   $txt$0$txt$,
   $txt$$txt$,
   0),
  ('c0000000-0000-0000-0000-000000000014',
   $txt$1
Alexandria 75$txt$,
   $txt$Alexandria   75$txt$,
   1),
  ('c0000000-0000-0000-0000-000000000014',
   $txt$2
Al 5
Bo -3$txt$,
   $txt$Al            5
Bo           -3$txt$,
   2),
  ('c0000000-0000-0000-0000-000000000014',
   $txt$3
A 1
BB 22
CCC 333$txt$,
   $txt$A             1
BB           22
CCC         333$txt$,
   3);

insert into questions
  (id, topic_id, title, prompt, difficulty, points, order_index, question_type, options, correct_option)
values
  ('d0000000-0000-0000-0000-000000000006', 'a0000000-0000-0000-0000-000000000002',
   $txt$Type of input()$txt$,
   $md$What type of value does Python's `input()` function always return, regardless of what the user types?$md$,
   'easy', 5, 11, 'mcq',
   '["int", "float", "str", "bool"]'::jsonb, 2),
  ('d0000000-0000-0000-0000-000000000007', 'a0000000-0000-0000-0000-000000000002',
   $txt$Displaying Output$txt$,
   $md$Which built-in function is used to display output to the console in Python?$md$,
   'easy', 5, 12, 'mcq',
   '["read()", "print()", "write()", "echo()"]'::jsonb, 1),
  ('d0000000-0000-0000-0000-000000000008', 'a0000000-0000-0000-0000-000000000002',
   $txt$Invalid Conversion$txt$,
   $md$What happens when you run `int(input())` and the user types the text `abc`?$md$,
   'medium', 5, 13, 'mcq',
   '["It raises a TypeError", "It raises a SyntaxError", "It raises a ValueError", "It silently returns 0"]'::jsonb, 2),
  ('d0000000-0000-0000-0000-000000000009', 'a0000000-0000-0000-0000-000000000002',
   $txt$Default print() Separator$txt$,
   $md$When you call `print("a", "b", "c")` without a `sep` argument, what separates the values in the output?$md$,
   'medium', 5, 14, 'mcq',
   '["A comma", "A single space", "A tab character", "No separator at all"]'::jsonb, 1),
  ('d0000000-0000-0000-0000-000000000010', 'a0000000-0000-0000-0000-000000000002',
   $txt$Parsing Multiple Numbers$txt$,
   $md$If the input line is `5 10 15`, what does `list(map(int, input().split()))` produce?$md$,
   'hard', 5, 15, 'mcq',
   '["[''5'', ''10'', ''15'']", "[5, 10, 15]", "(5, 10, 15)", "''5 10 15''"]'::jsonb, 1);

insert into questions
  (id, topic_id, title, prompt, difficulty, points, order_index, question_type, correct_answer)
values
  ('e0000000-0000-0000-0000-000000000004', 'a0000000-0000-0000-0000-000000000002',
   $txt$The input() Function$txt$,
   $md$The `___()` function reads a line of text input from the user in Python.$md$,
   'easy', 5, 16, 'fill_blank',
   $txt$input$txt$),
  ('e0000000-0000-0000-0000-000000000005', 'a0000000-0000-0000-0000-000000000002',
   $txt$Return Type of input()$txt$,
   $md$No matter what the user types, Python's `input()` function always returns a value of type `___`.$md$,
   'medium', 5, 17, 'fill_blank',
   $txt$str$txt$),
  ('e0000000-0000-0000-0000-000000000006', 'a0000000-0000-0000-0000-000000000002',
   $txt$Splitting a Line of Input$txt$,
   $md$The string method `___()` splits a line of input text into a list of substrings, using whitespace as the default separator.$md$,
   'medium', 5, 18, 'fill_blank',
   $txt$split$txt$);

update topics
set try_it_examples = '[{"description": "Reading input and converting its type", "code": "# Suppose the user enters: 7\nvalue = input()\nprint(type(value))\nnumber = int(value)\nprint(number + 3)", "output": "<class ''str''>\n10"}, {"description": "Printing multiple values with a custom separator and end", "code": "print(\"apple\", \"banana\", \"cherry\", sep=\", \", end=\"!\\n\")\nprint(\"Next line\")", "output": "apple, banana, cherry!\nNext line"}, {"description": "Formatting a number to two decimal places", "code": "price = 49.5\nquantity = 3\ntotal = price * quantity\nprint(f\"Total: ${total:.2f}\")", "output": "Total: $148.50"}]'::jsonb,
    common_mistakes = $md$Beginners run into the same handful of input/output traps:

- **Forgetting `input()` always returns a string.** `age = input()` makes `age` a `str`, so `age + 1` raises a `TypeError`. Fix: convert explicitly with `int(input())` or `float(input())` before doing math.
- **Mixing up `print()`'s `sep` and `end`.** `sep` controls what goes *between* multiple arguments in one `print()` call; `end` controls what's added *after* the whole call (default `"\n"`). Fix: pass `sep=", "` or `end=""` explicitly when you need something other than the defaults.
- **Off-by-one errors with `split()`.** `input().split()` splits on any whitespace and returns a list, so `a, b = input().split()` fails with "too many values to unpack" if the line has more or fewer than two tokens. Fix: check the expected number of values, or use `split(maxsplit=...)` when appropriate.
- **Typos in format strings.** Writing `f"{value:.2f"` (missing the closing brace) or forgetting the `f` prefix entirely prints the literal text instead of the value. Fix: double-check every f-string has a matching `{ }` pair and the `f` prefix.
- **Assuming extra whitespace or blank lines don't matter.** Leftover `\n` characters from `input()` (when reading pre-written input) or stray spaces in concatenated output can make output comparisons fail even though the "visible" text looks right. Fix: use `.strip()` on input when trailing whitespace isn't meaningful, and print exactly the format the problem asks for.$md$
where id = 'a0000000-0000-0000-0000-000000000002';
