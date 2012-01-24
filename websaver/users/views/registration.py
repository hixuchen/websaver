from django import forms
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from websaver.users.models.account import UserProfile, UserRegistrationForm
from django.shortcuts import render_to_response
from django.template import Context, RequestContext, loader
import datetime, random, sha
from websaver.util.email import send_template_email

def index(request):
    t = loader.get_template('websaver/template/base.html')
    c = RequestContext(request, {
        'latest_poll_list': 1,
    })
    return HttpResponse(t.render(c))

def register(request):
  if request.method == "POST":
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      email = form.cleaned_data['email']
      user = User.objects.create_user(username, email, password)
      user.first_name = first_name
      user.last_name = last_name
      user.is_active = False
      user.save()

      salt = sha.new(str(random.random())).hexdigest()[:5]
      activation_key = sha.new(salt + user.username).hexdigest()
      user_profile = UserProfile(user=user, activation_key=activation_key)
      user_profile.save()
      base_url = request.get_host()
      account_activation_link = "%s/user_id=%s&auth_key=%s" % (base_url, username, activation_key)
      subject = "Welcome to WebSaver! Please activate your account."
      template_var = { "username": username,
                       "account_activation_link": account_activation_link }
      send_template_email(subject, "randome@chen.com", [email], "websaver/template/emails/registration_activation_email.html", template_var)
      return HttpResponseRedirect('/')
  else:
    form = UserRegistrationForm(auto_id="%s_id")

  c = RequestContext(request, {
      'form': form,
  })
  c.update(csrf(request))
  t = loader.get_template('websaver/template/base.html')
  return HttpResponse(t.render(c))

def activate_registration(request):
  if request.user.is_authenticated():
    return HttpResponseRedirect('/myaccount')

  user_id = request.GET.get("user_id")
  activation_key = request.GET.get("activation_key")
  user = User.objects.filter(id=user_id)
  if len(user) != 0:
    user = user[0]
    user_profile = user.get_profile()
    if activation_key != user_profile.activation_key:
      # user_id and activation_key dont match
      return HttpResponseRedirect('/account_activation/error')
  else:
    # user_id does not exist error page
    return HttpResponseRedirect('/account_activation/error')

  if user.is_active:
    return HttpResponseRedirect('/login')
  else:
    user.is_active = True
    user.save()
    # account has been activated page.
  