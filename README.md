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

To use this script, you will need to create a file named `creds.py` in the same directory as the script. This file should contain the following variables:

Copy code

`identifiant = '<your UQAM student ID>'
motDePasse = '<your UQAM password>'
email_recever = '<the email address that will receive the notification>'`

Usage
-----

To run the script, use the following command:

Copy code

`python script.py`

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

`0 0 * * * /path/to/bash/script.sh`

1.  Save the crontab file and exit. The script will now be automated and run daily at 12:00am
