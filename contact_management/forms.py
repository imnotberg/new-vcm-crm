from django import forms
from django.forms import ModelForm
from contact_management.models import *

class CreateEmailCampaignForm(ModelForm):
	class Meta:
		model = EmailCampaign
		fields = ['date','subject','description','template','sg_template_on']
		def __init__(self,*args,**kwargs):
			super(CreateEmailCampaignForm,self).__init__(*args,**kwargs)
			for field in self.fields:
				self.fields[field].required = False





class EmailCampaignModalForm(forms.Form):
	campaign = forms.ChoiceField(choices=EmailCampaign.objects.filter(sent=False))
class AccountModalForm(ModelForm):
	class Meta:
		model = Account
		fields = '__all__'
	def __init__(self, *args, **kwargs):
		super(AccountModalForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].required = False
class ContactModalForm(ModelForm):
	class Meta:
		model = Contact
		fields = '__all__'
	def __init__(self, *args, **kwargs):
		super(ContactModalForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].required = False
class NoteForm(ModelForm):
	#user_choices = [(u.username,u.username) for u  in User.objects.all()]
	#user_choices.insert(0,(None,''))
	user_choices = [('','')]
	follow_up_type_choices = [('',''),('CALL','CALL'),('EMAIL','EMAIL'),('MAIL','MAIL')]
	contact_type_choices = [('',''),('CALL','CALL'),('EMAIL','EMAIL'),('MAIL','MAIL')]
	contact_type = forms.ChoiceField(required=False,choices=contact_type_choices)
	follow_up_user = forms.ChoiceField(required=False,choices=user_choices)
	follow_up_type = forms.ChoiceField(required=False,choices=follow_up_type_choices) 
	follow_up_date = forms.DateField(widget=forms.SelectDateWidget(),initial=datetime.now()+timedelta(days=21))
	class Meta:
		model = Note 
		fields = ['contact_type','note','follow_up','follow_up_user','follow_up_type','follow_up_date']
		widgets = {'follow_up_date':forms.SelectDateWidget(years=utils.YEAR_CHOICES),'follow_up_user':{'id':'user-id'},}
class EmailForm(forms.Form):
	subject = forms.CharField(max_length=2000,required=False)
	body = forms.CharField(widget=forms.Textarea(attrs={"rows":10,"cols":50}),required=False)
	template = forms.CharField(required=False,max_length=200)
	sg_template_on = forms.BooleanField(required=False)
	sg_template = forms.CharField(max_length=200,required=False)

class AddContactForm(ModelForm):
	class Meta:
		model = Contact 
		exclude = ["follow_up_date","account"]

	def __init__(self, *args, **kwargs):
		super(AddContactForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].required = False
		#self.fields['follow_up_date'].required = False


class EmailCampaignForm1(forms.Form):
	date = forms.DateField(widget=forms.SelectDateWidget(),initial=datetime.now())

class EmailCampaignForm2(forms.Form):
	description = forms.CharField(max_length=2000,required=False)
	subject = forms.CharField(max_length=2000,required=False)

class EmailCampaignForm3(forms.Form):
	sg_template_on = forms.BooleanField(required=False)
	
class EmailCampaignForm4(forms.Form):
	
	template = forms.CharField(max_length=500,required=False)