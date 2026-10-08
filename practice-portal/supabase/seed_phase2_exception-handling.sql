-- Phase 2 content expansion — Topic 10: Exception Handling (try/except/finally)
--
-- Adds 7 new code questions (3 easy, 3 medium, 1 hard; order_index 4-10, on top of the
-- existing 3 at order_index 1-3), 5 MCQ questions, 3 fill-in-the-blank questions, and
-- richer topic content (try_it_examples + common_mistakes).
--
-- Every solution_code below handles its own exceptions and always prints something to
-- stdout — nothing is left to propagate as an uncaught traceback.

-- ============================================================================
-- 1. NEW CODE QUESTIONS (7)
-- ============================================================================

insert into questions (id, topic_id, title, prompt, difficulty, points, starter_code, hint, solution_code, order_index, question_type) values

-- ---- Easy 1: ZeroDivisionError with // ------------------------------------
('c0000000-0000-0000-0000-000000000064', 'a0000000-0000-0000-0000-000000000010', 'Safe Integer Division',
$md$Read two integers `a` and `b` and print the result of integer-dividing `a` by `b`. If `b` is `0`, catch the error instead of crashing.

### Input Format
Two lines, each containing one integer: `a`, then `b`.

### Output Format
- If `b` is not zero: `Result: <a // b>`
- If `b` is zero: `Error: Cannot divide by zero`

### Example
```
Input:
10
2

Output:
Result: 5
```$md$,
'easy', 10,
$py$a = int(input())
b = int(input())
# Write your code here: try a // b, catch ZeroDivisionError$py$,
$txt$Wrap the `//` operation in a try/except block, catching ZeroDivisionError specifically.$txt$,
$py$a = int(input())
b = int(input())
try:
    result = a // b
    print(f"Result: {result}")
except ZeroDivisionError:
    print("Error: Cannot divide by zero")$py$,
4, 'code'),

-- ---- Easy 2: ValueError on int() conversion -------------------------------
('c0000000-0000-0000-0000-000000000065', 'a0000000-0000-0000-0000-000000000010', 'Safe Number Parsing',
$md$Read a line of text and try to convert it to an integer. If the text is not a valid integer, catch the error and report it instead of crashing.

### Input Format
One line containing a string `s`.

### Output Format
- If `s` can be converted to an integer: `You entered: <the integer>`
- Otherwise: `Error: Invalid number`

### Example
```
Input:
42

Output:
You entered: 42
```$md$,
'easy', 10,
$py$s = input()
# Write your code here: try int(s), catch ValueError$py$,
$txt$Wrap the int(s) conversion in a try/except block, catching ValueError specifically.$txt$,
$py$s = input()
try:
    n = int(s)
    print(f"You entered: {n}")
except ValueError:
    print("Error: Invalid number")$py$,
5, 'code'),

-- ---- Easy 3: IndexError with finally ---------------------------------------
('c0000000-0000-0000-0000-000000000066', 'a0000000-0000-0000-0000-000000000010', 'List Lookup with Finally',
$md$A fixed list `[10, 20, 30]` is defined for you. Read an integer index and try to print the value at that position in the list. Whether or not it works, always report that the lookup attempt finished.

### Input Format
One line containing an integer `index`.

### Output Format
First, one of:
```
Value: <the value at that index>
Error: Index out of range
```
Then, on the next line, always:
```
Lookup attempt finished.
```

### Example
```
Input:
1

Output:
Value: 20
Lookup attempt finished.
```$md$,
'easy', 10,
$py$fixed_list = [10, 20, 30]
index = int(input())
# Write your code here: try fixed_list[index], catch IndexError,
# and use finally to always print "Lookup attempt finished."$py$,
$txt$Put the list access inside try, catch IndexError, and put the final print statement in a finally block so it always runs.$txt$,
$py$fixed_list = [10, 20, 30]
index = int(input())
try:
    value = fixed_list[index]
    print(f"Value: {value}")
except IndexError:
    print("Error: Index out of range")
finally:
    print("Lookup attempt finished.")$py$,
6, 'code'),

