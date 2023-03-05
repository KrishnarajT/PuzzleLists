# in this file we are going to send an email via gmail, using the environment variables, and app passwords thing in google. Using this,
# I can send anyone emails using Python. The following code is enough for sending a mail with a text message and a subject.
# this will only work on my Laptop, coz the Env variable is only stored here.

import os
import smtplib
from email.message import EmailMessage
import random

EMAIL_ADDRESS = 'puzzlelists@gmail.com'
EMAIL_PASSWORD  = None
OTP = random.randint(100000, 999999)

with open(os.path.join(os.getcwd(), 'src/PASSWORD.txt')) as f:
    EMAIL_PASSWORD = f.read()

def send_mail( To, OTP, Subject = 'OTP Verfication for your Account on Puzzlelists'):
    """
    :param To: The person's *Gmail* id that you are trying to send to.
    :param Subject: The subject of your mail
    :param Content: What it is that you want to send
    :return: 0 if failed or error encountered, 1 if successfully sent
    """
    message_content = 'Thank you for Signing up with Puzzlelists! Here is your OTP for verification.\nPlease enter this in the app to verify your account. \n' \
    + str(OTP) + \
    '\nRegards, Team Puzzlelist - Parth and Krishnaraj'
    
    
    if '@gmail.com' not in To or type(Subject) != str or type( message_content ) != str :
        print('Either the email address is not a gmail address, or the content and Subject is not a String')
        return 0
    
    # declaring a message instance
    msg = EmailMessage()
    msg[ 'Subject' ] = Subject
    msg[ 'From' ] = 'puzzlelists@gmail.com'
    msg[ 'To' ] = To
    msg.set_content( message_content )
    
    # sending the email, by creating an SMTP_SSL instance
    try:
        with smtplib.SMTP_SSL( 'smtp.gmail.com', 465 ) as smtp :
            smtp.login( EMAIL_ADDRESS, EMAIL_PASSWORD )
            smtp.send_message( msg )
        return 1
    except Exception as e:
        print(e)
        return 0
  
# Example

# for i in range(100):
#     print(send_mail('devanshusurana2003@gmail.com', OTP))
    