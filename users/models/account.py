from django import forms
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
  user = models.OneToOneField(User)
  display_message = models.CharField(max_length=300)
  addr_line_1 = models.CharField(max_length=30)
  addr_line_2 = models.CharField(max_length=30)
  post_code = models.CharField(max_length=10)
  city = models.CharField(max_length=30)
  state = models.CharField(max_length=30)
  country = models.CharField(max_length=30)
  phone_number =  models.CharField(max_length=30)

  class Meta:
    app_label = "users"
    db_table = "profile"

class UserRegistrationForm(forms.Form):
  DUPLICATED_USERNAME_ERROR_MSG = "This username has been registered, please choose another one."
  DUPLICATED_EMAIL_ERROR_MSG = "This Email has been registered, please use another one."
  PASSWORD_CONFIRMATION_MISMATCH = "The passwords you entered don't match. Please try again."

  username = forms.CharField(label="User name", max_length=30)
  password = forms.CharField(label="Password", min_length=8, widget=forms.PasswordInput(render_value=True))
  cpassword = forms.CharField(label="Password confirmation", widget=forms.PasswordInput(render_value=False))
  first_name = forms.CharField(label="First name", max_length=30)
  last_name = forms.CharField(label="Last name", max_length=30)
  email = forms.EmailField(label="Email")

  def clean(self):
    self.validate_username()
    self.validate_password_confirmation()
    self.validate_email()
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
