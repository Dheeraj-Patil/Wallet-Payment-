from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

from .models import User, Wallet


class LoginView(TemplateView):

    template_name = "accounts/login.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["req"] = self.request
    #     if self.request.method == 'POST':
    #         print('lol')

    #     return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # Your code here
        # Here request.POST is the same as self.request.POST
        # You can also access all possible self variables
        # like changing the template name for instance
        email = self.request.POST['email']
        password = self.request.POST['password']
        user = authenticate(username=email, password=password)
        context['users'] = 'Login Failed'
        if user is not None:
            # Save session as cookie to login the user
            login(request, user)
            context['users'] = user
            return HttpResponseRedirect('/dashboard/')

        return self.render_to_response(context)


class SignupView(TemplateView):

    template_name = "accounts/signup.html"

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # Your code here
        # Here request.POST is the same as self.request.POST
        # You can also access all possible self variables
        # like changing the template name for instance
        email = self.request.POST['email']
        qs = User.objects.filter(email=email)
        if qs.exists():
            context['pmsg'] = 'Email already exists'
            return self.render_to_response(context)
        password1 = self.request.POST['password1']
        password2 = self.request.POST['password2']
        first_name = self.request.POST['first_name']
        last_name = self.request.POST['last_name']
        mobile = self.request.POST['mobile']
        ssn = self.request.POST['ssn']
        if password1 == password2:
            user = User.objects.create_wuser(
                email=email, password=password1, first_name=first_name, last_name=last_name, wallet_phone=mobile)
            print(user)
        else:
            context['pmsg'] = 'Passwords Do not match'
        if user is not None:
            # Save session as cookie to login the user
            wallet = Wallet.objects.create(user=user, ssn=ssn)
            login(request, user)
            context['pmsg'] = 'User' + str(user) + ' created'
            # return HttpResponseRedirect('/dashboard/')

        return self.render_to_response(context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
