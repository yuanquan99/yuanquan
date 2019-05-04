from django import forms
from article.models import Article
from django.db.models import ObjectDoesNotExist
from mdeditor.widgets import MDEditorWidget
from ckeditor.widgets import CKEditorWidget


class ArticleForm(forms.Form):
    content = forms.CharField(widget=MDEditorWidget)


class CommentForm(forms.Form):
    text = forms.CharField(widget=CKEditorWidget)
