from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from .questions import ModuleLevel, ModuleQA


# Reserve a distinct ID range for Java to avoid collisions with Python module IDs
# Python used 1..60; Java will use 1001..1060


def J(id_offset: int, level: ModuleLevel, question: str, answer: str = "", explanation: str = "", variants: Optional[List[str]] = None) -> ModuleQA:
    return ModuleQA(
        id=id_offset,  # unique across modules
        level=level,
        question=question,
        answer=answer,
        explanation=explanation,
        variants=list(variants or []),
    )


BEGINNER: List[ModuleQA] = [
    J(1001, ModuleLevel.beginner, "What is the final value of x?\n\nint x = 10;\nx = x + 5;", "15", "x starts at 10 and 5 is added."),
    J(1002, ModuleLevel.beginner, "What will this code print?\n\nSystem.out.println(5 + 3 * 2);", "11", "Multiplication happens before addition (5 + 6)."),
    J(1003, ModuleLevel.beginner, "What is the value of the element at index 2 in the array myArray?\n\nint[] myArray = {10, 20, 30, 40};", "30", "Array indices are zero-based; index 2 is the third element."),
    J(1004, ModuleLevel.beginner, "How many times will the word \"Hello\" be printed?\n\nfor (int i = 0; i < 5; i++) {\n  System.out.println(\"Hello\");\n}", "5 times", "Loop runs for i=0..4 (5 iterations).", ["5", "five", "prints 5 times", "5x"]),
    J(1005, ModuleLevel.beginner, "What will this code output?\n\nString a = \"10\";\nint b = 10;\nSystem.out.println(Integer.parseInt(a) == b);", "true", "'a' is parsed to int 10 then compared to 10.", ["True"]),
    J(1006, ModuleLevel.beginner, "What does this method return if age is 20?\n\npublic String canVote(int age) {\n  if (age >= 18) {\n    return \"Yes\";\n  } else {\n    return \"No\";\n  }\n}", "Yes", "20 >= 18 evaluates true so returns 'Yes'."),
    J(1007, ModuleLevel.beginner, "What is the output of this code?\n\nSystem.out.println(\"hello\".length());", "5", "'hello' has 5 characters."),
    J(1008, ModuleLevel.beginner, "What is the final value of count?\n\nint count = 0;\ncount++;\ncount++;", "2", "Two increments from 0 -> 1 -> 2."),
    J(1009, ModuleLevel.beginner, "What will be printed to the console?\n\nString fruit = \"apple\";\nSystem.out.printf(\"I have an %s.\", fruit);", "I have an apple.", "printf formats the string with 'fruit'.", ["i have an apple.", "I have an apple"]),
    J(1010, ModuleLevel.beginner, "What is the value of isTrue?\n\nboolean isTrue = (5 > 3) && (10 < 20);", "true", "Both comparisons are true; && yields true.", ["True"]),
    J(1011, ModuleLevel.beginner, "What is the third element printed by this loop?\n\nString[] letters = {\"a\", \"b\", \"c\", \"d\"};\nfor (String letter : letters) {\n    System.out.println(letter);\n}", "c", "The third printed element is 'c'.", ["'c'", '"c"']),
    J(1012, ModuleLevel.beginner, "What is the output?\n\nSystem.out.println(10 % 3);", "1", "% gives the remainder of division."),
    J(1013, ModuleLevel.beginner, "What will this code print?\n\nint x = 5;\nif (x * 2 == 10) {\n  System.out.println(\"Correct\");\n} else {\n  System.out.println(\"Incorrect\");\n}", "Correct", "Condition is true so prints 'Correct'.", ["correct"]),
    J(1014, ModuleLevel.beginner, "What is the content of text after this code runs?\n\nString text = \"abc\";\ntext = text + \"def\";", "abcdef", "String concatenation results in 'abcdef'.", ["abc def", "abcdef"]),
    J(1015, ModuleLevel.beginner, "What does this code print?\n\npublic class Greeter {\n    public static String greet(String name) {\n        return \"Hi, \" + name;\n    }\n    public static void main(String[] args) {\n        System.out.println(greet(\"Alice\"));\n    }\n}", "Hi, Alice", "The method returns 'Hi, ' + name; printing with 'Alice'.", ["hi, alice"]),
    J(1016, ModuleLevel.beginner, "What is the output of this snippet?\n\nSystem.out.println(5 == 5.0);", "true", "int 5 promoted to double 5.0; values equal.", ["True"]),
    J(1017, ModuleLevel.beginner, "What is the size of the numbers list after this code runs?\n\nimport java.util.ArrayList;\nArrayList<Integer> numbers = new ArrayList<>();\nnumbers.add(1);\nnumbers.add(2);\nnumbers.add(3);", "3", "Three elements were added."),
    J(1018, ModuleLevel.beginner, "What will this code print?\n\nint i = 0;\nwhile (i < 3) {\n  i++;\n}\nSystem.out.println(i);", "3", "Loop increments i until it reaches 3, then prints 3."),
    J(1019, ModuleLevel.beginner, "Which keyword is used to create an instance of a class?", "new", "The 'new' keyword creates objects in Java."),
    J(1020, ModuleLevel.beginner, "What value is at myArray[1][0]?\n\nint[][] myArray = { {1, 2}, {3, 4} };", "3", "Row index 1 is {3,4}; column 0 is 3."),
]


