from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Post


def ping_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse('pong', status=200)


def list_view(request: HttpRequest) -> HttpResponse:
    object_list = Post.objects.all()
    return render(request, 'posts/index.html', {'object_list': object_list})


def create_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        return render(request, 'posts/form.html', {'form': form})

    form = PostForm()
    return render(request, 'posts/form.html', {'form': form})


def update_view(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('index')
        return render(
            request,
            'posts/form.html',
            {'form': form, 'object': post},
        )

    form = PostForm(instance=post)
    return render(request, 'posts/form.html', {'form': form, 'object': post})


def delete_view(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('index')
    return render(request, 'posts/confirm_delete.html', {'object': post})
