from django.contrib.auth.models import User
from django.core import serializers
from django.db import models
from django.db.models import JSONField
from django.db.models.functions import ExtractWeek, ExtractYear, ExtractMonth,Concat
from django.db.models.signals import post_save
#from django.contrib.postgres.fields import JSONField
from django.template.loader import render_to_string
from django.urls import reverse
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _
from anymail.signals import tracking
#from phonenumber_field.modelfields import PhoneNumberField
from pyzipcode import ZipCodeDatabase
from crm.settings import SENDGRID_API_KEY,DEFAULT_FROM_EMAIL
from . import utils
import pandas as pd 
from pandas import DataFrame as df
from functools import reduce
from django.db.models import Q,Sum,Avg,Count,Value,CharField
from datetime import datetime,timedelta
from picklefield.fields import PickledObjectField
import re,requests,json
from bs4 import BeautifulSoup
print('asssss',SENDGRID_API_KEY,DEFAULT_FROM_EMAIL)
# Create your models here.
class Profile(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.user.username}"

	def get_absolute_url(self):
		return reverse('contact_management:profile_detail',kwargs={'pk':self.pk})

class Account(models.Model):
	ACCOUNT_STATUS_CHOICE = (("open", "Open"), ("close", "Close"))
	name = models.CharField(pgettext_lazy("Name of Account", "Name"), max_length=64)
	email = models.EmailField(null=True,blank=True)
	phone = models.CharField(max_length=200,null=True,blank=True)	
	address_line = models.CharField(
        _("Address"), max_length=255, blank=True, null=True)
	billing_street = models.CharField(_("Street"), max_length=55, blank=True, null=True)
	billing_city = models.CharField(_("City"), max_length=255, blank=True, null=True)
	billing_state = models.CharField(_("State"), max_length=255, blank=True, null=True)
	billing_postcode = models.CharField(_("Post/Zip-code"), max_length=64, blank=True, null=True)
	website = models.URLField(_("Website"), blank=True, null=True)
	is_active = models.BooleanField(default=False)
	contact_name = models.CharField(pgettext_lazy("Name of Contact", "Contact Name"), max_length=120,blank=True,null=True)
	customer_type = models.CharField(max_length=2,null=True)
	mail_list = models.BooleanField(null=True,blank=True)
	tags = models.ManyToManyField('contact_management.Tag',related_name='account_tags')
	follow_up_date = models.DateField(null=True)
	def __str__(self):
		return f"{self.name}"

	def get_absolute_url(self):
		return reverse('contact_management:account_detail',kwargs={'pk':self.pk})
	@property
	def contacts(self):
		return Contact.objects.filter(account=self)
	@property
	def logo(self):
		lname = self.name.replace(' ','').lower()
		url = f"https://autocomplete.clearbit.com/v1/companies/suggest?query={lname}"
		page = requests.get(url)
		info = json.loads(page._content)
		if bool(info):
			return info[0].get('logo',None)
		else:
			return None
	@property
	def seo(self):
		return SEO(self.name,self.website)
	@property
	def all_notes(self):
		return Note.objects.filter(Q(account=self)|Q(contact__account=self)).order_by('-date')
	@property
	def invoices(self):
		return Invoice.objects.filter(account=self).order_by('-date')
	@property
	def sales(self):
		return sum([x.total for x in self.invoices])
	
	@property 
	def model(self):
		return self._meta.verbose_name
	@property
	def notes(self):
		return Note.objects.filter(Q(account=self))
	
	
	
