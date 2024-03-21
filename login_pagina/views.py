from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.shortcuts import render

from .forms import ExamesForm
from .models import exames

# Create your views here.
def cliente_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('login_cliente:ver_exames')
        else:
            messages.success(request, ("Login nao encontrado, tente novamente"))
            return redirect('login_cliente:cliente_login')

    else:
        return render(request, 'pagina_login.html')
    
def logout_user(request):
    logout(request)
    messages.success(request, ("Voce saiu da sua conta"))
    return redirect('home')

def registro_exames(request):
    submitted = False
    if request.method == "POST":
        form = ExamesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            submitted=True
        else:
            form = ExamesForm()
            if 'submitted' in request.GET:
                submitted = True

    form = ExamesForm
    return render(request, 'registro_exames.html', {'form' : ExamesForm, 'submitted':submitted})

def ver_exames(request):
    if request.user.is_authenticated:
        current_user = request.user
        user_id = current_user.id

        exame = exames.objects.filter(paciente__exact=user_id)

    return render(request, 'exames_paciente.html', {'exame' : exame})

def registrar_paciente(request):
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            
            first_name = form.cleaned_data['firstname']
            last_name = form.cleaned_data['lastname']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            messages.success(request, ("Paciente registrado com sucesso"))
            return redirect('login_cliente:registro_usuario')
    else:
        form = UserCreationForm()
    
    return render(request, 'registro_usuarios.html', {'form' : form})



