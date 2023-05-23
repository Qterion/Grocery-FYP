from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import  get_object_or_404, render, redirect
from .forms import NewUserForm,AuthenticationForm, CustomUserChangeForm
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
import datetime as D
from .models import CustomUser
from django.conf import settings
def mainpage(request: HttpRequest)-> HttpResponse:
	if request.user.is_authenticated==False:
		return redirect('signin')
	else:
		if request.method == "POST":
			
			form = CustomUserChangeForm(request.POST,instance=request.user)
			if form.is_valid():
				user = form.save()
				messages.success(request, "details updated" )
				
				return redirect('mainpage')
			messages.error(request, "Unsuccessful")
		form = CustomUserChangeForm()
		return render (request=request, template_name="home.html", context={"edit_form":form})


def signup_request(request: HttpRequest)-> HttpResponse:
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			response=HttpResponseRedirect('http://localhost:8000/')
			now=D.datetime.utcnow()
			max_age=7 * 24 * 60 * 60
			exp=now+D.timedelta(seconds=max_age)
			format='%a, %d-%b-%Y %H:%M:%S GMT'
			exp_str=D.datetime.strftime(exp, format)
			response.set_cookie('id',request.user.id,expires=exp_str)
			print(request.user)
			# send_mail(
          	# 'Account Creation',
          	# 'Your account was created!',
          	# settings.EMAIL_HOST_USER,
          	# [str(request.user.email)],
          	# fail_silently=False,
          	# )
			return response
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})

	

def signin_request(request: HttpRequest)-> HttpResponse:
	if request.user.is_authenticated:
		response=HttpResponseRedirect('/')
		now=D.datetime.utcnow()
		max_age=7 * 24 * 60 * 60
		exp=now+D.timedelta(seconds=max_age)
		format='%a, %d-%b-%Y %H:%M:%S GMT'
		exp_str=D.datetime.strftime(exp, format)
		response.set_cookie('id',request.user.id,expires=exp_str)
		return response
	if request.method == "POST":
		form = AuthenticationForm(request.POST)
		
		if form.is_valid():
			
			username = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			user = authenticate(email=username, password=password)
			print(user)
			if user is not None:
				response=HttpResponseRedirect("http://localhost:8000/")
				login(request, user)
				now=D.datetime.utcnow()
				max_age=7 * 24 * 60 * 60
				exp=now+D.timedelta(seconds=max_age)
				format='%a, %d-%b-%Y %H:%M:%S GMT'
				exp_str=D.datetime.strftime(exp, format)
				response.set_cookie('id',request.user.id,expires=exp_str)
				messages.info(request, f"You are now logged in as {username}.")
				return response
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})


def signout_user(request: HttpRequest)-> HttpResponse:
	logout(request)
	response = redirect('signin')
	response.delete_cookie('messages')
	response.delete_cookie('id')
	response.delete_cookie('sessionid')
	response.delete_cookie('csrftoken')
	return response