class PatientAIAgent:
    def __init__(self, name, age, symptoms=None):
        self.name = name
        self.age = age
        self.symptoms = symptoms or []

    def add_symptom(self, symptom):
        self.symptoms.append(symptom)

    def get_summary(self):
        return {
            "name": self.name,
            "age": self.age,
            "symptoms": self.symptoms
        }

    def suggest_action(self):
        if not self.symptoms:
            return "No symptoms reported. No action needed."
        if "fever" in self.symptoms and "cough" in self.symptoms:
            return "Suggest COVID-19 test and consult a doctor."
        if "headache" in self.symptoms:
            return "Recommend rest and hydration."
        return "Monitor symptoms and consult a healthcare provider if they worsen."

# Example usage
if __name__ == "__main__":
    agent = PatientAIAgent("Ravi Umale", 52)
    agent.add_symptom("fever")
    agent.add_symptom("cough")
    print(agent.get_summary())
    print(agent.suggest_action())