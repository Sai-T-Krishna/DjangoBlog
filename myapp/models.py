
from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.utils.timezone import now

# Create your models here.

# Tag model
class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f"{self.caption}"

# author model -- one author can write many posts
class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

# post model
class Post(models.Model):
    title = models.CharField(max_length=100)
    excerpt = models.CharField(max_length=200)
    # image name to imagefield
    # image_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to = "posts", null=True)
    date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True, db_index=True)
    content = models.TextField(validators = [MinLengthValidator(10)])

    # one to many relation ship which is foreign key
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name='posts')  # dont delete complete post

    # many to many relation for tag model and post model
    tags = models.ManyToManyField(Tag)

    def __str__(self) -> str:
        return f"{self.title}"

# every post can have many comments - one to manyy
class Comment(models.Model):
    user_name = models.CharField(max_length=20)
    user_email = models.EmailField()
    text = models.TextField(max_length=400)
    date = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')






