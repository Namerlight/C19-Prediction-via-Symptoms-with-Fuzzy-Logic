import pandas as pd
import matplotlib.pyplot as plt

dataset1 = pd.read_csv(r'data/WolframPatients.csv')
dataset2 = pd.read_csv(r'data/NovelDataset.csv')

has_symptoms1 = dataset1[dataset1.Symptoms.notnull()]
has_symptoms2 = dataset2[dataset2.Symptoms.notnull()]

sympt_list_1 = pd.DataFrame(has_symptoms1, columns=['Symptoms'])
sympt_list_2 = pd.DataFrame(has_symptoms2, columns=['Symptoms'])

symptoms = sympt_list_1.append(sympt_list_2, ignore_index=True, sort=False)

print(symptoms)

total_count = len(symptoms.axes[0])

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

print(cough_count, fever_count, breath_count, pain_count, other_count)


plt.bar(["Positive", "Negative"], [cough_count, total_count - cough_count], width=.6)
plt.legend()
plt.xlabel('Cough')
plt.ylabel('Number of Reports')
plt.title('Reported Cough as Symptom')
plt.show()
print("Cough - Positive:", cough_count*100/total_count, "%,",
      "Negative", (total_count - cough_count)*100/total_count, "%")

plt.bar(["Positive", "Negative"], [fever_count, total_count - fever_count], width=.6)
plt.legend()
plt.xlabel('Fever')
plt.ylabel('Number of Reports')
plt.title('Reported Fever as Symptom')
plt.show()
print("Fever - Positive:", fever_count*100/total_count, "%,",
      "Negative", (total_count - fever_count)*100/total_count, "%")

plt.bar(["Positive", "Negative"], [breath_count, total_count - breath_count], width=.6)
plt.legend()
plt.xlabel('Breathing Difficulties')
plt.ylabel('Number of Reports')
plt.title('Reported Breathing Difficulties as Symptom')
plt.show()
print("Breathing Difficulties - Positive:", breath_count*100/total_count, "%,",
      "Negative", (total_count - breath_count)*100/total_count, "%")

plt.bar(["Positive", "Negative"], [pain_count, total_count - pain_count], width=.6)
plt.legend()
plt.xlabel('Pain')
plt.ylabel('Number of Reports')
plt.title('Reported Various Pains as Symptom')
plt.show()
print("Various Pains - Positive:", pain_count*100/total_count, "%,",
      "Negative", (total_count - pain_count)*100/total_count, "%")

plt.bar(["Positive", "Negative"], [other_count, total_count - other_count], width=.6)
plt.legend()
plt.xlabel('Others')
plt.ylabel('Number of Reports')
plt.title('Reported Other Symptoms')
plt.show()
print("Other Symptoms - Positive:", other_count*100/total_count, "%,",
      "Negative", (total_count - other_count)*100/total_count, "%")



