from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import CreateView, UpdateView
from authapp_custom.models import CustomUser, CustomUserProfile
from authapp_custom import forms
from django.core.signing import BadSignature
from .utilities import signer
from django.core.cache import cache


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

    def get(self, request, *args, **kwargs):
        # if request.user.is_anonymous:
        #     messages.add_message(request, messages.INFO, mark_safe(
        #         'Пожалуйста, войдите в систему, чтобы продолжить'))
        return super().get(request, *args, *kwargs)


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Регистрация"
        return context


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
        if not user.is_activation_key_expired():
            template = 'authapp_custom/activation_done.html'
            user.is_active = True
            user.save()
        else:
            user.delete()
            return render(request, 'authapp_custom/activation_failed.html')

    return render(request, template, {"page_title": "Активация"})


class ProfileEditView(UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = forms.CustomUserChangeForm
    profile_form = forms.CustomUserProfileUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Профиль"
        context['profile_form'] = self.profile_form(
            instance=self.object.customuserprofile)
        return context

    def form_valid(self, form):
        self.object = form.save()
        profile_form = self.profile_form(
            self.request.POST, instance=self.object.customuserprofile)
        if profile_form.is_valid():
            profile_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def test_func(self):
        return True if self.request.user.pk == self.kwargs.get("pk") else False

    def get_success_url(self):
        return reverse_lazy("auth:profile_edit", args=[self.request.user.pk])