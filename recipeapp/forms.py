from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Recipe, Comment


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        exclude = ('slug', 'creator', 'date_created', 'approved', 'saved',)
        widgets = {
            'about': SummernoteWidget(),
            'method': SummernoteWidget(),
            'nutrition': SummernoteWidget(),
            'ingredients': SummernoteWidget(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('message',)


class EmailForm(forms.Form):
    recipient = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
