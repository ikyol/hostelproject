from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from django.db.models import Q
from rest_framework.mixins import UpdateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django.db.models import Avg
from main.models import *
from main.permissions import IsAuthorPermission
from main.serializers import *


class MyPaginationClass(PageNumberPagination):
    page_size = 3

    def get_paginated_response(self, data):
        return super().get_paginated_response(data)


class PermissionMixin:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAuthenticated, ]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission, ]
        else:
            permissions = []
        return [permission() for permission in permissions]


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    pagination_class = MyPaginationClass


class HostelViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = Hostel.objects.all()
    serializer_class = HostelSerializer
    pagination_class = MyPaginationClass
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    @action(detail=False, methods=['get'])
    def my_hostels(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serializers = HostelSerializer(queryset, many=True,
                                       context={'request': request})
        return Response(serializers.data, 200)

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        serializers = HostelSerializer(queryset, many=True, context={'request': request})
        return Response(serializers.data, 200)

    # @action(detail=False, methods=['get'])
    # def favorite(self, request, pk=None):
    #     queryset = self.get_queryset()
    #     queryset = queryset.filter(author=request.user)
    #     serializers


class HostelImageView(PermissionMixin, generics.ListCreateAPIView):
    queryset = HostelImage.objects.all()
    serializer_class = HostelImageSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class CommentViewSet(PermissionMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context


class LikeViewSet(PermissionMixin, ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def my_likes(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serializers = LikeSerializer(queryset, many=True,
                                         context={'request': request})
        return Response(serializers.data, 200)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context


class RatingViewSet(PermissionMixin, ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def my_ratings(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serializers = RatingSerializer(queryset, many=True,
                                         context={'request': request})
        return Response(serializers.data, 200)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context


class FavoriteViewSet(PermissionMixin, ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    @action(detail=False, methods=['get'])
    def my_favorites(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serializers = FavoriteSerializer(queryset, many=True,
                                         context={'request': request})
        return Response(serializers.data, 200)