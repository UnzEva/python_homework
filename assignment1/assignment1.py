# Task 1: Hello
#-------------------------------------------------------------------
def hello():
    return "Hello!"

hello()

#Task 2: Greet with a Formatted String
#-------------------------------------------------------------------
def greet(name):
    return f"Hello, {name}!"

greet("Anna")

#Task 3: Calculator
#-------------------------------------------------------------------
def calc(a, b, operation="multiply"):
    try:
        if operation == "add":
            return a + b
        elif operation == "subtract":
            return a - b
        elif operation == "multiply":
            return a * b
        elif operation == "divide":
            return a / b
        elif operation == "modulo":
            return a % b
        elif operation == "int_divide":
            return a // b
        elif operation == "power":
            return a ** b
        else:
            return "Invalid operation"
    except ZeroDivisionError:
        return "You can't divide by 0!"
    except TypeError:
        return f"You can't {operation} those values!"

calc(10, 4, "divide")

#Task 4: Data Type Conversion
#-------------------------------------------------------------------
def data_type_conversion(value, target_type):
    try:
        if target_type == "float":
            return float(value)
        elif target_type == "int":
            return int(value)
        elif target_type == "str":
            return str(value)
        else:
            return f"Invalid target type: {target_type}"
    except (ValueError, TypeError):
        return f"You can't convert {value} into a {target_type}."

data_type_conversion(10, "str")

#Task 5: Grading System, Using *args
#-------------------------------------------------------------------
def grade(*args):
    try:
        average = sum(args) / len(args)
        if average >= 90:
            return "A"
        elif average >= 80:
            return "B"
        elif average >= 70:
            return "C"
        elif average >= 60:
            return "D"
        else:
            return "F"
    except (ZeroDivisionError, TypeError):
        return "Invalid data was provided."

grade(100, 90, 80)

#Task 6: Use a For Loop with a Range
#-------------------------------------------------------------------
def repeat(string, count):
    result = ""
    for i in range(count):
        result += string
    return result

repeat("Hello", 3)

#Task 7: Student Scores, Using **kwargs
#-------------------------------------------------------------------
def student_scores(operation, **kwargs):
    if not kwargs:
        return "No student data provided."
    if operation == "best":
        best_student = None
        best_score = -1
        for student, score in kwargs.items():
            if score > best_score:
                best_student = student
                best_score = score
        return best_student
    elif operation == "mean":
        return sum(kwargs.values()) / len(kwargs)
    else:
        return "Invalid operation."

student_scores("best", Anna=60, Max=80, Christine=70)

#Task 8: Titleize, with String and List Operations
#-------------------------------------------------------------------
def titleize(text):
    if not text:
        return ""
    little_words = {"a", "an", "the", "on", "of", "and", "is", "in"}
    words = text.split()
    for i, word in enumerate(words):              #first and last words
        if i == 0 or i == len(words) - 1:
            words[i] = word.capitalize()
        elif word.lower() not in little_words:
            words[i] = word.capitalize()
        else:
            words[i] = word.lower()
    return " ".join(words)

titleize("this is a title")

#Task 9: Hangman, with more String Operations
#-------------------------------------------------------------------
def hangman(secret, guess):
    result = ""
    for letter in secret:
        if letter in guess:
            result += letter
        else:
            result += "_"
    return result

hangman("alphabet", "ab")

#Task 10: Pig Latin, Another String Manipulation Exercise
#-------------------------------------------------------------------
def pig_latin(text):
    vowels = ['a', 'e', 'i', 'o', 'u']
    result = []

    words = []                    #splitting text into words
    word = ''
    i = 0
    while i < len(text):
        if text[i] != ' ':
            word = word + text[i]
        else:
            words.append(word)
            word = ''
        i = i + 1
    words.append(word)            #last word

    for w in words:               #processing each word
        if w == '':
            continue

        first_char = w[0]

        is_vowel = False          #if it starts with a vowel
        for v in vowels:
            if first_char == v:
                is_vowel = True
        if is_vowel:
            result.append(w + 'ay')
        else:
            consonants = ''       #processing of initial consonants and "qu"
            j = 0
            while j < len(w):
                if j + 1 < len(w) and w[j] == 'q' and w[j+1] == 'u':
                    consonants = consonants + 'qu'
                    j = j + 2
                    break
                else:
                    is_consonant = True
                    for v in vowels:
                        if w[j] == v:
                            is_consonant = False
                    if is_consonant:
                        consonants = consonants + w[j]
                        j = j + 1
                    else:
                        break
            rest = ''
            while j < len(w):
                rest = rest + w[j]
                j = j + 1
            result.append(rest + consonants + 'ay')

    final = ''                    #finalizing the result
    i = 0
    while i < len(result):
        final = final + result[i]
        if i < len(result) - 1:
            final = final + ' '
        i = i + 1

    return final

pig_latin("quick brown fox")
