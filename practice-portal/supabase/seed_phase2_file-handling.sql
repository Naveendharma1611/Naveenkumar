-- Phase 2 content expansion: File Handling topic
-- topic_id = a0000000-0000-0000-0000-000000000009
-- Adds 7 new code questions (3 easy, 3 medium, 1 hard) on top of the existing 3,
-- 5 MCQ questions, 3 fill-in-the-blank questions, and updates topic content
-- (try_it_examples, common_mistakes).
--
-- IMPORTANT: the judge sandbox has no pre-existing files on disk and no
-- guaranteed persistence between runs, so every solution_code below creates
-- the file it needs with open(path, "w"), writes to it, and then reads it
-- back -- all within the same script execution.

-- =========================================================================
-- 1. CODE QUESTIONS (7 new: order_index 4-10)
-- =========================================================================

insert into questions
  (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type)
values

-- ---------------------------------------------------------------------
-- Easy #1 (order 4): write a line to a file and read it back
-- ---------------------------------------------------------------------
(
  'c0000000-0000-0000-0000-000000000057',
  'a0000000-0000-0000-0000-000000000009',
  $txt$Write and Read a Line$txt$,
  $md$Read a single line of text from standard input, write it to a file named
`notes.txt` using a `with open(...) as f:` block, then open the file again
and read its content back, printing what you read.

This is the most basic file-handling pattern: **write first, then read**,
since the file does not exist until your program creates it.

**Input Format**

A single line of text.

**Output Format**

The same text, printed after being read back from the file.

**Example**

```
Input:
Hello World

Output:
Hello World
```
$md$,
  'easy',
  10,
  $py$line = input()
# 1. Write `line` to a file named "notes.txt"
# 2. Open "notes.txt" again and read its contents
# 3. Print what you read
$py$,
  $txt$Use `with open("notes.txt", "w") as f:` to write, and a separate `with open("notes.txt", "r") as f:` block to read it back with `f.read()`.$txt$,
  $py$line = input()
with open("notes.txt", "w") as f:
    f.write(line)

with open("notes.txt", "r") as f:
    content = f.read()
print(content)
$py$,
  4,
  'code'
),

-- ---------------------------------------------------------------------
-- Easy #2 (order 5): write multiple lines, count them with readlines()
-- ---------------------------------------------------------------------
(
  'c0000000-0000-0000-0000-000000000058',
  'a0000000-0000-0000-0000-000000000009',
  $txt$Count Lines in a File$txt$,
  $md$Read an integer `n`, then `n` lines of text. Write all `n` lines to a file
named `data.txt` (one per line), then open the file again, read it back
using `readlines()`, and print how many lines the file contains.

**Input Format**

- Line 1: an integer `n`
- Next `n` lines: text

**Output Format**

A single integer: the number of lines in the file.

**Example**

```
Input:
3
apple
banana
cherry

Output:
3
```
$md$,
  'easy',
  10,
  $py$n = int(input())
lines = [input() for _ in range(n)]
# 1. Write each line to "data.txt", each on its own line
# 2. Read the file back with readlines()
# 3. Print the number of lines
$py$,
  $txt$Remember to add "\n" after each line when writing, otherwise everything will be joined into one line. `readlines()` returns a list -- use `len()` on it.$txt$,
  $py$n = int(input())
lines = [input() for _ in range(n)]
with open("data.txt", "w") as f:
    for line in lines:
        f.write(line + "\n")

with open("data.txt", "r") as f:
    content_lines = f.readlines()
print(len(content_lines))
$py$,
  5,
  'code'
),

