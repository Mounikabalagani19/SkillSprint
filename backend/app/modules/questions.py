from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class ModuleLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    expert = "expert"


@dataclass(frozen=True)
class ModuleQA:
    id: int
    level: ModuleLevel
    question: str
    answer: str
    explanation: str
    variants: List[str] = field(default_factory=list)


def _mk(level: ModuleLevel, idx: int, question: str, answer: str, explanation: str, variants: Optional[List[str]] = None) -> ModuleQA:
    return ModuleQA(
        id=idx,
        level=level,
        question=question,
        answer=answer,
        explanation=explanation,
        variants=list(variants or []),
    )


# NOTE: The prompt includes only answers + explanations (no question text provided).
# We store them verbatim so the backend can serve them; the frontend can render
# them as module review cards or pair them with questions later when added.

BEGINNER: List[ModuleQA] = [
    _mk(ModuleLevel.beginner, 1, (
        "What is the final value of x?\n\nx = 10\nx = x + 5"
    ), "15", "The variable x is initialized to 10, and then 5 is added to it."),
    _mk(ModuleLevel.beginner, 2, (
        "What will this code print?\n\nprint(5 + 3 * 2)"
    ), "11", "Due to the order of operations (PEMDAS/BODMAS), multiplication (3 * 2) is performed before addition (5 + 6)."),
    _mk(ModuleLevel.beginner, 3, (
        "What is the value of the element at index 2 in the list my_list?\n\nmy_list = [10, 20, 30, 40]"
    ), "30", "List indexing is zero-based, so index 2 refers to the third element in the list."),
    _mk(ModuleLevel.beginner, 4, (
        "How many times will the word \"Hello\" be printed?\n\nfor i in range(5):\n  print(\"Hello\")"
    ), "5 times", "The range(5) function generates a sequence of five numbers (0 through 4), causing the loop to execute five times.", ["5", "five", "prints 5 times", "5x"]),
    _mk(ModuleLevel.beginner, 5, (
        "What will this code output?\n\n a = 10\n b = \"10\"\n print(a == int(b))"
    ), "True", "The string '10' is explicitly converted to an integer using int(b) before being compared to the integer a. 10 == 10 is True."),
    _mk(ModuleLevel.beginner, 6, (
        "What does this function return if age is 20?\n\n def can_vote(age):\n  if age >= 18:\n    return \"Yes\"\n  else:\n    return \"No\""
    ), "Yes", "The condition 20 >= 18 is true, so the function returns the string 'Yes'."),
    _mk(ModuleLevel.beginner, 7, (
        "What is the output of this code?\n\nprint(len(\"hello\"))"
    ), "5", "The len() function returns the number of characters in the string 'hello'."),
    _mk(ModuleLevel.beginner, 8, (
        "What is the final value of count?\n\ncount = 0\ncount += 1\ncount += 1"
    ), "2", "count starts at 0, is incremented to 1, and then incremented again to 2."),
    _mk(ModuleLevel.beginner, 9, (
        "What will be printed to the console?\n\nfruit = \"apple\"\nprint(f\"I have an {fruit}.\")"
    ), "I have an apple.", "This is an f-string, which embeds the value of the fruit variable directly into the string."),
    _mk(ModuleLevel.beginner, 10, (
        "What is the value of is_true?\n\n is_true = (5 > 3) and (10 < 20)"
    ), "True", "Both conditions (5 > 3) and (10 < 20) are true. The and operator results in True only if both operands are true.", ["true", "TRUE"]),
    _mk(ModuleLevel.beginner, 11, (
        "What is the third element printed by this loop?\n\nfor item in [\"a\", \"b\", \"c\", \"d\"]:\n    print(item)"
    ), "c", "The loop prints the elements in order. The third one printed is 'c'.", ["'c'", "\"c\""]),
    _mk(ModuleLevel.beginner, 12, (
        "What value does data['city'] retrieve?\n\n data = { \"name\": \"John\", \"city\": \"New York\" }"
    ), "New York", "This retrieves the value associated with the key 'city' in the data dictionary.", ["new york"]),
    _mk(ModuleLevel.beginner, 13, (
        "What is the output?\n\nprint(10 % 3)"
    ), "1", "The modulo operator (%) returns the remainder of a division. 10 divided by 3 is 3 with a remainder of 1."),
    _mk(ModuleLevel.beginner, 14, (
        "What will this code print?\n\n x = 5\n if x * 2 == 10:\n  print(\"Correct\")\n else:\n  print(\"Incorrect\")"
    ), "Correct", "The expression 5 * 2 equals 10, so the if condition is true.", ["correct"]),
    _mk(ModuleLevel.beginner, 15, (
        "What is the content of new_list?\n\n my_list = [1, 2, 3]\n new_list = my_list + [4, 5]"
    ), "[1, 2, 3, 4, 5]", "The + operator concatenates the two lists, creating a new list."),
    _mk(ModuleLevel.beginner, 16, (
        "What will be the final value of text?\n\n text = \"abc\"\n text = text + \"def\""
    ), "abcdef", "The + operator concatenates strings.", ["abc def", "abcdef"]),
    _mk(ModuleLevel.beginner, 17, (
        "What does this code print?\n\n def greet(name):\n  return f\"Hi, {name}\"\n print(greet(\"Alice\"))"
    ), "Hi, Alice", "The greet function is called with the argument 'Alice', which is formatted into the return string.", ["hi, alice"]),
    _mk(ModuleLevel.beginner, 18, (
        "What is the output of this snippet?\n\n print(bool(0))"
    ), "False", "In Python, 0, empty strings, empty lists, and None are considered 'falsy'. The bool() function converts 0 to False.", ["false"]),
    _mk(ModuleLevel.beginner, 19, (
        "What is the value of my_list after this code runs?\n\n my_list = [1, 2, 3]\n my_list.append(4)"
    ), "[1, 2, 3, 4]", "The .append() method modifies the list in-place by adding an element to the end."),
    _mk(ModuleLevel.beginner, 20, (
        "What will this code print?\n\n i = 0\n while i < 3:\n  i += 1\n print(i)"
    ), "3", "The while loop continues as long as i < 3. It increments i on each iteration. The loop stops when i becomes 3, and this final value is printed."),
]


