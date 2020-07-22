from pyit2fls import IT2FS, trapezoid_mf, tri_mf, IT2FS_Gaussian_UncertMean, \
    IT2FS_plot, IT2FLS, min_t_norm, max_s_norm, TR_plot, crisp
from numpy import linspace
from additional_risks import calc_additional_risks


def calculate_FLS(cough_inp, fever_inp, breath_inp, age, env_inp, hypertension_inp, diabetes_inp, cardiovascular_inp,
                  respiratory_inp, immune_inp):
    severity = linspace(0.0, 10.0, 100)

    # For IT2FS_Gaussian_UncertMean, the parameters define:
    # 1 - The tip of the center point of the curve
    # 2 - The width of the lower curve (higher value = lower width)
    # 3 - The height of the lower curve (higher value = higher tip)
    # 4 - The height of the center point of the outer curve.

    Cough_neg = IT2FS(severity, trapezoid_mf, [0., 0.001, 3, 7, 1.0],
                      tri_mf, [0, 0.001, 2, 0.5])
    Cough_pos = IT2FS(severity, trapezoid_mf, [5, 8, 9.999, 10, 1.0],
                      tri_mf, [8.5, 9.999, 10, 0.5])

    Fever_low = IT2FS_Gaussian_UncertMean(severity, [0, 2.65, 1, 1.0])
    Fever_mod = IT2FS_Gaussian_UncertMean(severity, [5, 2.65, 1, 1.0])
    Fever_high = IT2FS_Gaussian_UncertMean(severity, [10, 2.65, 1, 1.0])

    BreathDiff_low = IT2FS_Gaussian_UncertMean(severity, [0, 1.75, 1, 1.0])
    BreathDiff_mod = IT2FS_Gaussian_UncertMean(severity, [5, 2.5, 1, 1.0])
    BreathDiff_extr = IT2FS_Gaussian_UncertMean(severity, [10, 1.75, 1, 1.0])

    Add_low = IT2FS_Gaussian_UncertMean(severity, [0, 5, 2, 1.0])
    Add_high = IT2FS_Gaussian_UncertMean(severity, [10, 5, 2, 1.0])

    Risk_low = IT2FS_Gaussian_UncertMean(severity, [0, 3, 1, 1.0])
    Risk_high = IT2FS_Gaussian_UncertMean(severity, [6.5, 2, 1, 1.0])
    Risk_veryhigh = IT2FS_Gaussian_UncertMean(severity, [10.7, 1, 1, 1.0])

    def plot_cough_mf():
        IT2FS_plot(Cough_neg, Cough_pos,
                   title="Cough",
                   legends=["Negative", "Positive"],
                   )

    def plot_fever_mf():
        IT2FS_plot(Fever_low, Fever_mod, Fever_high,
                   title="Fever",
                   legends=["Low", "Moderate", "High"],
                   )

    def plot_additional_mf():
        IT2FS_plot(Add_low, Add_high,
                   title="Additional Risks",
                   legends=["Low", "High"],
                   )

    def plot_breathdiff_mf():
        IT2FS_plot(BreathDiff_low, BreathDiff_mod, BreathDiff_extr,
                   title="Breathing Difficulty",
                   legends=["Low", "Moderate", "High"],
                   )

    def plot_risk_mf():
        IT2FS_plot(Risk_low, Risk_high, Risk_veryhigh,
                   title="Overall Risk",
                   legends=["Unlikely", "Likely", "Extremely Likely"],
                   )

    plot_fever_mf()
    plot_cough_mf()
    plot_breathdiff_mf()
    plot_additional_mf()

    plot_risk_mf()

    myIT2FLS = IT2FLS()

    myIT2FLS.add_input_variable("cough")
    myIT2FLS.add_input_variable("fever")
    myIT2FLS.add_input_variable("breath")
    myIT2FLS.add_input_variable("add")
    myIT2FLS.add_output_variable("risk")

    myIT2FLS.add_rule([("cough", Cough_neg), ("fever", Fever_low), ("breath", BreathDiff_low), ("add", Add_low)],
                      [("risk", Risk_low)])
    myIT2FLS.add_rule([("cough", Cough_pos), ("fever", Fever_mod), ("breath", BreathDiff_low), ("add", Add_low)],
                      [("risk", Risk_low)])
    myIT2FLS.add_rule([("cough", Cough_neg), ("fever", Fever_high), ("breath", BreathDiff_low), ("add", Add_low)],
                      [("risk", Risk_low)])
    myIT2FLS.add_rule([("cough", Cough_neg), ("fever", Fever_high), ("breath", BreathDiff_low), ("add", Add_high)],
                      [("risk", Risk_low)])
    myIT2FLS.add_rule([("cough", Cough_neg), ("fever", Fever_low), ("breath", BreathDiff_extr), ("add", Add_low)],
                      [("risk", Risk_high)])
    myIT2FLS.add_rule([("cough", Cough_neg), ("fever", Fever_high), ("breath", BreathDiff_mod), ("add", Add_low)],
                      [("risk", Risk_high)])
    myIT2FLS.add_rule([("cough", Cough_pos), ("fever", Fever_mod), ("breath", BreathDiff_mod), ("add", Add_high)],
                      [("risk", Risk_veryhigh)])
    myIT2FLS.add_rule([("cough", Cough_pos), ("fever", Fever_low), ("breath", BreathDiff_extr), ("add", Add_high)],
                      [("risk", Risk_veryhigh)])
    myIT2FLS.add_rule([("cough", Cough_pos), ("fever", Fever_mod), ("breath", BreathDiff_mod), ("add", Add_high)],
                      [("risk", Risk_veryhigh)])
    myIT2FLS.add_rule([("cough", Cough_pos), ("fever", Fever_high), ("breath", BreathDiff_extr), ("add", Add_high)],
                      [("risk", Risk_veryhigh)])

    # cough_inp = float(input("Enter severity of coughing, between 0 and 10: "))
    # fever_inp = float(input("Enter severity of fever, between 0 and 10: "))
    # breath_inp = float(input("Enter severity of breathing difficulty, between 0 and 10: "))
    # print("Input age and other additional risk factors.")
    add_inp = calc_additional_risks(age, env_inp, hypertension_inp, diabetes_inp, cardiovascular_inp, respiratory_inp,
                                    immune_inp)

    it2out, tr = myIT2FLS.evaluate({"cough": cough_inp, "fever": fever_inp, "breath": breath_inp, "add": add_inp},
                                   min_t_norm, max_s_norm, severity,
                                   method="Centroid", algorithm="EKM")
    print(tr)
    print(it2out)

    it2out["risk"].plot(title="Type-2 output MF converted to Type-1")
    TR_plot(severity, tr["risk"])
    print("Chance of C19 Infection: ", int((crisp(tr["risk"])) * 10), "%")

    return int((crisp(tr["risk"])) * 10)

# print(calculate_FLS(), "%")
