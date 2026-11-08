"""Acceptance tests for the Cash exercise.

Each test runs your program as a whole, exactly as a user would: it types
some answers to the "Amount: " question, then checks what your program
prints and tries to explain what is wrong.

Run the tests from the exercise folder with:

    python test_cash.py
"""

import os
import subprocess
import sys
from pathlib import Path

EXERCISE_DIR = Path(__file__).resolve().parent
SCRIPT = "cash.py"
PROMPT = "Amount: "
TIMEOUT = 5  # seconds
COINS = [50, 20, 10, 5, 2, 1]  # in cents
MIN_AMOUNT = 1
MAX_AMOUNT = 99

# Each test case: (what is checked, answers typed by the user).
# Convention: only the LAST answer is a valid amount, all the others
# must be rejected by the program (which then asks again).
CASES = [
    ("64 cents (example of the instructions)", ["64"]),
    ("1 cent (smallest amount)", ["1"]),
    ("99 cents (largest amount)", ["99"]),
    ("24 cents", ["24"]),
    ("98 cents (every kind of coin is needed)", ["98"]),
    ("0 is rejected", ["0", "5"]),
    ("100 is rejected (more than 99)", ["100", "50"]),
    ("a large and a negative number are rejected", ["142", "-2", "79"]),
    ("a word and an empty answer are rejected", ["sixty", "", "26"]),
    ("decimal numbers are rejected", ["0.64", "64.5", "10"]),
]


# ---------------------------------------------------------------------------
# Running the student's program
# ---------------------------------------------------------------------------

