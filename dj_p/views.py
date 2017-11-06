
from django.shortcuts import render, get_object_or_404
from .models import Post

def post(request):
	context = {
		"key":"mood",

	}

	return render(request, 'post_create.html',context)

def post_list(request):
	objects = Post.objects.all()
	context = {
		"post_items": objects,
	}	
	return render(request, "list.html", context)


def post_detail(request, post_id):
	#item = Post.objects.get(id=2)
	item = get_object_or_404(Post, id=post_id)
	context = {
		"item": item,
	}
	return render(request, "detail.html", context)	

