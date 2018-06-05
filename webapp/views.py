from django.shortcuts import render,redirect
from webapp.froms import RegistrationForm
from .filters import BookFilter
from .models import Libro,Prestito
from django.contrib.auth.models import User
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


def prestiti(request):
    user = User.objects.get(username=request.user.username)
    loans= Prestito.objects.get(n_tessera=user).books.all()
    return render(request, 'dashboard/user_home.html',{'loans':loans,'user':request.user})



def search(request):
    book_list = Libro.objects.all()
    book_filter = BookFilter(request.GET, queryset=book_list)
    return render(request, 'search/book_searchengine.html', {'filter': book_filter})