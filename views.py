from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

