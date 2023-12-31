from django.shortcuts import render, redirect, get_object_or_404
from blogapp.forms import CommentForm, SubscribeForm, NewUserForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth import login

from blogapp.models import Post, Comment, Tag, Profile, WebsiteMeta

# Create your views here.


# Main Page View
def index(request):
    posts = Post.objects.all()
    top_posts = Post.objects.all().order_by("-view_count")[0:3]
    recent_posts = Post.objects.all().order_by("-last_updated")[0:3]
    featured_blog = Post.objects.filter(is_featured=True)
    subscribe_form = SubscribeForm()
    subscribe_successful = None
    website_info = None

    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]

    if featured_blog:
        featured_blog = featured_blog[0]

    if request.POST:
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
            request.session["subscribed"] = True
            subscribe_successful = "Subscribed Successfully"
            subscribe_form = SubscribeForm()

    context = {
        "posts": posts,
        "top_posts": top_posts,
        "website_info": website_info,
        "recent_posts": recent_posts,
        "subscribe_form": subscribe_form,
        "subscribe_successful": subscribe_successful,
        "featured_blog": featured_blog,
    }
    return render(request, "app/index.html", context)


# Post Page View
def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    comments = Comment.objects.filter(post=post, parent=None)
    form = CommentForm()

    # Bookmark Logic
    bookmarked = False
    if post.bookmarks.filter(id=request.user.id).exists():
        bookmarked = True
    is_bookmarked = bookmarked

    # Liked Logic
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True
    number_of_likes = post.number_of_likes()
    post_is_liked = liked

    if request.POST:
        comment_form = CommentForm(request.POST)

    if request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid and request.user.is_authenticated:
            parent_obj = None
            if request.POST.get("parent"):
                parent = request.POST.get("parent")
                parent_obj = Comment.objects.get(id=parent)
                if parent_obj:
                    comment_reply = comment_form.save(commit=False)
                    comment_reply.author = request.user
                    comment_reply.parent = parent_obj
                    comment_reply.post = post
                    comment_reply.save()
                    return HttpResponseRedirect(
                        reverse("post_page", kwargs={"slug": slug})
                    )
            else:
                if comment_form.is_valid:
                    comment = comment_form.save(commit=False)
                    comment.author = request.user
                    postid = request.POST.get("post_id")
                    post = Post.objects.get(id=postid)
                    comment.post = post
                    comment.save()
                    return HttpResponseRedirect(
                        reverse("post_page", kwargs={"slug": slug})
                    )

    # Logic in progress for view_count to increment only on refresh
    # or re-visiting the page
    # Increment view count only for GET requests
    # if request.method == 'GET':
    #     if post.view_count is None:
    #         post.view_count = 1
    #     else:
    #         post.view_count += 1
    #     post.save()

    if request.session.get(f"view_count_{post.id}", False):
        post.view_count = post.view_count + 1
        print("Count: ", post.view_count)
        pass
    else:
        post.view_count += 1
        post.save()
        request.session[f"view_count_{post.id}"] = True
        
    context = {
        "post": post,
        "form": form,
        "comments": comments,
        "is_bookmarked": is_bookmarked,
        "post_is_liked": post_is_liked,
        "number_of_likes": number_of_likes,
    }
    return render(request, "app/post.html", context)


# Logic for updating comments
def update_comment(request, pk):
    if request.user.is_authenticated:
        current_post = Comment.objects.get(id=pk)
        form = CommentForm(request.POST or None, instance=current_post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse("post_page", kwargs={"slug": current_post.post.slug})
            )
    return render(request, "app/update.html", {"form": form})


# Logic for deleting or cancel deletion of a post
def delete_comment(request, pk):
    if request.user.is_authenticated:
        current_post = Comment.objects.get(id=pk)
        form = CommentForm(request.POST or None, instance=current_post)
        if form.is_valid():
            current_post.delete()
            return HttpResponseRedirect(
                reverse("post_page", kwargs={"slug": current_post.post.slug})
                )
    return render(request, "app/delete.html", {"form": form, "post": current_post.post})  # noqa


# -DELETE func for future implementation.-
# def delete_comment(request, pk):
#     if request.user.is_authenticated:
#         delete_it = Comment.objects.get(id=pk)
#         form = CommentForm(request.POST or None, instance=delete_it)
#         post_slug = delete_it.post.slug
#         delete_it.delete()
#         return HttpResponseRedirect(reverse('post_page',
#         kwargs={'slug': post_slug}))


# Logic for tag page
def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)

    top_posts = Post.objects.filter(tags__in=[tag.id]).order_by("-view_count")[0:2]  # noqa
    recent_posts = Post.objects.filter(tags__in=[tag.id]).order_by("-last_updated")[0:2]  # noqa
    tags = Tag.objects.all()

    context = {
        "tag": tag,
        "top_posts": top_posts,
        "recent_posts": recent_posts,
        "tags": tags,
    }
    return render(request, "app/tag.html", context)


# Logic for author page for future implementation

# def author_page(request, slug):
#     profile = Profile.objects.get(slug=slug)

#     top_posts = Post.objects.filter(author=profile.user)
#     .order_by("-view_count")[0:2]
#     recent_posts = Post.objects.filter(author=profile.user)
#     .order_by("-last_updated")[
#         0:2
#     ]
#     top_authors = User.objects.annotate(number=
#     Count("post")).order_by("number")

#     context = {
#         "profile": profile,
#         "top_posts": top_posts,
#         "recent_posts": recent_posts,
#         "top_authors": top_authors,
#     }
#     return render(request, "app/author.html", context)


def about(request):
    website_info = None

    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]
    context = {"website_info": website_info}
    return render(request, "app/about.html", context)


def register_user(request):
    form = NewUserForm()
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")

    context = {"form": form}
    return render(request, "registration/registration.html", context)


def bookmark_post(request, slug):
    print("PRINT", request.POST.get("post_id"))
    post = get_object_or_404(Post, id=request.POST.get("post_id"))
    if post.bookmarks.filter(id=request.user.id).exists():
        post.bookmarks.remove(request.user)
    else:
        post.bookmarks.add(request.user)
    return HttpResponseRedirect(reverse("post_page", args=[str(slug)]))


def like_post(request, slug):
    print("PRINT", request.POST.get("post_id"))
    post = get_object_or_404(Post, id=request.POST.get("post_id"))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse("post_page", args=[str(slug)]))


def all_bookmarked_posts(request):
    all_bookmarked_posts = Post.objects.filter(bookmarks=request.user)
    context = {"all_bookmarked_posts": all_bookmarked_posts}
    return render(request, "app/all_bookmarked_posts.html", context)


def all_posts(request):
    all_posts = Post.objects.all()
    context = {"all_posts": all_posts}
    return render(request, "app/all_posts.html", context)


def all_liked_posts(request):
    all_liked_posts = Post.objects.filter(likes=request.user)
    context = {"all_liked_posts": all_liked_posts}
    return render(request, "app/all_liked_posts.html", context)


def handler404(request, exception):
    """
    Function for 404 (Page Not Found) errors.
    """
    return render(request, '404.html', status=404)
