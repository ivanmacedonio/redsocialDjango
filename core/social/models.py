from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='batman.png')
    def __str__(self):
        return f'Perfil de {self.user.username}'
    
    def following(self):
        user_ids = Relationship.objects.filter(from_user = self.user)\
        .values_list('to_user_id', flat=True)  #busca en la tabla relationship el usuario del perfil y retorna la lista de valores de usuarios con los que se relaciona
#el usuario A es el usuario del perfil y retorna todos los usuarios B con los que se relaciona
        return User.objects.filter(id__in=user_ids) #id__in hace un filtro en la consulta

    def followers(self):
        user_ids = Relationship.objects.filter(to_user = self.user)\
        .values_list('from_user_id', flat=True)  
        return User.objects.filter(id__in=user_ids) 

class Post(models.Model):
    id = models.IntegerField(unique=True, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    timestamp = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'{self.user.username} : {self.content}'
    
class Relationship(models.Model):#Esta tabla guarda dos usuarios por row, el usuario A y el usuario B
    from_user = models.ForeignKey(User, related_name='relationship', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='related_to', on_delete=models.CASCADE)

    def __str__(self):
        return f'De {self.from_user} Para {self.to_user}'

class RelationshipLike(models.Model):#Esta tabla guarda dos usuarios por row, el usuario A y el usuario B
    from_user = models.ForeignKey(User, related_name='relationship', on_delete=models.CASCADE)
    to_post = models.ForeignKey(Post, related_name='related_to', on_delete=models.CASCADE)

    def __str__(self):
        return f'De {self.from_user} Para {self.to_user}'
