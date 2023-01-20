import pickle
from flask import Flask, request, render_template
import numpy as np


app = Flask(__name__)

# load the model
model = pickle.load(open('models/model.pkl','rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/predict", methods=["POST"])
def predict():
    # Get the data from the form
    user_past_purchases = float(request.form.get("user_past_purchases"))


    email_text = request.form.get("email_text")
    if email_text == "short_email":
        email_text_short_email = 1
        email_text_long_email = 0
    else:
        email_text_short_email = 0
        email_text_long_email = 1
    
    email_version = request.form.get("email_version")
    if email_version == "personalized":
        email_version_personalized = 1
        email_version_generic = 0
    else:
        email_version_personalized = 0
        email_version_generic = 1



    weekday = request.form.get("weekday")
    if weekday == "Friday":
        weekday_Monday = 0
        weekday_Saturday = 0
        weekday_Sunday = 0
        weekday_Thursday = 0
        weekday_Tuesday = 0
        weekday_Wednesday = 0
    else:
        weekday_Monday = 1 if weekday == "Monday" else 0
        weekday_Saturday = 1 if weekday == "Saturday" else 0
        weekday_Sunday = 1 if weekday == "Sunday" else 0
        weekday_Thursday = 1 if weekday == "Thursday" else 0
        weekday_Tuesday = 1 if weekday == "Tuesday" else 0
        weekday_Wednesday = 1 if weekday == "Wednesday" else 0

    

    user_country = request.form.get("user_country")
    if user_country == "ES":
        user_country_FR = 0
        user_country_UK = 0
        user_country_US = 0
    else:
        user_country_FR = 1 if user_country == "FR" else 0
        user_country_UK = 1 if user_country == "UK" else 0
        user_country_US = 1 if user_country == "US" else 0
    
    
    time_of_day = request.form.get("time_of_day")
    if time_of_day == "afternoon":
        time_of_day_morning = 0
        time_of_day_evening = 0
        time_of_day_midnight = 0
    else:
        time_of_day_morning = 1 if time_of_day == "morning" else 0
        time_of_day_evening = 1 if time_of_day == "evening" else 0
        time_of_day_midnight = 1 if time_of_day == "midnight" else 0


    # Prepare the data for the model
    intercept = 1
    data = [user_past_purchases, intercept, email_text_short_email,
       email_version_personalized, weekday_Monday, weekday_Saturday,
       weekday_Sunday, weekday_Thursday, weekday_Tuesday,
       weekday_Wednesday, user_country_FR, user_country_UK,
       user_country_US, time_of_day_evening, time_of_day_midnight,
       time_of_day_morning]
    data = np.array(data).reshape(1,-1)

    prediction = model.predict_proba(data)[:,1]
    # Extract the scalar value from the numpy array
    prediction = prediction.item()
    # Multiply the prediction by 100 and format it as a percentage
    prediction_percentage = "{:.2f}%".format(prediction * 100)
    
    # Return the prediction as a JSON object
    return render_template('index.html', prediction_text = 'The User Click Probability is {}'.format(prediction_percentage))




if __name__ == '__main__':
    app.run(debug=True, port=8000)
