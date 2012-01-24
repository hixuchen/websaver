from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.template import Context

def send_template_email(subject, from_email, to_emails, template, template_var):
  html_template = get_template(template)
  c = Context(template_var)
  html_content = html_template.render(c)
  mail = EmailMessage(subject, html_content, from_email, to_emails)
  mail.content_subtype = "html"
  mail.send()
