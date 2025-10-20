from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    # Bu yerda siz statistik ma’lumotlarni jo‘natasiz
    stats = {
        'students': 120,
        'courses': 25,
        'teachers': 10,
        'active_users': 45,
    }
    return render(request, 'dashboard/dashboard.html', {'courses': stats})