-- ---------------------------------------------------------------------
-- Easy #3 (order 6): overwrite ("w") vs append ("a") mode
-- ---------------------------------------------------------------------
(
  'c0000000-0000-0000-0000-000000000059',
  'a0000000-0000-0000-0000-000000000009',
  $txt$Append to a File$txt$,
  $md$Read two lines of text: an initial line and a line to append.

1. Write the initial line to a file named `log.txt` using mode `"w"`.
2. Open the file again using mode `"a"` and append the second line (on a
   new line), **without erasing** what is already there.
3. Open the file in read mode and print its full contents.

**Input Format**

- Line 1: the initial content
- Line 2: the text to append

**Output Format**

The full contents of the file after appending.

**Example**

```
Input:
Line1
Line2

Output:
Line1
Line2
```
$md$,
  'easy',
  10,
  $py$initial = input()
to_append = input()
# 1. Write `initial` to "log.txt" with mode "w"
# 2. Append `to_append` to "log.txt" with mode "a"
# 3. Read and print the full file content
$py$,
  $txt$Mode "w" truncates (erases) existing content -- use it only once, for the initial write. Mode "a" adds to the end without erasing.$txt$,
  $py$initial = input()
to_append = input()
with open("log.txt", "w") as f:
    f.write(initial + "\n")
with open("log.txt", "a") as f:
    f.write(to_append)
with open("log.txt", "r") as f:
    print(f.read())
$py$,
  6,
  'code'
),

-- ---------------------------------------------------------------------
-- Medium #1 (order 7): word count across a file
-- ---------------------------------------------------------------------
(
  'c0000000-0000-0000-0000-000000000060',
  'a0000000-0000-0000-0000-000000000009',
  $txt$Word Count in File$txt$,
  $md$Read an integer `n`, then `n` lines of text. Write all the lines to a
file named `essay.txt`, then read the file back line by line and count
the **total number of words** across the whole file (words are separated
by whitespace).

**Input Format**

- Line 1: an integer `n`
- Next `n` lines: text

**Output Format**

A single integer: the total word count.

**Example**

```
Input:
2
hello world
foo bar baz

Output:
5
```
$md$,
  'medium',
  20,
  $py$n = int(input())
lines = [input() for _ in range(n)]
# 1. Write each line to "essay.txt"
# 2. Read the file back and count total words with str.split()
# 3. Print the total word count
$py$,
  $txt$`line.split()` with no arguments splits on any whitespace and ignores extra spaces -- use `len()` on the result to count words per line, then sum across lines.$txt$,
  $py$n = int(input())
lines = [input() for _ in range(n)]
with open("essay.txt", "w") as f:
    for line in lines:
        f.write(line + "\n")

total_words = 0
with open("essay.txt", "r") as f:
    for line in f:
        total_words += len(line.split())
print(total_words)
$py$,
  7,
  'code'
),

-- ---------------------------------------------------------------------
-- Medium #2 (order 8): search for lines containing a keyword
-- ---------------------------------------------------------------------
(
  'c0000000-0000-0000-0000-000000000061',
  'a0000000-0000-0000-0000-000000000009',
  $txt$Search for a Keyword in File$txt$,
  $md$Read an integer `n`, then `n` lines of text, then a final line containing
a search keyword. Write the `n` lines to a file named `records.txt`, then
read the file back and print every line (in its original order) that
**contains the keyword as a substring**. If no line matches, print
`Not Found`.

**Input Format**

- Line 1: an integer `n`
- Next `n` lines: text
- Last line: the keyword to search for

**Output Format**

Each matching line, in order, one per line -- or `Not Found` if there are
no matches.

**Example**

```
Input:
3
apple pie
banana split
apple juice
apple

Output:
apple pie
apple juice
```
$md$,
  'medium',
  20,
  $py$n = int(input())
lines = [input() for _ in range(n)]
keyword = input()
# 1. Write the lines to "records.txt"
# 2. Read the file back and print every line containing `keyword`
# 3. If nothing matched, print "Not Found"
$py$,
  $txt$When reading the file line by line, strip the trailing "\n" with `line.rstrip("\n")` before checking `keyword in line` or printing. Keep a boolean flag to know if anything matched.$txt$,
  $py$n = int(input())
lines = [input() for _ in range(n)]
keyword = input()
with open("records.txt", "w") as f:
    for line in lines:
        f.write(line + "\n")

found = False
with open("records.txt", "r") as f:
    for line in f:
        line = line.rstrip("\n")
        if keyword in line:
            print(line)
            found = True
if not found:
    print("Not Found")
$py$,
  8,
  'code'
),

