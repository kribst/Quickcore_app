import datetime
import os
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse, FileResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.views.decorators.http import require_POST
from .forms import UserRegistrationForm, AddStackForm, CustomerUser
from .models import Stack, ChatMessage, Visite
from .middleware import OnlineUsersMiddleware

# Create your views here.

@login_required
def chat_view(request):
    other_user = CustomerUser.objects.exclude(id=request.user.id).first()
    messages = ChatMessage.objects.all().order_by('timestamp')
    return render(request, 'message/chat.html', {'messages': messages, 'other_user': other_user})


@login_required
def get_messages(request):
    messages = ChatMessage.objects.all().order_by('timestamp')
    messages_data = [
        {
            'username': message.user.username,
            'message': message.message,
            'timestamp': message.timestamp.strftime("%H:%M"),
            'user_image': message.user.image.url if message.user.image else '/static/default_image.png'
        }
        for message in messages
    ]
    return JsonResponse(messages_data, safe=False)


@login_required
def send_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        chat_message = ChatMessage.objects.create(user=request.user, message=message)
        return JsonResponse({
            'username': chat_message.user.username,
            'message': chat_message.message,
            'timestamp': chat_message.timestamp.strftime("%H:%M"),
            'user_image': chat_message.user.image.url if chat_message.user.image else '/static/default_image.png'
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)


def acceuil(request):
    visiteur, created = Visite.objects.get_or_create(pk=1)  # Assurez-vous d'avoir un objet Visite
    visiteur.nombre_de_visiteurs += 1  # Incrémentez le nombre de visiteurs
    visiteur.save()
    return render(request, 'acceuil.html')


def signup(request):
    context = {}
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            context['errors'] = form.errors
    else:
        form = UserRegistrationForm
    return render(request, 'accounts/signup.html', context={'form': form})


@login_required
def dashboard(request):
    visiteur, created = Visite.objects.get_or_create(pk=1)  # Assurez-vous d'avoir un objet Visite
    visiteur.nombre_de_visiteurs += 1  # Incrémentez le nombre de visiteurs
    visiteur.save()
    return render(request, 'dashboard/dashboard.html',{'visite': visite})



@login_required
def addstack(request):
    today = datetime.now()
    current_time = today.strftime('%H H %M min %S s')
    customer = CustomerUser
    user_stacks = Stack.objects.filter(user=request.user)
    if request.method == 'POST':
        form = AddStackForm(request.POST, request.FILES)
        if form.is_valid():
            stack = form.save(commit=False)
            stack.user = request.user
            stack.save()
            return render(request, 'dashboard/allstack.html', {
        'stacks': user_stacks,
        'today': today,
        'current_time': current_time,
    })
    else:
        form = AddStackForm()
    return render(request, 'dashboard/add_stack.html', {'form': form, 'customer': customer, 'today': today, 'current_time': current_time,})


@login_required
def allstack(request):
    today = datetime.now()
    current_time = today.strftime('%H H %M min %S s')
    stacks = Stack.objects.all()  # Récupère tous les stacks
    paginator = Paginator(stacks, 10)  # 10 stacks par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        stack_ids = request.POST.getlist('stack_ids[]')
        if stack_ids:
            Stack.objects.filter(id__in=stack_ids).delete()
            messages.success(request, 'Stacks supprimés avec succès.')
        else:
            messages.warning(request, 'Aucun stack sélectionné.')

    context = {
        'stacks': page_obj,
        'page_obj': page_obj,
        'today': today,
        'current_time': current_time,
    }
    return render(request, 'dashboard/allstack.html', context)


@login_required
@require_POST
def delete_stacks(request):
    today = datetime.now()
    current_time = today.strftime('%H H %M min %S s')
    user_stacks = Stack.objects.filter(user=request.user)
    # Récupérer les IDs sous forme de liste
    stack_ids = request.POST.getlist('stack_ids[]')

    # Si aucune ID n'est reçue, vérifiez si un ID séparé par des virgules est présent
    if not stack_ids:
        stack_ids_string = request.POST.get('stack_ids', '')
        if stack_ids_string:
            stack_ids = stack_ids_string.split(',')  # Séparez les IDs par des virgules

    # Vérification et conversion des IDs
    valid_stack_ids = []
    invalid_ids = []

    # Traiter chaque ID
    for id in stack_ids:
        id = id.strip()  # Supprimer les espaces autour de chaque ID

        # Vérifier si l'ID est une chaîne contenant d'autres IDs
        if ',' in id:
            # Diviser les IDs et traiter chaque partie
            sub_ids = id.split(',')
            for sub_id in sub_ids:
                sub_id = sub_id.strip()  # Supprimer les espaces
                try:
                    valid_stack_ids.append(int(sub_id))  # Convertir en entier
                except ValueError:
                    invalid_ids.append(sub_id)  # Ajouter à la liste des IDs invalides
        else:
            # Traitement standard pour un seul ID
            try:
                valid_stack_ids.append(int(id))  # Convertir en entier
            except ValueError:
                invalid_ids.append(id)  # Ajouter à la liste des IDs invalides

    if invalid_ids:
        return JsonResponse({'success': False, 'error': 'Invalid ID format.', 'invalid_ids': invalid_ids})

    if valid_stack_ids:  # Vérifier si la liste d'IDs valides n'est pas vide
        stacks = Stack.objects.filter(id__in=valid_stack_ids, user=request.user)
        stacks.delete()
        return render(request, 'dashboard/allstack.html', {
        'stacks': user_stacks,
        'today': today,
        'current_time': current_time,
    })

    return JsonResponse({'success': False, 'error': 'No IDs provided.'})


def documentationfile(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)

    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'  # Définit le nom du fichier dans le téléchargement
        return response
    else:
        raise Http404('File not found')


def search_view(request):
    today = datetime.now()
    current_time = today.strftime('%H H %M min %S s')
    query = request.GET.get('q')
    results = []
    message = "Aucun résultat trouvé."

    if query:
        results = Stack.objects.filter(title__icontains=query)

        if not results:
            message = "Aucun résultat trouvé pour"

    # Pagination des résultats
    paginator = Paginator(results, 4)  # 10 résultats par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard/search_results.html', {
        'results': page_obj,
        'query': query,
        'message': message,
        'today': today,
        'current_time': current_time,
    })



def stack_detail(request, pk):
    today = datetime.now()
    current_time = today.strftime('%H H %M min %S s')
    stack = get_object_or_404(Stack, pk=pk)
    context = {
        'stack': stack,
        'today': today,
        'current_time': current_time,
    }
    return render(request, 'dashboard/stack_detail.html', context)
