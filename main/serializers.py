from decimal import Decimal

from rest_framework import serializers
from .models import *
from django.db.models import Avg


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class HostelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hostel
        fields = ('id', 'category', 'title', 'description', 'price', 'phone')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.email
        representation['category'] = CategorySerializer(instance.category).data
        representation['images'] = HostelImageSerializer(instance.images.all(), many=True, context=self.context).data
        representation['comments'] = CommentSerializer(instance.comments.all(), many=True, context=self.context).data
        representation['likes'] = instance.likes.count()

        rates = Rating.objects.filter(hostel=instance)
        if not rates:
            representation['rating'] = 'null'
        else:
            sum = 0
            for i in rates:
                sum = sum + i.rating
            representation['rating'] = Decimal(sum) / Decimal(Rating.objects.filter(hostel=instance).count())

        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        validated_data['author_id'] = user_id
        hostel = Hostel.objects.create(**validated_data)
        return hostel


class HostelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostelImage
        fields = '__all__'

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''
        return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        validated_data['author_id'] = user_id
        comment = Comment.objects.create(author=request.user, **validated_data)
        return comment


class LikeSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        likes, obj = Like.objects.update_or_create(author=request.user, **validated_data)
        return likes


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        rating, obj = Rating.objects.update_or_create(author=request.user, **validated_data)
        return rating


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        favorite, obj = Favorite.objects.update_or_create(author=request.user, **validated_data)
        return favorite
