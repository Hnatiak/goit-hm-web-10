from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm
from django.contrib import messages
# Create your views here.

class RegisterView(View):
    template_name = 'app_auth/register.html'
    form_class = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='quotes:home')
        return super().dispatch(request, *args, **kwargs)

    # Рендеримо форму
    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})

    # Відправляємо інформацію і зберігаємо в базу даних якщо все валідне
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f"{username} - Ти успішно зареєструвався")
            return redirect(to="app_auth:signin")
        return render(request, self.template_name, {"form": form})

def logout_view(request):
    messages.info(request, "Повертайся, до скорих зустрічей")
    logout(request)
    return redirect('/')