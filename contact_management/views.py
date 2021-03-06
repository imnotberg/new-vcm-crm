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
    ListView,
    FormView,
    TemplateView,
    UpdateView,
    View,
)
from formtools.wizard.views import SessionWizardView
from .filters import AccountFilter,ContactFilter,LeadFilter,ItemFilter,InvoiceFilter
from .forms import NoteForm,EmailForm,AddContactForm,AccountModalForm,ContactModalForm,CreateEmailCampaignForm,EmailCampaignForm1,EmailCampaignForm2,EmailCampaignForm3,EmailCampaignForm4
from .models import *
from .tables import AccountTable,ContactTable,LeadTable,ItemTable,InvoiceTable

from .utils import get_value,login_url

# Create your views here.
#PAGE VIEWS
def test(request):
    context = {}
    return render(request,'contact_management/test.html',context)
def accounts(request):
    context = {'accounts':Account.objects.all().order_by('name'),'note_form':NoteForm,'email_form':EmailForm,'add_contact_form':AddContactForm,'form':AccountModalForm,'contact_form':ContactModalForm,'campaign_form':CreateEmailCampaignForm,}    
    return render(request,'contact_management/accounts.html',context)

#PAGE FEEDS
def accounts_feed(request):
    #accounts = serializers.serialize("json",Account.objects.all())
    #tags = serializers.serialize("json",Tag.objects.all())
    accounts = [{"id":a.id,"name":a.name,"phone":a.phone,"email":a.email,"city":a.billing_city,"state":a.billing_state,"contacts":[c.full_name for c in a.contacts.all().order_by('last_name')],"tags":', '.join([t.name for t in a.tags.all()]),"button":f"<button class='form-control' onclick='selectAccount({a.id})'>View</button>"} for a in Account.objects.all()]
    return JsonResponse({'accounts':accounts,},safe=False)
def account_feed(request,account_id):
    
    account = Account.objects.get(pk=account_id)
    account_info = {x:y for x,y in account.__dict__.items() if x!='_state'}
    account_info["notes"] = [{"date":n.date,"user":n.user.username,"note":n.note} for n in account.notes.all().order_by('-date')]
    account_info["invoices"]=[{'date':i.date,'number':i.number,'total':i.total,'account_id':i.account.id,} for i in account.invoices.all()]
    account_info["contacts"]=[{'full_name':c.full_name,'phone':c.phone,'email':c.email,'id':c.id,} for c in account.contacts.all()]
    account_info["logo"] = account.logo
    return JsonResponse({"account":account_info})
def contacts_feed(request):
    contacts = [{"id":c.id,"first_name":c.first_name,"last_name":c.last_name,"phone":c.phone,"email":c.email,"account_name":c.account.name,"account_id":c.account.id,"city":c.account.billing_city,"state":c.account.billing_state,"full_name":c.full_name,"notes":[{"date":n.date,"note":n.note} for n in c.notes.all().order_by('-date')]} for c in Contact.objects.all().order_by('last_name')]

    return JsonResponse({"contacts":contacts},safe=False)

def contact_feed(request,contact_id):
    contact = Contact.objects.get(pk=contact_id)
    contact_info = {x:y for x,y in contact.__dict__.items() if x!='_state'}
    contact_info["full_name"]=contact.full_name
    contact_info["account"]={x:y for x,y in contact.account.__dict__.items() if x!='_state'}
    contact_info["contacts"] = [{x:y for x,y in c.__dict__.items() if x!='_state'} for c in Contact.objects.filter(account=contact.account).exclude(pk=contact.pk)]
    contact_info["notes"] = [{x:y for x,y in n.__dict__.items() if x != '_state'} for n in Note.objects.filter(Q(contact=contact)|Q(account=contact.account)).order_by('-date')]
    contact_info["invoices"] = [{x:y for x,y in i.__dict__.items() if x != '_state'} for i in Invoice.objects.filter(account=contact.account)]

    return JsonResponse({"contact":contact_info},safe=False)

#SEARCH FEEDS

#TABLES AND CHARTS


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
                try:
                    return redirect(request.GET.get('next'))
                except:
                    return redirect('contact_management:index')
            else:
                pass
        else:
            pass
    form = AuthenticationForm()
    return render(request,'contact_management/login.html',{'form':form,})
'''
'''
def logout_request(request):
    logout(request)
    return redirect('contact_management:login')
'''
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
'''
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
   
    
'''    
'''
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

''' 
'''  
@login_required(login_url='contact_management:login')
def make_primary_contact(request,account_id,contact_id):
    account = Account.objects.get(pk=account_id)
    contact = Contact.objects.get(pk=contact_id)
    account.contact_name = contact.full_name
    account.save()
    return redirect(request.META['HTTP_REFERER'])
