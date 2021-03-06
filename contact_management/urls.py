from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include,path
from . import views
app_name = 'contact_management'

urlpatterns = [
	#AUTHENTICATION
	path('logout',views.logout_request,name='logout'),
	path("login", views.login_request, name="login"),
	path('',views.index,name='index'),
	#PAGES
	path('test',views.test,name='test'),
	path('accounts',views.accounts,name='accounts'),
	path('email-campaign/campaign-id/<pk>',views.email_campaign_detail_view,name='email_campaign_detail_view'),
	path('email-campaign/campaign_id/<pk>/edit',views.EmailCampaignUpdateView.as_view(),name='email_campaign_update_view'),
	#FEEDS
	path('accounts-feed',views.accounts_feed,name='accounts_feed'),
	path('account-feed/account-id/<account_id>',views.account_feed,name='account_feed'),
	path('contacts-feed',views.contacts_feed,name="contacts_feed"),
	path('contact-feed/contact-id/<contact_id>',views.contact_feed,name='contact_feed'),
	path('campaign-ajax/campaign-id/<campaign_id>',views.campaign_ajax,name='campaign_ajax'),
	path('email-contacts-feed',views.email_contacts_feed,name='email_contacts_feed'),	
	#path('notes-main-account-feed/account-id/<account_id>',views.notes_main_account_feed,name='notes_main_account_feed'),	
	path('email-campaign-messages-feed/campaign-id/<campaign_id>/',views.email_campaign_messages_feed,name='email_campaign_messages_feed'),
	path('campaign-contacts/campaign-id/<campaign_id>',views.campaign_contacts,name='campaign_contacts'),
	#notes_main_add_note(request,contact_type,note,follow_up,follow_up_user,follow_up_type,follow_up_date_year,follow_up_date_month,follow_up_date_day):
	#path('notes-main-add-note/<account_id>/<contact_type>/<note>/<follow_up>/<follow_up_user>/<follow_up_type>/<follow_up_date_year>/<follow_up_date_month>/<follow_up_date_day>',views.notes_main_add_note,name='notes_main_add_note'),
	#CBV
	path('accounts/<pk>/detail/',views.AccountDetailView.as_view(),name='account_detail'),
	path('contacts/account/<account_id>/contact/<pk>/detail',views.ContactDetailView.as_view(),name='contact_detail'),
	path('account/<account_id>/invoice/<pk>/detail',views.InvoiceDetailView.as_view(),name='invoice_detail'),
	path('contacts/account/<account_id>/contact/<pk>/update',views.ContactUpdateView.as_view(),name='contact_update'),
	#ACTIONS
	path('ajax-add-contact-to-campaign/campaign_id/<campaign_id>/contact-type/<contact_type>/contact-pk/<contact_pk>',views.ajax_add_contact_to_campaign,name='ajax_add_contact_to_campaign'),
	path('add-contact-to-campaign-ajax/campaign-id/<campaign_id>/contact-type/<contact_type>/contact_pk/<contact_pk>',views.add_contact_to_campaign_ajax,name='add_contact_to_campaign_ajax'),
	path('accounts/<account_id>/contact/<contact_id>/make-primary',views.make_primary_contact,name='make_primary_contact'),
	path('contacts/<contact_id>/remove',views.remove_contact,name='remove_contact'),
	path('note-delete/<note_id>',views.note_delete,name='note_delete'),
	path('create-email-campaign',views.EmailCampaignFormView.as_view(),name='create_email_campaign'),
	path('send-email-campaign/campaign_id/<campaign_id>',views.send_email_campaign,name='send_email_campaign'),
	path('send-test-email-campaign/campaign_id/<campaign_id>',views.send_test_email_campaign,name='send_test_email_campaign'),
	path('datatable-test-email/campaign_id/<campaign_id>',views.datatable_send_test,name='datatable_send_test'),
	path('add-contact-to-campaign-from-datatable/campaign-id/<campaign_id>/contact-type/<contact_type>/contact-id/<contact_id>',views.add_contact_to_campaign_from_datatable,name='add_contact_to_campaign_from_datatable'),
	path('remove-contact-to-campaign-from-datatable/campaign-id/<campaign_id>/contact-type/<contact_type>/contact-id/<contact_id>',views.remove_contact_to_campaign_from_datatable,name='remove_contact_to_campaign_from_datatable'),

	#OLD
	path('accounts/<pk>/update',views.AccountUpdateView.as_view(),name='account_update'),
	path('email-contact-redirect/type/<contact_type>/id/<id>',views.email_contact_redirect,name='email_contact_redirect'),
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
