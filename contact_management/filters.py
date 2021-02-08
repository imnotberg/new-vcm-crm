import django_filters
from .models import Account,Contact,Lead, Item,Invoice


class AccountFilter(django_filters.FilterSet):
	class Meta:
		model = Account
		fields = ['name','id','billing_city','billing_state','tags']


class ContactFilter(django_filters.FilterSet):
	class Meta:
		model = Contact
		fields = ['first_name','last_name','account__name','account__billing_state','account__tags']

class LeadFilter(django_filters.FilterSet):
	class Meta:
		model = Lead
		fields = ['first_name','last_name','tags']

class ItemFilter(django_filters.FilterSet):
	description = django_filters.CharFilter(label='Item',field_name='description',lookup_expr='icontains')
	item = django_filters.TypedChoiceFilter(label='Item',field_name='item',choices=[('','')])
	class Meta:
		model = Lead
		fields = ['item','description']

class InvoiceFilter(django_filters.FilterSet):
	class Meta:
		model = Invoice
		fields = '__all__'
