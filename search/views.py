from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from store.models import Artifact, Category, Writer

def search(request):
	search = request.GET.get('q')
	artifacts = artifact.objects.all()
	if search:
		artifacts = artifacts.filter(
			Q(name__icontains=search)|Q(category__name__icontains=search)|Q(writer__name__icontains=search)

		)

	paginator = Paginator(artifacts, 10)
	page = request.GET.get('page')
	artifacts = paginator.get_page(page)

	context = {
		"artifact": artifacts,
		"search": search,
	}
	return render(request, 'store/category.html', context)
