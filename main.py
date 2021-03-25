print("Welcome to the SBU Physics 133 Uncertainty Tool")
print()
print("Enter the equation or range of equations you calculated. One Equation should be entered as 'A4*B2'. Ranges of equations should be entered as '[A|D]3+B[1|4]' Only one range is allowed per term. Only use one letter per term aswell ie. no cell AA3.")

char_to_int = {}
chars = 'abcdefghijklmnopqrytuvwxyz'
for i in range(len(chars)):
    char_to_int[chars[i]] = i

int_to_char = {v: k for k, v in char_to_int.items()}

while True:

    cmd = input(">").lower()

    eq = []
    sign = ""

    if '+' in cmd:
        sign = "+"
        eq = cmd.split('+')

    elif '-' in cmd:
        sign = "-"
        eq = cmd.split('-')

    elif '*' in cmd:
        sign = "*"
        eq = cmd.split('*')

    elif '/' in cmd:
        sign = "/"
        eq = cmd.split('/')

    elif '^' in cmd:
        #add this later
        pass

    if eq == []:
        print("Invalid input.")
        break

    directions = ["",""]

    for i in range(2):
        if eq[i][0] == '[':
            directions[i] = "horizontal"
            eq[i] = eq[i].split(']')
            eq[i][0] = eq[i][0][1:].split('|')
        elif '[' in eq[i]:
            directions[i] = "vertical"
            eq[i] = eq[i].split("[")
            eq[i][1] = eq[i][1][:-1].split('|')
        else:
            directions[i] = "constant"
            eq[i] = [eq[i][0],eq[i][1]]
            print("Where is the uncertainty cell for %s?" % (eq[i][0]+eq[i][1]))
            print("[1] Below %s" % (eq[i][0]+eq[i][1]))
            print("[2] To the right of %s" % (eq[i][0]+eq[i][1]))
            cmd = input('>')
            if cmd == '1':
                constant_direction = "vertical"
            else:
                constant_direction = "horizontal"

    uncertainties = [{},{}]

    for i in range(2):
        if directions[i] == "horizontal":
            for j in range(char_to_int[eq[i][0][0]], char_to_int[eq[i][0][1]] + 1):
                uncertainties[i][(int_to_char[j] + eq[i][1])] = int_to_char[j]+str(int(eq[i][1]) + 1)
        elif directions[i] == "vertical":
            for j in range(int(eq[i][1][0]), int(eq[i][1][1]) + 1):
                uncertainties[i][eq[i][0] + str(j)] = int_to_char[char_to_int[eq[i][0]] + 1] + str(j)
        else:
            if constant_direction == "vertical":
                uncertainties[i][eq[i][0] + eq[i][1]] = eq[i][0] + str(int(eq[i][1]) + 1)
            else:
                uncertainties[i][eq[i][0] + eq[i][1]] = int_to_char[char_to_int[eq[i][0]] + 1] + eq[i][1]

    if sign == "+" or sign == "-":
        for x in uncertainties[0]:
            for y in uncertainties[1]:
                print("= sqrt(%s^2 %s %s^2)" % (uncertainties[0][x], sign, uncertainties[1][y]))
    elif sign == "*" or sign == "/":
        for x in uncertainties[0]:
            for y in uncertainties[1]:
                print("= abs(%s %s %s) * sqrt( (%s/%s)^2  + (%s/%s)^2 )" % (x, sign, y, uncertainties[0][x], x, uncertainties[1][y], y))