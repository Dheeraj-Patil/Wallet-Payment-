from django.forms import ModelForm, TextInput, EmailInput, EmailField
from .models import Transaction
from accounts.models import User, Wallet


class TransactionForm(ModelForm):
    email = EmailField(required=False)

    def __init__(self, user, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=False):
        m = super(TransactionForm, self).save(commit=False)
        # do custom stuff
        wallet = Wallet.objects.get(user=self.user)
        print(self.cleaned_data)
        if self.cleaned_data['email']:
            try:
                m.t_to = User.objects.get(email=self.cleaned_data['email'])
            except User.DoesNotExist:
                m.t_to = User.objects.create(email=self.cleaned_data['email'])
        try:
            r_wallet = Wallet.objects.get(user=m.t_to)
        except Wallet.DoesNotExist:
            r_wallet = None
        m.t_from = self.user
        m.wallet = wallet
        if r_wallet is not None:
            r_wallet.balance += m.amount
            r_wallet.save()
        m.save()
        return m

    class Meta:
        model = Transaction
        fields = ['t_to', 'amount', 'memo', 'email']
        widgets = {
            'email': EmailInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Email that is not in wallet'
            }),
            # 'memo': TextInput(attrs={
            #     'class': "form-control",
            #     'style': 'max-width: 300px;',
            #     'placeholder': 'Memo'
            # }),
            # 'amount': TextInput(attrs={
            #     'class': "form-control",
            #     'style': 'max-width: 300px;',
            #     'placeholder': 'Amount in $'
            # })
        }
