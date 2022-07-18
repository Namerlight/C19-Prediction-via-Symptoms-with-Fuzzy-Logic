import pandas as pd
import matplotlib.pyplot as plt


def plot_chart(symptom, symptom_name):
    """
    Plots and displays a bar chart for a given symptom.

    Args:
        symptom (int): input symptom for which to draw the graph.
        symptom_name (str): name of the symptom
    """
    plt.bar(["Positive", "Negative"], [symptom, total_count - symptom], width=.6)
    plt.xlabel(symptom_name)
    plt.ylabel('Number of Reports')
    plt.title('Reported Positives and Negatives for ' + symptom_name)
    plt.show()
    print(symptom_name + " - Positive:", symptom * 100 / total_count, "%,",
          "Negative", (total_count - symptom) * 100 / total_count, "%")


# Load Data from Datasets.
dataset1 = pd.read_csv(r'data/WolframPatients.csv')
dataset2 = pd.read_csv(r'data/NovelDataset.csv')

# Check if the tuple has any symptoms listed. If not, discard those tuples.
has_symptoms1 = dataset1[dataset1.Symptoms.notnull()]
has_symptoms2 = dataset2[dataset2.Symptoms.notnull()]

# Extract a list of the symptoms given in the two datasets and combine them.
sympt_list_1 = pd.DataFrame(has_symptoms1, columns=['Symptoms'])
sympt_list_2 = pd.DataFrame(has_symptoms2, columns=['Symptoms'])
symptoms = pd.concat([sympt_list_1, sympt_list_2], ignore_index=True, sort=False)

# Print list of symptoms
# print(symptoms)

# Count the total number of entries.
total_count = len(symptoms.axes[0])

# Count each symptom by their frequency.
# We are combining several different terms, such as "sore" and "ache", where appropriate.
cough_count = len(symptoms[symptoms['Symptoms'].str.contains("cough")].axes[0])
fever_count = len(symptoms[symptoms['Symptoms'].str.contains("fever")].axes[0])
pain_count = len(symptoms[symptoms['Symptoms'].str.contains("sore")].axes[0]) + \
             len(symptoms[symptoms['Symptoms'].str.contains("myalgias")].axes[0]) + \
             len(symptoms[symptoms['Symptoms'].str.contains("ache")].axes[0])
breath_count = len(symptoms[symptoms['Symptoms'].str.contains("breath")].axes[0]) + \
               len(symptoms[symptoms['Symptoms'].str.contains("pneumo")].axes[0]) + \
               len(symptoms[symptoms['Symptoms'].str.contains("phary")].axes[0]) + \
               len(symptoms[symptoms['Symptoms'].str.contains("gasp")].axes[0])
other_count = len(symptoms[symptoms['Symptoms'].str.contains("diarrhea")].axes[0]) + \
              len(symptoms[symptoms['Symptoms'].str.contains("energy")].axes[0]) + \
              len(symptoms[symptoms['Symptoms'].str.contains("fatigue")].axes[0]) + \
              len(symptoms[symptoms['Symptoms'].str.contains("weakness")].axes[0])

# Print counted list of symptoms.
# print(cough_count, fever_count, breath_count, pain_count, other_count)

# Plot Chart for all counts.
plot_chart(cough_count, "Cough")
plot_chart(fever_count, "Fever")
plot_chart(pain_count, "Pain")
plot_chart(breath_count, "Breathing Difficulty")
plot_chart(other_count, "Other")