-- ---- Medium 1: KeyError with finally ---------------------------------------
('c0000000-0000-0000-0000-000000000067', 'a0000000-0000-0000-0000-000000000010', 'Dictionary Lookup with Finally',
$md$A fixed dictionary `{"a": 1, "b": 2, "c": 3}` is defined for you. Read a key as a string and try to print its value. Whether or not the key exists, always report that the lookup is complete.

### Input Format
One line containing a string `key`.

### Output Format
First, one of:
```
Value: <the value for that key>
Error: Key not found
```
Then, on the next line, always:
```
Lookup complete.
```

### Example
```
Input:
b

Output:
Value: 2
Lookup complete.
```$md$,
'medium', 20,
$py$fixed_dict = {"a": 1, "b": 2, "c": 3}
key = input()
# Write your code here: try fixed_dict[key], catch KeyError,
# and use finally to always print "Lookup complete."$py$,
$txt$Access the dictionary with fixed_dict[key] inside a try block, catch KeyError, and put the final print in finally.$txt$,
$py$fixed_dict = {"a": 1, "b": 2, "c": 3}
key = input()
try:
    value = fixed_dict[key]
    print(f"Value: {value}")
except KeyError:
    print("Error: Key not found")
finally:
    print("Lookup complete.")$py$,
7, 'code'),

-- ---- Medium 2: multiple except clauses -------------------------------------
('c0000000-0000-0000-0000-000000000068', 'a0000000-0000-0000-0000-000000000010', 'Divide with Multiple Except Clauses',
$md$Read two values (as text) and try to integer-divide the first by the second. Two different problems can occur: the text might not be a valid integer, or the second value might be zero. Handle each with its own `except` clause.

### Input Format
Two lines: `a`, then `b` (both read as text).

### Output Format
- If either value is not a valid integer: `Error: Invalid input, please enter numbers`
- Otherwise, if `b` is `0`: `Error: Cannot divide by zero`
- Otherwise: `Result: <a // b>`

### Example
```
Input:
20
4

Output:
Result: 5
```$md$,
'medium', 20,
$py$a_str = input()
b_str = input()
# Write your code here: try converting both to int and dividing a // b.
# Catch ValueError -> print "Error: Invalid input, please enter numbers"
# Catch ZeroDivisionError -> print "Error: Cannot divide by zero"$py$,
$txt$Put both int() conversions and the division inside one try block, then add two except clauses in order: ValueError first, ZeroDivisionError second.$txt$,
$py$a_str = input()
b_str = input()
try:
    a = int(a_str)
    b = int(b_str)
    result = a // b
    print(f"Result: {result}")
except ValueError:
    print("Error: Invalid input, please enter numbers")
except ZeroDivisionError:
    print("Error: Cannot divide by zero")$py$,
8, 'code'),

-- ---- Medium 3: raising and catching a custom ValueError --------------------
('c0000000-0000-0000-0000-000000000069', 'a0000000-0000-0000-0000-000000000010', 'Validate Age with a Raised Exception',
$md$Read a value as text meant to represent someone's age. Convert it to an integer, and if it converts but is negative, deliberately `raise ValueError("Age cannot be negative")` yourself. Catch any `ValueError` — whether it came from a bad conversion or from your own `raise` — and print its message.

### Input Format
One line containing a string `age_str`.

### Output Format
- If `age_str` converts to a non-negative integer: `Valid age: <age>`
- If `age_str` converts to a negative integer: `Error: Age cannot be negative`
- If `age_str` does not convert to an integer at all: `Error: <the exception's message>`

### Example
```
Input:
25

Output:
Valid age: 25
```$md$,
'medium', 20,
$py$age_str = input()
# Write your code here: try int(age_str); if negative, raise ValueError("Age cannot be negative");
# catch ValueError as e and print(f"Error: {e}")$py$,
$txt$Use `raise ValueError("Age cannot be negative")` inside the try block when the parsed number is negative, then catch ValueError as e and print(f"Error: {e}") — this one except handles both the raised error and a failed int() conversion.$txt$,
$py$age_str = input()
try:
    age = int(age_str)
    if age < 0:
        raise ValueError("Age cannot be negative")
    print(f"Valid age: {age}")
except ValueError as e:
    print(f"Error: {e}")$py$,
9, 'code'),