class Contact(models.Model):
	first_name = models.CharField(_("First name"), max_length=255)
	last_name = models.CharField(_("Last name"), max_length=255)
	email = models.EmailField(null=True,blank=True)
	phone = models.CharField(max_length=200,null=True,blank=True) 
	description = models.TextField(blank=True, null=True)
	assigned_to = models.ForeignKey(User, related_name="contact_assigned_users",on_delete=models.CASCADE,blank=True,null=True)
	account = models.ForeignKey(Account,on_delete=models.CASCADE,related_name="contact_account")
	follow_up_date = models.DateField(null=True)
	def __str__(self):
		return f"{self.first_name} {self.last_name} {self.account.name}"

	def get_absolute_url(self):
		return reverse('contact_management:contact_detail',kwargs={'account_id':self.account.id,'pk':self.pk})

	@property
	def full_name(self):
		return f"{self.first_name} {self.last_name}"
	@property
	def notes(self):
		return Note.objects.filter(contact=self).order_by('-date')
	@property 
	def model(self):
		return self._meta.verbose_name
	def send_email(self,subject=None,body=None,sg_template_on=False,sg_template=None,template=None,campaign=None):
		from anymail.message import AnymailMessage
		from django.core.mail import send_mail,EmailMultiAlternatives
		from django.utils.html import strip_tags
		if template is not None:
			try:
				html_content = render_to_string(f"contact_management/{template}",self.__dict__)
			except:
				html_content = None
			note = template
		else:
			html_content = None
			note = body
		if html_content is not None:
			plain_content = strip_tags(html_content)
		else:
			plain_content = body		
		
		message = EmailMultiAlternatives(subject,plain_content,DEFAULT_FROM_EMAIL,[self.email])

		if sg_template_on == True:					
			message.template_id = sg_template
			template = sg_template
			note = f"SENDGRID TEMPLATE {sg_template}"		

		message.metadata = {"account_id":self.account.id,"contact_id":self.id,"template":template,"campaign":campaign,"email_source":"VCM","contact_type":"CONTACT","FIRST_NAME":self.first_name,"LAST_NAME":self.last_name,"ACCOUNT_NAME":self.account.name,'DATETIME':datetime.now().isoformat(),}

		if html_content is not None:
			message.attach_alternative(html_content,"text/html")
		message.track_clicks = True
		message.track_opens = True
		try:
			print('we are here')
			print(template)			
			message.send()
			print('we just sent??')
			status = message.anymail_status
			status.message_id
			print(status.message_id,'MID!!')

			n = Note(contact=self,date=datetime.now(),note=note,follow_up_date=datetime.now()+timedelta(days=14),contact_type='EMAIL')
			print(n,'NOTE')
			n.save()
			print(n.follow_up_date,'NOTE SAVED')
		except Exception as errors:
			print(errors,'this is the erro!')
			print('message did not send to',self)
