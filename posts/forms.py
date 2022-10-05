from django import forms

from crispy_forms.helper import FormHelper

from posts.models import Post

class PostCreateForm(forms.Form):

    class Meta:
        model = Post
        fields = '__all__'

    def __init__(self, *args, **kws):
        # To get request.user. Do not use kwargs.pop('user', None) due to potential security hole
        self.user = kws.pop('user')
        super().__init__(*args, **kws)
        self.fields['user'].initial = self.user
