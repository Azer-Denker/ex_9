from django.urls import path, include

from webapp.views import *

app_name = 'webapp'


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('photo_list/', PIndexView.as_view(), name='p_index'),

    path('photo/', include([
        path('add/', PhotoCreateView.as_view(), name='photo_create'),
        path('<int:pk>/', include([
            path('', PhotoView.as_view(), name='photo_view'),
            path('update/', PhotoUpdateView.as_view(), name='photo_update'),
            path('delete/', PhotoDeleteView.as_view(), name='photo_delete'),
        ])),
    ])),

    path('album/', include([
        path('add/', AlbumCreateView.as_view(), name='album_create'),
        path('<int:pk>/', include([
            path('', AlbumView.as_view(), name='album_view'),
            path('update/', AlbumUpdateView.as_view(), name='album_update'),
            path('delete/', AlbumDeleteView.as_view(), name='album_delete'),
        ])),
    ])),
]
