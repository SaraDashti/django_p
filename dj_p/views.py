
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post
from .forms import PostForm
from django.contrib import messages

def post(request):
	context = {
		"key":"mood",

	}
	return render(request, 'post_create.html',context)


def post_list(request):
	objects = Post.objects.all()

	paginator = Paginator(objects, 5) # Show 25 contacts per page

	number = request.GET.get('page')
	try:
		objects = paginator.page(number)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		objects = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		objects = paginator.page(paginator.num_pages)
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


def post_create(request):
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		form.save()
		messages.success(request, "awesome, you just added a blog post")
		return redirect("more:list")
	context = {
		"form": form
	}
	return render(request, 'post_create.html', context)


def post_update(request, post_id):
	item = Post.objects.get(id=post_id)
	form = PostForm(request.POST or None,request.FILES or None, instance=item)
	if form.is_valid():
		form.save()
		messages.info(request, "awesome, you just updated ")
		return redirect("more:detail", post_id=item.id)
	context = {
		"form": form,
		"item": item,
	}
	return render(request, 'post_update.html', context)


def post_delete(request, post_id):
	Post.objects.get(id=post_id).delete()
	messages.warning(request, "nooo ")
	return redirect("more:list")


