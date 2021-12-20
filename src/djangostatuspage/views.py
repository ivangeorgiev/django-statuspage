"""View definitions for djangostatuspage application."""

from django.shortcuts import render  # noqa: F401
from rest_framework import generics

from . import models, schemas

# https://www.django-rest-framework.org/api-guide/serializers/#dealing-with-nested-objects
# class SystemCategorySerializer(serializers.Serializer):
#     category_id


class StatusPageView(generics.ListAPIView):
    """Status page API view."""

    schema = schemas.StatusPageSchema()
    queryset = models.StatusPage.objects.all()
    serializer_class = schemas.StatusPageSerializer
