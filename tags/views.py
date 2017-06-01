from django.shortcuts import render

from django.views.generic import ListView, DetailView


from .models import Tag


class TagDetailView(DetailView):
	model = Tag



class TagListView(ListView):
	model = Tag


	def get_queryset(self):
		return Tag.objects.filter(active=True)
