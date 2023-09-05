from django.shortcuts import render

# Create your views here.

from django.contrib import messages
from django.shortcuts import render, reverse, redirect
from .models import *
from . import models
from django.views.generic import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
import datetime

from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import redirect


def about(request):
    context = {}
    return render(request, 'includes/about.html', context)


# base home
def home(request):
    sliders = SliderImagesContent.objects.all()
    whocontents = WhoWeAreModel.objects.all()
    essentials = EssentialsPageModel.objects.all()
    essential_right_content = EssentialRightContent.objects.all()
    count_values = CountPageModel.objects.all()
    books_to_read = BooksToRead.objects.all()
    book_cards = BookCardsModel.objects.all()
    contact_me_context = ContactMePartContext.objects.all()
    context = {
        'sliders': sliders,
        'whocontents': whocontents,
        'essentials': essentials,
        'essential_right_content': essential_right_content,
        'count_values': count_values,
        'books_to_read': books_to_read,
        'book_cards': book_cards,
        'contact_me_context': contact_me_context,
    }
    return render(request, 'pages/home.html', context)


# create user profile
@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST,
                                         request.FILES,
                                         instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'pages/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


# book page for only registered users
@login_required
def login_required_book_lists(request):
    book_cards = BookCardsModel.objects.all()
    if request.user.is_authenticated :
     user = request.user
     order,created = models.Order.objects.get_or_create(user=user,complete = False)
     items = order.orderitem_set.all()
     get_cart_quantity = order.get_item
    else:
        items = [ ] 
        order = {'get_item':0,'get_total':0}
        get_cart_quantity = order['get_item']

    context = {'book_cards': book_cards,'items' : items,'order' : order,'get_cart_quantity':get_cart_quantity,'shipping': False}

    return render(request, 'pages/books.html', context)


def search(request):
    if request.method == 'POST':
        searched = request.POST["Searched"]
        keys = BookCardsModel.objects.filter(book_name__contains = searched)
    if request.user.is_authenticated :
     user = request.user
     order,created = models.Order.objects.get_or_create(user=user,complete = False)
     items = order.orderitem_set.all()
     get_cart_quantity = order.get_item
    else:
        items = [ ] 
        order = {'get_item':0,'get_total':0}
        get_cart_quantity = order['get_item']

    context = {"search": searched, "keys": keys,'items' : items,'order' : order,'get_cart_quantity':get_cart_quantity}    

    return render(request, 'pages/search.html',context)


# book details
def bookDetails(request, pk):
    book_detail = BookCardsModel.objects.get(id=pk)
    if request.user.is_authenticated :
     user = request.user
     order,created = models.Order.objects.get_or_create(user=user,complete = False)
     items = order.orderitem_set.all()
     get_cart_quantity = order.get_item
    else:
        items = [ ] 
        order = {'get_item':0,'get_total':0}
        get_cart_quantity = order['get_item']

    context = {'book_detail': book_detail,'items' : items,'order' : order,'get_cart_quantity':get_cart_quantity}

    return render(request, 'details/book_details.html', context)


# shop details
def shopDetails(request, pk):
    shop_detail = BookCardsModel.objects.get(id=pk)
    if request.user.is_authenticated :
     user = request.user
     order,created = models.Order.objects.get_or_create(user=user,complete = False)
     items = order.orderitem_set.all()
     get_cart_quantity = order.get_item
    else:
        items = [ ] 
        order = {'get_item':0,'get_total':0}
        get_cart_quantity = order['get_item']

    context = {'shop_detail': shop_detail,'items' : items,'order' : order,'get_cart_quantity':get_cart_quantity}
    return render(request, 'details/shop_details.html', context)


def cart(request):
    
  if request.user.is_authenticated:
     user = request.user
     order,created = models.Order.objects.get_or_create(user=user,complete = False)
     items = order.orderitem_set.all()
  else:
        items = [ ] 
        order = {'get_item':0,'get_total':0}

  context = {'items' : items,'order' : order}
    
  return render(request,'pages/cart.html',context)

def userProfileUpdateView(request, pk):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST,
                                         request.FILES,
                                         instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='/profile/')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request,'pages/update.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })



# card checkout to buy the book
def checkoutBookView(request):
    # checkout = BookCardsModel.objects.get(id=pk)
     if request.user.is_authenticated: 
      user = request.user
      order,created = models.Order.objects.get_or_create(user=user,complete = False)
      items = order.orderitem_set.all()
      usermodel = models.User.objects.get(id = user.id)  
     else:
        items = [ ] 
        order = {'get_item':0,'get_total':0}

     context = {'items' : items,'order' : order,'usermodel': usermodel,'shipping': False}

     return render(request, 'pages/checkout.html', context)


def updateItem(request):
    if request.method =='POST':
    # data = json.loads(request.body)
     data = json.loads(request.body.decode("utf-8"))
    bookId = data['bookId']
    action = data['action']
   
    user = request.user
    book = BookCardsModel.objects.get(id = bookId)
    order,created = models.Order.objects.get_or_create(user=user,complete = False)
    orderItem,created = models.OrderItem.objects.get_or_create(order = order,book = book)
    
    if action =='add':
        orderItem.quantity += 1
    elif action =='remove':
        orderItem.quantity -= 1   
        
    orderItem.save()
    
    if action == 'delete':
       orderItem.delete()
        
        
    if orderItem.quantity <= 0:
        orderItem.delete()
             
    return JsonResponse('Item was added',safe=False)
    


# create sign up view
class SignupView(CreateView):
    template_name = 'registration/signup.html'
    initial = {'key': 'value'}
    form_class = RegisterForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='/')

        return render(request, self.template_name, {'form': form})


# create profile update view
def userProfileUpdateView(request, pk):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST,
                                         request.FILES,
                                         instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='/profile/')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request,'pages/update.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


class CreateUserView(LoginRequiredMixin, CreateView):
    template_name = 'pages/user_create.html'
    form_class = UserFrom

    def get_success_url(self):
        return reverse('book:home')

    def form_valid(self, form):
        userOnline = form.save(commit=False)
        userOnline.organiser = self.request.user.profile
        userOnline.save()
        return super(CreateUserView, self).form_valid(form)


# create user list view
class UserListView(LoginRequiredMixin, ListView):
    template_name = 'pages/users.html'
    context_object_name = 'users'

    def get_queryset(self):
        user = self.request.user
        if user.is_organised:
            queryset = models.UserModel.objects.filter(organiser=user.profile)
        else:
            queryset = models.UserModel.objects.filter(organiser=user.agent.organiser)
            queryset = queryset.filter(agent__user=self.request.user)
        return queryset

@csrf_exempt 
def processOrder(request):
     print('Data',request.body)
     transaction_id = datetime.datetime.now().timestamp()
     data = json.loads(request.body)
     
     
     if request.user.is_authenticated: 
      user = request.user
      order,created = models.Order.objects.get_or_create(user=user,complete = False)
      total = float(data['form']['total'])
      order.transaction_id = transaction_id
    
     if total == order.get_total:
         order.complete = True
         order.save()   
     
     if (order.shipping == True):
         ShippingAddress.objects.create(
             user = user,
             order = order,
             address = data['shipping']['address'],
             city = data['shipping']['city'],
             state = data['shipping']['state'],
             zipcode = data['shipping']['zipcode'],
         )
      
     return JsonResponse('Payment Complete',safe=False)