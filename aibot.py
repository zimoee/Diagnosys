import cohere
co = cohere.Client('6wiKLlfFRI31ujWg8mYchzPZ29jaJVyIqHYply0L')

illnesses = [
    "Common Cold",
    "Influenza (Flu)",
    "Allergies",
    "COVID-19",
    "Strep Throat",
    "Sinusitis",
    "Bronchitis",
    "Gastroenteritis",
    "Migraine",
    "Hypertension (High Blood Pressure)",
]
illnesses_symptoms = [
    "Common Cold: Cough 3/10, Sneezing 4/10, Runny nose 4/10, Sore throat 2/10",
    "Influenza (Flu): Fever/Chills 6/10, Cough 5/10, Headache 5/10, Nausea/Vomiting 2/10",
    "Allergies: Sneezing 3/10, Runny nose 4/10, Itchy or watery eyes 3/10",
    "COVID-19: Fever/Chills 7/10, Cough 6/10, Loss of taste 8/10, Loss of smell 8/10",
    "Strep Throat: Sore throat 6/10, Fever/Chills 5/10, Headache 4/10",
    "Sinusitis: Runny nose 4/10, Headache 5/10, Loss of smell 4/10, Loss of taste 4/10",
    "Bronchitis: Cough 6/10, Fever/Chills 4/10, Headache 4/10",
    "Gastroenteritis: Nausea/Vomiting 7/10, Fever/Chills 3/10",
    "Migraine: Headache 9/10, Nausea 7/10, Vomiting 6/10",
    "Hypertension (High Blood Pressure): Headaches 5/10",
]
PLACEHOLDER_SYMPTOM_DICTIONARY = {
    " Cough " : '3',
    " Sneezing " : '4',
    " Runny nose " : '4',
    " Fever/Chills " : '0',
    " Headache " : '0',
    " Nausea/Vomiting " : '0',
    " Sore throat " : '2',
    " Loss of taste " : '0',
    " Loss of smell " : '0'
}


final_symptoms = ""
for s in PLACEHOLDER_SYMPTOM_DICTIONARY.items():
    if int(s[1])>0:
        final_symptoms = final_symptoms + ''.join(s) + '/10'


diagnosis = co.rerank(
  model = 'rerank-english-v2.0',
  query = final_symptoms,
  documents = illnesses_symptoms,
  top_n = 3,
)


for m in illnesses:
    for n in range(3):
        if m in str(diagnosis[n]):
            response = co.chat(
	            'What should i do if i have ' + m + '?', 
	            model="command", 
	            temperature=0.9
            )
            print(response.text)
