from email import message
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from django.utils.html import format_html

def sendEmail(subject, message, to):
    sender = 'faiz.meo179@gmail.com'
    send_mail(
        subject,
        message,
        sender,
        to,
        fail_silently=True
    )

def sendEmailOnUesrRegistration(obj):
    to =  obj.email
    courses = obj.student.subjects.all()
    subject = 'Account Successfully Regisratered'
    from_email = settings.EMAIL_HOST_USER
    text_content = "You are getting this email because you have attempted to create an account on School Management System. Kindly find the below information."
    html_content = render_to_string("email/user_registration_email.html", context={"obj":obj, "courses": courses})
    msg= EmailMultiAlternatives(subject, text_content, from_email, [to]) 
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        print("name : ",name)
        print("value : ",value)
        print("attrs : ",attrs)
        output = []
        if value and getattr(value, 'url', None):
            image_url = value.url
            file_name = str(value)
            output.append(f"<div><a href='{image_url}' target='_blank'><img src='{image_url}' alt='{file_name}' width='150' height='150' style='object-fit: cover; border:0.5px solid black;' /></a></div>")
        
        # removng the 'value' from render method will remove the link in admin image field
        # output.append(super(AdminFileWidget, self).render(name, value, attrs))
        output.append(super(AdminFileWidget, self).render(name, attrs))
        return mark_safe(f''.join(output))