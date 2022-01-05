import datetime
from pyexpat.errors import messages

from django.shortcuts import render, redirect

# Create your views here.
from django.views import generic
from .models import Post
from part1.models import CustomUser
from .forms import PostForm


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog/post_list.html'


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


class AddPostView(generic.CreateView):
        model = Post
        template_name = 'blog/add_post.html'
        fields = ['title', 'imgage', 'slug', 'author', 'content', 'status']














        # if request.method == 'GET':
        #     return render(request, 'auth/add_post.html', {'form': form})
        # if request.method == 'POST':
        #     if form.is_valid():
        #         form.save()
        #     else:
        #         form = PostForm()
        #     return render(request, 'auth/add_post.html', {'form': form})
        # return render(request, 'auth/add_post.html')
    # getUser = CustomUser.objects.get(id=userid)
    # if request.method == 'GET':
    #     return render(request, 'auth/add_post.html', {'user': getUser})
    # if request.method == 'Post':
    #     try:
    #         ti = request.POST['tittle']
    #         cont = request.POST['content']
    #         stat = request.POST['status']
    #         aut = getUser
    #         up_on = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    #         cr_on = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    #         if len(request.FILES) != 0:
    #             img = request.FILES['img']
    #         add = Post.object.create(tittle=ti, imgage=img, slug=request.POST['tittle'], author=aut, updated_on=up_on,
    #                                  content= cont, created_on=cr_on, status=stat)
    #         add.save()
    #         return redirect('blog')
    #     except Exception as e:
    #         messages.success(request, "Failed to post Try Again")
    #         return redirect('/', {'me':messages})
    # return render(request, 'auth/add_post.html')