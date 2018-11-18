from areview.category import aid_context,study_context,project_context,contact_context
from django.http import request, HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, JsonResponse, QueryDict
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User

from areview.forms import ScrapeForm,PostForm,UserForm,LoginForm
from django.views.generic import TemplateView

from django.http import request, HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render

from areview.asincrawler import asinCrawler
from areview.forms import ScrapeForm, ProductListForm


from areview.sentiment import WebCrawler, SentimentAnalysis, drawpiechart

from rest_framework import generics

from areview.models import Post
from areview.serializers import PostSerializer

import os
import json

#----------base start------------------#
def base(request):
    return render(request, 'areview/base.html')

def base2(request):
     return render(request, 'areview/base2.html')

#----------base end -------------#
def home(request):
    return render(request, 'areview/home.html')

def aid(request):
    context=aid_context()
    return render(request, 'areview/aid.html',{'context':context})

def study(request):
    context=study_context()
    return render(request, 'areview/study.html',{'context': context})

#------project start ------------#

def InputKeywordsView(request):
    if request.method == 'POST':
        form = ProductListForm(request.POST)
        if form.is_valid():
            # cd = form.cleaned_data
            # Review.objects.create()
            return HttpResponseRedirect ('/thanks/')
    else:
        form = ProductListForm()
    return render(request,'areview/project.html', {'form':form})

def ProductListView(request):
    product_list = asinCrawler(request)
    return render(request, 'areview/product_list.html', {'list': product_list})

def project(request):
    context=project_context()
    return render(request, 'areview/project.html',{'context':context})

def UrlInput(request):
    if request.method == 'POST':
        form = ScrapeForm(request.POST)
        if form.is_valid():
            # cd = form.cleaned_data
            # Review.objects.create()
            return HttpResponseRedirect ('/thanks/')
    else:
        form = ScrapeForm()
    return render(request,'areview/url_input.html', {'form':form})


def SentimentAnalysisView(request):
    if request.method == 'POST':
        asin=request.POST.get('asin')
        print(asin)
        crawled_data= WebCrawler(request,asin)
        aresult = SentimentAnalysis(crawled_data)

        message = "All reviews: " + str(aresult['b'])
        message_Positive= " Positive: " + str(aresult['a'][0])
        message_Negative= " Negative: " + str(aresult['a'][1])
        chart = drawpiechart(aresult['a'][0], aresult['a'][1])

        context = {'message': message, 'chart': chart ,'message_Positive':message_Positive, 'message_Negative':message_Negative}
        return render(request,'areview/webcrawling.html', context)

#-------------project end ----------#
#-------------comment start ----------------#
def comment(request):
    tmpl_vars = {
        'all_posts': Post.objects.reverse(),
        'form': PostForm()
        }
    print("사랑합니다"+os.getcwd())
    return render(request, 'areview/comment.html', tmpl_vars)

def like(request):
    print("like들어옴")
    if request.method == 'POST':
        print("1")
        user = request.user # 로그인한 유저를 가져온다.
        print("2")
        post_id = request.POST.get('postpk', None)
        print(post_id+os.getcwd())
        print("3")
        post = Post.objects.get(pk = post_id) #해당 메모 오브젝트를 가져온다.
        # post = Post.objects.get(pk=int(QueryDict(request.body).get('postpk')))
        print("4")


        if post.likes.filter(id = user.id).exists(): #이미 해당 유저가 likes컬럼에 존재하면
            print("삭제합니다.."+os.getcwd())
            post.likes.remove(user) #likes 컬럼에서 해당 유저를 지운다.
            message = 'You disliked this'
        else:
            print("추가합니다."+os.getcwd())
            post.likes.add(user)
            message = 'You liked this'

    print("추가/삭제 후")
    context = {'likes_count' : post.total_likes, 'message' : message}
    print("리턴 바로 전")
    return HttpResponse(json.dumps(context), content_type='application/json')
    # dic 형식을 json 형식으로 바꾸어 전달한다.


#########################
### class based views ###
#########################

class PostCollection(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostMember(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

def create_post(request):
    print("행복합니다")
    if request.method == 'POST':
        post_text = request.POST.get('the_post')
        response_data = {}

        post = Post(text=post_text, author=request.user)
        post.save()


        response_data['result'] = 'Create post successful!'
        response_data['postpk'] = post.pk
        response_data['text'] = post.text
        response_data['created'] = post.created.strftime('%B %d, %Y %I:%M %p')
        response_data['author'] = post.author.username
        response_data['like'] = post.total_likes

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )
def delete_post(request):
    print("삭제해서 죄송합니다.")

    if request.method == 'DELETE':
        post = Post.objects.get(pk=int(QueryDict(request.body).get('postpk')))

        post.delete()

        response_data = {}
        response_data['msg'] = 'Post was deleted.'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def signin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('/areview/home')
        else:
            return HttpResponse('로그인 실패. 다시 시도 해보세요.')
    else:
        form = LoginForm()
        return render(request, 'areview/login.html', {'form': form})

def signup(request):

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return redirect('/areview/home')
        else:
            message = 'name is arleady exist'
            return HttpResponse(json.dumps(message),content_type='application')
    else:
        form = UserForm()
        return render(request, 'areview/adduser.html', {'form': form})



def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/areview/home')

#---------comment end --------#
#---------contact start ----------#
def contact(request):
    context=contact_context()
    return render(request, 'areview/contact.html',{'context':context})
#--------contact end ---------------#










