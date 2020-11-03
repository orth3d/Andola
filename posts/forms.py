from django import forms
from django.forms import TextInput, Textarea, Select, FileInput
from tinymce.widgets import TinyMCE
from .models import Post, Comment, Author

# class TinyMCEWidget(TinyMCE):
#     def use_required_attribute(self, *args):
#         return False


class PostForm(forms.ModelForm):
    # content = forms.CharField(
    #     widget=TinyMCE(
    #         attrs={'required': False, 'cols':30, 'rows':10}
    #     )
    # )
    class Meta:
        model = Post
        fields = ('title', 'overview', 'content', 'thumbnail', 'categories', 'featured', 'previous_post', 'next_post')
        # widgets = {
        #     'title': TextInput(
        #         attrs={
                   
        #         }
        #     )
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['title'].widget.attrs['autofocus'] = True


    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class':'form-control',
        'placeholder': 'Escribe tu comentario',
        'id': 'usercomment',
        'rows': '4'
    }))
    class Meta:
        model = Comment
        fields = ('content', )
