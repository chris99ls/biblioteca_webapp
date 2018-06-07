from django.shortcuts import render,redirect
from webapp.froms import RegistrationForm
from .filters import BookFilter
from .models import Libro,Prestito,Prenotato,GiaVisto
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
# Create your views here.

def home(request):
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


def catalog(request):
    books = Libro.objects.all() 
    return render(request, 'dashboard/catalog.html',{'books':books})


def user_home(request):
    user = User.objects.get(username=request.user.username)
    
    #get prestiti collegati all'account loggato
    try:
      loans= Prestito.objects.get(n_tessera=user).books.all()
    except Prestito.DoesNotExist:
        booked_up = None
    #get prenotati collegati all'account loggato
    try:
       booked_up=Prenotato.objects.get(user=user).books.all()
    except Prenotato.DoesNotExist:
        booked_up = None

    #get gia letti collegati all'account loggato
    #try:
    already_read=GiaVisto.objects.get(user=user).books.all()
    #except GiaVisto.DoesNotExist:
     #   already_read = None


    return render(request, 'dashboard/user_home.html',{'loans':loans,'booked_up':booked_up,'already_read':already_read})



def search(request,pk):
    book_list = Libro.objects.all()
    book_filter = BookFilter(request.GET, queryset=book_list)
    return render(request, 'search/book_searchengine.html', {'filter': book_filter})

def detail(request, pk, xx):
    book = get_object_or_404(Libro, pk=pk)
    return render(request,'dashboard/detail.html',{'book':book}) 

def reserve_book(request, pk):
    user = User.objects.get(username=request.user.username)
    book= Libro.objects.get(pk=pk)
    p=Prenotato.objects.get(user=user)
    if p:
        p.books.add(book)
    else:
        p = Prenotato()
        p.user=user
        p.save()
        p.books.add(book)

    return redirect(user_home)


def delete_book(request, pk):
    user = User.objects.get(username=request.user.username)
    book= Libro.objects.get(pk=pk)
    p=Prenotato.objects.get(user=user)

    
    p.books.remove(book)

    return redirect(user_home)
    