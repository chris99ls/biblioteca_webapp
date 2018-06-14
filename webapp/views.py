from django.shortcuts import render,redirect
from webapp.forms import RegistrationForm
from .filters import BookFilter
from .models import Libro,Prestito,Prenotato,GiaVisto         
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.admin.views.decorators import staff_member_required


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
    books = Libro.objects.all() 
    return render(request, 'dashboard/catalog.html',{'books':books})

@login_required
def user_home(request):
    
    
    user = User.objects.get(username=request.user.username)
    
    #get prestiti collegati all'account loggato
    try:
        loans= Prestito.objects.get(n_tessera=user).books.all()
    except Prestito.DoesNotExist:
            loans = None
    #get prenotati collegati all'account loggato
    try:
        booked_up=Prenotato.objects.get(user=user).books.all()
    except Prenotato.DoesNotExist:
            booked_up = None

    #get gia letti collegati all'account loggato
    try:
        already_read=GiaVisto.objects.get(user=user).books.all()
    except GiaVisto.DoesNotExist:
        already_read = None


    return render(request, 'dashboard/user_home.html',{'loans':loans,'booked_up':booked_up,'already_read':already_read})

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
    #aggiungere controllo se libro già in prestito 
    
    book = Libro.objects.get(pk=pk)
    p,created = Prenotato.objects.get_or_create(user=request.user)
    p.books.add(book)

    return redirect(user_home)


@login_required
def delete_book(request, pk):
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
    a = json.load(urllib.request.urlopen("https://www.googleapis.com/books/v1/volumes?q="+isbn))
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
    
    
    book = Libro.objects.create(title=titolo, author=autori, description=descrizioni, isbn=int(isbn), tumbnail=img)
    
    if Libro.objects.get(pk=isbn):
        return redirect(admin_catalog)
    else:
        return render(request,'admin/fail.html',{})


@staff_member_required
def admin_home(request):
    return render(request,'admin/admin_home.html',{})
    
@staff_member_required
def admin_catalog(request):
    books = Libro.objects.all() 
    return render(request, 'admin/admin_catalog.html',{'books':books})
