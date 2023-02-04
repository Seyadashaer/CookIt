from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *

categories=['Breakfast','Lunch','Dinner','Dessert','Salad', 'Drinks']
categories_count=[]
for i in range(6):
    categories_count.append([categories[i], len(Recipe.objects.filter(category=categories[i]))])

# This function to display the home page of the website after the user has logged in
def index(request): 
    context={
        'recent_recipes' : Recipe.objects.order_by('-created_at')[:10],
        'featured_recipes' : Recipe.objects.order_by('-total_rating')[:6],
        'categories':categories_count,
    }
    return render(request, 'home.html', context )

# This function renders the register page
def register_page(request):
    return render(request, 'register.html')

# This function renders the login page
def login_page(request): 
    return render(request, 'login.html')


# This function validates the login and logs the user in
def login(request):
    errors = User.objects.validate_login(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login_page')
    else:
        user = User.objects.filter(email=request.POST['email'])
        request.session['id'] = user[0].id
        return redirect('/')

# This function validates the registration information and creates a new user
def register(request):
    errors = User.objects.validate_register(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register_page')
    else:
        User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        )
        user = User.objects.filter(email=request.POST['email'])
        request.session['id'] = user[0].id
        return redirect('/')

# This function clears the session data and redirects the user to the main page
def logout(request):
    request.session.clear()
    return redirect('/')

def my_recipes(request):
    if 'id' in request.session:
        context = {
        "recipes" :Recipe.objects.filter(user=User.objects.get(id=request.session['id'])),
        'title': "My Recipes"
        }
        return render(request, "recipes.html", context)
    return redirect("/")
    

def all_recipes(request):
    all_recipes = Recipe.objects.all()
    context = {
        "recipes" : all_recipes,
        'title' : "All Recipes"
    }
    return render(request, "recipes.html", context)

def category_recipes(request, category_name): 
    category_recipes = Recipe.objects.filter(category=category_name)
    context = { 
        'recipes' : category_recipes,
        'title': category_name
    }
    return render(request, "recipes.html", context)


def add_recipe_page(request):
    if 'id' in request.session:
        context = {
        "categories" :categories,
        }
        return render(request, "add_recipe.html", context)
    return redirect("/")

def add_recipe(request):
    context = {
        "categories" :categories,
        }

    recipe_creator=User.objects.get(id=request.session['id'])
    information=[request.POST['name'],request.POST['category'],request.POST['description'], request.FILES['image'], request.POST['preparation_time'], request.POST['cooking_time'], request.POST['serving_people']]
    recipe = Recipe.objects.create(name=information[0],category=information[1],description=information[2],recipe_img=information[3], preparation_time=information[4], cooking_time=information[5], serving_people=information[6], user = recipe_creator )
    for i in range(int(request.POST['number_of_ingredients'])):
        ingredient_name='ingredient_name_'+ str(i)
        ingredient_quantity='ingredient_quantity_'+ str(i)
        ingredient=Ingredient.objects.create(name=request.POST[ingredient_name], quantity=request.POST[ingredient_quantity])
        recipe.ingredients.add(ingredient)

    for i in range(int(request.POST['number_of_instructions'])):
        instruction_specification='instruction_specification_'+ str(i)
        Instruction.objects.create(specification=request.POST[instruction_specification], recipe=recipe)
    return redirect(f'/recipe_details/{recipe.id}')


def recipe_details(request, recipe_id):
    recipe =  Recipe.objects.get(id=recipe_id)
    ingredients = recipe.ingredients.all()
    instructions = recipe.instructions.all()
        

    context = { 
        'recipe' : recipe,
        "ingredients" : ingredients,
        'instructions' : instructions,
        'recipe_reviews' : Review.objects.filter(recipe = recipe),
        'recipe_reviews_number' : Review.objects.filter(recipe = recipe).count
    }
    return render(request, "recipe_details.html", context)
from math import *
def write_review(request, recipe_id):
    # Get the recipe and user
    user_id = request.session.get('id')
    if user_id:
        user = User.objects.get(id=user_id)
    else:
        return redirect('/login_page')
    recipe = Recipe.objects.get(id=recipe_id)
    user = User.objects.get(id=request.session['id'])
    if request.method == 'POST':
        # Get the rating and review from the request
        rating = request.POST.get('rating')
        review = request.POST.get('review')
        recipe.total_rating += int(rating)
        recipe.total_rating=round(recipe.total_rating/(len(Review.objects.filter(recipe = recipe))+1))
        recipe.save()

        # Create the review
        Review.objects.create(user=user, recipe=recipe, rating=rating, review=review)

        return redirect('/recipe_details/' + str(recipe_id))

def search(request):
    query = request.GET.get('q')
    if query:
        search_recipes = Recipe.objects.filter(name__icontains=query)
    else:
        search_recipes = []
    context = {
        'recipes': search_recipes,
        'categories':categories,
        'title' : 'Search Results'
    }
    return render(request, 'recipes.html', context)


def delete_review(request, review_id):
    review = Review.objects.get(id=review_id)
    user = User.objects.get(id=request.session['id'])

    if user == review.user:
        review.delete()
        return redirect("/recipe_details/" + str(review.recipe.id))
    else:
        return redirect("/recipe_details/" + str(review.recipe.id))