INTERMEDIATE: List[ModuleQA] = [
    J(1021, ModuleLevel.intermediate, "What is the output of this code?\n\nString s1 = \"Hello\";\nString s2 = new String(\"Hello\");\nSystem.out.println(s1 == s2);", "false", "s1 is from string pool; s2 is a new object. == compares references.", ["False"]),
    J(1022, ModuleLevel.intermediate, "What will be printed to the console?\n\nfor (int i = 0; i < 5; i++) {\n  if (i == 3) {\n    break;\n  }\n  System.out.println(i);\n}", "0, 1, 2", "Loop prints 0 then 1 then 2; breaks at 3.", ["0 1 2", "0\n1\n2", "0,1,2"]),
    J(1023, ModuleLevel.intermediate, "What is the value of result?\n\nimport java.util.HashMap;\nHashMap<String, Integer> map = new HashMap<>();\nmap.put(\"a\", 1);\nint result = map.getOrDefault(\"b\", 0);", "0", "Key 'b' not present; getOrDefault returns 0."),
    J(1024, ModuleLevel.intermediate, "What does this code print?\n\nString text = \"Java is fun\";\nSystem.out.println(text.substring(5, 7));", "is", "substring takes [start, end) -> 5..6 -> 'is'."),
    J(1025, ModuleLevel.intermediate, "What is the output of this code?\n\nimport java.util.ArrayList;\nArrayList<String> list = new ArrayList<>();\nlist.add(\"A\");\nlist.add(\"B\");\nlist.set(0, \"C\");\nSystem.out.println(list);", "[C, B]", ".set replaces element at index 0 with 'C'."),
    J(1026, ModuleLevel.intermediate, "What will this method print?\n\npublic void checkValue(Integer val) {\n    if (val == null) {\n        System.out.println(\"Null\");\n    } else {\n        System.out.println(\"Not Null\");\n    }\n}\n// Called with: checkValue(null);", "Null", "val is null so prints 'Null'.", ["null"]),
    J(1027, ModuleLevel.intermediate, "What is printed to the console?\n\npublic class Test {\n    int x = 10;\n    public void printX() {\n        int x = 20;\n        System.out.println(x);\n    }\n    // new Test().printX() is called\n}", "20", "Local variable shadows instance field inside the method."),
    J(1028, ModuleLevel.intermediate, "What is the final content of the mySet variable?\n\nimport java.util.HashSet;\nimport java.util.Arrays;\nHashSet<Integer> mySet = new HashSet<>(Arrays.asList(1, 2, 2, 3, 4, 4, 4));", "{1, 2, 3, 4}", "Set contains unique elements only.", ["1,2,3,4", "[1, 2, 3, 4]"]),
    J(1029, ModuleLevel.intermediate, "Find the bug in this code intended to find the maximum number.\n\npublic int findMax(int[] numbers) {\n  int maxNum = 0;\n  for (int n : numbers) {\n    if (n > maxNum) {\n      maxNum = n;\n    }\n  }\n  return maxNum;\n}\n// Hint: Consider the input [-10, -5, -2]", "Initialize maxNum = numbers[0]", "Initializing to 0 fails for all-negative arrays; use first element or Integer.MIN_VALUE.", ["initialize with first element", "integer.min_value", "initialize maxnum properly"]),
    J(1030, ModuleLevel.intermediate, "What happens when you run this code?\n\nSystem.out.println(\"5\" + 5);", "55", "String concatenation: '5' + '5' -> '55'."),
    J(1031, ModuleLevel.intermediate, "What keyword is used to prevent a method from being overridden?", "final", "final methods cannot be overridden."),
    J(1032, ModuleLevel.intermediate, "What will the list.contains(\"B\") method return?\n\nimport java.util.ArrayList;\nArrayList<String> list = new ArrayList<>();\nlist.add(\"A\");\nlist.add(\"B\");\nlist.remove(\"B\");", "false", "'B' was removed so contains returns false.", ["False"]),
    J(1033, ModuleLevel.intermediate, "What keyword is used by a subclass to call a constructor of its superclass?", "super()", "super() calls the superclass constructor.", ["super"]),
    J(1034, ModuleLevel.intermediate, "What does this code print?\n\nStringBuilder sb = new StringBuilder(\"hello\");\nsb.append(\" world\");\nsb.reverse();\nSystem.out.println(sb.toString());", "dlrow olleh", "StringBuilder reversed after appending ' world'."),
    J(1035, ModuleLevel.intermediate, "What will be printed?\n\ntry {\n  int result = 10 / 0;\n} catch (ArithmeticException e) {\n  System.out.println(\"Error\");\n}", "Error", "Division by zero throws ArithmeticException, caught in catch.", ["error"]),
    J(1036, ModuleLevel.intermediate, "What is the output?\n\nSystem.out.println(\"abc\".equals(\"ABC\"));", "false", "String.equals is case-sensitive.", ["False"]),
    J(1037, ModuleLevel.intermediate, "What is the output of this code snippet?\n\nint a = 0;\nint b = a++;\nSystem.out.println(a + \",\" + b);", "1,0", "Post-increment returns old value; after line a=1,b=0.", ["1, 0", "1 0"]),
    J(1038, ModuleLevel.intermediate, "What is the purpose of the static keyword when applied to a method?", "Allows calling without an instance; belongs to the class", "Static methods are associated with the class, not instances.", ["called without instance", "class method"]),
    J(1039, ModuleLevel.intermediate, "Which class is the superclass of all other classes in Java?", "Object", "All classes ultimately extend java.lang.Object.", ["java.lang.object", "object"]),
    J(1040, ModuleLevel.intermediate, "What is the output of this code?\n\npublic class Main {\n    public Main() {\n        System.out.print(\"A\");\n    }\n    public Main(String s) {\n        this();\n        System.out.print(s);\n    }\n    // new Main(\"B\") is called\n}", "AB", "this() prints 'A' first then prints 'B'.", ["A B", "A" "B"]),
]


