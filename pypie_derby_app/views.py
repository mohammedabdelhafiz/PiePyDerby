from django.shortcuts import render, redirect
from . import models
from django.contrib import messages

def render_login_regi(request):
    return render(request, 'login_regi.html')

def register(request):
    errors = models.validate_regi(request)
    print(errors)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
    else:
        models.register(request)
    return redirect('/')

def login(request):
    if request.method == 'POST':
        if models.login(request):
            return redirect('/dashboard')
    return redirect('/')

def logout(request):
    try: 
        del request.session['user_id']
        redirect('/')
    except:
        pass
    return redirect('/')

def dashboard(request):
    id = request.session['user_id']
    user = models.get_user_by_id(id)
    pies = models.get_user_pies(id)
    context = {
        'user': user,
        'pies': pies,
    }
    return render(request, 'dashboard.html', context)

def add_pie(request):
    user_id = request.session['user_id']
    user = models.get_user_by_id(user_id)
    errors = models.validate_presence(request)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
    else:
        models.add_pie(request, user)
    return redirect('/dashboard')

def render_edit_pie(request, id):
    pie = models.get_pie_by_id(id)
    context = {
        'pie': pie,
    }
    return render(request, 'edit_pie.html', context)

def edit_pie(request):
    models.update_pie(request)
    return redirect('/dashboard')

def delete_pie(request, id):
    models.delete_pie(id)
    return redirect('/pies')

def pies_show(request):
    pies = models.get_pies_asc()
    context = {
        'pies': pies,
    }
    return render(request, 'show_pies.html', context)

def pie_show(request, id):
    pie = models.get_pie_by_id(id)
    liked = models.is_pie_liked_by_id(pie_id=id, user_id=request.session['user_id'])
    context = {
        'pie': pie,
        'liked': liked,
    }
    return render(request, 'show_pie.html', context)

def vote(request, id):
    user_id=request.session['user_id']
    models.vote(pie_id=id, user_id=user_id)
    return redirect('/show/'+str(id))

def unvote(request, id):
    user_id=request.session['user_id']
    models.unvote(pie_id=id, user_id=user_id)
    return redirect('/show/'+str(id))