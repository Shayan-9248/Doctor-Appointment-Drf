from django.db import models
from django.conf import settings
from django.utils.text import slugify 


class TimeStamp(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStamp):
    name = models.CharField(max_length=150)
    slug = models.SlugField(null=True)

    def __str__(self) -> str:
        return self.name
    
    def save(self):
        self.slug = slugify(self.name)
        super().save()


class Doctor(TimeStamp):
    class Gender(models.TextChoices):
        male = 'm', 'Male'
        female = 'f', 'Female'
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    expertise = models.CharField(max_length=150)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=15, choices=Gender.choices)
    appointments = models.ManyToManyField('Appointment', blank=True, 
    related_name='appointments')
    picture = models.ImageField(upload_to='media/%Y-%m-%d/', null=True)

    def __str__(self):
        return f'{self.doctor.username} - {self.expertise}'


class Appointment(TimeStamp):
    class Status(models.TextChoices):
        accepted = 'a', 'Accept'
        canceled = 'c', 'Cancel'
        finished = 'f', 'Finished'
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    status = models.CharField(max_length=15, default=Status.accepted,
     choices=Status.choices)
    date = models.DateTimeField()
    time = models.DateField()
    # price = models.PositiveIntegerField()
    # discount = models.PositiveIntegerField(null=True)
    # total_price = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f'{self.doctor.username} - {self.category}'
    
    # def save(self):
    #     self.total_price = self.get_total_price
    #     super().save()
    
    # @property
    # def get_total_price(self):
    #     if not self.discount:
    #         return self.unit_price
    #     elif self.discount:
    #         total = (self.discount * self.unit_price) / 100
    #         return int(self.unit_price - total)
    #     return self.total_price
