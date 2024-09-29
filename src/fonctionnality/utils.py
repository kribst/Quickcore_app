# utils.py
from .models import Visite
from django.utils import timezone
from datetime import timedelta
from .models import Visite
from django.utils import timezone
from datetime import timedelta

# utils.py
from .models import Visite
from django.utils import timezone
from datetime import timedelta

# utils.py
def get_online_and_visiteurs(request):
    visiteur = Visite.objects.first()
    total_visiteurs = visiteur.nombre_de_visiteurs if visiteur else 0

    online_users_count = 0

    # Compter les utilisateurs en ligne
    for session_key in request.session.keys():
        session_data = request.session.get(session_key)

        # Vérifier si last_activity est défini
        if isinstance(session_data, dict) and 'last_activity' in session_data:
            last_activity_time = timezone.datetime.fromisoformat(session_data['last_activity'])
            if last_activity_time > timezone.now() - timedelta(minutes=5):
                online_users_count += 1

    print(f"Visiteurs en ligne : {online_users_count}, Total de visiteurs : {total_visiteurs}")
    return online_users_count, total_visiteurs