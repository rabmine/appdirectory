'''
Classes to handle email it functionality
'''
from django import forms
from django.forms.widgets import Textarea
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from app.models import Application
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.template.context import RequestContext

class EmailForm(forms.Form):
    name = forms.CharField(label="Your Name")
    your_email = forms.EmailField(label="Your Email")
    recipent_email = forms.EmailField(label="E-mail ID of recipient")
    message = forms.CharField(widget=Textarea())



class EmailItView(FormView):
    form_class = EmailForm
    template_name = 'email.html'
    
    def _get_app(self):
        app_id = int(self.kwargs['app_id'])
        return Application.objects.get(application_id=app_id)
    
    def get_context_data(self, **kwargs):
        context = super(EmailItView, self).get_context_data(**kwargs)
        context['app'] = self._get_app()
        return context
    
    def get_success_url(self):
        app = self._get_app()
        return reverse('app_detail_slug', args=[app.application_id, app.slug()])
    
    def form_valid(self, form):
        your_mail = form.cleaned_data['your_email']
        recipent_mail = form.cleaned_data['recipent_email']
        name = form.cleaned_data['name']
        
        context = {
                   'name' : name,
                   'mail' : your_mail,
                   'message' : form.cleaned_data['message'],
                   'app' : self._get_app(),
                   }
        
        txt_message = render_to_string('site/mail.txt', context, RequestContext(self.request)) 
        html_msg = render_to_string('site/mail.html', context, RequestContext(self.request))
        
        
        mail = EmailMultiAlternatives('Checkout this app', txt_message, 
                  "%s <%s>" % (name, your_mail), [recipent_mail])
        mail.attach_alternative(html_msg, "text/html")
        mail.send(fail_silently=False)
        
        return super(EmailItView, self).form_valid(form)
