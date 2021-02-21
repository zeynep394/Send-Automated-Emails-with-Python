import smtplib,ssl


from string import Template
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

MY_ADDRESS = 'mail@mail.com'
PASSWORD = 'password'

def get_info(filename):
    contact_list=[]
    liste=[]
    mail=[]
    name=[]
    group=[]
    school=[]
    f=open(filename,"r")
    for s in f:
        contact_list.append(s)
    
    for i in contact_list:
        liste=i.split()
        
        mail.append(liste[0])
        name.append(liste[1])
        group.append(liste[2])
        school.append(liste[3])
    return name,mail,school,group

def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """
    
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def main():
    name, mail,school,group  = get_info('deneme.txt') # read contacts
    message_template = read_template('message.txt')

    # set up the SMTP server
    s = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465)
    s.ehlo()
    s.login(MY_ADDRESS, PASSWORD)

    # For each contact, send the email:
    for name, mail, group,school in zip(name, mail, group, school):
        msg = MIMEMultipart()       # create a message

        # add in the actual person name to the message template
       
        message = message_template.substitute(PERSON_NAME=name.title(),GROUP_NAME=group.title(),SCHOOL_NAME=school.title())

        #msg.attach(MIMEText(message, 'plain'))

        # Prints out the message body for our sake
        print(message)

        # setup the parameters of the message
        msg['From']=MY_ADDRESS
        msg['To']=mail
        msg['Subject']="Subject of the Mail"
        
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
    
        pdf = MIMEApplication(open("filename.pdf", 'rb').read())
        pdf.add_header('Content-Disposition', 'attachment', filename= "filename.pdf")
        msg.attach(pdf)
        
        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg
        
    # Terminate the SMTP session and close the connection
    s.quit()
    
if __name__ == '__main__':
    main()
get_info("deneme.txt")

