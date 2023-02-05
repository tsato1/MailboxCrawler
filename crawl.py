import constants
import imaplib
import email
import base64
import re
from imap_tools.imap_utf7 import encode, decode

def extractEmail(text):
    pattern = r'Email:\[(.*)\]'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return '-no email-'

def extractName(text):
    pattern = r'Name:\'(.*)\''
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return '-no name'

def extractFurigana(text):
    pattern = r'Furigana:\"(.*)\"'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return '-no furigana-'

def crawl(enteredEventName, label): 
    user = constants.username
    password = constants.password

    imap_url = 'imap.gmail.com'
    my_mail = imaplib.IMAP4_SSL(imap_url)
    my_mail.login(user, password)
    my_mail.select('INBOX')
    my_mail.select(label)

    key = 'SUBJECT'
    value = encode(label)

    _, data = my_mail.search(None, key, value)
    mail_id_list = data[0].split()
    msgs = []

    for num in mail_id_list:
        typ, data = my_mail.fetch(num, '(RFC822)')
        msgs.append(data)

    resultMap = {}
    for msg in msgs[::-1]:
        for response_part in msg:
            if type(response_part) is tuple:
                my_msg = email.message_from_bytes((response_part[1]))

                decoded_bytes_subject = base64.b64decode(my_msg['subject'].split("?B?")[-1])
                decoded_string_subject = decoded_bytes_subject.decode("utf-8")

                registeredEventName = decoded_string_subject.split(maxsplit=1)[1]
                if (enteredEventName in registeredEventName):
                    if (resultMap.get(registeredEventName) == None):
                        resultMap[registeredEventName] = []
                        # print("title==="+registeredEventName)

                    for part in my_msg.walk():  
                        if part.get_content_type() == 'text/plain':
                            emailAddress = extractEmail(part.get_payload())
                            name = extractName(part.get_payload())
                            furigana = extractFurigana(part.get_payload())
                            resultMap[registeredEventName].append(name + "," + furigana + "," + emailAddress)

                            # print("result==="+name + "," + furigana + "," + emailAddress)
                    
                else:
                    continue
    
    return resultMap