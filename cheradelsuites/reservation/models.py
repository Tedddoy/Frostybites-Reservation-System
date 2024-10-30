from django.db import models
from django.contrib.auth.models import User

class Services(models.Model):
    service_name = models.CharField(max_length=255, null=True)
    details = models.CharField(max_length=255, null=True)
    price = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.service_name}"

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    date = models.DateField()
    phone_number = models.CharField(max_length=20, null=True)
    service = models.ForeignKey(Services, on_delete=models.CASCADE, null=True)

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Declined', 'Declined'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
      if self.user:
        return f"{self.user.username} - {self.user.first_name} - {self.user.last_name} - {self.service} on {self.date}"
      else:
        return f"{self.user} - {self.service} on {self.date}"  
      
class Transaction(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    amount = models.FloatField(max_length=200)
    date = models.DateTimeField(null=True)
    

    def __str__(self):
        if self.reservation:
            return f"{self.reservation.user} - {self.title} - {self.date}" 
        else:
            return f"No associated booking - {self.title}"