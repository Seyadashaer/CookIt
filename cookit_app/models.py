from django.db import models
import bcrypt
import re

NAME_REGEX = re.compile(r'[a-zA-Z]+$')
EMAIL_REGEX = re.compile(r'[a-zA-Z0-9.+_-]+@[a-zA_Z0-9._-]+\.[a-zA-z]+$')
TIME_REGEX = re.compile(r'[0-9]+[0-9]+[:]+[0-9]+[0-9]+[:]+[0-9]+[0-9]')
# UserManager class is used to handle the validation for user registration and login
class UserManager(models.Manager):
    def validate_register(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name should be at least 2 characters"
        elif not NAME_REGEX.match(postData['first_name']):
            errors['first_name'] = "First Name should contain letters only"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name should be at least 2 characters"
        elif not NAME_REGEX.match(postData['last_name']):
            errors['last_name'] = "Last name should contain letters only"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email format"
        elif len(User.objects.filter(email = postData['email'])) > 0:
            errors['email'] = "Email already registered"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters"
        if postData['password'] != postData['password_confirm']:
            errors['password_confirm'] = "Passwords do not match"

        return errors

    def validate_login(self, postData):
        errors = {}
        if len(User.objects.filter(email = postData['email'])):
            user = User.objects.get(email = postData['email'])
            if bcrypt.checkpw(postData['password'].encode(), user.password):
                return errors
            else:
                errors['login'] = "Email OR Password incorrect"
                return errors
        else:
            errors['login'] = "Email OR Password incorrect"
            return errors

# User class is used to define the user model, with fields for first name, last name, email, password
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.BinaryField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class RecipeManager(models.Manager):
    def validate_recipe(self, postData):
        errors = {}
        if not postData['serving_people'].isdigit():
            errors['password_confirm'] = "Serving People must be an integer."
        if not TIME_REGEX.match(postData['preparation_time']):
            errors['preparation_time'] = "Invalid Time format"
        if not TIME_REGEX.match(postData['cooking_time']):
            errors['cooking_time'] = "Invalid Time format"
        return errors

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    recipe_img = models.ImageField(upload_to = "recipe/")
    preparation_time = models.CharField(max_length=255)
    cooking_time = models.CharField(max_length=255)
    serving_people = models.IntegerField()
    total_rating = models.IntegerField(default=0)
    user = models.ForeignKey(User,related_name="recipes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = RecipeManager()

class Instruction(models.Model):
    specification=models.CharField(max_length=255)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='instructions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.CharField(max_length=255)
    recipe = models.ManyToManyField(Recipe, related_name='ingredients')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="reviewed_recipes", on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)