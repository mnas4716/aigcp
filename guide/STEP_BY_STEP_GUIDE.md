# 🚀 STEP-BY-STEP GUIDE (Idiot-proof)

## ✅ STEP 1: Google Cloud Setup
- Create new project at [Google Cloud](https://console.cloud.google.com/)
- Enable APIs:
  - Dialogflow API
  - Cloud Functions API
  - Google Sheets API
  - Google Calendar API
  - Vertex AI API (optional Gemini)

## ✅ STEP 2: Service Account & Credentials
- IAM > Service Accounts > Create
- Add roles: Dialogflow API Admin, Cloud Functions Admin, Sheets & Calendar Editor
- Download JSON key, copy content to env var `SERVICE_ACCOUNT_JSON`

## ✅ STEP 3: Google Sheets Setup
- Create Sheet named `PatientRegistry`
- Columns: Name, Mobile, DOB
- Share Sheet with Service Account email

## ✅ STEP 4: Google Calendar Setup
- Create Google Calendar named `Clinic Appointments`
- Share with Service Account email
- Copy Calendar ID to env var `CALENDAR_ID`

## ✅ STEP 5: Deploy Webhook (Cloud Functions)
- Navigate to Cloud Functions
- Create new function, Runtime: Python 3.11, HTTP trigger
- Paste `main.py` and `requirements.txt` contents
- Add environment vars: `SERVICE_ACCOUNT_JSON`, `CALENDAR_ID`
- Deploy & copy the public URL (for Dialogflow webhook)

## ✅ STEP 6: Dialogflow CX Setup
- Go to Dialogflow CX console, create new agent
- Add intents and flows exactly from `intents_flows.md`
- Connect webhook URL from Cloud Function
- Test intents thoroughly in simulator

---

# 💡 OPTIONAL: GEMINI FLASH INTEGRATION (Step 7)
- Set `USE_GEMINI = True` in `main.py`
- Vertex AI enabled in Google Cloud
- No extra setup (already included)

---

## 💸 COST MONITORING:
- Check billing periodically at [Google Cloud Billing](https://console.cloud.google.com/billing)
- Gemini Flash is very low-cost but keep an eye on it initially.

## 🔄 TOGGLE GEMINI:
- Simply change `USE_GEMINI` True/False in `main.py` and redeploy function.
