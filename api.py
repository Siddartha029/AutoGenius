import google.generativeai as genai

genai.configure(api_key="AIzaSyATLmKLm2SdBOZF3RAtvZM2TG1sgDaFkr8")

models = genai.list_models()
for model in models:
    print(model.name)
