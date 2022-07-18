def calc_additional_risks(age, env_inp, hypertension_inp, diabetes_inp, cardiovascular_inp, respiratory_inp, immune_inp):
    """
    Calculates additional risks and returns the answer as a score that can be fed into the FLS

    I originally threw this function together in 1.5 minutes.

    Args:
        age (int):
        env_inp (int):
        hypertension_inp (int):
        diabetes_inp (int):
        cardiovascular_inp (int):
        respiratory_inp (int):
        immune_inp:

    Returns:
        risk_score (float): how much other factors contribute to C19 risk.
    """

    # Converting from int input to bool. Don't ask me why I'm doing this.
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

    # Intialize risk score at 0. Laziest approach ever.
    risk_score = 0.0

    # Using If functions for everything like a true pro.
    if age <= 10: risk_score += 0.5
    elif age >= 80: risk_score += 1.5
    elif age >= 60: risk_score += 1
    elif age >= 50: risk_score += 0.5

    if env: risk_score += 1
    if hypertension: risk_score += 1.5
    if diabetes: risk_score += 1.5
    if cardiovascular: risk_score += 1
    if respiratory: risk_score += 3
    if immune: risk_score += 4

    if risk_score > 10: risk_score = 10

    return risk_score
