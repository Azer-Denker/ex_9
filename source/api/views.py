from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from webapp.models import Photo, Favorite


class AddToFavorite(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, reqyest, *args, **kwargs):

        photo = get_object_or_404(Photo, pk=kwargs['pk'])
        print(photo)
        favorite, created = Favorite.objects.get_or_create(photo=photo, author=self.request.user)
        if created:
            favorite.save()
            return Response({'pk': favorite.pk})
        else:
            return Response({'message': 'you also added this photo to favorite'}, status=403)


class RemoveFromFavorite(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,  request, *args, **kwargs):
        photo = get_object_or_404(Photo, pk=kwargs['pk'])
        favorite = get_object_or_404(Favorite, photo=photo, author=self.request.user)
        favorite.delete()
        return Response({'message': f'you succesfuly remove this photo( pk = {kwargs["pk"]}) from your favorite'})