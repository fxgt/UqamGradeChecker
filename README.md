UqamGradeChecker
================

This script checks for updates to grades on the UQAM student portal (<https://portailetudiant.uqam.ca/>) and sends an email or sms notification when a new grade is detected.

Requirements
------------

-   Twilio (with a Twilio account)
-   Python 3.6 or higher
-   requests library (can be installed with `pip install requests`)
-   smtplib library (included in Python standard library)
-   json library (included in Python standard library)
-   You will also need to have access to an email account to send the email notifications and a Twilio account to send the SMS notifications.

Setup
-----

1.  In the file named creds.py in the same directory as the script, change the values of the following variables with your information:
    -   identifiant (UQAM student portal username)
    -   motDePasse (UQAM student portal password)
    -   email_receiver (email address to receive grade updates)
    -   sms_sender_number (Twilio verified phone number to send SMS updates)
    -   account_sid (Twilio account sid)
    -   auth_token (Twilio auth token)
2.  Set up the email_sender account variables in the main.py file. You can refer to this tutorial for help setting up a gmail account: <https://youtu.be/g_j6ILT-X0k>
3.  Set up a Twilio account to fill in the necessary variables. You can refer to this tutorial for help setting up a Twilio account: <https://youtu.be/ywH2rsL371Q>

Usage
-----

1.  Clone the repository: `git clone https://github.com/fxgt/UqamGradeChecker.git`
2.  Change directory: `cd UqamGradeChecker`
3.  Make the main.py file executable: `chmod +x main.py`
4.  Run the script: `python3 main.py`

Automation
----------

1.  Create a Google Cloud VM instance and SSH into it.
2.  Install the necessary libraries and dependencies as specified in the Requirements section.
3.  Create a bash script to run the Python script at specified intervals using cron.
4.  To edit the crontab file, run the following command: `crontab -e`
5.  Add the following line to the crontab file to run the script every minute: `* * * * * /path/to/python3 /path/to/UqamGradeChecker/main.py`
6.  Save the crontab file and exit. The script will now be automated and run every minute.

Note
----

-   By default, the script will send an email and an SMS notification when a new grade is detected. If you prefer to receive notifications through only one method, you can comment out the corresponding lines of code in the main.py file.
-   The script is designed to be run on a Linux environment, and it is recommended to use a Google Cloud VM instance for automation.
-   Before running the script, make sure that you have the necessary libraries and dependencies installed on your environment.
-   The script will send an email and SMS notification every time a new grade is detected, so you should expect to receive multiple notifications if there are multiple new grades.
-   You can also edit the crontab entry to run the script at different intervals, for example, every hour
