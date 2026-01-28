from experta import *

class Symptoms(Fact):
    pass

class RespiratoryIllnessAgent(KnowledgeEngine):

    def __init__(self):
        super().__init__()
        self.flu_count = 0
        self.covid_count = 0
        self.flu_matched = []
        self.covid_matched = []
        self.total_symptoms = 0

        self.flu_symptoms = {
            "fever", "cough", "sore throat",
            "runny nose", "body ache", "fatigue"
        }

        self.covid_symptoms = {
            "fever", "dry cough", "fatigue",
            "loss of taste", "loss of smell",
            "shortness of breath", "chest pain"
        }

    # Runs FIRST
    @Rule(Symptoms(symptom=MATCH.symptom), salience=10)
    def count_symptoms(self, symptom):
        symptom = symptom.lower()
        self.total_symptoms += 1

        if symptom in self.flu_symptoms:
            self.flu_count += 1
            self.flu_matched.append(symptom)

        if symptom in self.covid_symptoms:
            self.covid_count += 1
            self.covid_matched.append(symptom)

    # Runs AFTER counting
    @Rule(Fact(action="diagnose"), salience=-10)
    def diagnose(self):
        print("\nMatched Symptom Report:")
        print("Flu matched symptoms:", self.flu_matched)
        print("COVID-19 matched symptoms:", self.covid_matched)

        if self.total_symptoms == 0:
            confidence = 0.0
        else:
            confidence = (max(self.flu_count, self.covid_count) /
                          self.total_symptoms) * 100

        print(f"\nConfidence Level: {confidence:.2f}%")

        print("\nDiagnosis Result:")

        if self.covid_count >= 5:
            print("COVID-19 detected — EXTREME condition")
        elif self.covid_count >= 3 and self.covid_count >= self.flu_count:
            print("COVID-19 detected — MILD condition")
        elif self.flu_count >= 3:
            print("Normal Flu detected")
        else:
            print("Insufficient indicators — consult a physician")

def main():
    agent = RespiratoryIllnessAgent()
    agent.reset()

    user_input = input(
        "Enter symptoms separated by commas: "
    ).strip().lower()

    symptoms = [s.strip() for s in user_input.split(",") if s.strip()]

    if len(symptoms) < 3:
        print("Please enter at least 3 symptoms for diagnosis.")
        return

    for symptom in symptoms:
        agent.declare(Symptoms(symptom=symptom))

    agent.declare(Fact(action="diagnose"))
    agent.run()

if __name__ == "__main__":
    main()
