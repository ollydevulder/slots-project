from django.db import models
from django.contrib.auth.models import User


class Slot(models.Model):
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE)
    position = models.IntegerField()
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
    )

    def __str__(self):
        return f"<Slot shop='{self.shop.name}' taken? {bool(self.user)}>"


class Shop(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slot_amount = models.PositiveIntegerField(default=10)

    def __str__(self):
        return f"<Shop '{self.name}'>"

    def save(self, *args, **kwargs):
        # Limit the slot amount.
        if self.slot_amount > 100:
            self.slot_amount = 100

        super().save(*args, **kwargs)
        # Overwrite save method to add slot objects.
        if self.slot_set.count() != self.slot_amount:
            for i in range(self.slot_amount):
                try:
                    self.slot_set.get(position=i)
                except Slot.DoesNotExist:
                    # The slot does not exist.
                    Slot(shop=self, position=i).save()


    @property
    def ordered_slots(self):
        # Template property for the sorted slots.
        return self.slot_set.order_by('position')

    @property
    def get_amount_available_slots(self):
        return len(self.slot_set.filter(user=None))
