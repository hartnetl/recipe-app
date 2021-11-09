from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from taggit.models import Tag
from .models import Recipe
from .forms import RecipeForm, CommentForm


def handle_not_found(request, exception):
    return render(request, 'not-found.html')

class TagMixin(object):
    def get_context_data(self, **kwargs):
        context = super(TagMixin, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context


class RecipeList(TagMixin, generic.ListView):
    model = Recipe
    queryset = Recipe.objects.filter(status=1, approved=True).order_by('title')
    template_name = 'recipes.html'
    paginate_by = 8


class TagList(TagMixin, generic.ListView):
    model = Recipe
    template_name = 'recipes.html'

    def get_queryset(self):
        return Recipe.objects.filter(tags__slug=self.kwargs.get('tag_slug'))


class CategoryView(generic.ListView):
    model = Recipe
    queryset = Recipe.objects.values('category').distinct()
    template_name = 'recipes.html'


class FullRecipe(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects
        recipe = get_object_or_404(queryset, slug=slug)
        comments = recipe.comments.filter(approved=True).order_by('date_posted')  # noqa
        saves = False
        if recipe.saved.filter(id=self.request.user.id).exists():
            saves = True

        return render(
            request,
            'view_recipe.html',
            {
                'recipe': recipe,
                'comments': comments,
                'saves': saves,
                "commented": False,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Recipe.objects.filter(status=1)
        recipe = get_object_or_404(queryset, slug=slug)
        comments = recipe.comments.filter(approved=True).order_by('date_posted') # noqa
        saves = False
        if recipe.saved.filter(id=self.request.user.id).exists():
            saves = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.recipe = recipe
            comment.save()
            messages.success(request, "Your comment was sent successfully and \
                             is pending approval by admin.")
        else:
            comment_form = CommentForm()

        return render(
            request,
            'view_recipe.html',
            {
                'recipe': recipe,
                'comments': comments,
                "commented": True,
                "saves": saves,
                "comment_form": CommentForm()
            },
        )


# CRUD FOR RECIPES (R is the full recipe view above)
class RecipeCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipe_form.html'
    success_message = "Your recipe has been successfully submitted and is now \
                        awaiting approval by admin"

    def get_success_url(self):
        return reverse('full_recipe', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        form.instance.creator = self.request.user
        print(form.cleaned_data)
        return super().form_valid(form)


class RecipeUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'update_recipe_form.html'
    success_message = "Your recipe has been successfully updated and will be \
                        reviewed by admin"

    def get_success_url(self):
        return reverse('full_recipe', kwargs={'slug': self.object.slug})


class RecipeDelete(LoginRequiredMixin, DeleteView):
    model = Recipe
    template_name = 'recipe_confirm_delete.html'
    success_url = reverse_lazy("recipes")


class ContactPage(TemplateView):
    template_name = 'contact.html'
    success_message = "Your message has been sent and someone will get back \
                        to you shortly. Please don't leave this page until \
                        the form clears."


# View to save recipes

class SaveRecipe(View):

    def post(self, request, slug):
        print(slug)
        recipe = get_object_or_404(Recipe, slug=slug)

        if recipe.saved.filter(id=request.user.id).exists():
            recipe.saved.remove(request.user)
        else:
            recipe.saved.add(request.user)

        return HttpResponseRedirect(reverse('full_recipe', args=[slug]))


# VIEWS FOR THE PROFILE PAGE - USERS RECIPES
class ProfileRecipes(View):

    def get(self, request, *args, **kwargs):
        published = Recipe.objects.filter(status=1, creator=request.user)
        draft = Recipe.objects.filter(status=0, creator=request.user)
        # display recipes saved by user credit
        # https://www.py4u.net/discuss/1270319
        # https://stackoverflow.com/questions/12615154/how-to-get-the-currently
        # -logged-in-users-user-id-in-django
        current_user = request.user
        saved = User.objects.get(pk=current_user.id).saved_recipes.all()

        return render(
            request,
            'profile.html',
            {
                'published': published,
                'draft': draft,
                'saved': saved
            },
        )


# Category views

class BreakfastView(generic.ListView):
    model = Recipe
    queryset = Recipe.objects.filter(status=1, approved=True,
                                     category='BFAST').order_by('title')
    template_name = 'breakfast.html'
    paginate_by = 8


class LunchView(generic.ListView):
    model = Recipe
    queryset = Recipe.objects.filter(status=1, approved=True,
                                     category='LUNCH').order_by('title')
    template_name = 'lunch.html'
    paginate_by = 8


class DinnerView(generic.ListView):
    model = Recipe
    queryset = Recipe.objects.filter(status=1, approved=True,
                                     category='DINNER').order_by('title')
    template_name = 'dinner.html'
    paginate_by = 8


class DrinksView(generic.ListView):
    model = Recipe
    queryset = Recipe.objects.filter(status=1, approved=True,
                                     category='DRINKS').order_by('title')
    template_name = 'drinks.html'
    paginate_by = 8


class OtherView(generic.ListView):
    model = Recipe
    queryset = Recipe.objects.filter(status=1, approved=True,
                                     category='OTHER').order_by('title')
    template_name = 'other.html'
    paginate_by = 8
