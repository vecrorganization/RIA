# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from ourWeb.models import Order

User._meta.get_field('email')._unique = True

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

    def get_order(self):
        try:
            return Order.objects.get(addressUser__user=self.user,status=Order.IN_PROCESS)
        except:
            return Order.objects.create(user=self.user)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class AddressUser(models.Model):
    user = models.ForeignKey(User)
    address = models.ForeignKey("ourAdmin.Address", verbose_name="Dirección",
                                related_name="addressUser") 
    
    class Meta:
        unique_together = (('user','address'),)

    def __str__(self):
        return str(self.address)


class PaymentUser(models.Model):
    user = models.ForeignKey(User)
    paymentMethod = models.ForeignKey("ourAdmin.PaymentMethod", verbose_name="Método de pago",
                                      related_name="paymentUser") 