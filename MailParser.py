import imaplib
import email
from configparser import ConfigParser


class MailParser:
    mail = ''

    # Log in Mail
    def login(self, host, username, password):
        # Connect to mail host
        self.mail = imaplib.IMAP4_SSL(host)
        self.mail.login(username, password)
        
        
    # Get video from last message
    def get_mail_attaches(self):

        # Check mail messages
        status, msgs = self.mail.select('INBOX')
        status, ids = self.mail.search(None, 'UNSEEN')

        photos = []
        videos = []
        music = []
        docs = []

        # Last message
        if ids != [b'']:

            # print(ids)
            last_email_id = ids[0].split()[-1]
            status, msg_data = self.mail.fetch(last_email_id, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])
            # typ, data = self.mail.store(last_email_id,'-FLAGS','\\Seen')

            # With attachments
            if msg.is_multipart():
                for part in msg.walk():
                    filename = part.get_filename()
                    content_type = part.get_content_maintype()
                    if filename:
                        # print(filename, '  ===  ', content_type)
                        file = part.get_payload(decode=True)

                        # File is image
                        if (content_type == 'image'): photos.append(file)

                        # File is video
                        elif (content_type == 'video'): videos.append(file)
                        
                        # File is audio
                        elif (content_type == 'audio'): music.append(file)

                        # Other types of file
                        else: docs.append(file)

        return photos, videos, music, docs


    # Log out from Mail
    def logout(self):
        self.mail.logout()



# eml = MailParser()
# eml.login()

# photos, videos, music, docs = eml.get_mail_attaches()