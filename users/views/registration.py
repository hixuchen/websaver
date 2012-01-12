from django import forms
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from users.models.account import UserRegistrationForm
from django.shortcuts import render_to_response
from django.template import Context, loader

def index(request):
    t = loader.get_template('users/template/base.html')
    c = Context({
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
      user.save()
      return HttpResponseRedirect('/')
  else:
    form = UserRegistrationForm(auto_id="%s_id")

  c = { 'form': form }
  c.update(csrf(request))
  return render_to_response('users/template/signup.html', c)