-- ---------------------------------------------------------------------
-- Medium #3 (order 9): write/parse structured "name,score" records
-- ---------------------------------------------------------------------
(
  'c0000000-0000-0000-0000-000000000062',
  'a0000000-0000-0000-0000-000000000009',
  $txt$Parse Name,Score Records$txt$,
  $md$Read an integer `n`, then `n` lines each formatted as `name,score`. Write
all the lines to a file named `scores.txt`, then read the file back,
parse each line by splitting on the comma, and print the **name with the
highest score**. If there is a tie, print the name that appeared first
in the file.

**Input Format**

- Line 1: an integer `n`
- Next `n` lines: a record formatted as `name,score`

**Output Format**

The name with the highest score.

**Example**

```
Input:
3
Alice,85
Bob,92
Charlie,78

Output:
Bob
```
$md$,
  'medium',
  20,
  $py$n = int(input())
records = [input() for _ in range(n)]
# 1. Write each record to "scores.txt"
# 2. Read the file back, split each line on "," into name and score
# 3. Print the name with the highest score (first one wins ties)
$py$,
  $txt$`line.split(",")` gives you `[name, score]` as strings -- convert the score with `int(...)` before comparing. Use strict `>` (not `>=`) when updating the best score so the first occurrence wins ties.$txt$,
  $py$n = int(input())
records = [input() for _ in range(n)]
with open("scores.txt", "w") as f:
    for r in records:
        f.write(r + "\n")

best_name = None
best_score = None
with open("scores.txt", "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        name, score = line.split(",")
        score = int(score)
        if best_score is None or score > best_score:
            best_score = score
            best_name = name
print(best_name)
$py$,
  9,
  'code'
),

-- ---------------------------------------------------------------------
-- Hard (order 10): combined file statistics report
-- ---------------------------------------------------------------------
(
  'c0000000-0000-0000-0000-000000000063',
  'a0000000-0000-0000-0000-000000000009',
  $txt$File Statistics Report$txt$,
  $md$Read an integer `n`, then `n` lines of text, then a final line containing
a keyword. Write the `n` lines to a file named `report.txt`, then read
the file back and compute:

- the total number of lines
- the total number of words (across all lines)
- the total number of characters (not counting newline characters)
- the number of lines that contain the keyword as a substring

Print the four results in exactly this format (four lines):

```
Lines: <total_lines>
Words: <total_words>
Characters: <total_chars>
Matches: <matches>
```

**Input Format**

- Line 1: an integer `n`
- Next `n` lines: text
- Last line: the keyword to search for

**Output Format**

Four lines, exactly as shown above.

**Example**

```
Input:
2
hello world
hello there
hello

Output:
Lines: 2
Words: 4
Characters: 22
Matches: 2
```
$md$,
  'hard',
  30,
  $py$n = int(input())
lines = [input() for _ in range(n)]
keyword = input()
# 1. Write the lines to "report.txt"
# 2. Read the file back, line by line, accumulating:
#    - total_lines, total_words, total_chars, matches
# 3. Print the four results in the required format
$py$,
  $txt$Strip the trailing "\n" from each line read back before counting its characters or checking the keyword, otherwise your character count and matches will be slightly off. `len(line.split())` gives words per line.$txt$,
  $py$n = int(input())
lines = [input() for _ in range(n)]
keyword = input()

with open("report.txt", "w") as f:
    for line in lines:
        f.write(line + "\n")

total_lines = 0
total_words = 0
total_chars = 0
matches = 0

with open("report.txt", "r") as f:
    for line in f:
        line = line.rstrip("\n")
        total_lines += 1
        total_words += len(line.split())
        total_chars += len(line)
        if keyword in line:
            matches += 1

print(f"Lines: {total_lines}")
print(f"Words: {total_words}")
print(f"Characters: {total_chars}")
print(f"Matches: {matches}")
$py$,
  10,
  'code'
);

-- ---------------------------------------------------------------------
-- Test cases: sample rows (is_sample = true) in test_cases
-- ---------------------------------------------------------------------
insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values
('c0000000-0000-0000-0000-000000000057', $txt$Hello World$txt$, $txt$Hello World$txt$, true, 0),
('c0000000-0000-0000-0000-000000000058', $txt$3
apple
banana
cherry$txt$, $txt$3$txt$, true, 0),
('c0000000-0000-0000-0000-000000000059', $txt$Line1
Line2$txt$, $txt$Line1
Line2$txt$, true, 0),
('c0000000-0000-0000-0000-000000000060', $txt$2
hello world
foo bar baz$txt$, $txt$5$txt$, true, 0),
('c0000000-0000-0000-0000-000000000061', $txt$3
apple pie
banana split
apple juice
apple$txt$, $txt$apple pie
apple juice$txt$, true, 0),
('c0000000-0000-0000-0000-000000000062', $txt$3
Alice,85
Bob,92
Charlie,78$txt$, $txt$Bob$txt$, true, 0),
('c0000000-0000-0000-0000-000000000063', $txt$2
hello world
hello there
hello$txt$, $txt$Lines: 2
Words: 4
Characters: 22
Matches: 2$txt$, true, 0);

-- ---------------------------------------------------------------------
-- Hidden test cases
-- ---------------------------------------------------------------------
insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values
-- Q057 (easy, 2 hidden)
('c0000000-0000-0000-0000-000000000057', $txt$Python File Handling$txt$, $txt$Python File Handling$txt$, 0),
('c0000000-0000-0000-0000-000000000057', $txt$12345$txt$, $txt$12345$txt$, 1),

-- Q058 (easy, 2 hidden)
('c0000000-0000-0000-0000-000000000058', $txt$5
a
b
c
d
e$txt$, $txt$5$txt$, 0),
('c0000000-0000-0000-0000-000000000058', $txt$1
single$txt$, $txt$1$txt$, 1),

-- Q059 (easy, 2 hidden)
('c0000000-0000-0000-0000-000000000059', $txt$Start
End$txt$, $txt$Start
End$txt$, 0),
('c0000000-0000-0000-0000-000000000059', $txt$A
B$txt$, $txt$A
B$txt$, 1),

-- Q060 (medium, 3 hidden)
('c0000000-0000-0000-0000-000000000060', $txt$3
a b c
d e
f$txt$, $txt$6$txt$, 0),
('c0000000-0000-0000-0000-000000000060', $txt$1
one two three four$txt$, $txt$4$txt$, 1),
('c0000000-0000-0000-0000-000000000060', $txt$2
x
y z$txt$, $txt$3$txt$, 2),

-- Q061 (medium, 3 hidden)
('c0000000-0000-0000-0000-000000000061', $txt$2
hello world
foo bar
zzz$txt$, $txt$Not Found$txt$, 0),
('c0000000-0000-0000-0000-000000000061', $txt$4
cat dog
dog cat
bird
catfish
cat$txt$, $txt$cat dog
dog cat
catfish$txt$, 1),
('c0000000-0000-0000-0000-000000000061', $txt$1
only line
only$txt$, $txt$only line$txt$, 2),

-- Q062 (medium, 3 hidden)
('c0000000-0000-0000-0000-000000000062', $txt$2
Tom,50
Jerry,50$txt$, $txt$Tom$txt$, 0),
('c0000000-0000-0000-0000-000000000062', $txt$1
Solo,99$txt$, $txt$Solo$txt$, 1),
('c0000000-0000-0000-0000-000000000062', $txt$4
A,10
B,20
C,30
D,25$txt$, $txt$C$txt$, 2),

-- Q063 (hard, 4 hidden)
('c0000000-0000-0000-0000-000000000063', $txt$3
the quick brown fox
jumps over
the lazy dog
the$txt$, $txt$Lines: 3
Words: 9
Characters: 41
Matches: 2$txt$, 0),
('c0000000-0000-0000-0000-000000000063', $txt$1
single line test
xyz$txt$, $txt$Lines: 1
Words: 3
Characters: 16
Matches: 0$txt$, 1),
('c0000000-0000-0000-0000-000000000063', $txt$4
data in file
file handling practice
learning python
data structures
data$txt$, $txt$Lines: 4
Words: 10
Characters: 64
Matches: 2$txt$, 2),
('c0000000-0000-0000-0000-000000000063', $txt$2
abc
abcdef
abc$txt$, $txt$Lines: 2
Words: 2
Characters: 9
Matches: 2$txt$, 3);

-- =========================================================================
-- 2. MCQ QUESTIONS (5 new: order_index 11-15)
-- =========================================================================

insert into questions
  (id, topic_id, title, prompt, difficulty, points, order_index, question_type, options, correct_option)
values
(
  'd0000000-0000-0000-0000-000000000041',
  'a0000000-0000-0000-0000-000000000009',
  $txt$Append Mode$txt$,
  $md$Which file mode opens a file for writing **without erasing** its existing content, adding new data to the end instead?$md$,
  'easy',
  5,
  11,
  'mcq',
  '["w", "r", "a", "x"]'::jsonb,
  2
),
(
  'd0000000-0000-0000-0000-000000000042',
  'a0000000-0000-0000-0000-000000000009',
  $txt$What readlines() Returns$txt$,
  $md$What does calling `readlines()` on an open file object return?$md$,
  'easy',
  5,
  12,
  'mcq',
  '["A single string containing the whole file", "A list of lines, each still ending with a newline character", "A list of individual words in the file", "An integer count of the number of lines"]'::jsonb,
  1
),
(
  'd0000000-0000-0000-0000-000000000043',
  'a0000000-0000-0000-0000-000000000009',
  $txt$The with Statement$txt$,
  $md$What is the key benefit of opening a file using `with open(...) as f:` instead of a plain `f = open(...)` call?$md$,
  'medium',
  5,
  13,
  'mcq',
  '["It opens the file faster than open() alone", "It automatically closes the file when the block exits, even if an exception occurs", "It automatically converts the file content to a list", "It opens the file in append mode by default"]'::jsonb,
  1
),
(
  'd0000000-0000-0000-0000-000000000044',
  'a0000000-0000-0000-0000-000000000009',
  $txt$Overwriting With "w" Mode$txt$,
  $md$If a file named `data.txt` already contains text and you open it again with `open("data.txt", "w")`, what happens to the existing content?$md$,
  'medium',
  5,
  14,
  'mcq',
  '["It is preserved and new writes are appended after it", "An error is raised because the file already exists", "It is immediately erased (truncated) as soon as the file is opened for writing", "It is moved to a backup file automatically"]'::jsonb,
  2
),
(
  'd0000000-0000-0000-0000-000000000045',
  'a0000000-0000-0000-0000-000000000009',
  $txt$Reading the Whole File$txt$,
  $md$Which method reads the **entire** remaining contents of a file and returns it as a single string?$md$,
  'easy',
  5,
  15,
  'mcq',
  '["readline()", "readlines()", "read()", "readall()"]'::jsonb,
  2
);

-- =========================================================================
-- 3. FILL-IN-THE-BLANK QUESTIONS (3 new: order_index 16-18)
-- =========================================================================

insert into questions
  (id, topic_id, title, prompt, difficulty, points, order_index, question_type, correct_answer)
values
(
  'e0000000-0000-0000-0000-000000000025',
  'a0000000-0000-0000-0000-000000000009',
  $txt$Write Mode$txt$,
  $md$The file mode `___` opens a file for writing, creating it if it does not
exist, and **truncating (erasing) it** if it already does.$md$,
  'easy',
  5,
  16,
  'fill_blank',
  $txt$w$txt$
),
(
  'e0000000-0000-0000-0000-000000000026',
  'a0000000-0000-0000-0000-000000000009',
  $txt$Append Mode$txt$,
  $md$To open a file so that new data is added to the end **without erasing**
the content already in it, you should open it in mode `___`.$md$,
  'easy',
  5,
  17,
  'fill_blank',
  $txt$a$txt$
),
(
  'e0000000-0000-0000-0000-000000000027',
  'a0000000-0000-0000-0000-000000000009',
  $txt$Context Manager Keyword$txt$,
  $md$The keyword `___` is used together with `open()` to automatically close a
file when its block finishes executing, even if an error occurs -- for
example: `___ open("file.txt") as f:`.$md$,
  'medium',
  5,
  18,
  'fill_blank',
  $txt$with$txt$
);

-- =========================================================================
-- 4. TOPIC CONTENT UPDATE (try_it_examples, common_mistakes)
-- =========================================================================

update topics
set
  try_it_examples = '[
    {
      "description": "Write a line to a file and read it back",
      "code": "with open(\"hello.txt\", \"w\") as f:\n    f.write(\"Hello, File!\")\n\nwith open(\"hello.txt\", \"r\") as f:\n    print(f.read())",
      "output": "Hello, File!"
    },
    {
      "description": "Write multiple lines and count them with readlines()",
      "code": "with open(\"items.txt\", \"w\") as f:\n    f.write(\"apple\\nbanana\\ncherry\\n\")\n\nwith open(\"items.txt\", \"r\") as f:\n    lines = f.readlines()\nprint(len(lines))\nprint(lines[0])",
      "output": "3\napple\n"
    },
    {
      "description": "Append to a file without erasing previous content",
      "code": "with open(\"log.txt\", \"w\") as f:\n    f.write(\"Day 1: Started project\\n\")\n\nwith open(\"log.txt\", \"a\") as f:\n    f.write(\"Day 2: Added file handling\\n\")\n\nwith open(\"log.txt\", \"r\") as f:\n    print(f.read())",
      "output": "Day 1: Started project\nDay 2: Added file handling"
    }
  ]'::jsonb,
  common_mistakes = $md$### Common Mistakes with File Handling