INTERMEDIATE: List[ModuleQA] = [
    _mk(ModuleLevel.intermediate, 21, (
        "What is the output of this code?\n\n my_list = [1, 2, 3, 4, 5]\n print(my_list[1:4])"
    ), "[2, 3, 4]", "This is list slicing. It extracts elements starting from index 1 up to (but not including) index 4."),
    _mk(ModuleLevel.intermediate, 22, (
        "What will be printed to the console?\n\n for i in range(5):\n  if i == 3:\n    break\n  print(i)"
    ), "0, 1, 2", "The break statement immediately terminates the loop when i equals 3, so 3 and 4 are never printed.", ["0 1 2", "0\n1\n2", "0,1,2"]),
    _mk(ModuleLevel.intermediate, 23, (
        "What is the value of result?\n\n my_dict = {\"a\": 1, \"b\": 2, \"c\": 3}\n result = my_dict.get(\"d\", 0)"
    ), "0", "The .get() dictionary method returns the value for a key if it exists. If the key is not found, it returns the default value provided (in this case, 0) instead of raising an error."),
    _mk(ModuleLevel.intermediate, 24, (
        "What does this list comprehension produce?\n\n numbers = [1, 2, 3, 4, 5]\n squares = [n*n for n in numbers if n % 2 == 0]"
    ), "[4, 16]", "This list comprehension first filters the numbers list to include only even numbers (n % 2 == 0), which are 2 and 4. It then squares each of those numbers."),
    _mk(ModuleLevel.intermediate, 25, (
        "What is the output of this code?\n\n arr = [10, 20, 30]\n new_arr = [num / 10 for num in arr]\n print(new_arr)"
    ), "[1.0, 2.0, 3.0]", "The list comprehension creates a new list where each number from the original arr has been divided by 10. Division in Python 3 results in a float."),
    _mk(ModuleLevel.intermediate, 26, (
        "What will this function return for the input [1, -2, 3, -4, 5]?\n\n def count_positives(nums):\n  count = 0\n  for n in nums:\n    if n > 0:\n      count += 1\n  return count"
    ), "3", "The function iterates through the list and counts the numbers that are strictly greater than 0 (which are 1, 3, and 5)."),
    _mk(ModuleLevel.intermediate, 27, (
        "What is printed to the console?\n\n x = 10\n def test():\n  x = 20\n  print(x)\n test()"
    ), "20", "The x defined inside the test function has a local scope. It shadows the global variable x. The print statement inside the function refers to the local x."),
    _mk(ModuleLevel.intermediate, 28, (
        "What is the final content of the my_set variable?\n\n my_list = [1, 2, 2, 3, 4, 4, 4]\n my_set = set(my_list)"
    ), "{1, 2, 3, 4}", "A set is an unordered collection of unique elements. When the list is converted to a set, all duplicate values are automatically removed."),
    _mk(ModuleLevel.intermediate, 29, (
        "Find the bug in this code snippet intended to find the maximum number.\n\n def find_max(numbers):\n  max_num = 0\n  for n in numbers:\n    if n > max_num:\n      max_num = n\n  return max_num\n# Hint: Consider the input [-10, -5, -2]"
    ), "Initialize max_num = numbers[0]", "The bug is that max_num is initialized to 0. If the input list contains only negative numbers (e.g., [-10, -5, -2]), the function will incorrectly return 0 instead of the actual maximum, -2. Fix by initializing with the first element of the list."),
    _mk(ModuleLevel.intermediate, 30, (
        "What happens when you run this code?\n\n result = \"5\" + 5"
    ), "TypeError", "Python does not allow concatenating a string and an integer with '+'. They must be of the same type.", ["type error", "type-error", "raises typeerror"]),
    _mk(ModuleLevel.intermediate, 31, (
        "What is printed by this code?\n\n for i in range(2):\n  for j in range(2):\n    print(f\"({i},{j})\")"
    ), "(0,0), (0,1), (1,0), (1,1)", "Nested loops: the outer loop runs twice (i=0 and i=1). For each iteration, the inner loop runs twice (j=0 and j=1).", ["(0,0) (0,1) (1,0) (1,1)", "(0,0)\n(0,1)\n(1,0)\n(1,1)"]),
    _mk(ModuleLevel.intermediate, 32, (
        "What will the list comprehension return?\n\n ages = [12, 25, 17, 30, 18]\n adults = [age for age in ages if age >= 18]"
    ), "[25, 30, 18]", "The list comprehension creates a new list containing only the elements from ages that satisfy the condition age >= 18."),
    _mk(ModuleLevel.intermediate, 33, (
        "What is the value of text after this code runs?\n\n text = \"hello world\"\n text = text.replace(\"world\", \"python\")"
    ), "hello python", "The .replace() method returns a new string where all occurrences of the first argument are replaced by the second."),
    _mk(ModuleLevel.intermediate, 34, (
        "What does this code print?\n\n obj = { 'a': 1 }\n new_obj = { **obj, 'b': 2 }\n print(new_obj)"
    ), "{'a': 1, 'b': 2}", "The ** operator unpacks the key-value pairs from obj into the new dictionary literal.", ["{ 'a': 1, 'b': 2 }", "{\"a\": 1, \"b\": 2}"]),
    _mk(ModuleLevel.intermediate, 35, (
        "What is the bug in this function meant to add an item to a list?\n\n def add_item(item, my_list=[]):\n    my_list.append(item)\n    return my_list\n\n list1 = add_item(1)\n list2 = add_item(2) # What is the value of list2?"
    ), "list2 is [1, 2]", "The bug is the use of a mutable default argument (my_list=[]). The default list is created only once when the function is defined and is reused across subsequent calls."),
    _mk(ModuleLevel.intermediate, 36, (
        "What is the output?\n\n print(type(None))"
    ), "<class 'NoneType'>", "None is a special singleton object in Python, and its type is NoneType."),
    _mk(ModuleLevel.intermediate, 37, (
        "What will be printed?\n\n try:\n  result = 10 / 0\n except ZeroDivisionError:\n  print(\"Error\")"
    ), "Error", "The code attempts to divide by zero, which raises a ZeroDivisionError. The except block catches this error and executes its print statement.", ["error"]),
    _mk(ModuleLevel.intermediate, 38, (
        "What is the value of total?\n\n nums = [1, 2, 3, 4]\n total = sum(nums)"
    ), "10", "The built-in sum() function returns the sum of all items in an iterable."),
    _mk(ModuleLevel.intermediate, 39, (
        "What is the output of this code snippet?\n\n a, b = 0, 1\n for _ in range(5):\n  a, b = b, a + b\n print(a)"
    ), "5", "This code generates the Fibonacci sequence. After 5 iterations, the value of a is 5."),
    _mk(ModuleLevel.intermediate, 40, (
        "What does this conditional expression return?\n\n is_member = True\n fee = \"$2.00\" if is_member else \"$10.00\""
    ), "$2.00", "This is a conditional expression. Since is_member is True, the expression evaluates to '$2.00'.", ["2.00", "$2", "2"]),
]


