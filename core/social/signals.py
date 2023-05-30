from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


'''

cuando creamos un User con el modelo de django, se crea un perfil automaticamente 
en nuestra BBDD, eso gracias a la signal 

sender - modelo que al ser creado activa la señal y añade  un True a created
instance - data 
created - al ser true activa la señal

'''

@receiver(post_save, sender=User)  #conectamos la funcion con el modelo activador
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)


'''sigue en apps.py importando las señales en ready'''