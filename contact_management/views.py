from django_filters.views import FilterView
from django_tables2.config import RequestConfig
from django_tables2.views import SingleTableMixin
from django.contrib.auth import logout,authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect,render
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    TemplateView,
    UpdateView,
    View,
)
from .filters import AccountFilter,ContactFilter,LeadFilter
from .forms import NoteForm,EmailForm,AddContactForm
from .models import *
from .tables import AccountTable,ContactTable,LeadTable
from .utils import get_value,login_url

# Create your views here.

def index(request):
	context = {

	}
	return render(request,'contact_management/index.html')

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():         
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            profile = Profile.objects.get(user=user)
            if user is not None:
                login(request, user)
                return redirect('contact_management:index')
            else:
                pass
        else:
            pass
    form = AuthenticationForm()
    return render(request,'contact_management/login.html',{'form':form,})

def logout_request(request):
    logout(request)
    return redirect('contact_management:login')

class AccountListView(LoginRequiredMixin,SingleTableMixin, FilterView):
    login_url = 'contact_management:login'
    model = Account
    table_class = AccountTable
    template_name = 'contact_management/account_list.html'
    filterset_class = AccountFilter

    def get_context_data(self,**kwargs):        
        context = super().get_context_data(**kwargs)
        table = self.get_table()
        RequestConfig(self.request, paginate={"per_page": 20}).configure(table)
        context['filter']=AccountFilter(self.request.GET,queryset=self.get_queryset())  

        return context

class AccountDetailView(LoginRequiredMixin,DetailView):
    login_url = 'contact_management:login'
    model = Account
    form_class = NoteForm
    template_name = 'contact_management/account_detail.html'

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            return JSONResponse('Success',safe=False, **response_kwargs)
        else:
            return super(AccountDetailView,self).render_to_response(context, **response_kwargs)
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['account'] = Account.objects.get(pk=self.kwargs['pk'])
        context['note_form'] = NoteForm
        context['email_form'] = EmailForm
        context['add_contact_form'] = AddContactForm
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
   
    
    

class AccountUpdateView(LoginRequiredMixin,UpdateView):
    model = Account
    fields = '__all__'

    def get_form(self,form_class=None):
        form = super(AccountUpdateView, self).get_form(form_class)
        form.fields['email'].required=False
        form.fields['phone'].required=False
        form.fields['billing_street'].required=False
        form.fields['billing_city'].required=False
        form.fields['billing_state'].required=False
        form.fields['billing_postcode'].required=False
        form.fields['contact_name'].required=False
        form.fields['customer_type'].required=False
        form.fields['tags'].required=False
        form.fields['follow_up_date'].required=False

        return form

    def get_context_data(self,**kwargs):
        context = super().get_context_data()
        note_form = NoteForm

        return context

    
@login_required(login_url='contact_management:login')
def make_primary_contact(request,account_id,contact_id):
    account = Account.objects.get(pk=account_id)
    contact = Contact.objects.get(pk=contact_id)
    account.contact_name = contact.full_name
    account.save()
    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url='contact_management:login')
def remove_contact(request,contact_id):
    contact = Contact.objects.get(pk=contact_id)
    contact.delete()

    return redirect(request.META['HTTP_REFERER'])
    


class ContactListView(LoginRequiredMixin,SingleTableMixin,FilterView):
    login_url = 'contact_management:login'
    model = Contact
    table_class = ContactTable
    template_name = 'contact_management/contact_list.html'
    filterset_class = ContactFilter

    def get_context_data(self,**kwargs):        
        context = super().get_context_data(**kwargs)
        table = self.get_table()
        RequestConfig(self.request, paginate={"per_page": 20}).configure(table)
        context['filter']=ContactFilter(self.request.GET,queryset=self.get_queryset())  

        return context

class ContactDetailView(LoginRequiredMixin,DetailView):
    login_url = 'contact_management:login'
    model = Contact
    form_class = NoteForm
    template_name = 'contact_management/contact_detail.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['account'] = Account.objects.get(pk=self.kwargs['account_id'])
        context['note_form'] = NoteForm
        context['email_form'] = EmailForm
        return context

class ContactUpdateView(LoginRequiredMixin,UpdateView):
    model = Contact
    fields = '__all__'

    def get_form(self,form_class=None):
        form = super(ContactUpdateView, self).get_form(form_class)
        for field in form.fields:
            form[field].required = False
        form.fields["follow_up_date"].required=False
        form.fields["account"].required=False

        return form

class LeadListView(LoginRequiredMixin,SingleTableMixin,FilterView):
    login_url = 'contact_management:login'
    model = Lead
    table_class = LeadTable
    template_name = 'contact_management/lead_list.html'
    filterset_class = LeadFilter

    def get_context_data(self,**kwargs):        
        context = super().get_context_data(**kwargs)
        table = self.get_table()
        RequestConfig(self.request, paginate={"per_page": 20}).configure(table)
        context['filter']=LeadFilter(self.request.GET,queryset=self.get_queryset())  

        return context