'''
'''
@login_required(login_url='contact_management:login')
def remove_contact(request,contact_id):
    contact = Contact.objects.get(pk=contact_id)
    contact.delete()

    return redirect(request.META['HTTP_REFERER'])
'''    

'''
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
'''
'''
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
'''
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
class ItemListView(LoginRequiredMixin,SingleTableMixin,FilterView):    
    login_url = 'contact_management:login'
    model = Item
    table_class = ItemTable
    template_name = 'contact_management/item_list.html'
    filterset_class = ItemFilter

    def get_context_data(self,**kwargs):        
        context = super().get_context_data(**kwargs)
        table = self.get_table()
        RequestConfig(self.request, paginate={"per_page": 20}).configure(table)
        context['filter']=ItemFilter(self.request.GET,queryset=self.get_queryset())  

        return context

class ItemDetailView(LoginRequiredMixin,DetailView):
    login_url = 'contact_management:login'
    model = Item

    template_name = 'contact_management/item_detail.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context

class InvoiceListView(LoginRequiredMixin,ListView):
    login_url = 'contact_management:login'
    model = Invoice
    table_class = InvoiceTable
    template_name = 'contact_management/invoice_list.html'
    filterset_class = InvoiceFilter

    def get_context_data(self,**kwargs):        
        context = super().get_context_data(**kwargs)
        table = InvoiceTable(Invoice.objects.all())
        context['filter']=InvoiceFilter(self.request.GET,queryset=self.get_queryset())  
        return context
'''
class InvoiceDetailView(LoginRequiredMixin,DetailView):
    login_url = login_url
    model = Invoice 

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['account'] = Account.objects.get(pk=self.kwargs['account_id'])
        context['table']=InvoiceTable(OrderItem.objects.filter(invoice=self.object))
        return context
'''
class InvoiceCreateView(LoginRequiredMixin,CreateView):
    login_url = login_url
    model = Invoice

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["account"] = Account.objects.get(pk=self.kwargs["account_id"])
        return context
@login_required(login_url=login_url)
'''
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
'''
'''
@login_required(login_url='contact_management:login')
def note_delete(request,note_id):
    note = Note.objects.get(pk=note_id)
    note.delete()
    return redirect(request.META['HTTP_REFERER']) 
'''
'''
def send_email_campaign(request,campaign_id):
    campaign = EmailCampaign.objects.get(pk=campaign_id)
    campaign.send_emails()

    return redirect(campaign)
def send_test_email_campaign(request,campaign_id):
    campaign = EmailCampaign.objects.get(pk=campaign_id)
    print(campaign)
    campaign.send_test_email()
    print('sent test email!!!')

    return JsonResponse({'success':'success'},safe=False)
def datatable_send_test(request,campaign_id):
    campaign = EmailCampaign.objects.get(pk=campaign_id)
    campaign.send_test_email()
    print('sent datattest email!!!')
    return JsonResponse({'success':'success'},safe=False)


def add_contact_to_campaign_ajax(request,campaign_id,contact_type,contact_pk):
    if request.is_ajax and request.method == 'POST':
        campaign = EmailCampaign.objects.get(pk=int(campaign_id))       
        if contact_type == 'CONTACT':           
            ser_contact = szers.serialize("json",[Contact.objects.get(pk=contact_pk),])         
            contact = Contact.objects.get(pk=contact_pk)            
            campaign.contacts.add(Contact.objects.get(pk=int(contact_pk)))      
            
            return JsonResponse({"new_contact":ser_contact},status=200)
        
        elif contact_type == 'LEAD':
            print('we here')
            ser_contact = szers.serialize("json",[Lead.objects.get(pk=contact_pk),])
            print(ser_contact)
            campaign.leads.add(Lead.objects.get(pk=int(contact_pk)))
            return JsonResponse({"new_contact":ser_contact},status=200)
        
        elif contact_type == 'ACCOUNT':
            ser_contact = szers.serialize("json",[Account.objects.get(pk=contact_pk)])
            
            campaign.accounts.add(Account.objects.get(pk=int(contact_pk)))
            return JsonResponse({"new_contact":ser_contact},status=200)
    else:
        return JsonResponse({'error':'you did something incorrectly'},status=400)
