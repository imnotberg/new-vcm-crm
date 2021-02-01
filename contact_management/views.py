from django_filters.views import FilterView
from django_tables2.config import RequestConfig
from django_tables2.views import SingleTableMixin
from django.contrib.auth import logout,authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
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
from .forms import NoteForm
from .models import *
from .tables import AccountTable,ContactTable,LeadTable

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

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['account'] = Account.objects.get(pk=self.kwargs['pk'])
        context['note_form'] = NoteForm
        return context
    def post(self, request, *args, **kwargs):
        contact_email = request.POST.get('contactEmail',None)
        if contact_email is not None and contact_email != '':
            contacts = Contact.objects.filter(pk__in=[y for x,y in self.request.POST.items() if 'checkbox' in x])
            body = request.POST.get('body',None)
            subject = request.POST.get('subject',None)
            template = request.POST.get('template',None)
            sg_template_on = request.POST.get('sg_template_on',False)
            sg_template = request.POST.get('sg_template',None)
            if template is not None:
                body = None
            if sg_template_on !=False:
                sg_template_on=True
            for c in contacts:
                c.send_email(subject,body,sg_template_on,sg_template,template)

        follow_up = request.POST.get('follow_up',None)
        follow_up_date_year = request.POST.get('follow_up_date_year',None)
        follow_up_date_month = request.POST.get('follow_up_date_month',None)
        follow_up_date_day = request.POST.get('follow_up_date_day',None)
        follow_up_type = request.POST.get('follow_up_type',None)
        follow_up_user = request.POST.get('follow_up_user',None)    

        if follow_up_date_year is not None and follow_up_date_month is not None and follow_up_date_day is not None:
            fud = datetime(int(follow_up_date_year),int(follow_up_date_month),int(follow_up_date_day))
        self.object = self.get_object()         
        form = self.form_class(request.POST)
        context = self.get_context_data()           
        if form.is_valid():
            account = context['account']        
            note = form.save(commit=False)
            note.date = datetime.now()          
            note.account = context['account']
            note.user = request.user
            note.save()
            targets = CallSheetTarget.objects.filter(account=note.account,contacted=False)
            for tgt in targets:
                tgt.contacted = True
                tgt.save()  
            if follow_up is not None and follow_up == 'on' and fud is not None:
                call_sheet,created = CallSheet.objects.get_or_create(date=fud,user=User.objects.get(username=follow_up_user),contact_type=follow_up_type)
                call_sheet.save()               
                target = CallSheetTarget(call_sheet=call_sheet,account=note.account,contact_type=follow_up_type)
                target.save()
                target.account.follow_up_date = fud
                target.account.save()
                
        def form_valid(self,form):
            context = self.get_context_data()
            note = form.save(commit=False)
            note.date = datetime.now()          
            note.account = context['account']
            note.user = request.user
            note.save()         
            #account.notes.add(note)
            #account.save()         
            return super().form_valid(form)
        return redirect(context['account'])
    

class AccountUpdateView(LoginRequiredMixin,UpdateView):
    model = Account
    fields = '__all__'

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
        return context

class ContactUpdateView(LoginRequiredMixin,UpdateView):
    model = Contact
    fields = '__all__'

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
        return context

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