EXPERT: List[ModuleQA] = [
    _mk(ModuleLevel.expert, 41, (
        "What will this code, which uses closures, print?\n\n def make_counter():\n  count = 0\n  def inner():\n    nonlocal count\n    count += 1\n    return count\n  return inner\n\n counter1 = make_counter()\n print(counter1())\n print(counter1())"
    ), "1, 2", "The inner function is a closure that remembers 'count' from its enclosing scope. nonlocal ensures updates the outer variable. First call returns 1, second returns 2.", ["1 then 2", "1\n2", "1 and 2"]),
    _mk(ModuleLevel.expert, 42, (
        "What is the output of this recursive function when called with factorial(4)?\n\n def factorial(n):\n  if n == 0:\n    return 1\n  else:\n    return n * factorial(n - 1)"
    ), "24", "This is a classic recursive implementation of factorial, calculating 4 * 3 * 2 * 1."),
    _mk(ModuleLevel.expert, 43, (
        "What is the potential issue with this code in a multi-threaded environment?\n\n class Counter:\n    def __init__(self):\n        self.count = 0\n    def increment(self):\n        self.count += 1"
    ), "Race condition", "In a multi-threaded context, two threads could read self.count at the same time, increment, and write back, losing an increment. This operation is not atomic."),
    _mk(ModuleLevel.expert, 44, (
        "What will be the final value of list_b?\n\n list_a = [1, 2, 3]\n list_b = list_a\n list_b.append(4)"
    ), "[1, 2, 3, 4]", "Assigning list_b = list_a makes both names reference the same list. Appending via list_b modifies that list, observed through list_a as well."),
    _mk(ModuleLevel.expert, 45, (
        "What is the result of this generator expression?\n\n gen = (x * x for x in range(5))\n result = list(gen)"
    ), "[0, 1, 4, 9, 16]", "The generator yields the squares of 0..4; list() consumes it into a list."),
    _mk(ModuleLevel.expert, 46, (
        "What is the output of this code?\n\n def my_func(a, b=[]):\n    b.append(a)\n    return b\n\n print(my_func(1))\n print(my_func(2))"
    ), "[1] then [1, 2]", "This is the mutable default argument bug. The default list b is created once; subsequent calls reuse it.", ["[1]\n[1, 2]", "[1], [1, 2]"]),
    _mk(ModuleLevel.expert, 47, (
        "What is the difference between list_b and list_c after this code runs?\n\n list_a = [[1], [2]]\n list_b = list_a[:]\n list_c = [item[:] for item in list_a]\n\n list_a[0][0] = 99"
    ), "list_b=[[99],[2]]; list_c=[[1],[2]]", "list_b is a shallow copy (inner lists shared), so it reflects the change. list_c deep-copies inner lists via slicing."),
    _mk(ModuleLevel.expert, 48, (
        "What is the primary bug in this binary search implementation?\n\n def binary_search(arr, target):\n    low, high = 0, len(arr) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if arr[mid] < target:\n            low = mid + 1\n        elif arr[mid] > target:\n            high = mid - 1\n        else:\n            return mid\n    return -1\n # Hint: What happens if `low` and `high` are very large numbers?"
    ), "integer overflow risk", "While Python's ints are arbitrary precision, in fixed-size integer languages low+high can overflow. Use mid = low + (high - low) // 2.", ["overflow", "mid = low + (high - low) // 2"]),
    _mk(ModuleLevel.expert, 49, (
        "What is the final value of data['a']['b']?\n\n data = { 'a': { 'b': 1 } }\n ref = data['a']\n ref['b'] = 2"
    ), "2", "ref references the same inner dict as data['a']; mutating through ref changes data['a'] as well."),
    _mk(ModuleLevel.expert, 50, (
        "This decorator is supposed to time a function. What is the mistake in its implementation?\n\n import time\n def timer(func):\n    def wrapper(*args, **kwargs):\n        start = time.time()\n        func(*args, **kwargs)\n        end = time.time()\n        print(f\"Time elapsed: {end - start}\")\n    return wrapper\n # Hint: The decorated function's return value is lost."
    ), "missing return of func result", "The wrapper must capture the return value of func and return it: result = func(*args, **kwargs); return result.", ["must return result", "not returning", "doesn't return"]),
    _mk(ModuleLevel.expert, 51, (
        "What is the difference between an iterator and a generator in Python?\n\n # This is a conceptual question."
    ), "Generators are iterators created with yield", "An iterator implements __iter__/__next__; a generator is a concise way to create an iterator using yield. All generators are iterators.", ["generators use yield", "all generators are iterators"]),
    _mk(ModuleLevel.expert, 52, (
        "Given a simple Node class for a linked list, write a single line of code to reverse the direction of two nodes, p and q, where p.next = q.\n\n # Before: p -> q\n # After: p <- q\n # Assume `p` and `q` are defined nodes."
    ), "q.next = p", "This single assignment reverses the link, making q's next pointer refer back to p (note: managing p.next is needed to avoid orphaning)."),
    _mk(ModuleLevel.expert, 53, (
        "What is the output of this dynamic programming approach to Fibonacci, specifically for fib(4)?\n\n memo = {}\n def fib(n):\n    if n in memo: return memo[n]\n    if n <= 1: return n\n    memo[n] = fib(n-1) + fib(n-2)\n    return memo[n]"
    ), "3", "This is a top-down DP approach using memoization. fib(4) = fib(3) + fib(2) = 3."),
    _mk(ModuleLevel.expert, 54, (
        "What is the problem with using float numbers for financial calculations, as shown below?\n\n price = 0.1 + 0.2\n # print(price == 0.3) will be False"
    ), "floating point precision", "Many decimal fractions (like 0.1) cannot be represented exactly in binary floating-point; 0.1 + 0.2 is close to but not exactly 0.3.", ["floating-point precision", "float precision", "precision error"]),
    _mk(ModuleLevel.expert, 55, (
        "What is the final value of x after this code runs?\n\n x = 10\n items = [1, 2, 3]\n _ = [x for x in items] "
    ), "10", "The list comprehension's iteration variable x is local to the comprehension and doesn't affect the outer x."),
    _mk(ModuleLevel.expert, 56, (
        "What is the difference in output between the two print statements?\n\n my_map = map(lambda x: x*2, [1, 2, 3])\n print(list(my_map)) # What is printed here?\n print(list(my_map)) # And what is printed here?"
    ), "first [2, 4, 6]; second []", "Iterators like map are single-use. The first list() consumes it; the second list() finds it exhausted.", ["[2,4,6] then []", "[2, 4, 6] and []"]),
    _mk(ModuleLevel.expert, 57, (
        "How does Python pass arguments to functions?\n\n def modify_list(my_list):\n    my_list.append(100)\n\n data = [1, 2]\n modify_list(data)\n # What is the value of `data` now?"
    ), "[1, 2, 100]", "Python uses pass-by-object-reference; lists are mutable so the function modifies the original object."),
    _mk(ModuleLevel.expert, 58, (
        "What does this method call print?\n\n class MyClass:\n    name = \"Class Name\"\n    def __init__(self, name):\n        self.name = name\n\n    def get_name(self):\n        print(self.name)\n\n instance = MyClass(\"Instance Name\")\n instance.get_name()"
    ), "Instance Name", "self.name refers to the instance attribute set in __init__, which overrides the class attribute."),
    _mk(ModuleLevel.expert, 59, (
        "What does this code print?\n\n class Parent:\n    def identify(self):\n        return \"Parent\"\n\n class Child(Parent):\n    def identify(self):\n        return \"Child\"\n\n class Grandchild(Child):\n    def identify(self):\n        return super().identify()\n\n print(Grandchild().identify())"
    ), "Child", "super() in Grandchild refers to Child in the MRO; thus it calls Child.identify()."),
    _mk(ModuleLevel.expert, 60, (
        "Given the list [1, 2, 3], what is the result of using functools.reduce with the operator.xor function?\n\n import functools, operator\n result = functools.reduce(operator.xor, [1, 2, 3], 0)"
    ), "0", "functools.reduce applies XOR cumulatively: ((0 ^ 1) ^ 2) ^ 3 -> 0."),
]


ALL_BY_LEVEL: Dict[ModuleLevel, List[ModuleQA]] = {
    ModuleLevel.beginner: BEGINNER,
    ModuleLevel.intermediate: INTERMEDIATE,
    ModuleLevel.expert: EXPERT,
}


def get_questions(level: ModuleLevel) -> List[ModuleQA]:
    return list(ALL_BY_LEVEL[level])


def get_all() -> List[ModuleQA]:
    return list(BEGINNER) + list(INTERMEDIATE) + list(EXPERT)
