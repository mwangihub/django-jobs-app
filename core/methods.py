'''
methods.py have simple functions that reduces the code repitation
'''
from django.conf import settings
'''
get_current_site to be used in deployement
for this case domain was attached to Job instace to mimic dynamics of domain name changes
'''
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


# Sub methods
def get_rendered_html(template_name, context={}):
    html_content = render_to_string(template_name, context)
    return html_content


# Exported methods
def send_email(subject,
               html_content,
               text_content=None,
               from_email=None,
               recipients=[],
               attachments=[],
               bcc=[],
               cc=[]):
    # send email to user with attachment
    if not from_email:
        from_email = settings.DEFAULT_FROM_EMAIL
    if not text_content:
        text_content = ''
    email = EmailMultiAlternatives(subject,
                                   text_content,
                                   from_email,
                                   recipients,
                                   bcc=bcc,
                                   cc=cc)
    email.attach_alternative(html_content, "text/html")
    for attachment in attachments:
        # Example: email.attach('design.png', img_data, 'image/png')
        email.attach(*attachment)
    email.send()


def send_mass_mail(data_list):
    for data in data_list:
        template = data.pop('template')
        context = data.pop('context')
        html_content = get_rendered_html(template, context)
        data.update({'html_content': html_content})
        send_email(**data)