class Lead(models.Model):
	title = models.CharField(pgettext_lazy("Treatment Pronouns for the customer", "Title"), max_length=64,null=True)
	first_name = models.CharField(_("First name"), null=True, max_length=255)
	last_name = models.CharField(_("Last name"), null=True, max_length=255)
	email = models.EmailField(null=True, blank=True)
	phone = models.CharField(max_length=200,null=True, blank=True)
	status = models.CharField(_("Status of Lead"), max_length=255, blank=True, null=True, choices=utils.LEAD_STATUS)
	source = models.CharField(_("Source of Lead"), max_length=255, blank=True, null=True)
	address_line = models.CharField(_("Address"), max_length=255, blank=True, null=True)
	street = models.CharField(_("Street"), max_length=55, blank=True, null=True)
	city = models.CharField(_("City"), max_length=255, blank=True, null=True)
	state = models.CharField(_("State"), max_length=255, blank=True, null=True)
	postcode = models.CharField(_("Post/Zip-code"), max_length=64, blank=True, null=True)
	website = models.CharField(_("Website"), max_length=255, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	assigned_to = models.ManyToManyField(User, related_name="lead_assigned_users")
	account_name = models.CharField(max_length=255, null=True, blank=True)
	opportunity_amount = models.DecimalField(_("Opportunity Amount"), decimal_places=2, max_digits=12, blank=True, null=True)
	created_by = models.ForeignKey(User, related_name="lead_created_by", on_delete=models.SET_NULL, null=True)
	created_on = models.DateTimeField(_("Created on"), auto_now_add=True)	
	tags = models.ManyToManyField('contact_management.Tag',related_name='lead_tags')
	is_active = models.BooleanField(default=False)
	follow_up_date = models.DateField(null=True)
	def __str__(self):
		return f"{self.first_name} {self.last_name} {self.account_name}"

	def get_absolute_url(self):
		return reverse('contact_management:lead_detail',kwargs={'pk':self.pk})
	@property
	def logo(self):
		lname = self.account_name.replace(' ','').lower()
		url = f"https://autocomplete.clearbit.com/v1/companies/suggest?query={lname}"
		page = requests.get(url)
		info = json.loads(page._content)
		if bool(info):
			return info[0].get('logo',None)
		else:
			return None
	@property
	def full_name(self):
		return f"{self.first_name} {self.last_name}"
	@property 
	def model(self):
		return self._meta.verbose_name
	def convert_lead(self):
		contact = Contact()
		account,created = Account.objects.get_or_create(name=self.name)
		contact_data = {"first_name":self.first_name,"last_name":self.last_name,"phone":self.phone,"email":self.email,}
		account_data = {"phone":self.phone,"email":self.email,"billing_city":self.city,"billing_street":self.street,"billing_state":self.state,"billing_postcode":self.postcode,"website":self.website,}
		for x,y in account_data.items():
			account.x = y 
		account.save()
		for x,y in contact_data.items():
			contact.x = y
		contact.account = account
		contact.save()
		return contact
	@property
	def seo(self):
		return SEO(self.account_name,self.website)
	@property 
	def notes(self):
		return Note.objects.filter(lead=self).order_by('-date')

	def send_email(self,subject=None,body=None,sg_template_on=False,sg_template=None,template=None,campaign=None):		
		from anymail.message import AnymailMessage
		from django.core.mail import send_mail,EmailMultiAlternatives
		from django.utils.html import strip_tags
		if template is not None:
			try:
				html_content = render_to_string(f"contact_management/{template}",self.__dict__)
			except:
				html_content = None
			note = template
		else:
			html_content = None
			note = body
		if html_content is not None:
			plain_content = strip_tags(html_content)
		else:
			plain_content = body		
		message = EmailMultiAlternatives(subject,plain_content,DEFAULT_FROM_EMAIL,[self.email])
		if sg_template_on == True:					
			message.template_id = sg_template
			template = sg_template	
		message.metadata = {"account_id":self.account_name,"contact_id":self.id,"template":template,"campaign":campaign,"email_source":"VCM","contact_type":"LEAD","FIRST_NAME":self.first_name,"LAST_NAME":self.last_name,"ACCOUNT_NAME":self.account_name,'DATETIME':datetime.now().isoformat()}
		if html_content is not None:
			message.attach_alternative(html_content,"text/html")
		message.track_clicks = True
		message.track_opens = True
		try:
			message.send()
			status = message.anymail_status
			status.message_id
			n = Note(lead=self,date=datetime.now(),note=note,follow_up_date=datetime.now() + timedelta(days=14),contact_type='EMAIL')
			n.save()
			print(f"email sent to {self}")
		except:
			print('message did not send to',self)
	

class Item(models.Model):
	item = models.CharField(max_length=200)
	description = models.TextField(blank=True,null=True)
	item_type = models.CharField(max_length=200)
	price = models.CharField(max_length=200)
	total_sales = models.FloatField(null=True)
	best_customers = PickledObjectField(null=True)

	def __str__(self):
		return f"{self.item}"
	def get_absolute_url(self):
		return reverse('contact_management:item_detail',kwargs={'pk':self.pk})
class Note(models.Model):
	account = models.ForeignKey('contact_management.Account',on_delete=models.CASCADE,null=True)
	date = models.DateField(null=True)
	note = models.TextField(null=True,blank=True)
	contact_type = models.CharField(max_length=200,null=True,blank=True,choices=utils.NOTECHOICES)
	contact = models.ForeignKey(Contact,on_delete=models.CASCADE,related_name='contact',null=True)
	follow_up_date = models.DateField(null=True)
	user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user',null=True)
	follow_up = models.BooleanField(default=True)
	lead = models.ForeignKey(Lead,on_delete=models.CASCADE,related_name='note_lead',blank=True,null=True)
	email_id = models.CharField(max_length=200,null=True,blank=True)

	def get_absolute_url(self):
		return reverse('contact_management:note_detail',kwargs={'pk':self.pk})
class Messages(models.Model):
	data = JSONField(null=True,blank=True)
class Invoice(models.Model):
	account = models.ForeignKey('contact_management.Account',on_delete=models.CASCADE,null=True)
	date = models.DateField(null=True)
	number = models.IntegerField(null=True)
	amount = models.FloatField(null=True)
	rep = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	total = models.FloatField(null=True)
	class Meta:
		ordering = ['-date']

	def __str__(self):
		return f"{self.date} {self.number}"

	def get_absoulte_url(self):
		return reverse('contact_management:invoice_detail',kwargs={'account_id':self.account.id,'pk':self.pk})

	

class Order(models.Model):
	account = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)	
	date = models.DateField(null=True)
	invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE,related_name='order_invoice',null=True)	

	def __str__(self):
		return f"{self.pk}"

	def get_absolute_url(self):
		try:
			return reverse('contact_management:order_detail', kwargs={'account_id':self.invoice.account.pk,'pk':self.pk,})
		except:
			return reverse('contact_management:account_detail',kwargs={'pk':self.account.pk,})

