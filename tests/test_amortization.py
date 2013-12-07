from pymortgage.amortization import Amortization_Schedule

schedule = Amortization_Schedule.create_schedule(.05, 250000, 360)


def check_value(month, key, expected):
    actual = schedule[month-1][key]
    if actual == expected: 
        print "Pass."
    else: 
        print "Fail. Expected: %s, but got: %s." % (expected, actual)

# check first month
print "Checking first month..."
check_value(1, 'month', 1)
check_value(1, 'principal', 300.39)
check_value(1, 'interest', 1041.67)
check_value(1, 'amount', 1342.05)
check_value(1, 'balance', 249699.61)

# check fifth month
print "Checking fifth month..."
check_value(5, 'month', 5)
check_value(5, 'principal', 305.43)
check_value(5, 'interest', 1036.63)
check_value(5, 'balance', 248485.49)

# check last month
print "Checking last month..."
check_value(360, 'month', 360)
check_value(360, 'principal', 1336.49)
check_value(360, 'interest', 5.57)
check_value(360, 'balance', 0)
