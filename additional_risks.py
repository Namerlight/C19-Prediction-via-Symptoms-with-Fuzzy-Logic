def calc_additional_risks(age, env_inp, hypertension_inp, diabetes_inp, cardiovascular_inp, respiratory_inp, immune_inp):

    # print("Enter 0 for 'No' and 1 for 'Yes'")
    # age, env_inp, hypertension_inp, diabetes_inp, cardiovascular_inp, respiratory_inp, immune_inp, = \
    #     int(input("Age: ")), (input("Polluted Env? ")), (input("Hypertension? ")), (input("Diabetes? ")), \
    #     (input("Cardiovascular issues? ")), (input("Respiratory issues? ")), (input("Immunological issues? "))

    if env_inp == '1': env = True
    else: env = False
    if hypertension_inp == '1': hypertension = True
    else: hypertension = False
    if diabetes_inp == '1': diabetes = True
    else: diabetes = False
    if cardiovascular_inp == '1': cardiovascular = True
    else: cardiovascular = False
    if respiratory_inp == '1': respiratory = True
    else: respiratory = False
    if immune_inp == '1': immune = True
    else: immune = False

    print(age, env, hypertension, diabetes, cardiovascular, respiratory, immune, )

    rm = 0.0

    if age <= 10: rm += 0.5
    elif age >= 80: rm += 1.5
    elif age >= 60: rm += 1
    elif age >= 50: rm += 0.5

    if env: rm += 1
    if hypertension: rm += 1.5
    if diabetes: rm += 1.5
    if cardiovascular: rm += 1
    if respiratory: rm += 3
    if immune: rm += 4

    if rm > 10: rm = 10

    return rm
