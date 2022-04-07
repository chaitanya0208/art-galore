from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Category, Writer, artifact, Review, Slider
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import RegistrationForm, ReviewForm


def index(request):
    newpublished = artifact.objects.order_by('-created')[:15]
    slide = Slider.objects.order_by('-created')[:3]
    context = {
        "newartifacts":newpublished,
        "slide": slide
    }
    return render(request, 'store/index.html', context)


def signin(request):
    if request.user.is_authenticated:
        return redirect('store:index')
    else:
        if request.method == "POST":
            user = request.POST.get('user')
            password = request.POST.get('pass')
            auth = authenticate(request, username=user, password=password)
            if auth is not None:
                login(request, auth)
                return redirect('store:index')
            else:
            	messages.error(request, 'username and password doesn\'t match')

    return render(request, "store/login.html")	


def signout(request):
    logout(request)
    return redirect('store:index')	


def registration(request):
	form = RegistrationForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('store:signin')

	return render(request, 'store/signup.html', {"form": form})

def payment(request):
    return render(request, 'store/payment.html')


def get_artifact(request, id):
    form = ReviewForm(request.POST or None)
    artifact = get_object_or_404(artifact, id=id)
    rartifacts = artifact.objects.filter(category_id=artifact.category.id)
    r_review = Review.objects.filter(artifact_id=id).order_by('-created')

    paginator = Paginator(r_review, 4)
    page = request.GET.get('page')
    rreview = paginator.get_page(page)

    if request.method == 'POST':
        if request.user.is_authenticated:
            if form.is_valid():
                temp = form.save(commit=False)
                temp.customer = User.objects.get(id=request.user.id)
                temp.artifact = artifact          
                temp = artifact.objects.get(id=id)
                temp.totalreview += 1
                temp.totalrating += int(request.POST.get('review_star'))
                form.save()  
                temp.save()

                messages.success(request, "Review Added Successfully")
                form = ReviewForm()
        else:
            messages.error(request, "You need login first.")
    context = {
        "artifact":artifact,
        "rartifacts": rartifacts,
        "form": form,
        "rreview": rreview
    }
    return render(request, "store/artifact.html", context)


def get_artifacts(request):
    artifacts_ = artifact.objects.all().order_by('-created')
    paginator = Paginator(artifacts_, 10)
    page = request.GET.get('page')
    artifacts = paginator.get_page(page)
    return render(request, "store/category.html", {"artifact":artifacts})

def get_artifact_category(request, id):
    artifact_ = artifact.objects.filter(category_id=id)
    paginator = Paginator(artifact_, 10)
    page = request.GET.get('page')
    artifact = paginator.get_page(page)
    return render(request, "store/category.html", {"artifact":artifact})

def get_writer(request, id):
    wrt = get_object_or_404(Writer, id=id)
    artifact = artifact.objects.filter(writer_id=wrt.id)
    context = {
        "wrt": wrt,
        "artifact": artifact
    }
    return render(request, "store/writer.html", context)

