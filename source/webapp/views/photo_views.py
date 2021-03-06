from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View

from webapp.models import Photo, Chosen


class IndexView(ListView):
    template_name = 'photo/index.html'
    context_object_name = 'photos'
    model = Photo
    ordering = '-creation_date'


class PhotoView(DetailView):
    template_name = 'photo/photo_view.html'
    pk_url_kwarg = 'pk'
    model = Photo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = context['photo'].comments.order_by('-created_at')
        self.paginate_comments_to_context(comments, context)
        context['user'] = self.request.user
        return context

    def paginate_comments_to_context(self, comments, context):
        paginator = Paginator(comments, 10, 0)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        context['paginator'] = paginator
        context['page_obj'] = page
        context['comments'] = page.object_list
        context['is_paginated'] = page.has_other_pages()


class PhotoCreateView(CreateView):
    template_name = 'photo/photo_create.html'
    model = Photo
    fields = ['image', 'description']

    def form_valid(self, form):
        form.instance.author_name = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:index')


class PhotoUpdateView(UpdateView):
    model = Photo
    template_name = 'photo/photo_update.html'
    fields = ['image', 'description', 'author_name']
    context_object_name = 'obj'

    def get_success_url(self):
        return reverse('webapp:index')


class PhotoDeleteView(DeleteView):
    template_name = 'photo/photo_delete.html'
    model = Photo
    context_object_name = 'obj'
    success_url = reverse_lazy('webapp:index')


class PhotoLikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        photo = get_object_or_404(Photo, pk=kwargs.get('pk'))
        chosen, created = Chosen.objects.get_or_create(photo=photo, user=request.user)
        if created:
            photo.chosen_count += 1
            photo.save()
            return HttpResponse(photo.chosen_count)
        else:
            return HttpResponseForbidden()


class PhotoNotChosenView(LoginRequiredMixin, View):
    def delete(self, request, *args, **kwargs):
        photo = get_object_or_404(Photo, pk=kwargs.get('pk'))
        chosen = get_object_or_404(photo.chosens, user=request.user)
        chosen.delete()
        photo.chosen_count -= 1
        photo.save()
        return HttpResponse(photo.chosen_count)
