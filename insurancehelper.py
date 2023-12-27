import streamlit as st
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from reportlab.pdfgen import canvas
from twilio.rest import Client
import openai
from twilio.twiml.voice_response import Gather, VoiceResponse
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve credentials from environment variables
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# Function to create the "customers" table in SQLite database
def create_customers_table():
    conn = sqlite3.connect('insurance.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to save customer information to SQLite database
def save_to_database(name, email):
    conn = sqlite3.connect('insurance.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO customers (name, email) VALUES (?, ?)', (name, email))
    conn.commit()
    conn.close()

# Function to generate PDF
def generate_pdf(name, email):
    filename = f"{name}_information.pdf"
    c = canvas.Canvas(filename)
    c.drawString(100, 750, f"Customer Information\nName: {name}\nEmail: {email}")
    c.save()

# Function to send email
def send_email(subject, body):
    # Add your email and password
    sender_email = "khanowais8888@gmail.com"
    sender_password = "lkxb gthp abld cllq"

    # Set up the MIME
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = "khanowais8888@example.com"
    message["Subject"] = subject

    # Attach body
    message.attach(MIMEText(body, "plain"))

    # Connect to the SMTP server
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, "your_email@example.com", message.as_string())

# Function to get FAQ response from GPT-3
def get_faq_response(query):
    # Replace 'YOUR_API_KEY' with your OpenAI API key
    # openai.api_key = "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"
    openai.api_key = OPENAI_API_KEY
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"FAQ: {query}\nAnswer:",
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Function to send WhatsApp message using Twilio
# def send_whatsapp_message(phone_number, message):
#     # Add your Twilio SID, Auth Token, and Twilio phone number
#     # account_sid = 'AC22dc8823526e8fe94a72c9f500166e77'
#     # auth_token = '59f4e124e0e30b301dc68610a3713f86'
#     # twilio_phone_number = '+19724981636'
#     account_sid = TWILIO_ACCOUNT_SID
#     auth_token = TWILIO_AUTH_TOKEN
#     twilio_phone_number = TWILIO_PHONE_NUMBER
#     client = Client(account_sid, auth_token)

#     message = client.messages.create(
#         from_=twilio_phone_number,
#         body=message,
#         to=f"whatsapp:{phone_number}"
#     )
# Function to send WhatsApp message using Twilio
def send_whatsapp_message(phone_number, message):
    # Add your Twilio SID, Auth Token, and Twilio phone number
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    twilio_phone_number = TWILIO_PHONE_NUMBER
    client = Client(account_sid, auth_token)

    # Use a Twilio phone number that is enabled for WhatsApp for the 'from_'
    from_whatsapp_number = f"whatsapp:{twilio_phone_number}"

    # Use a valid WhatsApp phone number with the 'whatsapp:' prefix for the 'to'
    to_whatsapp_number = f"whatsapp:{phone_number}"

    message = client.messages.create(
        from_=from_whatsapp_number,
        body=message,
        to=to_whatsapp_number
    )


# Function to make a VoIP call using Twilio
# def make_voip_call(phone_number, message):
#     # Add your Twilio SID, Auth Token, and Twilio phone number
#     account_sid = 'AC22dc8823526e8fe94a72c9f500166e77'
#     auth_token = '59f4e124e0e30b301dc68610a3713f86'
#     twilio_phone_number = '+18884828556'

#     client = Client(account_sid, auth_token)

#     call = client.calls.create(
#         twiml=f'<Response><Say>{message}</Say></Response>',
#         to=phone_number,
#         from_=twilio_phone_number
#     )
    # Function to make a VoIP call using Twilio
# def make_voip_call(phone_number, message):
#     # Add your Twilio SID, Auth Token, and Twilio phone number
#     account_sid = 'AC22dc8823526e8fe94a72c9f500166e77'
#     auth_token = '59f4e124e0e30b301dc68610a3713f86'
#     twilio_phone_number = '+18884828556'

#     client = Client(account_sid, auth_token)

#     # Create an introductory message
#     intro_message = "Hello and welcome to the Luc Nguyen Insurance Agency. " \
#                     "Your peace of mind is our priority. How can we help you today?"

#     # Concatenate the introductory message with the provided message
#     full_message = f"{intro_message} {message}"

#     call = client.calls.create(
#         twiml=f'<Response><Say>{full_message}</Say></Response>',
#         to=phone_number,
#         from_=twilio_phone_number
#     )


def make_voip_call(phone_number, message):
    # Add your Twilio SID, Auth Token, and Twilio phone number
    # account_sid = 'AC22dc8823526e8fe94a72c9f500166e77'
    # auth_token = '59f4e124e0e30b301dc68610a3713f86'
    # # twilio_phone_number = '+18884828556'
    # twilio_phone_number = '+19724981636'
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    twilio_phone_number = TWILIO_PHONE_NUMBER

    client = Client(account_sid, auth_token)

    # Create an introductory message
    intro_message = "Hello and welcome to the Luc Nguyen Insurance Agency. " \
                    "Your peace of mind is our priority. How can we help you today?"

    # Create a TwiML response with the introductory message and the provided message
    twiml_response = VoiceResponse()
    twiml_response.say(intro_message)
    twiml_response.say(message)

    # Initiate the call
    call = client.calls.create(
        twiml=str(twiml_response),
        to=phone_number,
        from_=twilio_phone_number
    )

# # Example usage:
# make_voip_call("+19724981636", "This is the message you want to convey.")

    # call = client.calls.create(
    #     twiml=f'<Response><Say>{message}</Say></Response>',
    #     to=f"+18884828556",  # Replace with the actual VoIP phone number
    #     from_=twilio_phone_number
    # )
# Streamlit app
def main():
    st.title("Luc Nguyen Insurance Agency")
    # st.markdown("Hello and welcome to the Luc Nguyen Insurance Agency, where your peace of mind is our priority.")
    # st.markdown("How can we help you today?")

    # Ensure the "customers" table is created
    create_customers_table()

    # FAQ Handling
    user_input = st.text_input("Ask a question:")

    # Check if the user has provided a question
    if user_input:
        # Use GPT-3 to get FAQ response
        bot_response = get_faq_response(user_input)
        st.text(f"Bot's response: {bot_response}")

    # Customer Information Collection
    st.header("Customer Information")
    customer_name = st.text_input("Name:")
    customer_email = st.text_input("Email:")

    # Check if the user has provided both name and email
    if customer_name and customer_email:
        if st.button("Submit"):
            # Save to database
            save_to_database(customer_name, customer_email)

            # Generate PDF
            generate_pdf(customer_name, customer_email)

            # Send Email
            send_email("New Customer Inquiry", f"Name: {customer_name}\nEmail: {customer_email}")

            # Send WhatsApp Message (replace phone_number with the actual phone number)
            # send_whatsapp_message(phone_number="replace_with_phone_number", message=f"New customer inquiry: {customer_name}")
            send_whatsapp_message(phone_number="+16614006221", message=f"New customer inquiry: {customer_name}")

            # Make VoIP Call (replace phone_number with the actual phone number)
            # make_voip_call(phone_number="replace_with_phone_number", message=f"New customer inquiry: {customer_name}")
            make_voip_call(phone_number="+16614006221", message=f"New customer inquiry: {customer_name}")

            st.success("Information submitted successfully!")

if __name__ == "__main__":
    main()

