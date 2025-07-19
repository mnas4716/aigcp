# webhook/main.py

import functions_framework
from flask import jsonify, request
import os
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import requests

# --- Gemini Integration (toggleable) ---
USE_GEMINI = False  # Set True to enable Gemini

if USE_GEMINI:
    import vertexai
    from vertexai.language_models import TextGenerationModel
    vertexai.init(project=os.getenv("GCP_PROJECT"), location="us-central1")
    gemini_model = TextGenerationModel.from_pretrained("gemini-1.5-flash")

# --- Google Sheets Setup ---
SERVICE_ACCOUNT_JSON = os.getenv("SERVICE_ACCOUNT_JSON")
creds = Credentials.from_service_account_info(eval(SERVICE_ACCOUNT_JSON))
gspread_client = gspread.authorize(creds)
sheet = gspread_client.open("PatientRegistry").sheet1

# --- Google Calendar Setup ---
calendar_service = build('calendar', 'v3', credentials=creds)
CALENDAR_ID = os.getenv("CALENDAR_ID")

# Helper Functions
def find_patient(mobile, dob):
    records = sheet.get_all_records()
    for patient in records:
        if patient['Mobile'] == mobile or patient['DOB'] == dob:
            return patient
    return None

def register_patient(name, mobile, dob):
    sheet.append_row([name, mobile, dob])

def schedule_appointment(patient_name, datetime_str):
    event = {
        'summary': f"Appointment - {patient_name}",
        'start': {'dateTime': datetime_str, 'timeZone': 'Australia/Sydney'},
        'end': {'dateTime': (datetime.fromisoformat(datetime_str) + timedelta(minutes=30)).isoformat(), 'timeZone': 'Australia/Sydney'}
    }
    calendar_service.events().insert(calendarId=CALENDAR_ID, body=event).execute()

def send_reminder(mobile, datetime_str):
    print(f"Sending SMS reminder to {mobile} for appointment at {datetime_str}")
    # (Replace this with actual SMS API call)

def gemini_response(prompt):
    response = gemini_model.predict(
        prompt,
        max_output_tokens=128,
        temperature=0.2
    )
    return response.text

# --- Cloud Function ---
@functions_framework.http
def webhook(request):
    req = request.get_json()
    intent = req['queryResult']['intent']['displayName']
    parameters = req['queryResult'].get('parameters', {})

    mobile = parameters.get('mobile')
    dob = parameters.get('dob')
    datetime_str = parameters.get('date-time')
    patient_name = parameters.get('name', 'Patient')

    patient = find_patient(mobile, dob)

    if intent == 'Schedule Appointment':
        if not patient:
            register_patient(patient_name, mobile, dob)
        schedule_appointment(patient_name, datetime_str)
        send_reminder(mobile, datetime_str)
        response_text = f"Appointment confirmed for {datetime_str}."
    elif intent == 'Cancel Appointment':
        response_text = "Appointment cancelled."
    elif intent == 'Reschedule Appointment':
        schedule_appointment(patient_name, datetime_str)
        response_text = f"Appointment rescheduled to {datetime_str}."
    elif intent == 'General Info':
        response_text = "Our clinic is open Mon-Fri, 9am to 5pm."
    elif intent == 'Speak to Doctor':
        response_text = "Transferring you to the doctor now."
    else:
        response_text = "Sorry, I couldn't understand your request."

    if USE_GEMINI:
        prompt = f"Patient asked: {req['queryResult']['queryText']}. Reply briefly: {response_text}"
        response_text = gemini_response(prompt)

    return jsonify({'fulfillmentText': response_text})
