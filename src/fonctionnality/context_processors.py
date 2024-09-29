# context_processors.py
# from .models import Visite

#
# def nombre_visiteurs(request):
#     try:
#         visite = Visite.objects.get(id=1)
#         nombre_visiteurs = visite.nombre_de_visiteurs
#     except Visite.DoesNotExist:
#         nombre_visiteurs = 0
#
#     return {
#         'nombre_visiteurs': nombre_visiteurs,
#         'enligne': ActiveUserMiddleware.get_active_user_count(),
#     }


# context_processors.py
from .utils import get_online_and_visiteurs

def global_variables(request):
    online, total_visiteurs = get_online_and_visiteurs(request)
    return {
        'online': online,
        'visiteur': total_visiteurs,
    }