def run_program(answers):
    """Run the program, typing the answers one per line.

    Return (stdout, stderr, return code), or None if the program
    did not stop in time.
    """
    try:
        # sys.executable is the Python running the tests,
        # so "python" vs "python3" does not matter.
        result = subprocess.run(
            [sys.executable, SCRIPT],
            input="\n".join(answers) + "\n",
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=EXERCISE_DIR,
            env=dict(os.environ, PYTHONIOENCODING="utf-8"),
            timeout=TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return None
    stdout = result.stdout.replace("\r\n", "\n")
    return stdout, result.stderr.strip(), result.returncode


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def show(lines):
    """Indent lines and make spaces visible (shown as '·')."""
    if not lines:
        return "    (nothing)"
    return "\n".join("    " + line.replace(" ", "·") for line in lines)


def plural(number, word):
    """Return e.g. '1 coin' or '3 coins'."""
    return f"{number} {word}" if number == 1 else f"{number} {word}s"


def last_lines(text, nb_lines=4):
    """Return the last lines of a text, indented."""
    lines = text.split("\n")[-nb_lines:]
    return "\n".join("    " + line for line in lines)


def is_whole_number(text):
    """Return True if text is a whole number, possibly negative."""
    return text.removeprefix("-").isdigit()


def is_decimal_number(text):
    """Return True if text looks like a decimal number such as 4.0."""
    integer_part, dot, decimal_part = text.removeprefix("-").partition(".")
    return dot == "." and integer_part.isdigit() and decimal_part.isdigit()


# ---------------------------------------------------------------------------
# Expected answer
# ---------------------------------------------------------------------------

def greedy_change(amount, coins):
    """Return the list of (coin, number of coins) used by the greedy method."""
    change = []
    for coin in coins:
        if amount >= coin:
            change.append((coin, amount // coin))
            amount = amount % coin
    return change


def nb_coins(amount, coins=COINS):
    """Return the number of coins given back by the greedy method."""
    return sum(count for _, count in greedy_change(amount, coins))


def explain_change(amount):
    """Return e.g. '64 = 1x50 + 1x10 + 2x2, so 4 coins'."""
    terms = " + ".join(f"{count}x{coin}"
                       for coin, count in greedy_change(amount, COINS))
    return f"{amount} = {terms}, so {plural(nb_coins(amount), 'coin')}"


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def count_prompts(stdout):
    """Count the "Amount: " questions at the start of the output.

    Return (number of questions, rest of the output).
    """
    nb_prompts = 0
    while stdout.startswith(PROMPT):
        stdout = stdout[len(PROMPT):]
        nb_prompts += 1
    return nb_prompts, stdout


def check_questions(stdout, stderr, return_code, answers):
    """Check that the program asks the question the right number of times.

    Return (error message or None, rest of the output after the questions).
    """
    nb_prompts, rest = count_prompts(stdout)
    printed = "Your program printed:\n" + show(stdout.splitlines())

    if stdout.startswith((PROMPT + "\n", PROMPT.strip() + "\n")):
        return (f"The answer must be typed on the same line as the question: "
                f"use input({PROMPT!r}) instead of print().\n{printed}"), rest
    if nb_prompts == 0:
        if stdout.startswith(PROMPT.strip()):
            message = (f"The question must be exactly {PROMPT!r}, "
                       f"with a space after the colon.")
        else:
            message = f"Your program should start by asking {PROMPT!r}."
        return f"{message}\n{printed}", rest

    if "EOFError" in stderr:
        return (f"Your program asked again after {answers[-1]!r}, "
                f"but {answers[-1]} is a valid amount (between "
                f"{MIN_AMOUNT} and {MAX_AMOUNT} included)."), rest
    if return_code != 0:
        answer = answers[min(nb_prompts, len(answers)) - 1]
        message = (f"Your program crashed after reading {answer!r}:\n"
                   f"{last_lines(stderr)}")
        if "ValueError" in stderr:
            message += ("\nint() fails when the text is not a whole number: "
                        "check the text first (e.g. with str.isdigit()) "
                        "before converting it.")
        return message, rest

    if PROMPT in rest:
        extra = rest[:rest.index(PROMPT)]
        return (f"Your program printed {extra!r} before asking again. "
                f"When an answer is invalid, it should only ask again.\n"
                f"{printed}"), rest
    if nb_prompts < len(answers):
        accepted = answers[nb_prompts - 1]
        return (f"Your program accepted {accepted!r} as an amount, but it "
                f"should ask again: an amount must be a whole number "
                f"between {MIN_AMOUNT} and {MAX_AMOUNT} included.\n"
                f"{printed}"), rest
    return None, rest


def explain_wrong_number(given, amount):
    """Explain why the number of coins printed is wrong."""
    expected = nb_coins(amount)
    if given == amount:
        return (f"Your program printed the amount ({amount}), but it should "
                f"print the number of coins.")
    message = f"Your program printed {given}, but it should print {expected}."
    # Which coin, if never used, would give the number printed?
    missing = []
    for coin in COINS:
        without_coin = [other for other in COINS if other != coin]
        if given == nb_coins(amount, without_coin):
            missing.append(f"{coin}-cent")
    if len(missing) == 1:
        message += f" It looks like the {missing[0]} coin is never used"
    elif len(missing) == 2:
        message += (f" It looks like the {missing[0]} or the {missing[1]} "
                    f"coin is never used")
    if 1 <= len(missing) <= 2:
        message += (": check your list of coins and your conditions "
                    "(> or >= ?).")
    return message


def check_answer(rest, amount):
    """Check what is printed after the questions. Return a message or None."""
    expected = nb_coins(amount)
    lines = rest.splitlines()
    printed = "Your program printed after the questions:\n" + show(lines)
    explanation = f"Expected: {explain_change(amount)}."

    if not lines:
        return (f"Your program printed nothing after reading {amount}: "
                f"it should print the number of coins ({expected}).")
    if len(lines) > 1:
        message = ("Your program should print only the number of coins, "
                   "on a single line.")
        if str(expected) in lines:
            message += (" The right number is there: remove the other "
                        "print() (for instance prints used to debug).")
        return f"{message}\n{printed}\n{explanation}"

    line = lines[0]
    if line != line.strip():
        return (f"Nothing should be printed before or after the number "
                f"(not even spaces).\n{printed}")
    if is_whole_number(line):
        return f"{explain_wrong_number(int(line), amount)}\n{explanation}"
    if is_decimal_number(line):
        if float(line) == expected:
            message = (f"Your program printed {line}, but it should print "
                       f"{expected}: a number of coins is an int.")
        else:
            message = (f"Your program printed {line}, but a number of coins "
                       f"is a whole number.")
        return (f"{message} Use // (integer division) instead of / "
                f"(/ always gives a float).\n{explanation}")
    if str(expected) in line.split():
        return (f"Your program should print only the number ({expected}), "
                f"without any other text.\n{printed}")
    return (f"Your program should print the number of coins ({expected}).\n"
            f"{printed}\n{explanation}")


def check_case(answers):
    """Run one test case. Return None if it passes, else an error message."""
    result = run_program(answers)
    if result is None:
        return ("Your program did not stop (infinite loop?). Check that "
                "input() is called inside your loop, and that the amount "
                "decreases each time a coin is given.")
    stdout, stderr, return_code = result

    message, rest = check_questions(stdout, stderr, return_code, answers)
    if message is not None:
        return message
    amount = int(answers[-1])
    if rest == str(nb_coins(amount)) + "\n":
        return None
    return check_answer(rest, amount)


# ---------------------------------------------------------------------------
# Main program
# ---------------------------------------------------------------------------

def main():
    sys.stdout.reconfigure(errors="replace")
    use_colors = sys.stdout.isatty() and (
        os.name != "nt" or "WT_SESSION" in os.environ)
    green = "\033[32m" if use_colors else ""
    red = "\033[31m" if use_colors else ""
    reset = "\033[0m" if use_colors else ""

    if not (EXERCISE_DIR / SCRIPT).is_file():
        print(f"No {SCRIPT} found in {EXERCISE_DIR}")
        return 1

    nb_ok = 0
    for description, answers in CASES:
        typed = ", ".join(repr(answer) for answer in answers)
        message = check_case(answers)
        if message is None:
            nb_ok += 1
            print(f"{green}✔{reset} {description}")
        else:
            print(f"{red}✗{reset} {description}")
            print(f"    Answers typed: {typed}")
            print("    " + message.replace("\n", "\n    ") + "\n")

    color = green if nb_ok == len(CASES) else red
    print(f"Validated: {color}{nb_ok}/{len(CASES)}{reset}")
    return 0 if nb_ok == len(CASES) else 1


if __name__ == "__main__":
    sys.exit(main())
