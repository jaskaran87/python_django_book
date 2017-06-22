from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
def post_list(request):
    posts = Post.objects.all()
    paginator = Paginator(posts,2) # 2 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page':page, 'posts': posts})

def post_share(request,post_id):
    post = Post.objects.get(id=post_id)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            print(cd)
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recomends you reading "{}"'. format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {} {}\'s comments: {}'. format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'jaskarans@selectsourceintl.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post':post ,'form': form, 'sent':sent })

def post_detail(request,slug):
    post = get_object_or_404(Post, slug = slug)

    #List of active comments for this post
    # comments is related name which is define in models
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data= request.POST)
        if comment_form.is_valid():
            #Created comment object but don't save to database Yet!!
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            #Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()


    return render(request, 'blog/post/detail.html',{'post':post,'comments': comments,'comment_form': comment_form})

class PostListView(ListView):
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

