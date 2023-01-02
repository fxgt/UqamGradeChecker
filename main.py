import requests
import os
import sys
import smtplib
import creds
import json
import ssl
from email.message import EmailMessage

# Email that sends notification (https://youtu.be/g_j6ILT-X0k check this video for complete tutorial)
email_sender = '<the gmail address that sends the notification>'
email_sender_pass = '<password of that gmail>'

# Email that receive the notification
email_receiver = creds.email_recever

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
email_body = 'Cliques sur ce lien pour la découvrir: https://portailetudiant.uqam.ca/'

# Send an email Function
def send_email():
    em= EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = email_subject
    em.set_content(email_body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context ) as smtp:
        smtp.login(email_sender, email_sender_pass)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

#Function that check if you've received a new grade
def checkChanges(data):
    # Load the saved data file
    with open('notes.json', "r", encoding='utf-8') as f:
        saved_data = f.read()        
    saved_data=json.loads(saved_data)
    if(data!=saved_data):  
        seen_notes = set()
        seen_compteurEvaluation = set()
    # Iterate through the "resultats" array
        for i, result in enumerate(saved_data['data']['resultats']):
            # Check if the trimestre is 20223 or higher
            if result['trimestre'] >= 20223:
                # Iterate through the "programmes" array
                for j, prog in enumerate(result['programmes']):
                    # Iterate through the "activites" array
                    for k, act in enumerate(prog['activites']):
			#Check if note and compteurEvaluation values are the same
                        if act['compteurEvaluation'] == data['data']['resultats'][i]['programmes'][j]['activites'][k]['compteurEvaluation'] and act['note'] == data['data']['resultats'][i]['programmes'][j]['activites'][k]['note']:
                            seen_notes.add(act['note'])
                            seen_compteurEvaluation.add(act['compteurEvaluation']) 
                        # Check for changes in the "compteurEvaluation" key
                        if act['compteurEvaluation'] != data['data']['resultats'][i]['programmes'][j]['activites'][k]['compteurEvaluation']:
                            send_email()
                            # Convert the data to a string
                            json_str = json.dumps(data)
                            # Save the data to the file notes.json
                            with open('notes.json', 'w', encoding='utf-8') as f:
                                json.dump(json_str, f, ensure_ascii=False, indent=2)
                            sys.exit()  

                        # Check for changes in the "note" key
                        if act['note'] != data['data']['resultats'][i]['programmes'][j]['activites'][k]['note']:
                            send_email()
                            # Convert the data to a string
                            json_str = json.dumps(data)
                            # Save the data to the file notes.json
                            with open('notes.json', 'w', encoding='utf-8') as f:
                                json.dump(json_str, f, ensure_ascii=False, indent=2)
                            sys.exit()  

                    #check for extra note or compteurEvaluation keys in data JSON
                    if act['note'] not in seen_notes or act['compteurEvaluation'] not in seen_compteurEvaluation:  
                        # Convert the data to a string
                        json_str = json.dumps(data)
                        # Save the data to the file notes.json
                        with open('notes.json', 'w', encoding='utf-8') as f:
                            json.dump(json_str, f, ensure_ascii=False, indent=2)
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

    # Convert the data to a string
    json_str = json.dumps(data)

    # Open the new file and write the string into it
    with open('notes.json', 'w', encoding='utf-8') as f:
        f.write(json_str)


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

    
