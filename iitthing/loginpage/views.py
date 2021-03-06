from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth import models as auth_models 
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm 
import traceback

import models
# Create your views here.

unauthorizedmsg = "UNAUTHORIZED ACCESS. DISPATCHING GOONS."


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username= username, password=raw_password)
            login(user)
            return redirect('/')
        else:
            return HttpResponse("Form not valid. Does the user exist? Is the password complex enough? ")
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form':form})

def login(request):
    return redirect('/login')

def homescreen(request):
    if request.user.is_authenticated():
        newcontext = {}
        if request.method == "POST":
            topic = request.POST["topic"]
            idnum = request.POST["id"]
            print "session entered: ", idnum, " ", topic 
            try:
                s = models.Session(sessionid=int(idnum), topic=topic)
                s.save()
            except:
                err = traceback.format_exc()
                return HttpResponse("error with session input\n" + err)


        
        session_list = models.Session.objects.all()
        newcontext["session_list"] =  session_list
        return render(request,'index.html' ,newcontext)
    else:
        return HttpResponse(unauthorizedmsg)


def studypostcatalog(request):
    return HttpResponse("Study post catalog")

def createnewsession(request):
    return HttpResponse("Create new session screen")

def homeredirect(request):
    if request.user.is_authenticated():
        return redirect('/userhome')
    else:
        return HttpResponse(unauthorizedmsg)



@csrf_protect
def viewsessionpost(request):
    if request.user.is_authenticated():
        sessionsview = loader.get_template('sessions.html')

        newcontext = {}
        if request.method == 'POST':
            radiobutton = request.POST['filter']
            try:
                subject = request.POST['selected_subjects']
                print "selected sort by ", radiobutton, " subject ", subject
            except:
                return HttpResponse("Please select a subject next time")
            try:
                res = models.Course.objects.filter(coursesubject=subject).order_by(radiobutton)

                newcontext["course_list"] = res 
                
                print "found ", res
            except:
                print "query ", subject, " failed. Not found" 
                newcontext["course_list"] = ["not found"]
        else:
            res = models.Course.objects.all()
            newcontext["course_list"] = res


        return render(request, 'sessions.html',newcontext)
    else:
        return HttpResponse(unauthorizedmsg)

def mapscreen(request):
    if request.user.is_authenticated():
        return render(request, 'map.html',{})
    else:
        return HttpResponse(unauthorizedmsg)


