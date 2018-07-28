# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from models import User, UserManager, Book, Review
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'belt/index.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.validation(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:
            print "Its working"
            hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            User.objects.create(name=request.POST['name'], email=request.POST['email'], password=hash1)
            messages.error(request, 'Registration Successful. Please login in below')
        return redirect('/')

def login(request):
    email = request.POST['email']
    password = request.POST['password']
    user = User.objects.filter(email=email)
    if len(user) == 0:
        messages.error(request, "Invalid Email")
        return redirect('/')
    else:
        if ( bcrypt.checkpw(password.encode(), user[0].password.encode()) ):
            print "Password Matches, Login Successful!"
            request.session['id'] = user[0].id
            request.session['email'] = email
        return redirect('/home')

def home(request):
    context = {
        'users' : User.objects.get(id=request.session['id']),
        'reviews' : Review.objects.all().order_by('-created_at')[:5],
        'books' : Book.objects.all()
    }
    return render(request, 'belt/home.html', context)

def add_book(request):
    return render(request, 'belt/add_book.html')

def create(request):
    # if request.POST['select'] != "none":
    #     print request.POST
    #     s = request.Session()
    #     print s
    #     r = Book.objects.get(title=request.POST['select'])
    #     Review.objects.create(review=request.POST['review'], book=Book.objects.get(id=r.id), user=User.objects.get(request.session['email']))
    # else:
        # r = Book.objects.create(title=request.POST['title'], author=request.POST['author'])
    review = Review.objects.create(review=request.POST['review'], rating=request.POST['rating'], book=Book.objects.get(id=id), user = User.objects.get(email=request.session['email']))
    review.save()
    return redirect('/home')
def book(request, id):
    context = {
        'books' : Book.objects.get(id=id)
    }
    return render(request, 'belt/book.html', context)

def user(request, id):
    context = {
        'users' : User.objects.get(id=request.session['id']),
        'review' : Review.objects.filter(user=User.objects.get(id=id).order_by('-created_at')),
        'review_count' : Review.objets.filter(user=User.objects.get(id=id).order_by('-created_at').count())
    }
    return render(request, 'belt/user.html', context)
    
def logout(request):
    request.session.flush()
    return redirect('/')
        