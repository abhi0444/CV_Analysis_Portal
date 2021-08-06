import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send(e_mail_sender,name,company,action,p):

    sender_address = ''         # paste your mail id
    sender_pass = ''            # paste your password
    receiver_address = e_mail_sender
    message = MIMEMultipart()
    if p==1:
        if action == 0:
            message['Subject'] = 'Not Shortlisted for further rounds in ' + company +' thanks for applying' #The subject line
            mail_content = "Hi " + name + " You are "+ 'Not Shortlisted for further rounds in ' + company +' thanks for applying'
        else:
            message['Subject'] = 'Shortlisted for Interview in ' + company   #The subject line
            mail_content = "Hi " + name + " You are Shortlizted for our PI round. We will reach you soon regarding further details"
    else:
        message['Subject'] = 'Error Can Not Open Your Resume '
        mail_content = "Hi " + name + " , you have to upadate resume link again on CV Analysis Portal "
    #The mail addresses and password
    #Setup the MIME
    message['From'] = sender_address
    message['To'] = receiver_address
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')