import imaplib
import email
import getpass
import re
import base64
import smtplib
from email.mime.text import MIMEText

user_email = ''
user_password = ''

gmail_connected = False
menu_count = -1

mail = imaplib.IMAP4_SSL('imap.gmail.com')

def encoded_words_to_text(encoded_words):
    try:
        encoded_word_regex = r'=\?{1}(.+)\?{1}([B|Q])\?{1}(.+)\?{1}='
        charset, encoding, encoded_text = re.match(encoded_word_regex, encoded_words).groups()
        if encoding is 'B':
            byte_string = base64.b64decode(encoded_text)
        elif encoding is 'Q':
            byte_string = quopri.decodestring(encoded_text)
        return byte_string.decode(charset)
    except Exception:
        return encoded_words

####################################################
############# GMAIL IMAP CONNECTION ################
####################################################

def input_user_credentials():
    global user_email, user_password

    print "Please enter your gmail address : "
    user_email = raw_input()
    print "please enter your gmail password : "
    user_password = getpass.getpass()
    connect_gmail_imap()

def connect_gmail_imap():
    global mail, gmail_connected
    mail.login(user_email, user_password)
    mail.select("INBOX")
    result2, new_messages = mail.search(None, '(UNSEEN)')
    gmail_connected = True
    print 
    print "Welcome " + user_email
    print "New Messages : " + str(len(new_messages[0].split()))

####################################################
############## SEND A SIMPLE EMAIL #################
####################################################

def send_simple_mail():
    global mail
    print 'Enter message of the email'
    msg = MIMEText(raw_input())
    print 'Enter subject of the email'
    msg['Subject'] = raw_input()
    print 'Enter the email to which you want to send the email : '
    to_email = raw_input()
    msg['To'] = to_email
    print 'Enter the CC leave blank if you do not need CC : '
    msg['CC'] = raw_input()
    msg['From'] = user_email

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(user_email, user_password)
    server.sendmail(user_email, to_email, msg.as_string())
    server.quit()

####################################################
############## OPEN A GIVEN EMAIL ##################
####################################################

def open_an_email():
    global mail
    esult, data = mail.uid('search', 'CHARSET', 'UTF-8', "ALL")
    list_of_ids = data[0].split()
    last_count_of_email = len(list_of_ids) - 1
    print 'Enter the number of mail you want to open : '
    mail_number = int(input()) - 1
    current_email_uid = list_of_ids[last_count_of_email - mail_number]
    result2, message_fetch = mail.uid('fetch', current_email_uid, '(RFC822)')
    raw_email = message_fetch[0][1]
    email_message = email.message_from_string(raw_email)
    print 
    print 'Subject: ' + encoded_words_to_text(email_message['subject'])
    print 'Sender: ' + email_message['from']
    print 'Date: ' + email_message['Date']

    attachment_count = 0

    for part in email_message.walk():
        if part.get('Content-Disposition') is None:
            continue
        attachment_count += 1

    if attachment_count != 0:
        print str(attachment_count) + ' attachments found'

    if email_message.is_multipart():
        for part in email_message.get_payload():

            text = None
            
            if part.get_content_charset() is None:
                # We cannot know the character set, so return decoded "something"
                text = part.get_payload(decode=True)
                continue

            charset = part.get_content_charset()

            if part.get_content_type() == 'text/plain':
                text = unicode(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')
            if part.get_content_type() == 'text/html':
                html = unicode(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')
            if text is not None:
                print
                print 'Content: ' + text.strip()
                print
    else:
        text = unicode(email_message.get_payload(decode=True), email_message.get_content_charset(), 'ignore').encode('utf8', 'replace')
        print 'Content: ' + text.strip()

####################################################
############## GET LAST N MESSAGES #################
####################################################

def get_last_n_messages():
    global mail
    print 'Enter number of emails to fetch : '
    n = int(input())
    result, data = mail.uid('search', 'CHARSET', 'UTF-8', "ALL")
    list_of_ids = data[0].split()
    last_count_of_email = len(list_of_ids) - 1
    for i in range(n):
        current_email_uid = list_of_ids[last_count_of_email - i]
        result2, message_fetch = mail.uid('fetch', current_email_uid, '(RFC822)')
        raw_email = message_fetch[0][1]
        email_message = email.message_from_string(raw_email)
        print 
        print 'Subject: ' + encoded_words_to_text(email_message['subject'])
        print 'Sender: ' + email_message['from']
        print 'Date: ' + email_message['Date']

        attachment_count = 0

        for part in email_message.walk():
            if part.get('Content-Disposition') is None:
                continue
            attachment_count += 1
        
        if attachment_count != 0:
            print str(attachment_count) + ' attachments found'

        if email_message.is_multipart():
            for part in email_message.get_payload():

                text = None
            
                if part.get_content_charset() is None:
                    # We cannot know the character set, so return decoded "something"
                    text = part.get_payload(decode=True)
                    continue

                if part.get_content_type() == 'text/plain':
                    charset = part.get_content_charset()
                    text = unicode(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')
                if text is not None:
                    print
                    print 'First sentence: ' + text.strip().split('\n')[0]
                    print
        


####################################################
##################### MENU #########################
####################################################

while menu_count != 0:
    print 
    if gmail_connected == False:
        print "To connect your gmail address please enter 1"
    elif gmail_connected == True:
        print "To get last N received messages enter 2"
        print "To send a message enter 3"
        print "To read a mail enter 4"
    print "To exit the app please enter 0"
    print

    menu_count = int(input())

    if gmail_connected == False:
        if menu_count == 1:
            input_user_credentials()
    elif gmail_connected == True:
        if menu_count == 2:
            get_last_n_messages()
        elif menu_count == 3:
            send_simple_mail()
        elif menu_count == 4:
            open_an_email()