1. **Forgetting to close the file.** Calling `open()` without closing the
   file can leak file handles and, on some systems, means your written
   data is never actually flushed to disk. **Fix:** always use
   `with open(...) as f:` -- it closes the file automatically when the
   block ends, even if an exception is raised inside it.

2. **Using `"w"` mode when you meant to append.** Opening a file with
   `"w"` immediately truncates (erases) any existing content, which
   surprises beginners who expected their old data to still be there.
   **Fix:** use `"a"` mode to add to the end of a file without erasing
   what's already in it.

3. **Forgetting newline characters when writing multiple lines.**
   Writing several strings in a loop without adding `"\n"` after each
   one makes them all run together on a single line in the file.
   **Fix:** explicitly write `f.write(line + "\n")` for each line, or
   join lines with `"\n".join(...)` before writing.

4. **Not accounting for the trailing `"\n"` from `readlines()`.**
   `readlines()` keeps the newline character at the end of every line
   it returns, so comparing a line directly to an expected string (for
   example `line == "apple"`) silently fails because the real value is
   `"apple\n"`. **Fix:** strip it first with `line.rstrip("\n")` or
   `line.strip()` before comparing.

5. **Confusing `read()`, `readline()`, and `readlines()`.** `read()`
   returns the whole file as one string, `readline()` returns just the
   next single line, and `readlines()` returns a list of all lines.
   Using the wrong one often leads to iterating over individual
   characters instead of lines, or vice versa. **Fix:** pick the method
   that matches what you actually need -- looping with `for line in f:`
   is usually the simplest and most memory-efficient option.
$md$
where id = 'a0000000-0000-0000-0000-000000000009';