-- ---- Hard: combined IndexError / ValueError / ZeroDivisionError + finally --
('c0000000-0000-0000-0000-000000000070', 'a0000000-0000-0000-0000-000000000010', 'Robust Token Calculator',
$md$Read a line of space-separated tokens, then an index, then a divisor. Look up the token at that index, convert it to an integer, and integer-divide it by the divisor. Three different problems can occur along the way — handle each with its own `except` clause, and always report that the operation was attempted.

### Input Format
Three lines:
1. A line of space-separated tokens (strings, not necessarily numeric)
2. A line containing the index to look up (always a valid integer)
3. A line containing the divisor (always a valid integer)

### Output Format
First, one of:
```
Result: <token value // divisor>
Error: Index out of range
Error: Invalid number format
Error: Cannot divide by zero
```
Then, on the next line, always:
```
Operation attempted.
```

### Example
```
Input:
10 20 30 40
2
5

Output:
Result: 6
Operation attempted.
```$md$,
'hard', 30,
$py$tokens = input().split()
index = int(input())
divisor = int(input())
# Write your code here: try tokens[index], convert it to int, and divide by divisor.
# Catch IndexError, ValueError, and ZeroDivisionError with the messages described,
# and use finally to always print "Operation attempted."$py$,
$txt$One try block can cover all three risky steps (indexing, int() conversion, division) — add three except clauses, one per exception type, then a finally that always prints "Operation attempted."$txt$,
$py$tokens = input().split()
index = int(input())
divisor = int(input())
try:
    token = tokens[index]
    value = int(token)
    result = value // divisor
    print(f"Result: {result}")
except IndexError:
    print("Error: Index out of range")
except ValueError:
    print("Error: Invalid number format")
except ZeroDivisionError:
    print("Error: Cannot divide by zero")
finally:
    print("Operation attempted.")$py$,
10, 'code');

-- ============================================================================
-- 2. SAMPLE TEST CASES (test_cases, order_index 0)
-- ============================================================================

insert into test_cases (question_id, stdin, expected_output, is_sample, order_index) values
('c0000000-0000-0000-0000-000000000064', $txt$10
2$txt$, $txt$Result: 5$txt$, true, 0),
('c0000000-0000-0000-0000-000000000065', $txt$42$txt$, $txt$You entered: 42$txt$, true, 0),
('c0000000-0000-0000-0000-000000000066', $txt$1$txt$, $txt$Value: 20
Lookup attempt finished.$txt$, true, 0),
('c0000000-0000-0000-0000-000000000067', $txt$b$txt$, $txt$Value: 2
Lookup complete.$txt$, true, 0),
('c0000000-0000-0000-0000-000000000068', $txt$20
4$txt$, $txt$Result: 5$txt$, true, 0),
('c0000000-0000-0000-0000-000000000069', $txt$25$txt$, $txt$Valid age: 25$txt$, true, 0),
('c0000000-0000-0000-0000-000000000070', $txt$10 20 30 40
2
5$txt$, $txt$Result: 6
Operation attempted.$txt$, true, 0);

-- ============================================================================
-- 3. HIDDEN TEST CASES (hidden_test_cases, order_index 0, 1, ...)
-- ============================================================================

insert into hidden_test_cases (question_id, stdin, expected_output, order_index) values

-- Safe Integer Division (c...0064) — easy: 1 sample + 2 hidden
('c0000000-0000-0000-0000-000000000064', $txt$7
0$txt$, $txt$Error: Cannot divide by zero$txt$, 0),
('c0000000-0000-0000-0000-000000000064', $txt$9
3$txt$, $txt$Result: 3$txt$, 1),

-- Safe Number Parsing (c...0065) — easy: 1 sample + 2 hidden
('c0000000-0000-0000-0000-000000000065', $txt$abc$txt$, $txt$Error: Invalid number$txt$, 0),
('c0000000-0000-0000-0000-000000000065', $txt$-7$txt$, $txt$You entered: -7$txt$, 1),

-- List Lookup with Finally (c...0066) — easy: 1 sample + 2 hidden
('c0000000-0000-0000-0000-000000000066', $txt$5$txt$, $txt$Error: Index out of range
Lookup attempt finished.$txt$, 0),
('c0000000-0000-0000-0000-000000000066', $txt$0$txt$, $txt$Value: 10
Lookup attempt finished.$txt$, 1),

