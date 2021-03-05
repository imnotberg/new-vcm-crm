from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include,path
from . import views
app_name = 'contact_management'

urlpatterns = [
	#PAGES
	path('test',views.test,name='test'),
	path('accounts',views.accounts,name='accounts'),
	#FEEDS
	path('accounts-feed',views.accounts_feed,name='accounts_feed'),
	path('account-feed/account-id/<account_id>',views.account_feed,name='account_feed'),
	path('contacts-feed',views.contacts_feed,name="contacts_feed"),
	path('contact-feed/contact-id/<contact_id>',views.contact_feed,name='contact_feed'),
	#CBV
	path('accounts/<pk>/detail/',views.AccountDetailView.as_view(),name='account_detail'),
	path('contacts/account/<account_id>/contact/<pk>/detail',views.ContactDetailView.as_view(),name='contact_detail'),
	path('account/<account_id>/invoice/<pk>/detail',views.InvoiceDetailView.as_view(),name='invoice_detail'),
	#ACTIONS
	path('accounts/<account_id>/contact/<contact_id>/make-primary',views.make_primary_contact,name='make_primary_contact'),
	path('contacts/<contact_id>/remove',views.remove_contact,name='remove_contact'),
	#OLD
	path('accounts/<pk>/update',views.AccountUpdateView.as_view(),name='account_update'),
	#FORM URLS
	path('note-create/<form_data>',views.note_create,name='note_create'),
	path('send-email-form/<form_data>',views.send_email_form,name='send_email_form'),
	path('add-contact/<form_data>',views.add_contact,name='add_contact'),
	#TABLES
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
'''
urlpatterns = [
	
	path('',views.index,name='index'),
	path('accounts',views.AccountListView.as_view(),name='account_list'),
	path('accounts/<pk>/detail/',views.AccountDetailView.as_view(),name='account_detail'),
	path('accounts/<pk>/update',views.AccountUpdateView.as_view(),name='account_update'),
	path('accounts/<account_id>/contact/<contact_id>/make-primary',views.make_primary_contact,name='make_primary_contact'),
	path('contacts/<contact_id>/remove',views.remove_contact,name='remove_contact'),
	path('contacts',views.ContactListView.as_view(),name='contact_list'),
	path('contacts/account/<account_id>/contact/<pk>/detail',views.ContactDetailView.as_view(),name='contact_detail'),
	path('contacts/account/<account_id>/contact/<pk>/update',views.ContactUpdateView.as_view(),name='contact_update'),
	path('leads/',views.LeadListView.as_view(),name='lead_list'),
	path('leads/<pk>/detail',views.LeadDetailView.as_view(),name='lead_detail'),
	path('leads/<pk>/delete',views.delete_lead,name='delete_lead'),
	path('leads/<pk>/convert',views.convert_lead,name='convert_lead'),
	path('leads/<pk>/update',views.LeadUpdateView.as_view(),name='lead_update'),
	path('items',views.ItemListView.as_view(),name='item_list'),
	path('item/<pk>/detail',views.ItemDetailView.as_view(),name='item_detail'),
	path('invoices',views.InvoiceListView.as_view(),name='invoice_list'),
	path('account/<account_id>/invoice/<pk>/detail',views.InvoiceDetailView.as_view(),name='invoice_detail'),
	path('account/<account_id>/new-order',views.InvoiceCreateView.as_view(),name='new_order'),
	path('sales-data',views.sales_data,name='sales_data'),
	path('note-create/<form_data>',views.note_create,name='note_create'),
	path('note-delete/<note_id>',views.note_delete,name='note_delete'),
	path('add-contact/<form_data>',views.add_contact,name='add_contact'),
	path('send-email-form/<form_data>',views.send_email_form,name='send_email_form'),
	path('logout',views.logout_request,name='logout'),
	path("login", views.login_request, name="login"),
	#FEEDS
	path('email-data',views.email_data,name='email_data'),
	#CHARTS
	path('sales-by-year-chart',views.sales_by_year_chart,name='sales_by_year_chart'),
	path('sales-by-month-year-chart/year/<year_id>',views.sales_by_month_year_chart,name='sales_by_month_year_chart'),
	path('sales-by-item-chart/item/<item_id>',views.sales_by_item_chart,name='sales_by_item_chart'),
	path('sales-by-month-chart/month/<month_id>',views.sales_by_month_chart,name='sales_by_month_chart'),
	] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
'''
