# UqamGradeChecker
This script checks for updates to grades on the UQAM student portal (<https://portailetudiant.uqam.ca/>) and sends an email notification if a new grade is detected.

Requirements
------------

-   Python 3.6 or higher
-   requests library (pip install requests)
-   smtplib library (included in Python standard library)
-   json library (included in Python standard library)

Setup
-----

To use this script, you will need to change the variables in the file named `creds.py` in the same directory as the script. The file contains the following variables:

`identifiant = '<your UQAM student ID>'` 
`motDePasse = '<your UQAM password>'`
`email_recever = '<the email address that will receive the notification>'`

You will aslo need to set up the email_sender account variables in the main.py file. You can check this tutorial if you need help setting up the gmail account:
https://youtu.be/g_j6ILT-X0k

Usage
-----

To run the script, use the following command:

Copy code

`git clone https://github.com/fxgt/UqamGradeChecker.git`

Copy code

`cd UqamGradeChecker`

Copy code

`chmod +x main.py`

Copy code

`python3 main.py`

Automation
----------

To automate this script on a Google Cloud VM, you can do the following:

1.  Create a Google Cloud VM instance and SSH into it.
2.  Install the necessary libraries and dependencies as specified in the Requirements section.
3.  Create a bash script to run the Python script at specified intervals using cron.
4.  To edit the crontab file, run the following command:

Copy code

`crontab -e`

1.  Add the following line to the crontab file to run the script every day at 12:00am:

Copy code

`* * * * * /path/to/UqamGradeChecker/main.py`

1.  Save the crontab file and exit. The script will now be automated and run every minutes.
