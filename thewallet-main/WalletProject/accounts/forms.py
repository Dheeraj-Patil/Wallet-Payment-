from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import BankAccount, User, Wallet


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    fullname = forms.CharField(label="First name")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class BankAccountForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(BankAccountForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=False):
        m = super(BankAccountForm, self).save(commit=False)
        # do custom stuff
        wallet = Wallet.objects.get(user=self.user)
        m.wallet = wallet
        print(self.cleaned_data)
        m.save()
        return m

    class Meta:
        model = BankAccount
        fields = ['bank_id', 'account_number']
        # widgets = {
        #     # 'email': EmailInput(attrs={
        #     #     'class': "form-control",
        #     #     'style': 'max-width: 300px;',
        #     #     'placeholder': 'Email that is not in wallet'
        #     # }),
        #     # 'memo': TextInput(attrs={
        #     #     'class': "form-control",
        #     #     'style': 'max-width: 300px;',
        #     #     'placeholder': 'Memo'
        #     # }),
        #     # 'amount': TextInput(attrs={
        #     #     'class': "form-control",
        #     #     'style': 'max-width: 300px;',
        #     #     'placeholder': 'Amount in $'
        #     # })
        # }
