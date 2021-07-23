from typing import ContextManager
from django.shortcuts import render, redirect
from .models import Book, User
from libros_app.models import User
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect("/")       
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('register_email')
        password=request.POST.get('register_password')
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        logged_user= User.objects.create(first_name=first_name, last_name=last_name, email=email, password= pw_hash)
        request.session['id'] = logged_user.id
        print(logged_user)
        return redirect("/books")
    else:
        if "user.id" not in request.session:
            return redirect("/")
    return redirect("/")
        
def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect("/")
        email=request.POST.get('login_email')
        user = User.objects.filter(email = email)
        if len(user) == 1:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['login_password'].encode(), logged_user.password.encode()):
                request.session['id'] = logged_user.id
                return redirect("/books")
    return redirect("/")

def books(request):
    if 'id' in request.session:
        user_id= request.session['id']
        user = User.objects.get(id= user_id)
        books = Book.objects.all()
        context={
            'name': f'{user.first_name}  {user.last_name}',
            'books': books,
            'user':user
        }
        return render(request, 'books.html', context)
    return redirect("/")

def add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('description')
        user_id = request.POST.get('user_id')
        uploaded = User.objects.get(id= user_id)
        nuevo_titulo = Book.objects.create(title =title, desc= desc, uploaded_by= uploaded)
        nuevo_titulo.users_who_like.add(uploaded)
        print(nuevo_titulo.users_who_like)

        return redirect("/books")
    return redirect("/")
     
def edit(request, id):
    
        book = Book.objects.get(id=id)
        user_id= request.session['id']
        user = User.objects.get(id= user_id)
        print(book.uploaded_by)
        if user == book.uploaded_by:
            if request.method == 'POST':
                title = request.POST.get('title')
                desc = request.POST.get('description')
                book.title = title
                book.desc = desc
                book.save()
                url= '/edit/' + str(book.id)
                return redirect(url)
            context={
                'book':book,
                'user':user
            }
            return render(request, "edit.html", context)
        context={
            'book':book,
            'user':user
        }
        return render(request, 'detalles.html', context)
    
def delete(request, id):
    book = Book.objects.get(id=id)
    book.delete()
    context={
        'book':book
    }
    return redirect("/books", context)

def add_book(request):
    if request.method == 'POST':
        agregar = request.POST.get('agregar')
        print(agregar)
        user_id= request.session['id']  
        print(user_id)           
        id_book =Book.objects.get(id=agregar)
        id_users= User.objects.get(id= user_id)
        id_users.liked_books.add(id_book)
        return redirect("/books")

def remove(request, id):
        book = Book.objects.get(id=id)
        user_id= request.session['id']
        user = User.objects.get(id= user_id)
        book.users_who_like.remove(user)
        return redirect('/edit/' + str(id))  

def logout(request):
    request.session.clear()
    return redirect("/")
