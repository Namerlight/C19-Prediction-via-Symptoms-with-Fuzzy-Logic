from pyit2fls import IT2FS, trapezoid_mf, tri_mf, IT2FS_Gaussian_UncertMean, \
    IT2FS_plot, IT2FLS, min_t_norm, max_s_norm, TR_plot, crisp
from numpy import linspace
from additional_risks import calc_additional_risks


class PredictC19FLS:

    def __init__(self, cough_inp, fever_inp, breath_inp, age, env_inp, hypertension_inp, diabetes_inp,
                 cardiovascular_inp,
                 respiratory_inp, immune_inp):
        """
        Takes inputs into the class and also generates the parameters for our FLS.

        Args:
            cough_inp (float): input value for Coughing
            fever_inp (float): input value for Fever
            breath_inp (float) : input value for Breathing Difficulty
            age (int): input value for age
            env_inp (bool): Status of patient's environment
            hypertension_inp (bool): Status of existing hypertension
            diabetes_inp (bool): Status of existing diabetes
            cardiovascular_inp (bool): Status of existing heart problems
            respiratory_inp (bool): Status of existing lung problems
            immune_inp (bool): Status of patient's immune system
        """

        # Initialize the IT2FLS class from the library.
        self.myIT2FLS = IT2FLS()

        # Initialize input variables
        self.cough_inp = cough_inp
        self.fever_inp = fever_inp
        self.breath_inp = breath_inp
        self.age = age
        self.env_inp = env_inp
        self.hypertension_inp = hypertension_inp
        self.diabetes_inp = diabetes_inp
        self.cardiovascular_inp = cardiovascular_inp
        self.respiratory_inp = respiratory_inp
        self.immune_inp = immune_inp

        # Initializing linespace. Using 0.0 to 10.0 with 100 intervals in between for simplicity.
        self.severity = linspace(0.0, 10.0, 100)

        # For IT2FS_Gaussian_UncertMean, the parameters define:
        # 1 - The tip of the center point of the curve
        # 2 - The width of the lower curve (higher value = lower width)
        # 3 - The height of the lower curve (higher value = higher tip)
        # 4 - The height of the center point of the outer curve.

        # Set Parameters for Cough
        self.cough_neg = IT2FS(self.severity, trapezoid_mf, [0., 0.001, 3, 7, 1.0],
                               tri_mf, [0, 0.001, 2, 0.5])
        self.cough_pos = IT2FS(self.severity, trapezoid_mf, [5, 8, 9.999, 10, 1.0],
                               tri_mf, [8.5, 9.999, 10, 0.5])

        # Set Parameters for Fever
        self.fever_low = IT2FS_Gaussian_UncertMean(self.severity, [0, 2.65, 1, 1.0])
        self.fever_mod = IT2FS_Gaussian_UncertMean(self.severity, [5, 2.65, 1, 1.0])
        self.fever_high = IT2FS_Gaussian_UncertMean(self.severity, [10, 2.65, 1, 1.0])

        # Set Parameters for Breathing Difficulty
        self.breath_diff_low = IT2FS_Gaussian_UncertMean(self.severity, [0, 1.75, 1, 1.0])
        self.breath_diff_mod = IT2FS_Gaussian_UncertMean(self.severity, [5, 2.5, 1, 1.0])
        self.breath_diff_extr = IT2FS_Gaussian_UncertMean(self.severity, [10, 1.75, 1, 1.0])

        # Set Parameters for Additional Risks
        self.add_low = IT2FS_Gaussian_UncertMean(self.severity, [0, 5, 2, 1.0])
        self.add_high = IT2FS_Gaussian_UncertMean(self.severity, [10, 5, 2, 1.0])

        # Set Parameters for Overall Risk
        self.risk_low = IT2FS_Gaussian_UncertMean(self.severity, [0, 3, 1, 1.0])
        self.risk_high = IT2FS_Gaussian_UncertMean(self.severity, [6.5, 2, 1, 1.0])
        self.risk_veryhigh = IT2FS_Gaussian_UncertMean(self.severity, [10.7, 1, 1, 1.0])

    def plot_fuzzy_curves(self, curve_name, *args):
        """
            Plots the fuzzy curve for the given symptom.

        Args:
            curve_name (str): name of the symptom
            args (IT2FS_Gaussian_UncertMean): Fuzzy Curve objects. Pass as many of these as needed according to the
                                                parameters initialized. Expected 2 or 3 curves.

        """

        # Set legends according to the input. Bit clumsy.
        if curve_name == "Cough":
            legends_list = ["Negative", "Positive"]
        elif curve_name == "Fever" or curve_name == "Breath Difficulty":
            legends_list = ["Low", "Moderate", "High"]
        elif curve_name == "Additional Risks":
            legends_list = ["Low", "High"]
        elif curve_name == "Risk":
            legends_list = ["Low", "High", "Very High"]
        else:
            legends_list = [str(i) for i in range(len(args))]

        # Plot Curve
        IT2FS_plot(
            *args,
            title=curve_name,
            legends=legends_list,
        )

    def set_rules(self):
        """
            Sets the rules for the FLS. Modify this function to test your own rules.
        """

        # Add each input we need.
        self.myIT2FLS.add_input_variable("cough")
        self.myIT2FLS.add_input_variable("fever")
        self.myIT2FLS.add_input_variable("breath")
        self.myIT2FLS.add_input_variable("add")
        self.myIT2FLS.add_output_variable("risk")

        # Adding Rules one by one. Bit clumsy.
        self.myIT2FLS.add_rule([("cough", self.cough_neg), ("fever", self.fever_low), ("breath", self.breath_diff_low),
                                ("add", self.add_low)],
                               [("risk", self.risk_low)])
        self.myIT2FLS.add_rule([("cough", self.cough_pos), ("fever", self.fever_mod), ("breath", self.breath_diff_low),
                                ("add", self.add_low)],
                               [("risk", self.risk_low)])
        self.myIT2FLS.add_rule([("cough", self.cough_neg), ("fever", self.fever_high), ("breath", self.breath_diff_low),
                                ("add", self.add_low)],
                               [("risk", self.risk_low)])
        self.myIT2FLS.add_rule([("cough", self.cough_neg), ("fever", self.fever_high), ("breath", self.breath_diff_low),
                                ("add", self.add_high)],
                               [("risk", self.risk_low)])
        self.myIT2FLS.add_rule([("cough", self.cough_neg), ("fever", self.fever_mod), ("breath", self.breath_diff_extr),
                                ("add", self.add_low)],
                               [("risk", self.risk_high)])
        self.myIT2FLS.add_rule([("cough", self.cough_neg), ("fever", self.fever_high), ("breath", self.breath_diff_mod),
                                ("add", self.add_low)],
                               [("risk", self.risk_high)])
        self.myIT2FLS.add_rule([("cough", self.cough_pos), ("fever", self.fever_mod), ("breath", self.breath_diff_mod),
                                ("add", self.add_high)],
                               [("risk", self.risk_veryhigh)])
        self.myIT2FLS.add_rule([("cough", self.cough_pos), ("fever", self.fever_mod), ("breath", self.breath_diff_extr),
                                ("add", self.add_high)],
                               [("risk", self.risk_veryhigh)])
        self.myIT2FLS.add_rule([("cough", self.cough_pos), ("fever", self.fever_mod), ("breath", self.breath_diff_mod),
                                ("add", self.add_high)],
                               [("risk", self.risk_veryhigh)])
        self.myIT2FLS.add_rule([("cough", self.cough_pos), ("fever", self.fever_high), ("breath", self.breath_diff_extr),
                                ("add", self.add_high)],
                               [("risk", self.risk_veryhigh)])

    def calculate_probability(self):
        """
            Calculates the probability of an C19 infection based on the rules and inputs.

        Return:
             probability (int): probability of a C19 infection based on visible symptoms
        """

        # Converts additional risks into a single input.
        add_inp = calc_additional_risks(self.age, self.env_inp, self.hypertension_inp, self.diabetes_inp,
                                        self.cardiovascular_inp, self.respiratory_inp,
                                        self.immune_inp)

        # Plots individual fuzzy curves. Comment out if not necessary.
        self.plot_fuzzy_curves("Cough", self.cough_neg, self.cough_pos)
        self.plot_fuzzy_curves("Fever", self.fever_low, self.fever_mod, self.fever_high)
        self.plot_fuzzy_curves("Breath Difficulty", self.breath_diff_low, self.breath_diff_mod, self.breath_diff_extr)
        self.plot_fuzzy_curves("Additional Risks", self.add_low, self.add_high)
        self.plot_fuzzy_curves("Risk", self.risk_low, self.risk_high, self.risk_veryhigh)

        # Evaluates and outputs the results of the Fuzzy Curve
        it2out, tr = self.myIT2FLS.evaluate(
            {"cough": self.cough_inp, "fever": self.fever_inp, "breath": self.breath_inp, "add": add_inp},
            min_t_norm, max_s_norm, self.severity,
            method="Centroid", algorithm="EKM")
        print(tr)
        print(it2out)

        # Plots output curve after evaluation
        it2out["risk"].plot(title="Type-2 output MF converted to Type-1")
        TR_plot(self.severity, tr["risk"])

        # Extract the final computed result for probability
        probability = int((crisp(tr["risk"])) * 10)
        print("Chance of C19 Infection: ", str(probability) + "%")

        return probability
