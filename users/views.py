from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.views import View

from .forms import EmailLoginForm, UserRegistrationForm
from .models import CustomUser
from .utils import delete_unconfirmed_users


def register(request):
    delete_unconfirmed_users()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.token = get_random_string(length=32)
            user.save()

            confirmation_link = request.build_absolute_uri(
                reverse("confirm_email", kwargs={"token": user.token})
            )

            send_mail(
                "Подтверждение вашей регистрации",
                f"Перейдите по следующей ссылке, чтобы подтвердить свою регистрацию: {confirmation_link}",
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            messages.success(
                request,
                "На вашу почту отправлено письмо для подтверждения регистрации.",
            )
            return redirect("login")

    else:
        form = UserRegistrationForm()

    return render(request, "users/register.html", {"form": form})


def confirm_email(request, token):
    try:
        user = CustomUser.objects.get(token=token)
    except CustomUser.DoesNotExist:
        messages.error(
            request, "Неверная ссылка подтверждения или пользователь не найден."
        )
        return redirect("register")

    if timezone.now() - user.created_at > timedelta(minutes=5):
        user.delete()
        messages.error(
            request,
            "Срок действия ссылки подтверждения истек. Пожалуйста, зарегистрируйтесь снова.",
        )
        return redirect("register")

    user.is_active = True
    user.token = ""
    user.save()

    messages.success(
        request, "Ваш email был подтверждён! Теперь вы можете войти в систему."
    )
    return redirect("login")


def login_view(request):
    if request.method == "POST":
        form = EmailLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Неверный email или пароль.")
    else:
        form = EmailLoginForm()

    return render(request, "users/login.html", {"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("home")