EXPERT: List[ModuleQA] = [
    J(1041, ModuleLevel.expert, "What will this code print?\n\nList<String> list = new ArrayList<>();\nlist.add(\"A\");\nlist.add(\"B\");\nlist.forEach(s -> {\n    if (\"B\".equals(s)) {\n        list.remove(s); // Potential issue here\n    }\n});", "ConcurrentModificationException", "Modifying a collection while iterating it triggers ConcurrentModificationException.", ["throws concurrentmodificationexception"]),
    J(1042, ModuleLevel.expert, "What is the output of this recursive method when called with factorial(4)?\n\npublic int factorial(int n) {\n  if (n == 0) {\n    return 1;\n  } else {\n    return n * factorial(n - 1);\n  }\n}", "24", "Computes 4 * 3 * 2 * 1 using recursion."),
    J(1043, ModuleLevel.expert, "What is the potential issue with this code in a multi-threaded environment?\n\npublic class Counter {\n    private int count = 0;\n    public void increment() {\n        count++;\n    }\n}", "Race condition", "count++ is not atomic; increments can be lost.", ["race-condition", "racecondition"]),
    J(1044, ModuleLevel.expert, "What does this lambda expression and Stream API code do?\n\nimport java.util.Arrays;\nList<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);\nint sum = numbers.stream()\n                 .filter(n -> n % 2 == 1)\n                 .map(n -> n * n)\n                 .reduce(0, Integer::sum);\n// What is the value of sum?", "35", "Filters odd (1,3,5), squares (1,9,25), sums to 35."),
    J(1045, ModuleLevel.expert, "What is the output of this code?\n\nString s1 = \"Test\";\nString s2 = \"Test\";\nSystem.out.println(s1 == s2);", "true", "String literals point to same pooled instance.", ["True"]),
    J(1046, ModuleLevel.expert, "Why is it important to override hashCode() when you override equals()?", "Maintain equals-hashCode contract", "Equal objects must have equal hash codes to work correctly in hash-based collections.", ["hashmap hashset contract", "equal -> same hash"]),
    J(1047, ModuleLevel.expert, "What is the output of this code snippet?\n\npublic class Parent {\n    public void display() { System.out.println(\"Parent\"); }\n}\npublic class Child extends Parent {\n    @Override\n    public void display() { System.out.println(\"Child\"); }\n}\n// Parent p = new Child();\n// p.display(); is called", "Child", "Dynamic dispatch chooses Child.display()."),
    J(1048, ModuleLevel.expert, "What is a Singleton design pattern?", "One instance globally accessible", "Ensures a class has only one instance and provides a global point of access.", ["single instance", "single object globally accessible"]),
    J(1049, ModuleLevel.expert, "What is the difference between final, finally, and finalize?", "final=const/non-override/non-inherit; finally=always runs; finalize=GC hook (discouraged)", "final for constants/method/class; finally executes regardless; finalize called before GC (legacy)."),
    J(1050, ModuleLevel.expert, "What does this code print?\n\nSet<String> set = new HashSet<>();\nset.add(\"A\");\nset.add(\"B\");\nset.add(\"A\");\nSystem.out.println(set.size());", "2", "Sets keep unique elements; duplicate 'A' ignored."),
    J(1051, ModuleLevel.expert, "What is the output of this code?\n\npublic class Test {\n    static { System.out.print(\"A\"); }\n    public Test() { System.out.print(\"B\"); }\n    public static void main(String[] args) {\n        new Test();\n        new Test();\n    }\n}", "ABB", "Static block runs once printing 'A'; constructor prints 'B' twice.", ["AB B", "A B B"]),
    J(1052, ModuleLevel.expert, "What is the difference between an interface and an abstract class?", "Interface: only abstract/default/static; Abstract class: mix of abstract/concrete. Multiple interfaces; single abstract superclass", "Interfaces declare contracts; abstract classes can hold state and concrete methods.", ["interface vs abstract class"]),
    J(1053, ModuleLevel.expert, "What will this code print?\n\nString str = \"a,b,c\";\nString[] parts = str.split(\",\", 2);\nSystem.out.println(parts.length);", "2", "Split with limit=2 results in at most 2 parts."),
    J(1054, ModuleLevel.expert, "What is the problem with this code?\n\ndouble price = 0.1 + 0.2;\n// System.out.println(price == 0.3); will be false", "Floating-point precision errors", "Binary floats cannot exactly represent some decimals; use BigDecimal.", ["floating point precision", "precision error"]),
    J(1055, ModuleLevel.expert, "What will the following code print?\n\nInteger a = 128;\nInteger b = 128;\nSystem.out.println(a == b);", "false", "Integer cache covers -128..127; 128 creates distinct objects.", ["False"]),
    J(1056, ModuleLevel.expert, "What is the output of this finally block example?\n\npublic int testFinally() {\n    try {\n        return 1;\n    } finally {\n        return 2;\n    }\n}", "2", "Return in finally overrides try/catch return."),
    J(1057, ModuleLevel.expert, "What is the purpose of the volatile keyword?", "Ensures visibility across threads; happens-before", "Writes to a volatile variable are visible to other threads and establish happens-before.", ["visibility", "happens-before"]),
    J(1058, ModuleLevel.expert, "What is printed by this code snippet?\n\nMap<String, String> map = new HashMap<>();\nmap.put(\"key\", \"value\");\nmap.put(\"key\", \"newValue\");\nSystem.out.println(map.get(\"key\"));", "newValue", "Putting the same key replaces the previous value."),
    J(1059, ModuleLevel.expert, "What is method overloading vs. method overriding?", "Overloading: same name, diff params; Overriding: subclass replaces superclass method", "Overloading varies signature in same class; overriding provides new implementation in subclass."),
    J(1060, ModuleLevel.expert, "What does (0b101 ^ 0b110) evaluate to in decimal?\n\n// 0b101 is 5 in decimal\n// 0b110 is 6 in decimal", "3", "Bitwise XOR: 101 ^ 110 = 011 (3)."),
]


def get_questions(level: ModuleLevel) -> List[ModuleQA]:
    if level == ModuleLevel.beginner:
        return list(BEGINNER)
    if level == ModuleLevel.intermediate:
        return list(INTERMEDIATE)
    if level == ModuleLevel.expert:
        return list(EXPERT)
    return []
