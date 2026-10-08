-- ============================================================================
-- Phase 2 content seed: Strings topic
-- topic_id = a0000000-0000-0000-0000-000000000006 (slug: strings, title: Strings)
--
-- Adds 7 new code questions (order_index 4-10, on top of the 3 existing
-- questions at order_index 1-3), 5 MCQ questions (order_index 11-15), and
-- 3 fill-in-the-blank questions (order_index 16-18). Also updates the
-- topic's try_it_examples and common_mistakes columns.
--
-- Every code solution was executed against every one of its test cases with
-- a real Python 3 interpreter (trimmed stdout compared to expected_output)
-- before this file was finalized. See the agent report for verification
-- details.
-- ============================================================================


-- ----------------------------------------------------------------------------
-- 1. CODE QUESTIONS
-- ----------------------------------------------------------------------------

-- Q1 (easy, order_index 4): String Length ----------------------------------
insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type)
values (
  'c0000000-0000-0000-0000-000000000036',
  'a0000000-0000-0000-0000-000000000006',
  $txt$String Length$txt$,
  $md$Write a program that reads a single line of text and prints the number of characters it contains.

**Input Format**
A single line containing a string `s` (it may contain spaces, or be empty).

**Output Format**
A single integer: the length of `s`.

**Example**
```
Input:
hello

Output:
5
```
$md$,
  'easy',
  10,
  $py$s = input()
# TODO: print the length of s
$py$,
  $txt$Python's built-in len() function returns the number of characters in a string, including spaces.$txt$,
  $py$s = input()
print(len(s))
$py$,
  4,
  'code'
);

insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values
  ('c0000000-0000-0000-0000-000000000036', $txt$hello$txt$, $txt$5$txt$, true, 0);

insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values
  ('c0000000-0000-0000-0000-000000000036', $txt$
$txt$, $txt$0$txt$, 0),
  ('c0000000-0000-0000-0000-000000000036', $txt$Hello World!$txt$, $txt$12$txt$, 1);


-- Q2 (easy, order_index 5): Reverse a String --------------------------------
insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type)
values (
  'c0000000-0000-0000-0000-000000000037',
  'a0000000-0000-0000-0000-000000000006',
  $txt$Reverse a String$txt$,
  $md$Write a program that reads a single line of text and prints it reversed.

**Input Format**
A single line containing a string `s`.

**Output Format**
A single line: `s` reversed.

**Example**
```
Input:
hello

Output:
olleh
```
$md$,
  'easy',
  10,
  $py$s = input()
# TODO: print the reverse of s
$py$,
  $txt$Slicing with a step of -1 (s[::-1]) walks through a string backwards.$txt$,
  $py$s = input()
print(s[::-1])
$py$,
  5,
  'code'
);

insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values
  ('c0000000-0000-0000-0000-000000000037', $txt$hello$txt$, $txt$olleh$txt$, true, 0);

insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values
  ('c0000000-0000-0000-0000-000000000037', $txt$a$txt$, $txt$a$txt$, 0),
  ('c0000000-0000-0000-0000-000000000037', $txt$Python 3$txt$, $txt$3 nohtyP$txt$, 1);


-- Q3 (easy, order_index 6): Upper and Lower Case -----------------------------
insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type)
values (
  'c0000000-0000-0000-0000-000000000038',
  'a0000000-0000-0000-0000-000000000006',
  $txt$Upper and Lower Case$txt$,
  $md$Write a program that reads a single line of text and prints it in uppercase, then on the next line prints it in lowercase.

**Input Format**
A single line containing a string `s`.

**Output Format**
Two lines: `s` converted to uppercase, then `s` converted to lowercase.

**Example**
```
Input:
Hello World

Output:
HELLO WORLD
hello world
```
$md$,
  'easy',
  10,
  $py$s = input()
# TODO: print s in uppercase, then on the next line print s in lowercase
$py$,
  $txt$Strings have .upper() and .lower() methods that return new strings -- they do not change the original.$txt$,
  $py$s = input()
print(s.upper())
print(s.lower())
$py$,
  6,
  'code'
);

insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values
  ('c0000000-0000-0000-0000-000000000038', $txt$Hello World$txt$, $txt$HELLO WORLD
hello world$txt$, true, 0);

insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values
  ('c0000000-0000-0000-0000-000000000038', $txt$abc$txt$, $txt$ABC
abc$txt$, 0),
  ('c0000000-0000-0000-0000-000000000038', $txt$MiXeD CaSe!$txt$, $txt$MIXED CASE!
mixed case!$txt$, 1);


