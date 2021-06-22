import imaplib
import email
from configparser import ConfigParser


class MailParser:
    # Read config file
    config = ConfigParser()
    config.read("./mailConf.ini")

    # Configs for mail authorization
    host = config['MailService']['host']
    username = config['MailService']['username']
    password = config['MailService']['password']

    # Connect to mail host
    mail = imaplib.IMAP4_SSL(host)

    # Log in Mail
    def login(self):
        self.mail.login(self.username, self.password)

    # print(server)
    # print(port)
    # print(username)
    # print(password)

    # Get video from last message
    def get_msg_video(self):

        # Check mail messages
        status, msgs = self.mail.select('INBOX')
        status, ids = self.mail.search(None, 'UNSEEN')
        # print(ids)

        # Last message
        if ids != [b'']:
            # print(ids)
            last_email_id = ids[0].split()[-1]
            status, msg_data = self.mail.fetch(last_email_id, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])
            # typ, data = self.mail.store(last_email_id,'-FLAGS','\\Seen')

            # With attachments
            if msg.is_multipart():
                # print('multi')
                for part in msg.walk():
                    # print('part')
                    # content_type = part.get_content_type()
                    filename = part.get_filename()
                    if filename:
                        # print(filename)
                        msg_video = part.get_payload(decode=True)
                        return filename, msg_video
                    
        return '', b''



    # Log out from Mail
    def logout(self):
        self.mail.close()
        self.mail.logout()



# eml = MailParser()
# filename, msg_video = eml.get_msg_video()
# if filename:
#     with open(filename, 'wb') as mail_file:
#         mail_file.write(msg_video)