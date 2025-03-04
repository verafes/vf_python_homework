# Write your code here.
def hello():
    return "Hello!"

print("hello: ", hello())

def greet(name):
    return f"Hello, {name}!"

print("greet: ", greet("Fred"))

def calc(v1, v2, op="multiply"):
    try:
        match op:
            case "multiply":
                return v1 * v2
            case "add":
                return v1 + v2
            case "subtract":
                return v1 - v2
            case "divide":
                return v1 / v2
            case "power":
                return v1 ** v2
            case "modulo":
                return v1 % v2
            case "int_divide":
                return v1 // v2
            case _:
                return "unsupported operation"
    except ZeroDivisionError:
        return "You can't divide by 0!"
    except TypeError:
        return f"You can't {op} those values!"
    
print("calc: ", calc(7,8,"add"))

def data_type_conversion(value, type_name):
    try:
        match type_name:
            case "int":
                return int(value)
            case "float":
                return float(value)
            case "str":
                return str(value)
    except ValueError:
        return f"You can't convert {value} into a {type_name}."
    
print("data_type_conversion: ", data_type_conversion(5.23, "int"))

def grade(*args):
    try:
        avg = sum(args) / len(args)
        if avg >= 90:
            return "A"
        elif avg >= 80:
            return "B"
        elif avg >= 70:
            return "C"
        elif avg >= 60:
            return "D"
        else:
            return "F"
    except TypeError:
        return "Invalid data was provided."
    
print("grade: ", grade(90,79, 95, 80))
    
def repeat(string, count):
    out_string = string
    for i in range(1,count):
        out_string += string
    return out_string

print("repeat: ", repeat("good ",3))

def student_scores(operation, **kwargs):
    if operation == "best":
        best_value = 0
        for key, value in kwargs.items():
            if value > best_value:
                best_name = key
                best_value = value
        return best_name
    else:
        return sum(kwargs.values()) / len(kwargs.values())
    
print("student_scores: ", student_scores("best", Bob=70, Susan=90))
    
def titleize(title):
    title_list = title.split()
    little_words = ["a", "on", "an", "the", "of", "and", "is", "in"]
    for i, word in enumerate(title_list):
        if word not in little_words:
            title_list[i] = word.capitalize()
    title_list[0] = title_list[0].capitalize()
    title_list[-1] = title_list[-1].capitalize()
    return " ".join(title_list)

print("titleize: ", titleize("dancing at the rascal fair"))

def hangman(secret, guess):
    report = ""
    for c in secret:
        if c in guess:
            report += c
        else:
            report += "_"
    return report

print("hangman: ", hangman("obscurely", "bur"))

def pig_latin(s):
    vowels = "aeiouAEIOU"
    out_string = ""
    start_string = ""
    rest_string = ""
    for ch in s:
        if (ch == " "):
            if (rest_string):
                if len(out_string) > 0:
                    out_string += " "
                out_string += rest_string + start_string + "ay"
                rest_string = ""
                start_string = ""
        elif len(rest_string) > 0:
            rest_string += ch
        elif (ch == "u" or ch == "U") and len(start_string) > 0 and \
            (start_string[-1] == "q" or start_string[-1] == "Q"):
            start_string += ch
        elif ch in vowels:
            rest_string += ch
        elif len(rest_string) > 0:
            rest_string += ch
        else:
            start_string += ch
    if len(rest_string) > 0:
        if len(out_string) > 0:
            out_string += " "
        out_string += rest_string + start_string + "ay"
    return out_string

print("pig_latin: ", pig_latin("it is forbidden to spit on cats"))
