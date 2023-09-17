from taipy import *
from taipy.gui import *
import pandas as pd
import cohere
co = cohere.Client('6wiKLlfFRI31ujWg8mYchzPZ29jaJVyIqHYply0L')

value = ""
text = "Symptom"
severity = 0
dictionary = {}
df = {}
result = ""

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
    "Common Cold: Cough 5/10, Sneezing 7/10, Runny nose 8/10, Fever/Chills 2/10, Headache 4/10, Nausea/Vomiting 2/10, Sore throat 6/10, Loss of taste 2/10, Loss of smell 2/10",
    "Influenza (Flu): Fever/Chills 8/10, Cough 7/10, Sneezing 2/10, Headache 6/10, Nausea/Vomiting 4/10, Sore throat 4/10, Loss of taste 2/10, Loss of smell 2/10",
    "Allergies: Sneezing 8/10, Runny nose 8/10, Itchy or watery eyes 7/10, Cough 3/10, Headache 2/10, Nausea/Vomiting 1/10, Sore throat 2/10, Loss of taste 1/10, Loss of smell 1/10",
    "COVID-19: Fever/Chills 9/10, Cough 8/10, Sneezing 2/10, Loss of taste 9/10, Loss of smell 9/10, Headache 7/10, Nausea/Vomiting 3/10, Sore throat 3/10, Runny nose 2/10",
    "Strep Throat: Sore throat 9/10, Fever/Chills 8/10, Headache 6/10, Nausea/Vomiting 3/10, Cough 2/10, Sneezing 1/10, Runny nose 2/10, Loss of taste 1/10, Loss of smell 1/10",
    "Sinusitis: Runny nose 8/10, Cough 4/10, Headache 7/10, Loss of smell 7/10, Loss of taste 6/10, Fever/Chills 2/10, Sneezing 2/10, Nausea/Vomiting 1/10, Sore throat 2/10",
    "Bronchitis: Cough 8/10, Fever/Chills 6/10, Headache 4/10, Chest discomfort 5/10, Sneezing 1/10, Runny nose 1/10, Loss of taste 1/10, Loss of smell 1/10, Nausea/Vomiting 1/10",
    "Gastroenteritis: Nausea/Vomiting 9/10, Diarrhea 8/10, Fever/Chills 3/10, Cough 1/10, Sneezing 1/10, Runny nose 1/10, Headache 2/10, Sore throat 1/10, Loss of taste 1/10, Loss of smell 1/10",
    "Migraine: Headache 9/10, Nausea 8/10, Vomiting 7/10, Sensitivity to light 8/10, Sensitivity to sound 8/10, Cough 1/10, Sneezing 1/10, Runny nose 1/10, Fever/Chills 1/10, Sore throat 1/10",
    "Hypertension (High Blood Pressure): Headaches 8/10, Cough 2/10, Sneezing 1/10, Runny nose 1/10, Fever/Chills 1/10, Nausea/Vomiting 1/10, Sore throat 1/10, Loss of taste 1/10, Loss of smell 1/10",
] 

# symptomsDF = pd.DataFrame(columns=["Symptom", "Severity"])

page = """
<|layout|columns=70px 1fr 70px|

<| |>

<|{"title.png"}|image|>

<| |>

<| |>

Please select symptom(s) from the list and select the severity of each symptom. Press "Add Symptom" after each symptom added. 

<| |>

<| |>

Press "Submit" once you are finished entering symptoms.

<| |>

<| |>

Your symptom: <|{value}|>

<| |>

<| |>

<|{value}|selector|lov=Coughing;Sneezing;Runny nose;Fever/Chills;Headache;Nausea/Vomiting;Sore throat;Loss of taste; Loss of smell|dropdown|>

<| |>

<| |>

Severity: <|{severity}|>

<| |>

<| |>

<|{severity}|slider|min=1|max=10|>

<| |>

<| |>

<|Add Symptom|button|on_action=on_button_action|><|Submit|button|on_action=on_submit_action|class_name=plain|>

<| |>

<| |>

<|{df}|table|page_size = 10|rebuild|>

<| |>

<| |>

<|card card-bg|
We believe you have: <|{condition}|>
|>

<| |>

<| |>

<|card card-bg|
<|{result}|>
|>

<| |>

<| |>

|>

"""

def on_button_action(state):
    symptomToAdd = state.value
    severityToAdd = str(state.severity)
    
    if "" in dictionary:
        dictionary.pop("")
        
    if symptomToAdd not in dictionary:
        dictionary[symptomToAdd] = severityToAdd
    print(dictionary)

    df = pd.DataFrame(dictionary.items(), columns=['Symptom', 'Severity'])
    state.df = df
    print(df)
    
def on_submit_action(state):
    final_symptoms = ""
    for s in dictionary.items():
        if int(s[1])>0:
            final_symptoms = final_symptoms + ''.join(s) + '/10'


    diagnosis = co.rerank(
    model = 'rerank-english-v2.0',
    query = final_symptoms,
    documents = illnesses_symptoms,
    top_n = 1,
    )

    for condition in illnesses:
        if condition in str(diagnosis):
            response = co.chat(
	            'What should I do if I have ' + condition + '? write only 3 sentences and do not under any circumstance ask any questions. Answer in the form of a statement as if you are a textbook. ', 
	            model="command", 
	            temperature=0.9
            )

            result =  response.text
            state.result = result
            print(result)
            return result, condition

stylekit = {
  "color_primary": "#BADA55",
}

Gui(page=page).run(stylekit=stylekit)

use_reloader = True