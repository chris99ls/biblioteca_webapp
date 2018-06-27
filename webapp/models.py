from django.db import models
from django.utils import timezone

# Create your models here.


class Libro(models.Model):
    
    title= models.CharField(max_length=200)
    author= models.CharField(max_length=200)
    subject=models.CharField(max_length=200)
    description=models.CharField(max_length=1000)
    tumbnail=models.CharField(max_length=200)
    isbn=models.BigIntegerField(primary_key='true')
        
    def __str__(self):
        return self.title

    def publish(self):
        self.save()


class Sinossi(models.Model):

    id=models.AutoField(primary_key='True')
    title= models.CharField(max_length=200)
    author= models.CharField(max_length=200)
    subject=models.CharField(max_length=200)
    description=models.CharField(max_length=1000)
    tumbnail=models.CharField(max_length=200)

    def __str__(self):
        return self.title

    def publish(self):
        self.save()


class Prestito(models.Model):

    id=models.AutoField(primary_key='True')
    n_tessera= models.ForeignKey('auth.User', on_delete=models.CASCADE)
    books= models.ManyToManyField(Libro)
    start_loan_date = models.DateTimeField(default=timezone.now)
    end_loan_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.n_tessera.username

    def publish(self):
        self.save()



class Prenotato(models.Model):

    id=models.AutoField(primary_key='True')
    user= models.ForeignKey('auth.User', on_delete=models.CASCADE)
    books= models.ManyToManyField(Libro)

    def __str__(self):
        return self.user.username

    def publish(self):
        self.save()
