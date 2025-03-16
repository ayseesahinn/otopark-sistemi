from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('alıcı', 'Alıcı'),
        ('satıcı', 'Satıcı'),
    ]
    
    user_type = models.CharField(max_length=6, choices=USER_TYPE_CHOICES)
    
    def __str__(self):
        return self.username

class Parking(models.Model):
    satıcı = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'satıcı'})
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=255)  # Örnek: "İstanbul, Kadıköy"
    total_spots = models.IntegerField()
    available_spots = models.IntegerField()
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.location}"
    
    def update_available_spots(self, spots_reserved):
        self.available_spots -= spots_reserved
        self.save()

class Reservation(models.Model):
    alıcı = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'alıcı'})
    otopark = models.ForeignKey(Parking, on_delete=models.CASCADE)
    reserved_time = models.DateTimeField()
    spots_reserved = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        self.total_price = self.spots_reserved * self.otopark.price_per_hour
        self.otopark.update_available_spots(self.spots_reserved)  # Boş alanları güncelle
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Reservation by {self.alıcı.username} at {self.otopark.name}"

class Review(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comment = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Review for {self.reservation.otopark.name} by {self.reservation.alıcı.username}"


