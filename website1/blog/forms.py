# -*- coding: utf-8 -*-
from django import forms

TOPIC_CHOICES = (

    ('bug', 'Bug report'),
    ('general', 'General enquiry'),
    ('suggestion', 'Suggestion'),
)

class ContactForm(forms.Form):
    topic = forms.ChoiceField(choices=TOPIC_CHOICES) #选择框
    message = forms.CharField(initial="Replace with your feedback")#设置初始值
    sender = forms.EmailField(required=False)
class AddForm(forms.Form):
    a = forms.IntegerField()
    b = forms.IntegerField()
class movieForm(forms.Form):
    name = forms.CharField()
class loginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()
    email=forms.CharField()