class LeadDetailView(LoginRequiredMixin,DetailView):
    login_url = 'contact_management:login'
    model = Lead
    form_class = NoteForm
    template_name = 'contact_management/lead_detail.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['note_form'] = NoteForm
        context['email_form']=EmailForm
        return context
class LeadUpdateView(LoginRequiredMixin,UpdateView):
    login_url = 'contact_management:login'
    model = Lead
    fields = '__all__'

    def get_form(self,form_class=None):
        form = super(LeadUpdateView, self).get_form(form_class)
        for field in form.fields:
            form.fields[field].required = False
        return form
@login_required(login_url=login_url)
@login_required(login_url='contact_management:login')
def add_contact(request,form_data):
    if request.is_ajax and request.method == 'POST':
        jform = json.loads(form_data)
        account= Account.objects.get(pk=int(jform["account_id"]))
        first_name = jform.get("first_name",None)
        last_name = jform.get("last_name",None)
        phone = jform.get("phone",None)
        email = jform.get("email",None)
        description = jform.get("description",None)
        c = Contact(first_name=first_name,last_name=last_name,phone=phone,email=email,account=account,description=description)
        c.save()
        new_contact = serializers.serialize("json",[c,])
        print(new_contact)
        return JsonResponse({"new_contact":new_contact},safe=False)
    else:
        return JsonResponse({"error":"error",},safe=False)

@login_required(login_url='contact_management:login')
def note_delete(request,note_id):
    note = Note.objects.get(pk=note_id)
    note.delete()
    return redirect(request.META['HTTP_REFERER']) 
@login_required(login_url='contact_management:login')
def send_email_form(request,form_data):
    #send_email(self,subject=None,body=None,sg_template_on=False,sg_template=None,template=None,campaign=None):
    if request.is_ajax and request.method == 'POST':
        jform = json.loads(form_data)
        print(jform)
        contacts = Contact.objects.filter(pk__in=[v for k,v in jform.items() if 'contact-checkbox' in k])
        leads = Lead.objects.filter(pk__in=[v for k,v in jform.items() if 'lead-checkbox' in k])
        subject = jform.get("subject",None)
        body = jform.get("body",None)
        sg_template_on = jform.get("sg_template_on",None)
        sg_template = jform.get("sg_template",None)
        template = jform.get("template",None)
        if template == '':
            template = None        
        if template is not None:
            body = None
        if sg_template_on == True:
            template = sg_template
        
        for c in contacts:
            #c.send_email(subject,body,self.sg_template_on,sg_template,template,self.id)
            c.send_email(subject,body,sg_template_on,sg_template,template,campaign=None)
        for l in leads:
            l.send_email(subject,body,sg_template_on,sg_template,template,campaign=None)
       
        return JsonResponse(jform)      
@login_required(login_url='contact_management:login')
def note_create(request,form_data):
    if request.is_ajax and request.method == 'POST':
        jform = json.loads(form_data)
        if jform["note_type"] == "ACCOUNT":
            n = Note(account= Account.objects.get(pk=jform["account_id"]))
        elif jform["note_type"] == "CONTACT":
            n = Note(contact= Contact.objects.get(pk=jform["contact_id"]))
        elif jform["note_type"] == "LEAD":
            n = Note(lead= Lead.objects.get(pk=jform["lead_id"]))
        contact_type = jform.get("contact_type",None)
        note = jform.get("note",None)
        n.date = datetime.now()
        n.user = request.user
        follow_up = jform.get("follow_up",None)
        follow_up_user = jform.get("follow_up_user",None)
        follow_up_type = jform.get("follow_up_type",None)
        follow_up_year = jform.get("follow_up_date_year",None)
        follow_up_month = jform.get("follow_up_date_month",None)
        follow_up_day = jform.get("follow_up_date_day",None)
        if contact_type is not None and contact_type != '':
            n.contact_type = contact_type
        if note is not None and note != '':
            print(note,'this si the note')
            n.note = note
        if follow_up == 'on':
            n.follow_up = True
            follow_up_date = datetime(int(follow_up_year),int(follow_up_month),int(follow_up_day))
            n.follow_up_date = follow_up_date
            if follow_up_type is not None and follow_up_type != '':
                n.follow_up_type = follow_up_type
        n.save()
        print('notesaved',n)
        new_note = serializers.serialize("json",[n,])
        return JsonResponse({"new_note":new_note,})
    else:
        return JsonResponse({"not_data":"not_data"})
@login_required(login_url='contact_management:login')
def delete_lead(request,pk):
    lead = Lead.objects.get(pk=pk)
    lead.delete()

    return redirect('contact_management:lead_list')

@login_required(login_url='contact_management:login')
def convert_lead(request,pk):
    lead = Lead.objects.get(pk=pk)
    new_contact = lead.convert_lead()

    return redirect('contact_management:contact_detail',args={"account_id":new_contact.account.id,"pk":new_contact.pk})



