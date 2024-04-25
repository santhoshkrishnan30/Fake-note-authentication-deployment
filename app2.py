# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 21:40:41 2020

@author: win10
"""

# 1. Library imports
import uvicorn
from fastapi import FastAPI
from BankNotes import BankNote
import numpy as np
import pickle
import pandas as pd
from pydantic import BaseModel
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# 2. Create the app object
app = FastAPI()

# Load dataset
df = pd.read_csv('BankNote_Authentication.csv')

# Independent and Dependent features
X = df.iloc[:, :-1]
y = df.iloc[:, -1]

# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# Implement Random Forest classifier
classifier = RandomForestClassifier()
classifier.fit(X_train, y_train)

# 3. Index route, opens automatically on http://127.0.0.1:8000
# Add this import at the top of your FastAPI script
from fastapi.responses import FileResponse

# Add this route to serve the HTML file
@app.get('/')
async def get_index():
    return FileResponse("templates/index.html")


# 4. Route with a single parameter, returns the parameter within a message
#    Located at: http://127.0.0.1:8000/AnyNameHere
@app.get('/{name}')
def get_name(name: str):
    return {'WELCOME TO BANK NOTE DETECTION': f'{name}'}

# 5. Expose the prediction functionality, make a prediction from the passed
#    JSON data and return the predicted Bank Note with the confidence
@app.post('/predict')
def predict_banknote(data: BankNote):
    data = data.dict()
    variance = data['variance']
    skewness = data['skewness']
    curtosis = data['curtosis']
    entropy = data['entropy']
    
    prediction = classifier.predict([[variance, skewness, curtosis, entropy]])
    if prediction[0] > 0.5:
        prediction = "Fake note"
    else:
        prediction = "Its a Bank note"
    
    return {'prediction': prediction}

# Create a Pickle file using serialization
with open("classifier.pkl", "wb") as f:
    pickle.dump(classifier, f, protocol=pickle.HIGHEST_PROTOCOL)

# 6. Run the API with uvicorn
#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
