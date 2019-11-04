import email
import smtplib
import imaplib


if __name__ == '__main__':
    class Email:
        login = 'login@gmail.com'
        password = 'qwerty'
        subject = 'Subject'
        recipients = ['vasya@email.com', 'petya@email.com']
        message = 'Message'
        header = None

        def send_message(self, login, password, recipients, subject, message, gmail_smtp="smtp.gmail.com"):
            msg = email.MIMEMultipart()
            msg['From'] = login
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = subject
            msg.attach(email.MIMEText(message))
            ms = smtplib.SMTP(gmail_smtp, 587)
            ms.ehlo()  # identify ourselves to smtp gmail client
            ms.starttls()  # secure our email with tls encryption
            ms.ehlo()  # re-identify ourselves as an encrypted connection
            ms.login(login, password)
            ms.sendmail(login, ms, msg.as_string())
            ms.quit()

        def recieve_message(self, login, password, header, gmail_imap="imap.gmail.com"):
            mail = imaplib.IMAP4_SSL(gmail_imap)
            mail.login(login, password)
            mail.list()
            mail.select("inbox")
            criterion = '(HEADER Subject "%s")' % header if header else 'ALL'
            result, data = mail.uid('search', None, criterion)
            assert data[0], 'There are no letters with current header'
            latest_email_uid = data[0].split()[-1]
            result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
            raw_email = data[0][1]
            email_message = email.message_from_string(raw_email)
            mail.logout()
