from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from .models import Book, User, Image, Order
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, FormView, ListView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy, reverse
from .forms import UploadFileForm, LoginForm, UserForm
from django.views import View
import datetime




def index(request):
    list_of_books = Book.objects.all()
    noOrderedBooks = 0
    if 'books_to_buy' in request.session:
        noOrderedBooks = len(request.session['books_to_buy'])
    username=""
    role = "client"
    if 'user_id' in request.session:
         username = User.objects.get(id = request.session['user_id']).username
         role =  User.objects.get(id =  request.session['user_id'] ).role
    context = {'list_of_books': list_of_books, 'userLogged':username, 'role':role,'noOrderedBooks':noOrderedBooks}
    
    return render(request, 'miniLibrary/index.html', context)
def addToCart(request, book_id):
    if 'books_to_buy' in request.session :
        books = request.session['books_to_buy'];
        books.append(book_id)
        request.session['books_to_buy']=books
    else:
        request.session['books_to_buy']=[book_id]
    return HttpResponseRedirect('../../')
       
class BookDetail(DetailView):
        model=Book
        template_name="miniLibrary/book_details.html"
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['role'] = "client" 
            if 'user_id' in self.request.session:
                 context['role'] = User.objects.get(id = self.request.session['user_id']).role
            return context
        


class UserCreate(FormView):
    form_class=UserForm
    template_name='miniLibrary/createUserForm.html'
    success_url = 'login-view'

    def post(self, request):
        
        # if this is a POST request we need to process the form data
        print (request.method)
        if request.method == 'POST':
            status = ""
            # create a form instance and populate it with data from the request:
            username = request.POST.get('username')
            password = request.POST.get('password')
            password_match = request.POST.get('password_match')
            if len(username) > 9:
                if password == password_match and len(password)>=8:
                    user = User(username = username, password = password)
                    user.save()
                    status = "Your account have been created. Please login"
                    return HttpResponseRedirect('http://localhost:8000/miniLibrary/books/login')
                else:
                    status = "Password mush have at least 8 characters"
            else:
                status = "Username must have at least 9 characters"  
        form = UserForm()
        return render(request, self.template_name, {'form': form, 'status':status})

   


class BookCreate(CreateView):
    model=Book
    fields = ( 'name', 'author','description','publisher', 'price')
    template_name = 'miniLibrary/book_form.html'

class BookUpdate(UpdateView):
    model=Book
    fields = ('description', 'price')
    template_name = 'miniLibrary/book_update.html'

class BookDelete(DeleteView):
    model=Book
    template_name="miniLibrary/delete_book.html"
    def get_success_url(self):
        return reverse("index")

def upload_file(request, book_id):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = Image(name=request.FILES['file'],book_id=Book.getBookWithId(book_id))
            instance.save()
            return HttpResponseRedirect('../')
    else:
        form = UploadFileForm()
    return render(request, 'miniLibrary/upload_image.html', {'form': form})



class LoginView(FormView):
    form_class=LoginForm
    template_name='miniLibrary/loginForm.html'
    success_url = ''

    def post(self, request):
        
        # if this is a POST request we need to process the form data
        print (request.method)
        if request.method == 'POST':
            
            # create a form instance and populate it with data from the request:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = User.objects.get(username=username);
            if (not user is None) and (user.password == password):
                request.session['user_id'] = user.id
                return HttpResponseRedirect('http://localhost:8000/miniLibrary/books/')
        form = LoginForm()

        return render(request, self.template_name, {'form': form})
        
def logout(request):
    try:
        del request.session['user_id']
        del request.session['books_to_buy']
    except KeyError:
        pass
    return render(request, 'miniLibrary/logout.html')


class CartView(ListView):
    template_name='miniLibrary/order.html'
    def get_context_data(self, **kwargs):
        sum = 0
        context = super().get_context_data(**kwargs)
        books=[]
        if 'books_to_buy' in self.request.session:
            for x in self.request.session['books_to_buy']:
                books.append(Book.objects.get(id = x))
                sum = sum + Book.objects.get(id = x).price
        context['books']=books
        context['Total']=sum
        return context

class OrderView(ListView):
    #template_name = 'miniLibrary/successOrder.html'
    def get(self, request):
        if 'user_id' in request.session:
            user = User.objects.get(id = request.session['user_id'])
            if 'books_to_buy' in request.session:
                for x in self.request.session['books_to_buy']:
                    order = Order(userId = user, bookId = Book.objects.get(id = x), placement_date = datetime.datetime.now())
                    order.save()
                return HttpResponse("Your order have been sent")
            return HttpResponse("You don't have any books in the cart") 
        return HttpResponse("You have to be logged in")