class EmailCampaign(models.Model):
	date = models.DateField(null=True,blank=True)
	subject = models.CharField(max_length=2000,null=True,blank=True)
	sg_template_on = models.BooleanField(default=False)
	description = models.CharField(max_length=200,null=True,blank=True)
	contacts = models.ManyToManyField(Contact)
	leads = models.ManyToManyField(Lead)
	accounts = models.ManyToManyField(Account)
	template = models.CharField(max_length=2000)
	sent = models.BooleanField(default=False)

	def __str__(self):
		return f"{self.date}: {self.description}"
	def get_absolute_url(self):
		return reverse('contact_management:email_campaign_detail_view',kwargs={'pk':self.pk})
	def send_test_email(self):
		if self.sent == False:
			subject = self.subject
			body = None
			if self.sg_template_on == True:
				sg_template = self.template
				template = None
			else:
				sg_template = None
				template = self.template
			c = Contact.objects.get(pk=26)
			c.send_email(subject,body,self.sg_template_on,sg_template,template,self.id)
			print(self.sg_template_on,sg_template)
			print('sg info ',SENDGRID_API_KEY,DEFAULT_FROM_EMAIL)
			print('successful testful')
	def send_emails(self):
		import time
		print('sending EMALSISS')
		email_info = SendGridInfoData.objects.get(pk=1).data
		sent = email_info[email_info.CAMPAIGN==str(self.pk)].TO.to_list()
		print(self.leads.exclude(email__in=sent).count(),'LEADS COUNT < 1390')
		if self.sent == False:
			subject = self.subject
			body = None
			if self.sg_template_on == True:
				sg_template = self.template
				template = None
			else:
				sg_template = None
				template = self.template
			for a in self.accounts.exclude(email__in=sent):
				if email_info[(email_info['TO']==a.email)&(email_info['CAMPAIGN']==str(self.pk))].empty==True:
					try:
						a.send_email(subject,body,self.sg_template_on,sg_template,template,self.id)
					except:
						print('not sent to ',a)
						pass
				time.sleep(1)
			for c in self.contacts.exclude(email__in=sent):
				if email_info[(email_info['TO']==c.email)&(email_info['CAMPAIGN']==str(self.pk))].empty==True:
					try:
						c.send_email(subject,body,self.sg_template_on,sg_template,template,self.id)
						print(f"sent email to {c}")		
					except:
						print('not sent to', c)
						pass
				else:
					print('already sent to ', c)
				time.sleep(1)
			for l in self.leads.exclude(email__in=sent):
				if email_info[(email_info['TO']==l.email)&(email_info['CAMPAIGN']==str(self.pk))].empty==True:
					try:
						l.send_email(subject,body,self.sg_template_on,sg_template,template,self.id)	
						print(f"sent email to {l}")
					except:
						print('not sent to l', l)
				else:
					print('already sent to ', l)
				time.sleep(1)
			self.sent = True
			self.save()
	@property
	def data(self):
		raw_data = SendGridInfoData.objects.get(pk=1)
		email_data = raw_data.messages
		sample = email_data[email_data['CAMPAIGN']==str(self.pk)]
		stats = sample_stats(sample).iloc[0]
		activity = raw_data.data[raw_data.data.CAMPAIGN==str(self.id)].sort_values(by=['DATETIME'],ascending=False)

		return {'messages':sample,'stats':stats,'activity':activity,}
	def targetify(self):
		targets = []
		for l in self.leads.all():
			targets.append( {'TYPE':'LEAD','ID':l.id,'ACCOUNT_NAME':l.account_name,'CONTACT_NAME':l.full_name})
		for c in self.contacts.all():
			targets.append({"TYPE":"CONTACT","ID":c.id,"ACCOUNT_NAME":c.account.name,"CONTACT_NAME":c.full_name})
		for a in self.accounts.all():
			targets.append({'TYPE':"ACCOUNT","ID":a.id,"ACCOUNT_NAME":a.name,"CONTACT_NAME":a.contact_name})

		return targets

	@property
	def targets(self):
		return self.targetify
	
		
