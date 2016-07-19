from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/',redirect_field_name=None)
def dashboard(request):
	return HttpResponse('YO!')