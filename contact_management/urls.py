from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include,path
from . import views
app_name = 'contact_management'
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
	path('leads/<pk>/delete',views.delete_lead,name='delete_lead'),
	#path('leads/create',views.LeadCreateView.as_view(),name='leads_create'),
	path('note-create/<form_data>',views.note_create,name='note_create'),
	path('note-delete/<note_id>',views.note_delete,name='note_delete'),
	path('add-contact/<form_data>',views.add_contact,name='add_contact'),
	path('send-email-form/<form_data>',views.send_email_form,name='send_email_form'),
	path('logout',views.logout_request,name='logout'),
	path("login", views.login_request, name="login"),

	] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
