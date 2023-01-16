import requests
import os
import sys
import smtplib
import creds
import json
import ssl
from email.message import EmailMessage
from twilio.rest import Client

# Email that sends notification (https://youtu.be/g_j6ILT-X0k check this video for complete tutorial)
email_sender = '<the gmail address that sends the notification>'
email_sender_pass = '<password of that gmail>'

# URL of request
request_url1 = 'https://portailetudiant.uqam.ca/authentification'

request_url2 = 'https://portailetudiant.uqam.ca/apis/resumeResultat/identifiant'

payload = {
    'identifiant': creds.identifiant,
    'motDePasse': creds.motDePasse
}

# Email settings
to_email = creds.email_recever
email_subject = 'Tu as reçu une nouvelle note !'
email_body = 'Clique sur ce lien pour la découvrir: https://portailetudiant.uqam.ca/'

# Send an email Function
def send_email():
    em= EmailMessage()
    em['From'] = email_sender
    em['To'] = creds.email_recever
    em['Subject'] = email_subject
    em.set_content(email_body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context ) as smtp:
        smtp.login(email_sender, email_sender_pass)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

#sends sms using twilio 
def send_sms():   
    message = client.messages.create(
        body="\n\nTu as reçu une nouvelle note !"+
        '\n\nClique sur ce lien pour la découvrir: https://portailetudiant.uqam.ca/' ,
        from_=creds.sms_sender_number,
        to=creds.sms_receiver
)
    print(message.sid)	

#Function that check if you've received a new grade
def checkChanges(new_data):
    # Load the saved data file
    with open('notes.json', "r", encoding='utf-8') as f:
        saved_data_str = f.read()  # read the contents of the file as a string
        old_data = json.loads(saved_data_str)  # parse the string as JSON

    #Check if the file are the same
    if new_data != old_data:  
        #iterating through all the elements of the first json
        for old_result in old_data['data']['resultats']:
            for old_program in old_result['programmes']:
                for old_activity in old_program['activites']:
                    old_note = old_activity.get('note')
                    old_compteurEvaluation = old_activity.get('compteurEvaluation')
                    for new_result in new_data['data']['resultats']:
                        for new_program in new_result['programmes']:
                            for new_activity in new_program['activites']:
                                new_note = new_activity.get('note')
                                new_compteurEvaluation = new_activity.get('compteurEvaluation')
                                # Compare the values
                                if old_note != new_note:
                                    send_email()
                                    send_sms()
                                    with open('notes.json', 'w', encoding='utf-8') as f:
                                        json.dump(new_data, f, ensure_ascii=False, indent=2)
                                    sys.exit()
                                if old_compteurEvaluation != new_compteurEvaluation:
                                    send_email()
                                    send_sms()
                                    with open('notes.json', 'w', encoding='utf-8') as f:
                                        json.dump(new_data, f, ensure_ascii=False, indent=2)
                                    sys.exit()

        #Check if there's more keys in the new json
        new_keys = set(new_data.keys()) - set(old_data.keys())
        if new_keys:
            send_email()
            send_sms()
            with open('notes.json', 'w', encoding='utf-8') as f:
                json.dump(new_data, f, ensure_ascii=False, indent=2)
            sys.exit()

    
# Check if the script has been run before
if not os.path.exists("notes.json"):
    # Headers for the first request to obtain our JWT
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://portailetudiant.uqam.ca',
        'Referer': 'https://portailetudiant.uqam.ca/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    # Creating a session object
    session = requests.Session()

    # Json Object containing our JWT token
    response_Jwt_Token = session.post(request_url1, headers=headers, json=payload)
    response_data = response_Jwt_Token.json()

    # Extracting our token and creating cookies object
    token = response_data["token"]
    cookiez = '%22'+token+'%22'
    cookies = {
        'token': cookiez,
    }

    # Second headers for our second request to obtain a json with all our grades in it
    headers2 = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': 'Bearer '+token,
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Referer': 'https://portailetudiant.uqam.ca/resultats/20223',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    response = session.get(request_url2, cookies=cookies, headers=headers2)

    # Convert the response to a JSON object
    data = json.loads(response.text)

    with open('notes.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Compare the current webpage with the saved version
else:

  # Headers for the first request to obtain our JWT
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://portailetudiant.uqam.ca',
        'Referer': 'https://portailetudiant.uqam.ca/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    # Creating a session object
    session = requests.Session()

    # Json Object containing our JWT token
    response_Jwt_Token = session.post(request_url1, headers=headers, json=payload)
    response_data = response_Jwt_Token.json()

    # Extracting our token and creating cookies object
    token = response_data["token"]
    cookiez = '%22'+token+'%22'
    cookies = {
        'token': cookiez,
    }

    # Second headers for our second request to obtain a json with all our grades in it
    headers2 = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': 'Bearer '+token,
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Referer': 'https://portailetudiant.uqam.ca/resultats/20223',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    response = session.get(request_url2, cookies=cookies, headers=headers2)

    # Convert the response to a JSON object
    data = json.loads(response.text)
    checkChanges(data)

    
