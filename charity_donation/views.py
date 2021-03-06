
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Count, Sum
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, TemplateView, FormView, CreateView, RedirectView

from charity_donation.forms import RegisterForm, LoginForm, DonationForm
from charity_donation.models import Donation, Institution, CustomUser, Category


class LandingPage(TemplateView):
    model = Institution
    template_name = 'index.html'
    extra_context = {'foundations': model.objects.filter(type=0),
                     'organizations': model.objects.filter(type=1),
                     'locals': model.objects.filter(type=2),
                     }

    def get_context_data(self, **kwargs):
        donations = Donation.objects.aggregate(bags=Sum('quantity'))
        quantity_of_organizations = Donation.objects.aggregate(institution=Count('institution', distinct=True))
        context = super().get_context_data(**donations, **quantity_of_organizations, **kwargs)
        return context


class AddDonationView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'form.html'
    context_object_name = 'category_name'
    extra_context = {'institutions': Institution.objects.all(),
                     }

    def post(self, request):
        if request.method == 'POST':
            response_data = {}
            bags = request.POST['bags']
            categories = request.POST.getlist('categories')
            organization = request.POST['organization']
            address = request.POST['address']
            city = request.POST['city']
            postcode = request.POST['postcode']
            phone = request.POST['phone']
            data = request.POST['data']
            time = request.POST['time']
            more_info = request.POST['more_info']

            donation = Donation(quantity=bags,
                                address=address,
                                institution_id=organization,
                                phone_number=phone,
                                city=city,
                                zip_code=postcode,
                                pick_up_date=data,
                                pick_up_time=time,
                                pick_up_comment=more_info,
                                user_id=request.user.id)
            donation.save()

            for category in categories:
                donation.categories.add(category)

            return JsonResponse(response_data)


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
