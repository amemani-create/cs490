from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Post  # , Category
from .forms import PostForm, EditForm, CommentForm
from django.urls import reverse_lazy, reverse
from taggit.models import Tag
from django.http import HttpResponseRedirect


class PostList(generic.ListView):
    model = Post
    template_name = 'blog/index.html'


def HomeView(request):
    return render(request, 'home.html')


class DetailPostView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    fields = ['title', 'tags', 'content']

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        likes_connected = get_object_or_404(Post, id=self.kwargs['pk'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = likes_connected.number_of_likes()
        data['post_is_liked'] = liked
        return data


def PostLike(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('blogpost_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))


def AddComment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form': form})


class AddPostView(generic.CreateView):
    model = Post
    template_name = 'blog/add_post.html'
    # fields = ['title', 'author', 'content']
    form_class = PostForm


class UpdatePostView(generic.UpdateView):
    model = Post
    template_name = 'blog/update_post.html'
    # fields = ['title', 'content']
    form_class = EditForm


class DeletePostView(generic.DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('post_list')


def TagView(request, tag_slug):
    tag_list = Post.objects.all()
    tag = get_object_or_404(Tag, slug=tag_slug)
    tag_list = tag_list.filter(tags__in=[tag])
    paginator = Paginator(tag_list, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results

        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/tags.html', locals())


def SearchBar(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        search_list = Post.objects.all().filter(title=search)
        return render(request, 'blog/searchbar.html', {'search_list': search_list})


"""def CategoryView(request, cats):
    category_posts = Post.objects.filter(category=cats)
    return render(request, 'tags.html', {'cats': cats, 'category_posts':category_posts})

class AddCategoryView(generic.CreateView):
    model = Category
    template_name = 'add_category.html'
    fields = '__all__'"""