class OrderItem(models.Model):
	order_item = models.ForeignKey(Item,on_delete=models.CASCADE,related_name='order_item_order_item')
	quantity = models.IntegerField(null=True,blank=True)
	price = models.FloatField()
	description = models.CharField(max_length=1000,null=True,blank=True)
	invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE,related_name='invoice_for_order_item',null=True,blank=True)
	total = models.FloatField(null=True)
	def __str__(self):
		return f"{self.order_item.item} {self.invoice.pk}"

	
class SendGridInfoData(models.Model):
	data = PickledObjectField(null=True)

	@property
	def messages(self):
		return self.data

	def stats(self,sample):
		data = sample
		stats = df({'SENT':[len(data)],'DELIVERED':[data.DELIVERED.sum()],"OPENED":[data.OPENED.sum()],"CLICKED":[data.CLICKED.sum()],"UNSUBSCRIBED":[data.UNSUBSCRIBED.sum()],"BOUNCED":[data.BOUNCED.sum()],"DEFERRED":[data.DEFERRED.sum()],"DROPPED":[data.DROPPED.sum()],"UNIQUE_OPENS":[sum(data.OPENED.value_counts().to_list())],"UNIQUE_CLICKS":[sum(data.CLICKED.value_counts().to_list())]},index=['STATS'])
		return stats


