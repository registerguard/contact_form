"""
Example URLConf for a contact form.

Because the ``contact_form`` view takes configurable arguments, it's
recommended that you manually place it somewhere in your URL
configuration with the arguments you want. If you just prefer the
default, however, you can hang this URLConf somewhere in your URL
hierarchy (for best results with the defaults, include it under
``/contact/``).

"""

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

from contact_form.forms import ContactForm
from contact_form.rg_forms import DeliveryContactForm, ClassifiedsSearchContactForm, \
    FlagContactForm, WeddingForm
from contact_form.views import obituary, obituary_logout

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from recaptcha_django import captcha

def contact_form(request, form_class=ContactForm,
                 template_name='contact_form/contact_form.html',
                 success_url='/contact/sent/', login_required=False,
                 fail_silently=False, *args, **kwargs):
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
        form = form_class(data=request.POST, files=request.FILES, request=request, auto_id='fm_subscribe_%s', *args, **kwargs)
        # if check_captcha.is_valid is False:
        #     # Captcha is wrong show a error ...
        #     html_captcha = captcha.displayhtml(settings.RECAPTCHA_PUB_KEY, error = check_captcha.error_code)
        #     return render_to_response(template_name,
        #                       { 'form': form, 'html_captcha': html_captcha, },
        #                       context_instance=RequestContext(request))
        if form.is_valid():
            form.save(fail_silently=fail_silently)
            return HttpResponseRedirect(success_url)
        # html_captcha = captcha.displayhtml(settings.RECAPTCHA_PUB_KEY)
    else:
        form = form_class(request=request, auto_id='fm_subscribe_%s')
        # html_captcha = captcha.displayhtml(settings.RECAPTCHA_PUB_KEY)
    
    return render_to_response(
        template_name,
        {
            'form': form,
            # 'html_captcha': html_captcha,
            'google_recaptcha_site_key': settings.RECAPTCHA_PUB_KEY,
        },
        context_instance=RequestContext(request)
    )

def flag_comment_form(request, form_class=ContactForm,
                 template_name='contact_form/contact_form.html',
                 success_url='/contact/sent/', login_required=False,
                 fail_silently=False, *args, **kwargs):
    """
    This is 'flag_comment_form' method is identical to the 'contact_form' method
    immediately above except for the two 'form = ' lines since this is a 
    'hybrid' form that accepts keyword variables from the comments on DT pages 
    as well as form POST data. So we need to have different versions of the GET 
    and POST versions of the 'form' variable.
    """
    
    if login_required and not request.user.is_authenticated():
        return redirect_to_login(request.path)
    
    if request.method == 'POST':
        # Check the captcha
        check_captcha = captcha.submit(request.POST['recaptcha_challenge_field'], request.POST['recaptcha_response_field'], settings.RECAPTCHA_PRIVATE_KEY, request.META['REMOTE_ADDR'])
        form = form_class(data=request.POST, files=request.FILES, request=request, auto_id=False)
        if check_captcha.is_valid is False:
            # Captcha is wrong show a error ...
            html_captcha = captcha.displayhtml(settings.RECAPTCHA_PUB_KEY, error = check_captcha.error_code)
            return render_to_response(template_name,
                              { 'form': form, 'html_captcha': html_captcha, },
                              context_instance=RequestContext(request))
#             return HttpResponseRedirect('/url/error/')
        if form.is_valid():
            form.save(fail_silently=fail_silently)
            return HttpResponseRedirect(request.POST['refering_url'])
        html_captcha = captcha.displayhtml(settings.RECAPTCHA_PUB_KEY)
    else:
        # Check to see if request for the flag_comment_form came from a link somewhere,
        if request.META.has_key('HTTP_REFERER'):
            success_redirect = request.META['HTTP_REFERER']
        else:
            return HttpResponseRedirect('http://www.registerguard.com/')
            
        form = form_class(request=request, auto_id=False, initial={'cms_id': kwargs['cms_id'], 'comment_id': kwargs['comment_id'], 'refering_url': request.META['HTTP_REFERER']})
        html_captcha = captcha.displayhtml(settings.RECAPTCHA_PUB_KEY)
    return render_to_response(template_name,
                              { 'form': form, 'html_captcha': html_captcha, },
                              context_instance=RequestContext(request))

urlpatterns = patterns('',
#                        url(r'^/$',
#                            contact_form,
#                            name='contact_form'),
                       url(r'^delivery/$',
                           redirect_to, {
                               'url': 'http://services.registerguard.com/#become-a-carrier',
                               'permanent': True,
                           },
                           name='delivery_contact_form'),
                       url(r'^flag/(?P<cms_id>\d+)/(?P<comment_id>\d+)/$',
                           flag_comment_form, {
                               'form_class': FlagContactForm,
                               'template_name': 'contact_form/contact_form_flag.html'
                           },
                           name='contact_form_flag'),
                       url(r'^sent/$',
                           direct_to_template,
                           { 'template': 'contact_form/contact_form_sent.html' },
                           name='contact_form_sent'),
#                        url(r'^classifieds-search-feedback/$',
#                            contact_form, {
#                                'form_class': ClassifiedsSearchContactForm,
#                                'template_name': 'contact_form/contact_form_classifieds_search_feedback.html',
#                                'success_url': 'http://classifieds.registerguard.com/',
#                            },
#                            name='classifieds_feedback_contact_form'),
                       url(r'^wedding-announcement/$',
                            redirect_to, {
                                'url': 'https://www.registerguard.com/send-us-your-news',
                                'permanent': True,
                            }
                       ),
#                        url(r'^obituary/$',
#                            contact_form, { 'form_class': ObituaryForm, 
#                                'template_name': 'contact_form/contact_form_obituary.html',
#                                'success_url': 'http://blogs.registerguard.com/cms/index.php/static/pages/news-forms/', 
#                                'login_required': True },
#                            name='obituary'),
                       url(r'^obituary/$', login_required(obituary), name='obituary'),
                       url(r'^obituary/logout/$', obituary_logout, name='obituary_local'),
                       url(r'^response/$', direct_to_template, {
                               'template': 'contact_form/contact_form_response.html',
                               'extra_context': {
                                   'death_notice': True,
                               }
                           })
                       )
