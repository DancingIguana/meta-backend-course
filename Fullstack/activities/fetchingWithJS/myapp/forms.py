from django import forms
from . import models

class CommentForm(forms.ModelForm):
    class Meta:
        model = models.UserComments
        fields = "__all__"