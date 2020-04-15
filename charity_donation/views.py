from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.db.models import Count, Sum
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, TemplateView, FormView, CreateView, RedirectView
from charity_donation.forms import RegisterForm, LoginForm
from charity_donation.models import Donation, Institution, CustomUser, Category


class LandingPage(TemplateView):
    def render_to_response(self, context):
        # Liczenie worków i wspartych organizacji
        donations = Donation.objects.aggregate(bags=Sum('quantity'))
        quantity_of_organizations = Donation.objects.aggregate(institution=Count('institution', distinct=True))
        foundations = Institution.objects.filter(type=0)
        organizations = Institution.objects.filter(type=1)
        local = Institution.objects.filter(type=2)
        context = {**donations, **quantity_of_organizations, 'foundations': foundations, 'organizations': organizations,
                   'local': local}

        return self.response_class(
            request=self.request,
            template='index.html',
            context=context,
            using=self.template_engine,
        )


class AddDonationView(ListView):
    pass

class LoginUserView(LoginView):
    template_name = 'login.html'
    form_class = LoginForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            email = form.cleaned_data['username']
            try:
                CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return redirect('/register')
            return self.form_invalid(form)


class LogoutUserView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('landing_page'))


class RegisterUserView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = '/login'

    # 1.jeśli jest okej to powinno normalnie się loguje i przekierowuje na main
    # 2. jeśli nie ma danego maila to przekierowuje na rejestrace
    # 3. jeśli błędne dane, pokazuje informacje - błędne dane. Zaloguj się jeszcze raz