-- Dictionary Lookup with Finally (c...0067) — medium: 1 sample + 3 hidden
('c0000000-0000-0000-0000-000000000067', $txt$z$txt$, $txt$Error: Key not found
Lookup complete.$txt$, 0),
('c0000000-0000-0000-0000-000000000067', $txt$a$txt$, $txt$Value: 1
Lookup complete.$txt$, 1),
('c0000000-0000-0000-0000-000000000067', $txt$c$txt$, $txt$Value: 3
Lookup complete.$txt$, 2),

-- Divide with Multiple Except Clauses (c...0068) — medium: 1 sample + 3 hidden
('c0000000-0000-0000-0000-000000000068', $txt$abc
4$txt$, $txt$Error: Invalid input, please enter numbers$txt$, 0),
('c0000000-0000-0000-0000-000000000068', $txt$20
0$txt$, $txt$Error: Cannot divide by zero$txt$, 1),
('c0000000-0000-0000-0000-000000000068', $txt$15
3$txt$, $txt$Result: 5$txt$, 2),

-- Validate Age with a Raised Exception (c...0069) — medium: 1 sample + 3 hidden
('c0000000-0000-0000-0000-000000000069', $txt$-5$txt$, $txt$Error: Age cannot be negative$txt$, 0),
('c0000000-0000-0000-0000-000000000069', $txt$xyz$txt$, $txt$Error: invalid literal for int() with base 10: 'xyz'$txt$, 1),
('c0000000-0000-0000-0000-000000000069', $txt$0$txt$, $txt$Valid age: 0$txt$, 2),

-- Robust Token Calculator (c...0070) — hard: 1 sample + 4 hidden
('c0000000-0000-0000-0000-000000000070', $txt$10 20 30
5
2$txt$, $txt$Error: Index out of range
Operation attempted.$txt$, 0),
('c0000000-0000-0000-0000-000000000070', $txt$10 abc 30
1
2$txt$, $txt$Error: Invalid number format
Operation attempted.$txt$, 1),
('c0000000-0000-0000-0000-000000000070', $txt$10 20 30
1
0$txt$, $txt$Error: Cannot divide by zero
Operation attempted.$txt$, 2),
('c0000000-0000-0000-0000-000000000070', $txt$5 15 25
0
3$txt$, $txt$Result: 1
Operation attempted.$txt$, 3);

-- ============================================================================
-- 4. MCQ QUESTIONS (5)
-- ============================================================================

insert into questions (id, topic_id, title, prompt, difficulty, points, question_type, options, correct_option) values

('d0000000-0000-0000-0000-000000000046', 'a0000000-0000-0000-0000-000000000010', 'Division by Zero Exception',
$md$Which exception does Python raise when you attempt to divide a number by zero (e.g. `10 / 0` or `10 // 0`)?$md$,
'easy', 5, 'mcq',
'["ZeroDivisionError", "ValueError", "IndexError", "KeyError"]'::jsonb, 0),

('d0000000-0000-0000-0000-000000000047', 'a0000000-0000-0000-0000-000000000010', 'The finally Block',
$md$Which block always executes after a try statement, whether or not an exception occurred (and whether or not it was caught)?$md$,
'easy', 5, 'mcq',
'["except", "else", "finally", "raise"]'::jsonb, 2),

('d0000000-0000-0000-0000-000000000048', 'a0000000-0000-0000-0000-000000000010', 'Which except Runs First?',
$md$What does the following code print?

    try:
        x = int("abc")
    except ValueError:
        print("A")
    except Exception:
        print("B")
    finally:
        print("C")$md$,
'medium', 5, 'mcq',
'["A\nC", "B\nC", "A", "C"]'::jsonb, 0),

('d0000000-0000-0000-0000-000000000049', 'a0000000-0000-0000-0000-000000000010', 'Bare except Clauses',
$md$What is the main risk of using a bare `except:` clause instead of `except SomeSpecificError:`?$md$,
'medium', 5, 'mcq',
'["It only catches SomeSpecificError exceptions", "It silently catches every exception, including ones you did not anticipate, which can hide real bugs", "It causes a SyntaxError at import time", "It prevents the finally block from running"]'::jsonb, 1),

