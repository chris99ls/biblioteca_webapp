from django.shortcuts import render,redirect
from webapp.forms import RegistrationForm
from .filters import BookFilter
from .models import Libro,Prestito,Prenotato       
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.db.models import Q
from django.db.models import Count


import urllib.request
import json
# Create your views here.


def home(request):
    logout(request)
    return render(request, 'webapp/index.html', {})


def register(request):
    if request.method=="POST":
        form= RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form=RegistrationForm()

    args= {'form':form}
    return render(request, 'accounts/reg_form.html',args)

@login_required
def catalog(request):
    piu_letti=[]
    books = Libro.objects.all() 
    piu_letti_query=Prestito.objects.values('books').annotate(ripetizioni=Count('books')).order_by('-ripetizioni')[:5]
    for i in piu_letti_query:
        piu_letti.extend(list(Libro.objects.filter(isbn=i['books'])))

    return render(request, 'dashboard/catalog.html',{'books':books,'piu_letti': piu_letti})

@login_required
def user_home(request):
    
    seen_books=[]
    loans=[]
    user = User.objects.get(username=request.user.username)
    
    #get prestiti collegati all'account loggato
    try:
        loaned=Prestito.objects.filter(n_tessera=user.id).exclude(end_loan_date__isnull=False)
        for l in loaned:
            loans.extend(list(l.books.all()))
    except Prestito.DoesNotExist:
            loans = None
    #get prenotati collegati all'account loggato
    try:
        booked_up=Prenotato.objects.get(user=user).books.all()
    except Prenotato.DoesNotExist:
            booked_up = None

    #get gia letti collegati all'account loggato
    try:
        seen=Prestito.objects.filter(n_tessera=user.id).exclude(end_loan_date__isnull=True)
        for l in seen:
            seen_books.extend(list(l.books.all()))
    except Prestito.DoesNotExist:
        seen = None


    return render(request, 'dashboard/user_home.html',{'loans':loans,'booked_up':booked_up,'already_read':seen_books})

@login_required
def search(request,pk):
    book_list = Libro.objects.all()
    book_filter = BookFilter(request.GET, queryset=book_list)
    return render(request, 'search/book_searchengine.html', {'filter': book_filter})


@login_required
def detail(request, pk, xx):
    book = get_object_or_404(Libro, pk=pk)
    return render(request,'dashboard/detail.html',{'book':book}) 


@login_required
def reserve_book(request, pk):
        
    book = Libro.objects.get(pk=pk)
    p,created = Prenotato.objects.get_or_create(user=request.user)
    p.books.add(book)

    return redirect(user_home)


@login_required
def delete_reserved_book(request, pk):
    book= Libro.objects.get(pk=pk)
    p=Prenotato.objects.get(user=request.user)
    p.books.remove(book)
    return redirect(user_home)    



@staff_member_required
def search_book_google(request):
    return render(request, 'admin/search_book_google.html',{})


@staff_member_required
def add_book(request,pk):
    url= request.path
    
    isbn= url.rsplit('/', 1)[-1]

    a = json.load(urllib.request.urlopen("https://www.googleapis.com/books/v1/volumes?q="+pk))
    titolo = a['items'][0]['volumeInfo']['title']

    autori = ""
    img = ""
    

    if a['items'][0]['volumeInfo'].get('description'):
        descrizioni = a['items'][0]['volumeInfo']['description']
    else:
        descrizioni=""      

    
    isbn = a['items'][0]['volumeInfo']['industryIdentifiers'][0]['identifier']
   
    for author in a['items'][0]['volumeInfo']['authors']:
        autori += author+","
    
    for img in a['items'][0]['volumeInfo']['imageLinks']:
        img = a['items'][0]['volumeInfo']['imageLinks'][img]
    
    
    Libro.objects.create(title=titolo, author=autori, description=descrizioni, isbn=int(isbn), tumbnail=img)
    
    return redirect(admin_catalog)



@staff_member_required
def admin_home(request):
    user_with_reserved = Prenotato.objects.all()
    return render(request,'admin/admin_home.html',{'user_with_reserved':user_with_reserved})

@staff_member_required
def admin_user_detail(request,xx):
    print(xx)
    user=User.objects.get(username=xx) 
    loaned_books=[]

    try:
        reserved=Prenotato.objects.get(user=user)
        reserved_books=reserved.books.all()
    except:
        reserved_books='' 
       
    try:
        loaned=Prestito.objects.filter(n_tessera=user.id).exclude(end_loan_date__isnull=False)
        for l in loaned:
            loaned_books.extend(list(l.books.all()))    
    except:
        loaned_books='' 
    
    return render(request, 'admin/admin_user_detail.html',{'reserved_books':reserved_books,'loaned_books':loaned_books,'user':user})


@staff_member_required
def admin_catalog(request):
    books = Libro.objects.all() 
    return render(request, 'admin/admin_catalog.html',{'books':books})



@staff_member_required
def admin_detail(request, pk, op, user):
    xx=User.objects.get(username=user)
    book = get_object_or_404(Libro, pk=pk)
    return render(request,'admin/admin_detail.html',{'book':book,'xx':xx}) 


@staff_member_required
def admin_reserved_book(request,user,pk):
    
    xx = User.objects.get(username=user)
    book = Libro.objects.get(pk=pk)
    reserved = Prenotato.objects.get(user=xx)
    reserved.books.remove(book)
    
    #nuovo prestito
    loan = Prestito.objects.create(n_tessera=xx,start_loan_date=timezone.now() )
    loan.books.add(book)
    
    return redirect(admin_home)

@staff_member_required
def admin_loaned_book(request,user,pk):
    
    xx=User.objects.get(username=user)
    book= Libro.objects.get(pk=pk)
    p=Prestito.objects.filter(n_tessera=xx.id, books=book)
    p.update(end_loan_date=timezone.now())

    return redirect(admin_home)

