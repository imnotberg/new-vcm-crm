import django_tables2 as tables
from django_tables2 import TemplateColumn
from django_tables2.utils import A
from .models import Account,Contact,Lead,Item,Invoice

class AccountTable(tables.Table):
	name = tables.LinkColumn('contact_management:account_detail',args=[A('pk')])
		
	class Meta:
		atrrs:{"class":"table table-hover table-sm"}
		template_name = "django_tables2/bootstrap4.html"
		model = Account
		fields = ("id","name","tags","billing_city","follow_up_date","billing_state","billing_postcode","last_order__date","add_to_campaign")

class ContactTable(tables.Table):
	contact = tables.LinkColumn(accessor='full_name',verbose_name='Full Name',args=[A("account.pk"),A("pk")])
	account = tables.LinkColumn('contact_management:account_detail',args=[A('account__id')])

	class Meta:
		attrs:{"class":"table table-hover table-sm"}
		template_name = "django_tables2/bootstrap4.html"
		model = Contact
		fields = ("contact","account","account__state","account__tags")

	def render_name(self,value,record):
		return f"Your name here"

class LeadTable(tables.Table):
	first_name = tables.LinkColumn(verbose_name='First Name',args=[A("pk")])
	last_name = tables.LinkColumn(verbose_name='First Name',args=[A("pk")])
	account_name = tables.LinkColumn(verbose_name='First Name',args=[A("pk")])
	class Meta:
		attrs:{"class":"table table-hover table-sm"}
		template_name = "django_tables2/bootstrap4.html"
		model = Lead
		fields = ("first_name","last_name","account_name","phone","email","tags")

class ItemTable(tables.Table):
	item = tables.LinkColumn(verbose_name='Item',args=[A('pk')])
	description = tables.Column(verbose_name="Description")

	class Meta:
		attrs:{"class":"table table-hover table-sm"}
		template_name = "django_tables2/bootstrap4.html"
		model = Item
		fields = ("item","description")

class InvoiceTable(tables.Table):
	account = tables.LinkColumn('contact_management:account_detail',args=[A('account__pk')])
	class Meta:
		attrs:{"class":"table table-sm table-hover"}
		template_name = "django_tables2/bootstrap4.html"
		model = Invoice
		fields = ("account","date","total")

