# Install latest OpenAI library first
# pip install --upgrade openai
from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv(".env.local")

# --- Set API key directly ---
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
response = client.models.list()
print(response)
# --- Example email ---
null_email_text = """
My Office Hours are Via Zoom Today: MATH 4A - LIN ALG W/APPS - Fall 2025,

Hi all,

Just for today I am moving my office hours to Zoom. Please join the following room:

Connor Marrs is inviting you to a scheduled Zoom meeting.

Topic: Connor Marrs's Personal Meeting Room
Join Zoom Meeting
https://ucsb.zoom.us/j/3922706684 

Meeting ID: 392 270 6684

---

One tap mobile
+16694449171,,3922706684# US
+16699006833,,3922706684# US (San Jose)

Join instructions
https://ucsb.zoom.us/meetings/3922706684/invitations?signature=Hz12PcUQFTxNt6rf4sOHFIsSdGrWKF3qbAMPtktySSQ

Best,

Connor
"""
true_email_text = """
Invitation: Aarnav Kousik and Samyak Ghevaria @ Thu Oct 2, 2025 2:30pm - 3pm (PDT) (akoushik@ucsb.edu)
Event Name
30 Minute Meeting
Location: Caje Cafe

Need to make changes to this event?
Cancel: https://calendly.com/cancellations/7aaf3d39-857e-4d83-bf49-811b3cf463a5
Reschedule: https://calendly.com/reschedulings/7aaf3d39-857e-4d83-bf49-811b3cf463a5

Powered by Calendly.com

When
Thursday Oct 2, 2025 ⋅ 2:30pm – 3pm (Pacific Time - Los Angeles)
Location
Caje Cafe
View map
Guests
Samyak Ghevaria - organizer
mailtomeask@gmail.com
akoushik@ucsb.edu
View all guest info
"""

# --- Prompt for event extraction ---
prompt = f"""
You are an assistant that extracts event information from emails.

Rules:
1. An event MUST include a specific start date and start time.
   - If either date or time is missing or ambiguous, treat it as NO EVENT.
   - Do not guess or invent dates/times.
2. If an event exists, return JSON with:
   - event_title
   - start_time (ISO format, required)
   - end_time (ISO format, optional)
   - location
   - participants (list of names)
3. If no valid event exists, return: {{"has_event": false}}

Email:
\"\"\"{null_email_text}\"\"\"
"""



# --- Call the new API ---
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
    temperature=0
)

# --- Parse and print JSON output ---
output_text = response.choices[0].message.content


try:
    event_data = json.loads(output_text)
except json.JSONDecodeError:
    event_data = {"error": "Failed to parse JSON", "raw_output": output_text}

print(json.dumps(event_data, indent=4))

# --- Extra filtering after AI ----#
'''the bare minimum is start & end time for an event, the rest can be choose by the user'''
if not event_data["start_time"] or not event_data["end_time"]:
    event_data["has_event"] = 'false'

