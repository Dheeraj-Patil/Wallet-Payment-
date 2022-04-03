from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import Wallet, BankAccount
from accounts.forms import BankAccountForm
from .models import Transaction
from .forms import TransactionForm


class HomePageView(TemplateView):

    template_name = "transact/index.html"


class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'

    template_name = "transact/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wallet = Wallet.objects.get(user=self.request.user)
        context['wallet'] = wallet
        transactions = Transaction.objects.filter(
            wallet=wallet).order_by('-datetime')
        rec_transactions = Transaction.objects.filter(
            t_to=self.request.user).order_by('-datetime')
        the_list = transactions | rec_transactions
        the_list = the_list[:5]
        context['trc'] = the_list
        return context


class SendView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'

    template_name = "transact/send.html"
    model = Transaction
    form_class = TransactionForm
    success_url = reverse_lazy('history')

    def get_form_kwargs(self):
        kwargs = super(SendView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class RequestView(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'

    template_name = "transact/request.html"


class HistoryView(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'

    template_name = "transact/history.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wallet = Wallet.objects.get(user=self.request.user)
        context['wallet'] = wallet
        transactions = Transaction.objects.filter(
            wallet=wallet).order_by('-datetime')
        rec_transactions = Transaction.objects.filter(
            t_to=self.request.user).order_by('-datetime')
        context['trc'] = transactions | rec_transactions
        return context


class AccountsView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'

    template_name = "transact/accounts.html"
    model = BankAccount
    form_class = BankAccountForm
    success_url = reverse_lazy('accounts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wallet = Wallet.objects.get(user=self.request.user)
        context['wallet'] = wallet
        banks = BankAccount.objects.filter(
            wallet=wallet)
        context['banks'] = banks
        return context

    def get_form_kwargs(self):
        kwargs = super(AccountsView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class PaymentIDView(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'

    template_name = "transact/pid.html"