def ajax_add_contact_to_campaign(request,campaign_id,contact_type,contact_pk):
    campaign = EmailCampaign.objects.get(pk=campaign_id)
    if contact_type == 'ACCOUNT':
        campaign.accounts.add(Account.objects.get(pk=contact_pk))
    elif contact_type == 'CONTACT':
        campaign.contacts.add(Contact.objects.get(pk=contact_pk))
    elif contact_type == 'LEAD':
        campaign.leads.add(Lead.objects.get(pk=contact_pk))

    return JsonResponse({'complete':'task completed'})
def campaign_ajax(request,campaign_id):
    campaign = EmailCampaign.objects.get(pk=campaign_id)
    data = campaign.data
    activity = data['activity'].to_json(orient="records")
    messages = data['messages'].to_json(orient="records")
    stats = data['stats'].to_json()

    json_data = {"activity":activity,"messages":messages,"stats":stats,}

    return JsonResponse(json_data)
def email_contacts_feed(request):
    
    return JsonResponse({"contacts":EmailList().list.to_json(orient='records')})
def email_campaign_messages_feed(request,campaign_id):
    email = SendGridInfoData.objects.get(pk=1)
    campaign = email.data[email.data.CAMPAIGN==str(campaign_id)].to_json(orient='records')

    return JsonResponse({"campaign":campaign},safe=False)
@login_required(login_url='contact_management:login')
def email_contact_redirect(request,contact_type,id):
    if contact_type == 'LEAD':
        lead = Lead.objects.get(pk=id)
        return redirect(lead)
    elif contact_type == 'CONTACT':
        contact = Contact.objects.get(pk=id)
        return redirect(contact)
    elif contact_type == 'ACCOUNT':
        account = Account.objects.get(pk=id)
        return redirect(account)
@login_required(login_url='contact_management:login')
def send_email_form(request,form_data):
    #send_email(self,subject=None,body=None,sg_template_on=False,sg_template=None,template=None,campaign=None):
    if request.is_ajax and request.method == 'POST':
        jform = json.loads(form_data)
        contact_id = jform.get('contact_id',None)
        j = [v for k,v in jform.items() if 'contact-checkbox' in k]       
        contacts = Contact.objects.filter(Q(pk__in=[v for k,v in jform.items() if 'contact-checkbox' in k]+[contact_id]))        
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
            print('we sending to contacts')
            #c.send_email(subject,body,self.sg_template_on,sg_template,template,self.id)
            c.send_email(subject,body,sg_template_on,sg_template,template,campaign=None)
            print('we sent to contacts')
        for l in leads:
            l.send_email(subject,body,sg_template_on,sg_template,template,campaign=None)
       
        return JsonResponse(jform)
'''
'''      
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
        print(n.note,'is the note here?')
        n.save()
        print(n.note,'maybe its here?')
        print('notesaved',n)
        new_note = serializers.serialize("json",[n,])
        return JsonResponse({"new_note":new_note,})
    else:
        return JsonResponse({"not_data":"not_data"})

class EmailCampaignFormView(LoginRequiredMixin,SessionWizardView):
    login_url = 'contact_management:login'
    template_name = 'contact_management/campaign_create_form.html'
    form_list = [EmailCampaignForm1,EmailCampaignForm2,EmailCampaignForm3,EmailCampaignForm4]   

    def done(self, form_list, **kwargs):
        fd = [form.cleaned_data for form in form_list]
        form_data = {k: v for list_item in fd for (k, v) in list_item.items()}
        c = EmailCampaign(date=form_data['date'],description=form_data['description'],template=form_data['template'],sg_template_on=form_data['sg_template_on'],subject=form_data["subject"])
        c.save()
        return redirect(c)

    def get(self, request, *args, **kwargs):
        try:
            return self.render(self.get_form())
        except KeyError:
            return super().get(request, *args, **kwargs)
@login_required(login_url='contact_management:login')
def email_campaign_detail_view(request,pk):
    
    object = EmailCampaign.objects.get(pk=pk)
    contacts = EmailList().list
    #contacts = contacts[~contacts['email'].isin(object.email_addresses)]
    #data = object.data
    #messages = data['messages']
    filtered = False

    context = {'campaigns':EmailCampaign.objects.all().order_by('-date'),'object':object,'contacts':contacts,}
    return render(request,'contact_management/emailcampaign_detail.html',context)
class EmailCampaignUpdateView(LoginRequiredMixin,UpdateView):
    login_url = 'contact_management:login'
    model = EmailCampaign
    fields = ['subject','date','description','template','sg_template_on','sent']