-- Q4 (medium, order_index 7): Count the Vowels -------------------------------
insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type)
values (
  'c0000000-0000-0000-0000-000000000039',
  'a0000000-0000-0000-0000-000000000006',
  $txt$Count the Vowels$txt$,
  $md$Write a program that reads a single line of text and prints how many vowels it contains. Count `a`, `e`, `i`, `o`, `u` in both uppercase and lowercase.

**Input Format**
A single line containing a string `s` (it may be empty).

**Output Format**
A single integer: the number of vowels in `s`.

**Example**
```
Input:
Hello World

Output:
3
```
$md$,
  'medium',
  20,
  $py$s = input()
# TODO: count and print the number of vowels (a, e, i, o, u, case-insensitive) in s
$py$,
  $txt$Loop over each character and check if it is in the string "aeiouAEIOU".$txt$,
  $py$s = input()
vowels = "aeiouAEIOU"
count = 0
for ch in s:
    if ch in vowels:
        count += 1
print(count)
$py$,
  7,
  'code'
);

insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values
  ('c0000000-0000-0000-0000-000000000039', $txt$Hello World$txt$, $txt$3$txt$, true, 0);

insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values
  ('c0000000-0000-0000-0000-000000000039', $txt$
$txt$, $txt$0$txt$, 0),
  ('c0000000-0000-0000-0000-000000000039', $txt$xyz$txt$, $txt$0$txt$, 1),
  ('c0000000-0000-0000-0000-000000000039', $txt$AEIOUaeiou$txt$, $txt$10$txt$, 2);


-- Q5 (medium, order_index 8): Palindrome Check -------------------------------
insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type)
values (
  'c0000000-0000-0000-0000-000000000040',
  'a0000000-0000-0000-0000-000000000006',
  $txt$Palindrome Check$txt$,
  $md$Write a program that reads a single line of text and prints `Yes` if it is a palindrome (reads the same forwards and backwards), ignoring spaces and letter case, or `No` otherwise.

**Input Format**
A single line containing a string `s` (it may contain spaces, or be empty).

**Output Format**
A single line: `Yes` or `No`.

**Example**
```
Input:
Madam

Output:
Yes
```
$md$,
  'medium',
  20,
  $py$s = input()
# TODO: print "Yes" if s is a palindrome (ignoring spaces and case), else print "No"
$py$,
  $txt$Remove spaces and normalize case first, then compare the string to its reverse using slicing.$txt$,
  $py$s = input()
normalized = s.replace(" ", "").lower()
if normalized == normalized[::-1]:
    print("Yes")
else:
    print("No")
$py$,
  8,
  'code'
);

insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values
  ('c0000000-0000-0000-0000-000000000040', $txt$Madam$txt$, $txt$Yes$txt$, true, 0);

insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values
  ('c0000000-0000-0000-0000-000000000040', $txt$Hello$txt$, $txt$No$txt$, 0),
  ('c0000000-0000-0000-0000-000000000040', $txt$race a car$txt$, $txt$No$txt$, 1),
  ('c0000000-0000-0000-0000-000000000040', $txt$
$txt$, $txt$Yes$txt$, 2);


-- Q6 (medium, order_index 9): Count Occurrences of a Substring ---------------
insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type)
values (
  'c0000000-0000-0000-0000-000000000041',
  'a0000000-0000-0000-0000-000000000006',
  $txt$Count Occurrences of a Substring$txt$,
  $md$Write a program that reads two lines: a string, then a substring to search for. Print how many non-overlapping times the substring occurs in the string.

**Input Format**
Line 1: a string `s`.
Line 2: a substring `sub` to search for.

**Output Format**
A single integer: the number of non-overlapping occurrences of `sub` in `s`.

**Example**
```
Input:
the quick brown fox jumps over the lazy dog
the

Output:
2
```
$md$,
  'medium',
  20,
  $py$s = input()
sub = input()
# TODO: print how many times sub occurs in s
$py$,
  $txt$The .count(sub) method counts non-overlapping occurrences of sub in a string.$txt$,
  $py$s = input()
sub = input()
print(s.count(sub))
$py$,
  9,
  'code'
);

insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values
  ('c0000000-0000-0000-0000-000000000041', $txt$the quick brown fox jumps over the lazy dog
the$txt$, $txt$2$txt$, true, 0);

insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values
  ('c0000000-0000-0000-0000-000000000041', $txt$aaaa
aa$txt$, $txt$2$txt$, 0),
  ('c0000000-0000-0000-0000-000000000041', $txt$Hello World
o$txt$, $txt$2$txt$, 1),
  ('c0000000-0000-0000-0000-000000000041', $txt$banana
ana$txt$, $txt$1$txt$, 2);


-- Q7 (hard, order_index 10): Caesar Cipher Encoder ---------------------------
insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type)
values (
  'c0000000-0000-0000-0000-000000000042',
  'a0000000-0000-0000-0000-000000000006',
  $txt$Caesar Cipher Encoder$txt$,
  $md$Write a program that reads two lines: a string, then an integer shift amount. Encode the string with a Caesar cipher: shift every letter forward by `shift` positions in the alphabet, wrapping around from `z` back to `a` (and `Z` back to `A`). Preserve the case of each letter, and leave non-letter characters (spaces, punctuation, digits) unchanged.

**Input Format**
Line 1: a string `s`.
Line 2: an integer `shift`.

**Output Format**
A single line: `s` encoded with the Caesar cipher.

**Example**
```
Input:
Hello, World!
3

Output:
Khoor, Zruog!
```
$md$,
  'hard',
  30,
  $py$s = input()
shift = int(input())
# TODO: print s with each letter shifted by `shift` positions in the alphabet
# (wrap around, preserve case, leave non-letters unchanged)
$py$,
  $txt$Use ord() and chr() to shift letters within the alphabet, wrapping around with % 26. Handle uppercase and lowercase letters separately, and leave everything else unchanged.$txt$,
  $py$s = input()
shift = int(input())
result = []
for ch in s:
    if ch.isupper():
        result.append(chr((ord(ch) - ord('A') + shift) % 26 + ord('A')))
    elif ch.islower():
        result.append(chr((ord(ch) - ord('a') + shift) % 26 + ord('a')))
    else:
        result.append(ch)
print("".join(result))
$py$,
  10,
  'code'
);

insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values
  ('c0000000-0000-0000-0000-000000000042', $txt$Hello, World!
3$txt$, $txt$Khoor, Zruog!$txt$, true, 0);

insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values
  ('c0000000-0000-0000-0000-000000000042', $txt$abc
1$txt$, $txt$bcd$txt$, 0),
  ('c0000000-0000-0000-0000-000000000042', $txt$xyz
3$txt$, $txt$abc$txt$, 1),
  ('c0000000-0000-0000-0000-000000000042', $txt$
5$txt$, $txt$$txt$, 2),
  ('c0000000-0000-0000-0000-000000000042', $txt$ABC xyz
2$txt$, $txt$CDE zab$txt$, 3);


-- ----------------------------------------------------------------------------
-- 2. MCQ QUESTIONS
-- ----------------------------------------------------------------------------

insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type, options, correct_option, correct_answer)
values (
  'd0000000-0000-0000-0000-000000000026',
  'a0000000-0000-0000-0000-000000000006',
  $txt$Slicing a String$txt$,
  $md$Given `s = "Python"`, what does `s[1:4]` evaluate to?$md$,
  'medium',
  5,
  '', '', '',
  11,
  'mcq',
  '["yth", "Pyth", "ytho", "ython"]'::jsonb,
  0,
  ''
);

insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type, options, correct_option, correct_answer)
values (
  'd0000000-0000-0000-0000-000000000027',
  'a0000000-0000-0000-0000-000000000006',
  $txt$Uppercase Conversion$txt$,
  $md$What does `"hello".upper()` return?$md$,
  'easy',
  5,
  '', '', '',
  12,
  'mcq',
  '["HELLO", "Hello", "hello", "Hello (unchanged)"]'::jsonb,
  0,
  ''
);

insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type, options, correct_option, correct_answer)
values (
  'd0000000-0000-0000-0000-000000000028',
  'a0000000-0000-0000-0000-000000000006',
  $txt$Splitting a String$txt$,
  $md$What does the expression `"a,b,c".split(",")` evaluate to?$md$,
  'medium',
  5,
  '', '', '',
  13,
  'mcq',
  '["A list containing a, b, and c as separate strings", "A single string a b c", "A list containing one string a,b,c", "A tuple containing a, b, and c"]'::jsonb,
  0,
  ''
);

insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type, options, correct_option, correct_answer)
values (
  'd0000000-0000-0000-0000-000000000029',
  'a0000000-0000-0000-0000-000000000006',
  $txt$Using find()$txt$,
  $md$What does `"Hello".find("z")` return?$md$,
  'medium',
  5,
  '', '', '',
  14,
  'mcq',
  '["-1", "0", "None", "It raises an error"]'::jsonb,
  0,
  ''
);

insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type, options, correct_option, correct_answer)
values (
  'd0000000-0000-0000-0000-000000000030',
  'a0000000-0000-0000-0000-000000000006',
  $txt$Removing Whitespace$txt$,
  $md$Which method call removes leading and trailing whitespace from a string `s`?$md$,
  'easy',
  5,
  '', '', '',
  15,
  'mcq',
  '["s.strip()", "s.trim()", "s.clean()", "s.remove_whitespace()"]'::jsonb,
  0,
  ''
);


-- ----------------------------------------------------------------------------
-- 3. FILL-IN-THE-BLANK QUESTIONS
-- ----------------------------------------------------------------------------

insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type, options, correct_option, correct_answer)
values (
  'e0000000-0000-0000-0000-000000000016',
  'a0000000-0000-0000-0000-000000000006',
  $txt$Strip Whitespace$txt$,
  $md$The string method `___()` removes leading and trailing whitespace from a string.$md$,
  'easy',
  5,
  '', '', '',
  16,
  'fill_blank',
  '[]'::jsonb,
  null,
  $txt$strip$txt$
);

insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type, options, correct_option, correct_answer)
values (
  'e0000000-0000-0000-0000-000000000017',
  'a0000000-0000-0000-0000-000000000006',
  $txt$Lowercase Conversion$txt$,
  $md$To convert a string to all lowercase letters, you call the `___()` method on it.$md$,
  'easy',
  5,
  '', '', '',
  17,
  'fill_blank',
  '[]'::jsonb,
  null,
  $txt$lower$txt$
);

insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type, options, correct_option, correct_answer)
values (
  'e0000000-0000-0000-0000-000000000018',
  'a0000000-0000-0000-0000-000000000006',
  $txt$Joining Strings$txt$,
  $md$To join a list of strings into one string using `","` as the separator, you call `",".___(my_list)`.$md$,
  'medium',
  5,
  '', '', '',
  18,
  'fill_blank',
  '[]'::jsonb,
  null,
  $txt$join$txt$
);


-- ----------------------------------------------------------------------------
-- 4. TOPIC CONTENT UPDATE
-- ----------------------------------------------------------------------------

update topics
set
  try_it_examples = '[
    {
      "description": "Slicing a string to extract parts of it",
      "code": "s = \"Python Programming\"\nprint(s[0:6])\nprint(s[-11:])",
      "output": "Python\nProgramming"
    },
    {
      "description": "Looping over characters and counting matches",
      "code": "word = \"banana\"\ncount = 0\nfor ch in word:\n    if ch == \"a\":\n        count += 1\nprint(count)",
      "output": "3"
    },
    {
      "description": "Formatting values into a string with an f-string",
      "code": "name = \"Ada\"\nscore = 95\nprint(f\"{name} scored {score} points\")",
      "output": "Ada scored 95 points"
    }
  ]'::jsonb,
  common_mistakes = $md$## Common Mistakes with Strings

**1. Trying to change a string in place.** Strings are immutable in Python, so `s[0] = 'X'` raises a `TypeError`. Build a new string instead, e.g. `s = 'X' + s[1:]`.

**2. Off-by-one errors in slicing.** `s[1:4]` includes indices 1, 2, and 3 -- the end index is exclusive. If you want the last character, use `s[-1]`, not `s[len(s)]`, which is out of range and raises an `IndexError`.

**3. Forgetting to `.strip()` input before comparing it.** `input()` keeps any accidental trailing spaces or newline artifacts the user typed, so `if answer == 'yes':` can silently fail even when the user typed "yes " with a trailing space. Normalize with `answer.strip()` (and often `.lower()`) before comparing.

**4. Assuming string comparisons are case-insensitive.** `'Hello' == 'hello'` is `False` -- Python compares strings exactly, character by character. Call `.lower()` or `.upper()` on both sides first if the comparison should ignore case.

**5. Treating `.find()` as if it raises an error when nothing is found.** `.find()` returns `-1` for a missing substring instead of raising an exception, so `if s.find('x'):` is a bug because `-1` is truthy. Compare explicitly with `if s.find('x') != -1:`, or use `in` instead: `if 'x' in s:`.$md$
where id = 'a0000000-0000-0000-0000-000000000006';
