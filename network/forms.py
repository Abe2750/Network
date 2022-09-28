from django.forms import ModelForm
from network.models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = "__all__"