('d0000000-0000-0000-0000-000000000050', 'a0000000-0000-0000-0000-000000000010', 'Code After a Raised Exception',
$md$What does the following code print?

    try:
        print("A")
        raise ValueError("oops")
        print("B")
    except ValueError:
        print("C")$md$,
'medium', 5, 'mcq',
'["A\nB\nC", "A\nC", "A\nB", "C"]'::jsonb, 1);

-- ============================================================================
-- 5. FILL-IN-THE-BLANK QUESTIONS (3)
-- ============================================================================

insert into questions (id, topic_id, title, prompt, difficulty, points, question_type, correct_answer) values

('e0000000-0000-0000-0000-000000000028', 'a0000000-0000-0000-0000-000000000010', 'Cleanup Block',
$md$The `___` block always executes whether or not an exception occurred, making it ideal for cleanup code.$md$,
'easy', 5, 'fill_blank', $txt$finally$txt$),

('e0000000-0000-0000-0000-000000000029', 'a0000000-0000-0000-0000-000000000010', 'Catching a Specific Exception',
$md$To catch the specific error raised when dividing a number by zero, you would write `except ___:`.$md$,
'easy', 5, 'fill_blank', $txt$ZeroDivisionError$txt$),

('e0000000-0000-0000-0000-000000000030', 'a0000000-0000-0000-0000-000000000010', 'Manually Triggering an Exception',
$md$The `___` statement is used to manually trigger an exception, as in `___ ValueError("invalid input")`.$md$,
'medium', 5, 'fill_blank', $txt$raise$txt$);

-- ============================================================================
-- 6. TOPIC CONTENT UPDATE (try_it_examples + common_mistakes)
-- ============================================================================

update topics set
try_it_examples = '[
  {
    "description": "Catch a ZeroDivisionError",
    "code": "try:\n    result = 10 / 0\nexcept ZeroDivisionError:\n    print(\"Cannot divide by zero\")",
    "output": "Cannot divide by zero"
  },
  {
    "description": "Use finally for guaranteed cleanup",
    "code": "try:\n    print(\"Trying...\")\n    raise ValueError(\"bad value\")\nexcept ValueError as e:\n    print(f\"Caught: {e}\")\nfinally:\n    print(\"Cleanup done\")",
    "output": "Trying...\nCaught: bad value\nCleanup done"
  },
  {
    "description": "Raise and catch a custom exception",
    "code": "def check_age(age):\n    if age < 0:\n        raise ValueError(\"Age cannot be negative\")\n    return age\n\ntry:\n    check_age(-5)\nexcept ValueError as e:\n    print(f\"Invalid: {e}\")",
    "output": "Invalid: Age cannot be negative"
  }
]'::jsonb,
common_mistakes = $md$Beginners run into a handful of recurring traps when learning exception handling:

1. **Using a bare `except:`.** Writing `except:` with no exception type catches *everything*, including typos like a misspelled variable name (`NameError`) or even `KeyboardInterrupt`. This hides real bugs instead of fixing them. **Fix:** always name the specific exception, e.g. `except ValueError:`.

2. **Catching `Exception` too broadly.** `except Exception:` is only slightly better than a bare `except:` — it still lumps together errors you meant to handle with ones you didn't anticipate. **Fix:** list the specific exception types you actually expect (`ValueError`, `KeyError`, etc.), and use multiple `except` clauses if needed.

3. **Assuming code after the failing line still runs.** Once a line inside `try` raises, Python jumps straight to the matching `except` — every line after the failure point in that `try` block is skipped. **Fix:** don't rely on later lines in the same `try` block to run; put code that must always run in `finally` instead.

4. **Forgetting `finally` for cleanup.** Closing a file, releasing a lock, or printing a "done" message is easy to forget when an exception short-circuits the normal flow. **Fix:** put must-always-run code in a `finally` block, not just at the end of the function.

5. **Confusing a fresh `raise` with a re-raise.** Inside an `except` block, `raise` alone re-raises the *same* exception (preserving its traceback), while `raise ValueError("new message")` starts a brand-new exception. Mixing these up loses the original error context. **Fix:** use bare `raise` to propagate the original error, and only construct a new exception when you intend to replace it.$md$
where id = 'a0000000-0000-0000-0000-000000000010';