'''
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

@login_required(login_url=login_url)
def sales_data(request):
    context = {'years':range(2017,datetime.now().year+1),'items':Item.objects.all().order_by('item'),'months':range(1,13),}
    return render(request,'contact_management/sales_data.html',context)

def sales_by_year_chart(request):
    sales = Sales()
    dataset = [x['sales'] for x in sales.sales_by_year]
    labels = [x['year'] for x in sales.sales_by_year]
    table_info = [{"account__id":x['account__id'],"account__name":x['account__name'],"sales":x["sales"]} for x in sales.sales_by_account]
    chart_title = f"Sales By Year"
    table_title = f"Sales by Account"    
    return JsonResponse({'dataset':dataset,'labels':labels,'chart_title':chart_title,"table_info":table_info,},safe=False)

def sales_by_month_year_chart(request,year_id):
    sales = Sales(year=year_id)
    dataset = [x['sales'] for x in sales.year_sales]
    labels = [x['month'] for x in sales.year_sales]
    table_info = [{"account__id":x['account__id'],"account__name":x['account__name'],"sales":x["sales"]} for x in sales.sales_by_account_year]
    table_title = f"Account Sales for {year_id}"
    chart_title = f"Sales by Month for year: {year_id}"
    return JsonResponse({'dataset':dataset,'labels':labels,'chart_title':chart_title,"table_info":table_info,"table_title":table_title,},safe=False)

def sales_by_month_chart(request,month_id):
    sales = Sales(month=month_id)
    dataset = [x['sales'] for x in sales.month_sales_by_year]
    labels = [x['year'] for x in sales.month_sales_by_year]
    table_info = [{"account__id":x['account__id'],"account__name":x['account__name'],"sales":x["sales"]} for x in sales.month_sales_by_year_account]
    table_title = f"Account Sales for {month_id}"
    chart_title = f"Sales by Year for year: {month_id}"
    return JsonResponse({'dataset':dataset,'labels':labels,'chart_title':chart_title,"table_info":table_info,"table_title":table_title,},safe=False)

def sales_by_item_chart(request,item_id):
    item = Item.objects.get(pk=item_id)
    sales = Sales(item=item)
    dataset = [x['sales'] for x in sales.sales_by_item_by_year]
    labels = [x['year'] for x in sales.sales_by_item_by_year]
    table_info = [{"account__id":x['invoice__account__id'],"account__name":x['invoice__account__name'],"sales":x["sales"]} for x in sales.sales_by_item_by_account]
    table_title = f"Account Sales for {item}"
    chart_title = f"Sales by Year for: {item}"
    return JsonResponse({'dataset':dataset,'labels':labels,'chart_title':chart_title,"table_info":table_info,"table_title":table_title,},safe=False)

def email_data(request):
    data = EmailData().data 
    return JsonResponse(data.to_json(orient="index"),safe=False)


'''
def campaign_contacts(request,campaign_id):
    campaign = EmailCampaign.objects.get(pk=campaign_id)
    return JsonResponse({"targets":campaign.targets()},safe=False)

def add_contact_to_campaign_from_datatable(request,campaign_id,contact_type,contact_id):
    campaign = EmailCampaign.objects.get(pk=campaign_id)
    if contact_type == 'LEAD':
        contact = Lead.objects.get(pk=contact_id) 
        campaign.leads.add(contact)
        return JsonResponse({"contact":{"ID":contact_id,"TYPE":"LEAD","NAME":contact.full_name,"ACCOUNT":contact.account_name}},safe=False)
    elif contact_type == 'CONTACT':
        contact = Contact.objects.get(pk=contact_id) 
        campaign.contacts.add(contact)
        return JsonResponse({"contact":{"ID":contact_id,"TYPE":"CONTACT","NAME":contact.full_name,"ACCOUNT":contact.account.name}},safe=False)
def remove_contact_to_campaign_from_datatable(request,campaign_id,contact_type,contact_id):
    campaign = EmailCampaign.objects.get(pk=campaign_id)
    if contact_type == 'LEAD':
        contact = Lead.objects.get(pk=contact_id) 
        campaign.leads.remove(contact)
        return JsonResponse({"contact":{"ID":contact_id,"TYPE":"LEAD","NAME":contact.full_name,"ACCOUNT":contact.account_name}},safe=False)
    elif contact_type == 'CONTACT':
        contact = Contact.objects.get(pk=contact_id) 
        campaign.contacts.remove(contact)
        return JsonResponse({"contact":{"ID":contact_id,"TYPE":"CONTACT","NAME":contact.full_name,"ACCOUNT":contact.account.name}},safe=False)

    elif contact_type == 'ACCOUNT':
        contact = Account.objects.get(pk=contact_id)
        campaign.accounts.remove(account)
        return JsonResponse({"contact":{"ID":contact_id,"TYPE":"ACCOUNT","NAME":contact.contact_name,"ACCOUNT":contact.name}},safe=False)


