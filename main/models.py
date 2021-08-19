from django.db import models

from account.models import MyUser


class Category(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True)
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class Hostel(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='hostels')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='hostels')
    title = models.CharField(max_length=255)
    description = models.TextField()
    phone = models.CharField(max_length=12, default=996)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return self.title


class HostelImage(models.Model):
    image = models.ImageField(upload_to='hostels', blank=True, null=True)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='images')


class Comment(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='comments')
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ('created',)


class Like(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='likes')
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='likes')
    likes = models.BooleanField(default=False)

    def __str__(self):
        return self.likes


class Rating(models.Model):
    author = models.ForeignKey(MyUser, default='', on_delete=models.CASCADE, related_name='rating')
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='rating')
    rating = models.SmallIntegerField()

    class Meta:
        ordering = ['-rating']

    def __str__(self):
        return f'{self.rating}'


class Favorite(models.Model):
    author = models.ForeignKey(MyUser, default='', on_delete=models.CASCADE, related_name='favorite')
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='favorite')
    favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.favorite
