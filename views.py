"""
The def ``contact_form`` view below has been manually placed in the contact_form
urls.py file as per James Bennett's recommendation.
- JPH, 1/20/009  (Obama Day)
"""

"""
View which can render and send email from a contact form.

"""

from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import loader, Context, RequestContext
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth import logout
from contact_form.forms import ContactForm
from contact_form.rg_forms import DeathNoticeForm, ObituaryForm

def contact_form(request, form_class=ContactForm,
                 template_name='contact_form/contact_form.html',
                 success_url='/contact/sent/', login_required=False,
                 fail_silently=False):
    """
    Renders a contact form, validates its input and sends an email
    from it.
    
    To specify the form class to use, pass the ``form_class`` keyword
    argument; if no ``form_class`` is specified, the base
    ``ContactForm`` class will be used.
    
    To specify the template to use for rendering the form (*not* the
    template used to render the email message sent from the form,
    which is handled by the form class), pass the ``template_name``
    keyword argument; if not supplied, this will default to
    ``contact_form/contact_form.html``.
    
    To specify a URL to redirect to after a successfully-sent message,
    pass the ``success_url`` keyword argument; if not supplied, this
    will default to ``/contact/sent/``.
    
    To allow only registered users to use the form, pass a ``True``
    value for the ``login_required`` keyword argument.
    
    To suppress exceptions raised during sending of the email, pass a
    ``True`` value for the ``fail_silently`` keyword argument. This is
    **not** recommended.
    
    Template::
    
        Passed in the ``template_name`` argument.
        
    Context::
    
        form
            The form instance.
    
    """
    if login_required and not request.user.is_authenticated():
        return redirect_to_login(request.path)
    
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES, request=request)
        if form.is_valid():
            form.save(fail_silently=fail_silently)
            return HttpResponseRedirect(success_url)
    else:
        form = form_class(request=request)
    
    return render_to_response(template_name,
                              { 'form': form, },
                              context_instance=RequestContext(request)
                              )

def obituary(request):
    def arrangements_by(my_key):
        pretty_names = {
            u'musgroves': { 
                u'name': u'Musgrove Family Mortuary',
                u'city': u'Eugene',
            },
        }
        if hasattr(request, 'user'):
            return pretty_names.get(request.user.username, None)[my_key]
    
    if request.method == 'POST':
        form = DeathNoticeForm(request.POST)
        obit_form = ObituaryForm(request.POST)
        if form.is_valid() and obit_form.is_valid():
            # make, send e-mail
            subject = u'Death notice for %s' % (form.cleaned_data['deceased_last_name'])
            msg_template = loader.get_template('contact_form/contact_form_obituary.txt')
            msg_context = Context(form.cleaned_data)
            msg = msg_template.render(msg_context)
#             mail = EmailMessage(subject, msg, 'noreply@registerguard.com', bcc=['john.heasly@registerguard.com', 'christian.wihtol@registerguard.com',])
            mail = EmailMessage(subject, msg, 'noreply@registerguard.com', bcc=['john.heasly@registerguard.com','rob.denton@registerguard.com',])
            mail.send(fail_silently=False)
            
            return HttpResponseRedirect('/contact/response/')
    else:
        form = DeathNoticeForm(initial={'arrangements': arrangements_by('name'), 'arrangements_city': arrangements_by('city') })
        obit_form = ObituaryForm()
    
    return render_to_response('contact_form/contact_form_obituary.html',{
        'form': form, 
        'obit_form': obit_form },
        context_instance=RequestContext(request))

def obituary_logout(request):
    logout(request)
    return HttpResponseRedirect('/contact/obituary')
