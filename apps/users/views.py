from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm


def login_view(request):
    """
    View para autenticação de usuários.
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {username}!')
                
                # Redirect to next page if exists, otherwise to home
                next_page = request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect('home')
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """
    View para logout de usuários.
    """
    logout(request)
    messages.info(request, 'Você foi desconectado com sucesso.')
    return redirect('users:login')


def password_reset_view(request):
    """
    View para recuperação de senha.
    """
    return render(request, 'users/password_reset.html')


@login_required
def profile_view(request):
    """
    View para perfil do usuário.
    """
    return render(request, 'users/profile.html')
