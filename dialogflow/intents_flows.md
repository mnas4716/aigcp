# Dialogflow CX Intents and Flows Setup

## Intents and Training Phrases

### Schedule Appointment
- I want to book an appointment
- Can I see a doctor?
- Book me for tomorrow at 10am
- Schedule me for next Monday

### Cancel Appointment
- Cancel my appointment
- Please cancel my booking
- I can't make my appointment

### Reschedule Appointment
- Can I reschedule my appointment?
- Move my booking to another day
- Change my appointment to Friday 2pm

### General Info
- What are your opening hours?
- Where are you located?
- Are you open on weekends?

### Speak to Doctor
- I need to speak to the doctor
- Transfer me to the doctor
- Can I talk directly with the doctor?

## Flows
- After intents Schedule, Cancel, or Reschedule Appointment, first ask:
> "Can I have your mobile number or date of birth to look you up?"
- If patient not found, prompt:
> "I couldn't find you in our system. Please provide your full name, mobile number, and date of birth."
