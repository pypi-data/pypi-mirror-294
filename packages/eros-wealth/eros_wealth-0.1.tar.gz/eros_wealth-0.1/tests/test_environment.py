from head import eros
import numpy as np

def test_challenging_scenarios():
    print("Starting challenging scenarios tests...")

    # Σενάριο 1: Μεταβαλλόμενοι Πόροι
    print("\nScenario 1: Dynamic Resource Management")
    main_script.run_full_environment()

    # Σενάριο 2: Εισαγωγή θορύβου και τυχαίων σφαλμάτων
    print("\nScenario 2: Noise and Errors Injection")
    inputs = {
        "decision_factors": np.array([0.6, 0.8, 0.4]) + np.random.normal(0, 0.1, 3),
        "internal_motivations": np.array([0.7, 0.3, 0.9]) + np.random.normal(0, 0.1, 3),
        "scenario": "Δίλημμα ηθικής απόφασης",
        "ethical_factors": np.array([0.9, 0.7, 0.6]) + np.random.normal(0, 0.1, 3),
        "risk_factors": np.array([0.4, 0.5, 0.3]) + np.random.normal(0, 0.1, 3),
        "current_state": np.array([0.3, 0.6, 0.2]) + np.random.normal(0, 0.1, 3),
        "emotional_influences": np.array([0.7, -0.2, 0.5]) + np.random.normal(0, 0.1, 3),
        "experiences": [0.1, 0.2, 0.3],
        "feedback": [0.05, -0.1, 0.2],
        "strategy": np.array([0.5, 0.7, 0.8]),
        "initial_population": [np.random.rand(10) for _ in range(20)],
        "a": 3,
        "b": 4,
        "theta": np.pi / 4,
        "idea_space": np.array([0.3, 0.6, 0.9]),
        "random_factor": np.random.rand(3),
        "variables": np.array([0.5, 0.7, 0.9]),
        "luck_coefficient": 0.8,
        "ethics_factor": 0.9,
        "excellence_factor": 1.1,
        "neural_connections": [0.3, 0.7, 0.4],
        "sensory_inputs": [0.5, 0.9, 0.3],
        "data_points": [1.2, 2.1, 0.9],
        "emotional_states": [0.8, 0.6, 0.9],
        "events": ["Event A", "Event B", "Event C"],
        "historical_data": [10, 15, 20],
        "current_data": [22, 25, 27],
        "initial_state": 0.5,
        "cognitive_tasks": [0.4, 0.6, 0.3],
        "text_corpus": [
            "Η τύχη επηρεάζει τη ζωή μας.",
            "Η αβεβαιότητα είναι συχνή στις αποφάσεις.",
            "Η αυτογνωσία βελτιώνει τις επιλογές μας."
        ],
        "query_text": "αποφάσεις",
        "emotions": np.array([0.9, -0.8, 0.5, -0.4]),
        "cognitive_processes": np.array([0.1, 0.5, 1.0, 1.5]),
        "options": ["Δράση Α", "Δράση Β", "Δράση Γ"],  # Απαραίτητο για zeus_decision_maker
        "probabilities": [0.6, 0.3, 0.1],  # Απαραίτητο για zeus_decision_maker
        "utilities": [50, 80, 30],  # Απαραίτητο για zeus_decision_maker
        "initial_strategy": np.array([1.0, 2.0, 3.0]),  # Απαραίτητο για athena_strategy_optimizer
        "strategies": [
            np.array([1.0, 0.5, 0.3]),
            np.array([0.8, 0.6, 0.2]),
            np.array([0.9, 0.4, 0.7])
        ],  # Απαραίτητο για ares_conflict_resolver
        "environmental_factors": np.array([0.4, 0.5, 0.6])  # Απαραίτητο για artemis_adaptive_protector
    }
    main_script.nlp.unified_intelligence_scenario(inputs)

    # Σενάριο 3: Αυξημένο Φορτίο Εργασίας
    print("\nScenario 3: Increased Workload")
    for _ in range(5):
        main_script.run_full_environment()

    # Σενάριο 4: Σενάριο Υψηλού Ρίσκου
    print("\nScenario 4: High-Risk Decision Making")
    inputs = {
        "decision_factors": np.array([0.2, 0.9, 0.7]),
        "internal_motivations": np.array([0.4, 0.2, 0.6]),
        "scenario": "Επιλογή με άμεσο κίνδυνο",
        "ethical_factors": np.array([0.8, 0.3, 0.9]),
        "risk_factors": np.array([0.9, 0.7, 0.9]),
        "current_state": np.array([0.5, 0.7, 0.9]),
        "emotional_influences": np.array([0.6, -0.3, 0.4]),
        "experiences": [0.2, 0.3, 0.4],
        "feedback": [0.1, -0.05, 0.2],
        "strategy": np.array([0.6, 0.8, 0.9]),
        "initial_population": [np.random.rand(10) for _ in range(20)],
        "a": 5,
        "b": 7,
        "theta": np.pi / 3,
        "idea_space": np.array([0.5, 0.7, 0.8]),
        "random_factor": np.random.rand(3),
        "variables": np.array([0.6, 0.9, 0.4]),
        "luck_coefficient": 0.7,
        "ethics_factor": 0.85,
        "excellence_factor": 1.2,
        "neural_connections": [0.2, 0.8, 0.5],
        "sensory_inputs": [0.4, 0.7, 0.6],
        "data_points": [1.1, 2.0, 0.8],
        "emotional_states": [0.7, 0.5, 0.8],
        "events": ["Event X", "Event Y", "Event Z"],
        "historical_data": [12, 18, 25],
        "current_data": [26, 28, 30],
        "initial_state": 0.6,
        "cognitive_tasks": [0.5, 0.4, 0.7],
        "text_corpus": [
            "Η ανάλυση της πληροφορίας είναι κρίσιμη.",
            "Η διαχείριση των δεδομένων καθορίζει το αποτέλεσμα.",
            "Η τεχνητή νοημοσύνη βοηθά στη λήψη αποφάσεων."
        ],
        "query_text": "δεδομένα",
        "emotions": np.array([0.8, -0.6, 0.3, -0.2]),
        "cognitive_processes": np.array([0.2, 0.7, 1.1, 1.6]),
        "options": ["Δράση Δ", "Δράση Ε", "Δράση Ζ"],  # Απαραίτητο για zeus_decision_maker
        "probabilities": [0.5, 0.3, 0.2],  # Απαραίτητο για zeus_decision_maker
        "utilities": [40, 60, 20],  # Απαραίτητο για zeus_decision_maker
        "initial_strategy": np.array([1.5, 2.5, 3.5]),  # Απαραίτητο για athena_strategy_optimizer
        "strategies": [
            np.array([1.2, 0.4, 0.4]),
            np.array([0.7, 0.5, 0.3]),
            np.array([0.8, 0.3, 0.9])
        ],  # Απαραίτητο για ares_conflict_resolver
        "environmental_factors": np.array([0.3, 0.6, 0.5])  # Απαραίτητο για artemis_adaptive_protector
    }
    main_script.nlp.unified_intelligence_scenario(inputs)

    print("Challenging scenarios tests completed.")

if __name__ == "__main__":
    test_challenging_scenarios()
