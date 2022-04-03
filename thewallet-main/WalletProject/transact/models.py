from django.db import models
import uuid
from accounts.models import User, Wallet


class Transaction(models.Model):
    """Model to store trasaction details

    Args:
        models ([type]): [description]
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    datetime = models.DateTimeField(auto_now_add=True)
    wallet = models.ForeignKey(
        Wallet, on_delete=models.SET_NULL, null=True, blank=True)
    t_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    t_from = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tt_from')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    memo = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return str(self.datetime)

    class Meta:
        ordering = ['-datetime']


class Request(models.Model):
    """Model to store money requests details

    Args:
        models ([type]): [description]
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    datetime = models.DateTimeField(auto_now_add=True)
    wallet = models.ForeignKey(
        Wallet, on_delete=models.SET_NULL, null=True, blank=True)
    t_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    t_from = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='t_from')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    memo = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return str(self.datetime)

    class Meta:
        ordering = ['-datetime']
