import pickle

def load_model_total_case():
    with open('model/xgb_model_total_imputed_cases.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

def load_model_total_death():
    with open('model/xgb_model_total_deaths.pkl', 'rb') as file:
        model = pickle.load(file)
    return model
