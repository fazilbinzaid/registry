from django.core.mail import EmailMultiAlternatives
import threading
import hashlib
from django.conf import settings
from email.mime.text import MIMEText

# custom imports
from src.accounts.models import *

# todo
# LINK = 'http://128.199.76.148/'
# LINK = 'http://192.168.1.111:3000/'
LINK = 'http://139.59.72.184/'
DEMO_MANAGER = 'manager.vja@gmail.com'


def send_simple_message(subject, body, from_mail, recipient_list, html=None):
    """
    Email sending with text and template in the body.
    """
    subject, from_email, to = subject, from_mail, recipient_list
    text_content = body
    html_content = html
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    if html:
        msg.attach_alternative(html_content, "text/html")
    msg.content_subtype = "html"
    msg.send()


class EmailThread(threading.Thread):

    def __init__(self, subject, body, from_email, recipient_list,
                 fail_silently, html):
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.html = html
        threading.Thread.__init__(self)

    def run(self):
        if self.html is None:
            send_simple_message(self.subject, self.body, self.from_email,
                self.recipient_list)
        else:
            send_simple_message(self.subject, self.body, self.from_email,
                self.recipient_list, html=self.html)


def thread_mail(subject, body, from_email, recipient_list,
                fail_silently=False, html=None, *args, **kwargs):
    EmailThread(subject, body, from_email, recipient_list, fail_silently,
                html).start()

def apply_leave_mail(user, leave):
    if leave.daytype == 'FL':
        subject = 'Leave Application - %s %s to %s' \
            % (user.first_name,
                leave.from_date.strftime("%d-%b-%y"),
                leave.to_date.strftime("%d-%b-%y"))

    else:
        subject = 'Halfday Leave Application - %s on %s %s' \
            % (user.first_name, leave.date.strftime("%d-%b-%y"),
                leave.halfdaytype)
    link = ''.join([LINK, 'authentication/after_login/'])
    message = 'You have one new leave request.%s' % link
    from_mail = user.email
    partners = Account.objects.filter(role='P')
    partner_mail_list = [partner.email for partner in partners]
    for p in partner_mail_list:
        thread_mail(subject, message, from_mail, [p])


def format(date):
    return date.strftime("%d-%b-%Y")


def leave_approved_mail(leave):
    subject = '%s Leave Approved' % (leave.person_applied.first_name)
    if leave.daytype == 'FL':
        message = """%s's leave from %s to %s has been approved by %s.
        Note: %s""" % (leave.person_applied.first_name, format(leave.from_date),
            format(leave.to_date), leave.person_approved.first_name, leave.note)
    else:
        message = """%s's halfday leave %s %s has been approved by %s.
        Note: %s""" % (leave.person_applied.first_name, format(leave.date),
                       (leave.get_datatype_display()), leave.person_approved.first_name, leave.note)
    from_mail = leave.person_approved.email

    partners = Account.objects.filter(role__code='P')
    partner_mail_list = [partner.email for partner in partners]

    applied_person_list = [leave.person_applied.email]

    to_mail_list = partner_mail_list + ACCOUNTS_MAIL + applied_person_list

    thread_mail(subject, message, from_mail, to_mail_list)



def reset_password(email):
    subject = 'Password Reset-VJA'
    email = email.encode('utf-8')
    key = settings.SECRET_KEY.encode('utf-8')
    hash_object = hashlib.sha512(email+key)
    key = hash_object.hexdigest()
    account_id = Account.objects.get(email=email).id
    link = ''.join([LINK, 'forgotpassword/', str(account_id), '/', key])
    message = 'Reset Link'
    html = '''<p>Please click on the <strong>link</strong> below to reset your password for VJA.</p>
        <br>Reset link : <a href="{0}">{0}</a>'''.format(link)
    from_mail = DEMO_MANAGER
    mail_list = [email]

    thread_mail(subject, message, from_mail, mail_list, fail_silently=False,
                html=html)
