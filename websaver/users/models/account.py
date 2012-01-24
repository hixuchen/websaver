from django import forms
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
  user = models.OneToOneField(User)
  activation_key = models.CharField(max_length=40)
  display_message = models.CharField(max_length=300, blank=True)
  city = models.CharField(max_length=30, blank=True)
  state = models.CharField(max_length=30, blank=True)
  country = models.CharField(max_length=30, blank=True)
  phone_number =  models.CharField(max_length=30, blank=True)

  class Meta:
    app_label = "users"
    db_table = "profile"

class UserRegistrationForm(forms.Form):
  DUPLICATED_USERNAME_ERROR_MSG = "This username has been registered."
  DUPLICATED_EMAIL_ERROR_MSG = "This Email has been registered."
  PASSWORD_CONFIRMATION_MISMATCH = "The passwords you entered don't match."

  username = forms.CharField(label="User name",
                             max_length=20,
                             error_messages={'required': 'Username is required.'})
  password = forms.CharField(label="Password", min_length=8, 
                             widget=forms.PasswordInput(render_value=True),
                             error_messages={'required': 'Password is required.'})
  cpassword = forms.CharField(label="Password confirmation",
                              widget=forms.PasswordInput(render_value=False))
  first_name = forms.CharField(label="First name", max_length=30)
  last_name = forms.CharField(label="Last name", max_length=30)
  email = forms.EmailField(label="Email", error_messages={'required': 'Please enter your email'})

  def clean(self):
    self.validate_username()
    self.validate_password_confirmation()
#    self.validate_email()
    return self.cleaned_data

  def validate_username(self):
    user_name = self.cleaned_data.get("username")
    user = User.objects.filter(username=user_name)
    if len(user) > 0:
      self._errors["username"] = self.error_class([self.DUPLICATED_USERNAME_ERROR_MSG])
      del self.cleaned_data["username"]

  def validate_password_confirmation(self):
    if self.cleaned_data.get("password") != self.cleaned_data.get("cpassword") and self.cleaned_data.get("cpassword"):
      self._errors["cpassword"] = self.error_class([self.PASSWORD_CONFIRMATION_MISMATCH])
      del self.cleaned_data["cpassword"]

  def validate_email(self):
    email = self.cleaned_data.get("email")
    email_addr = User.objects.filter(email=email)
    if len(email_addr) > 0:
      self._errors["email"] = self.error_class([self.DUPLICATED_EMAIL_ERROR_MSG])
      del self.cleaned_data["email"]

  def haha(self):
    return "<h1>jj<h1>"