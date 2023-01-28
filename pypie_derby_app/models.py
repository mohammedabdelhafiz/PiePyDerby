from django.db import models
import bcrypt
import re

class PyPieManager(models.Manager):
    errors = {}
    EMAIL_REGEX = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    def presence_validator(self, postData):
        self.errors = {}
        for key, value in postData.items():
            if len(value) < 1:
                self.errors['required'] = f"All fields are required!"
                break
        return self.errors

    def regi_validator(self, postData):
        self.errors = {}
        for key, value in postData.items():
            if len(value) < 1:
                self.errors['required'] = f"All fields are required!"
                break
        if len(postData['first_name']) < 3:
            self.set_error('first_name', 'First name must be at least 3 characters')
        if len(postData['last_name']) < 3:
            self.set_error('last_name', 'Last name must be at least 3 characters')
        if not self.EMAIL_REGEX.match(postData['email']):
            self.set_error('email', 'Invalid email address')
        if len(postData['password']) < 8:
            self.set_error('password', 'Password must be at least 8 characters')
        if postData['password'] != postData['conf_password']:
            self.set_error('conf_password', 'Passwords do not match')
        return self.errors

    def set_error(self, key, value):
        self.errors[key] = value

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PyPieManager()

class Pie(models.Model):
    name = models.CharField(max_length=255)
    filling = models.CharField(max_length=255)
    crust = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name="pies", on_delete = models.CASCADE, null=True)
    voted_by = models.ManyToManyField(User, related_name="fav_pies")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PyPieManager()

def register(request):
    user = request.POST
    first_name = user['first_name']
    last_name = user['last_name']
    email = user['email']
    password = user['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    print(pw_hash)
    User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pw_hash)

def login(request):
    post = request.POST
    user = User.objects.filter(email=post['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(post['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return True

def validate_regi(request):
    return User.objects.regi_validator(request.POST)

def validate_presence(request):
    return Pie.objects.presence_validator(request.POST)

def get_user_by_id(id):
    return User.objects.get(id=id)

def get_user_pies(id):
    user = get_user_by_id(id)
    return user.pies.all()

def add_pie(request, user):
    pie = request.POST
    name = pie['name']
    filling = pie['filling']
    crust = pie['crust']
    Pie.objects.create(name=name, filling=filling, crust=crust, created_by = user)

def get_pie_by_id(id):
    return Pie.objects.get(id=id)

def get_pies_asc():
    return Pie.objects.all()

def is_pie_liked_by_id(pie_id, user_id):
    pie = get_pie_by_id(pie_id)
    user = get_user_by_id(user_id)
    for user in pie.voted_by.all():
        if user.id == user_id:
            return True
        else: return False
    
def vote(pie_id, user_id):
    pie = get_pie_by_id(pie_id)
    user = get_user_by_id(user_id)
    pie.voted_by.add(user)

def unvote(pie_id, user_id):
    pie = get_pie_by_id(pie_id)
    user = get_user_by_id(user_id)
    pie.voted_by.remove(user)

def delete_pie(pie_id):
    pie = get_pie_by_id(pie_id)
    pie.delete()

def update_pie(request):
    pie = request.POST
    name = pie['name']
    filling = pie['filling']
    crust = pie['crust']
    id = pie['pie_id']
    old_pie = get_pie_by_id(id)
    old_pie.name = name
    old_pie.filling = filling
    old_pie.crust = crust
    old_pie.save()