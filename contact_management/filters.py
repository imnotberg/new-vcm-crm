import django_filters
from .models import Account,Contact,Lead


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