class Tag(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return f"{self.name}"

class EmailDataFull(models.Model):
	data = JSONField()

	def update_data(self):
		pass
class EmailData:
	def __init__(self):
		data = SendGridInfoData.objects.using('email').get(pk=1).data
		self.data = data[data.email_source=='VCM']

class EmailList:
	def __init__(self):
		self.list = pd.concat([df(Contact.objects.filter(email__isnull=False).exclude(email='').exclude(account__customer_type='DS').annotate(type=Value('CONTACT',CharField()),full_name=Concat('first_name',Value(' '),'last_name')).values('pk','first_name','last_name','email','account__id','account__name','type','full_name','account__billing_state')).rename(columns={'account__name':'account','account__billing_state':'state'}),df(Lead.objects.filter(email__isnull=False).exclude(email='').annotate(type=Value('LEAD',CharField()),full_name=Concat('first_name',Value(' '),'last_name')).values('pk','first_name','last_name','email','account_name','type','full_name','state')).rename(columns={'account_name':'account'}),df(Account.objects.filter(email__isnull=False).exclude(email='').exclude(customer_type='DS').annotate(type=Value('ACCOUNT',CharField())).values('pk','email','id','name','type','billing_state')).rename(columns={'name':'account','billing_state':'state'})]).drop_duplicates(subset=['email'],keep='first')		
		self.leads = self.list[self.list['type']=='LEAD']
		self.contacts = self.list[self.list['type']=='CONTACT']
		self.account = self.list[self.list['type']=='ACCOUNT']

class SEO:
	def __init__(self,company,website):
		ATTRIBUTES = ['description', 'keywords', 'Description', 'Keywords']
		entry = {'url':website,'company':company}
		self.url = website
		try:
			r = requests.get(self.url)
		except Exception as e:
			r = None
			print(f"Could not load page {self.url}")			
		if r is not None and r.status_code == 200:
			soup = BeautifulSoup(r.content,'html.parser')
			meta_list = soup.find_all("meta")
			for meta in meta_list:
				if "name" in meta.attrs:
					name = meta.attrs['name']
					if name in ATTRIBUTES:
						entry[name.lower()]=meta.attrs['content']
			self.info = df.from_dict(entry,orient='index').T
			try:
				keywords = self.info.keywords.values[0].split()
				print(keywords,'keywords!')
				self.keywords = keywords
			except:
				self.keywords = None
		else:
			self.info = df()

class Sales:
	def __init__(self,year=None,month=None,item=None,account=None):
		if year == None:
			year = datetime.now().year
		if month == None:
			month = datetime.now().month
		self.sales_by_year = Invoice.objects.annotate(year=ExtractYear('date')).order_by('year').values('year').annotate(sales=Sum('total'))
		self.sales_by_account = Invoice.objects.order_by('account').values('account__id','account__name').annotate(sales=Sum('total')).order_by('-sales')
		self.sales_by_account_year = Invoice.objects.annotate(year=ExtractYear('date')).filter(year=year).order_by('account').values('account__id','account__name').annotate(sales=Sum('total')).order_by('-sales')
		self.year_sales = Invoice.objects.annotate(year=ExtractYear('date'),month=ExtractMonth('date')).order_by('year').filter(year=year).values('month').annotate(sales=Sum('total'))
		self.month_sales = Invoice.objects.annotate(year=ExtractYear('date'),month=ExtractMonth('date')).order_by('year','month').filter(year=year,month=month).values('year','month').annotate(sales=Sum('total'))
		self.month_sales_by_year = Invoice.objects.annotate(year=ExtractYear('date'),month=ExtractMonth('date')).order_by('year','month').filter(month=month).values('year').annotate(sales=Sum('total'))
		self.month_sales_by_year_account = Invoice.objects.annotate(month=ExtractMonth('date')).filter(month=month).order_by('account').values('account__id','account__name').annotate(sales=Sum('total')).order_by('-sales')
		self.sales_by_item = OrderItem.objects.order_by('order_item').values('order_item__item').annotate(sales=Sum('total')).values('order_item__item','sales').order_by('-sales')
		self.sales_by_item_by_year = OrderItem.objects.filter(order_item=item).annotate(year=ExtractYear('invoice__date')).order_by('order_item','year').values('order_item__item','year').annotate(sales=Sum('total')).values('year','sales').order_by('year')
		self.sales_by_item_by_account = OrderItem.objects.filter(order_item=item).order_by('invoice__account').values('invoice__account__id','invoice__account__name').annotate(sales=Sum('total')).order_by('-sales')
		self.sales_by_customer = Invoice.objects.filter(account=account)



#SIGNALS
@receiver(post_save, sender=Note)
def note_follow_up_date(sender, instance, **kwargs):
	if instance.account is not None and instance.follow_up_date is not None:
		instance.account.save()
		print('saved account!')
	elif instance.contact is not None and instance.follow_up_date is not None:
		instance.contact.follow_up_date = instance.follow_up_date
		instance.contact.save()
	elif instance.lead is not None and instance.follow_up_date is not None:
		instance.lead.follow_up_date = instance.follow_up_date
		instance.lead.save()
@receiver(post_save,sender=Messages)
def messages_update(sender,instance,**kwargs):
	print("vcm messages saved")
@receiver(tracking)
def handle_bounce(sender, event, esp_name, **kwargs):
	def pandafy(event):		
		info = {k:v for k,v in event.__dict__.items() if k!='esp_event' and k!='metadata'}
		for k,v in event.__dict__['esp_event'].items():
			info[k]=v
		for k in ['account_id','contact_id','template']:
			try:
				info[k]=event.__dict__['metadata'][k]
			except:
				info[k]=None		

		return df.from_dict(info,orient='index').T		
	
	data,created = SendGridInfoData.objects.get_or_create(pk=1)
	if created == True:
		data.save()
	if df(pandafy(event)).empty == False:
		data.data = data.data.append(pandafy(event),ignore_index=True)
	data.save()
def sample_stats(sample):
	messages = sample
	sent = len(messages)
	delivered = messages.DELIVERED.sum()
	opens = messages.OPENED.sum()
	clicks = messages.CLICKED.sum()
	bounces = messages.BOUNCED.sum()
	unsubscribes = messages.UNSUBSCRIBED.sum()
	unique_opens = len(messages[messages['OPENED']>0])
	unique_clicks = len(messages[messages['CLICKED']>0])
	if sent > 0:
		pct_unique_opens = unique_opens/sent
		pct_unique_clicks = unique_clicks/sent
		pct_bounce = bounces/sent
		pct_unsubscribe = unsubscribes/sent
		pct_delivered = delivered/sent 
	else:
		pct_unique_opens = 0
		pct_unique_clicks = 0
		pct_bounce = 0
		pct_unsubscribe = 0
		pct_delivered = 0
	return df([[sent,delivered,opens,clicks,bounces,unsubscribes,unique_opens,unique_clicks,pct_unique_clicks,pct_unique_opens,pct_bounce,pct_unsubscribe,pct_delivered]],columns=['sent','delivered','opens','clicks','bounces','unsubscribes','unique_opens','unique_clicks','pct_unique_clicks','pct_unique_opens','pct_bounce','pct_unsubscribe','pct_delivered'])