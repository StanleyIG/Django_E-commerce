from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import CreateView, UpdateView
from authapp_custom.models import CustomUser
from authapp_custom import forms
from django.core.signing import BadSignature
from .utilities import signer


class CustomLoginView(LoginView):
    template_name = 'authapp_custom/login.html'
    form_class = forms.CustomLoginView

    def form_valid(self, form):
        ret = super().form_valid(form)
        message = "Вход выполнен!<br>Привет, %(username)s" % {
            "username": self.request.user.get_full_name()
            if self.request.user.get_full_name()
            else self.request.user.get_username()
        }
        messages.add_message(self.request, messages.INFO, mark_safe(message))
        return ret

    def form_invalid(self, form):
        for _unused, msg in form.error_messages.items():
            messages.add_message(
                self.request,
                messages.WARNING,
                mark_safe(f"Неверный логин или пароль:<br>{msg}"),
            )
        return self.render_to_response(self.get_context_data(form=form))


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.INFO, "До встречи!")
        return super().dispatch(request, *args, **kwargs)


class RegisterView(CreateView):
    # template_name = 'authapp_custom/register.html'
    form_class = forms.CustomUserCreationForm
    model = get_user_model()
    # success_url = reverse_lazy("auth:login")
    success_url = reverse_lazy('auth:done')


class RegisterDoneView(TemplateView):
    template_name = 'authapp_custom/register_done.html'


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'authapp_custom/activation_failed.html')
    user = get_object_or_404(CustomUser, username=username)
    if user.is_active:
        template = 'authapp_custom/activation_done_earlier.html'
    else:
        template = 'authapp_custom/activation_done.html'
        user.is_active = True
        user.save()
    return render(request, template)
