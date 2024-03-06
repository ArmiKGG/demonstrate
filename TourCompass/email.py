from djoser import email


class ActivationEmail(email.ActivationEmail):
    template_name = r'../templates/activate.html'
