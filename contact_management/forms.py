from django import forms
from django.forms import ModelForm
from contact_management.models import *

class NoteForm(ModelForm):
	user_choices = [(u.username,u.username) for u  in User.objects.all()]
	user_choices.insert(0,(None,''))
	follow_up_type_choices = [('',''),('CALL','CALL'),('EMAIL','EMAIL'),('MAIL','MAIL')]
	follow_up_user = forms.ChoiceField(required=False,choices=user_choices)
	follow_up_type = forms.ChoiceField(required=False,choices=follow_up_type_choices) 
	follow_up_date = forms.DateField(widget=forms.SelectDateWidget(),initial=datetime.now()+timedelta(days=21))
	class Meta:
		model = Note 
		fields = ['contact_type','note','follow_up','follow_up_user','follow_up_type','follow_up_date']
		widgets = {'follow_up_date':forms.SelectDateWidget(years=utils.YEAR_CHOICES)}
