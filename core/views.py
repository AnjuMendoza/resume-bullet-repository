from django.shortcuts import render
from .models import Bullet


def bullet_list(request):
    bullets = Bullet.objects.all()
    return render(request, 'core/bullet_list.html', {'bullets': bullets})