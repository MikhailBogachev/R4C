from django.db import models

from customers.models import Customer


class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    robot_serial = models.CharField(max_length=5,blank=False, null=False)
    is_notified = models.BooleanField(default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'customer': self.customer.email,
            'robot_serial': self.robot_serial
        }

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['customer', 'robot_serial'],
                name='unique order'
            )
        ]
