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
