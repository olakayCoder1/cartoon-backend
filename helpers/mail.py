from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings



class MailServices():


    def forget_password_mail(*args ,**kwargs):
        receiver_email = kwargs['email']
        token = kwargs['token']
        uuidb64 = kwargs['uuidb64']
        redirect_url = kwargs['redirect_url']
        reset_link = f'{redirect_url}?token={token}&uuidb64={uuidb64}'
        html = render_to_string('accounts/password-reset-mail.html', {'activation_link': reset_link})
        plain_message = strip_tags(html)  
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [receiver_email]

        send_mail("Reset your password", plain_message, from_email, recipient_list, html_message=html)




    
    def account_activation_mail(*args ,**kwargs):
        receiver_email = kwargs['email']
        name = kwargs['name']
        html = render_to_string('email/welcome.html', { "name": name})
        plain_message = strip_tags(html)  
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [receiver_email]

        send_mail("Account activation", plain_message, from_email, recipient_list, html_message=html)


    def send_successfully_order_mail(*args ,**kwargs):
        receiver_email = kwargs['email']
        name = kwargs['name']
        order_id = kwargs['order_id']
        txn_id = kwargs['txn_id']
        water_mark = kwargs['water_mark']
        html = render_to_string('email/order_confirm.html', { "name": name , 'order_id' : order_id, 'txn_id' : txn_id , 'water_mark':water_mark})
        plain_message = strip_tags(html)  
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [receiver_email]

        send_mail("🎨 Your Custom Digital Portrait Order Update!", plain_message, from_email, recipient_list, html_message=html)


    def come_back_mail(*args ,**kwargs):
        receiver_email = kwargs['email']
        name = kwargs['name']
        html = render_to_string('email/order_confirm.html', { "name": name})
        plain_message = strip_tags(html)  
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [receiver_email]

        send_mail("Let's Make Your Return Extra Special 🎉", plain_message, from_email, recipient_list, html_message=html)



# MailServices.send_successfully_order_mail(email='olakaycoder1@gmail.com',name='Olanrewaju',order_id='o3874t3rekri4iuj3evsuy',txn_id='09283747gjbersufuriw3k',water_mark=True)
# MailServices.account_activation_mail(email='olakaycoder1@gmail.com',name='Olanrewaju')