from django.shortcuts import render

# Create your views here.
from codex.baseerror import *
from codex.baseview import APIView
from wechat.models import Activity,Ticket
from wechat.views import CustomWeChatView
import WeChatTicket.settings
import time,os,datetime

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required

class Login(APIView):
    def get(self):
        if self.request.user.is_authenticated():
            return 0
        else:
            raise ValidateError('用户未登录！')

    def post(self):
        self.check_input('username', 'password')
        username=self.input['username']
        password=self.input['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(self.request,user)
        else:
            raise ValidateError('用户登录失败！')

class Logout(APIView):
    def post(self):
        if self.request.user.is_authenticated():
            logout(self.request)
        else:
            raise ValidateError('登出失败！')

class Activitylist(APIView):
    def get(self):
        if not self.request.user.is_authenticated():
            raise ValidateError('用户未登录！')
        activtyList=Activity.objects.all()
        data=[]
        for item in activtyList:
            if item.status>=0:
                temp={
                'id':item.id,
                'name':item.name,
                'description':item.description,
                'startTime':int(time.mktime(item.start_time.timetuple()))+28800,
                'endTime':int(time.mktime(item.end_time.timetuple()))+28800,
                'place':item.place,
                'bookStart':int(time.mktime(item.book_start.timetuple()))+28800,
                'bookEnd':int(time.mktime(item.book_end.timetuple()))+28800,
                'currentTime':int(time.time()),
                'status':item.status,
                }
                data.append(temp)
            else:
                continue
        return data

class Activitydelete(APIView):
    def post(self):
        self.check_input('id')
        id=self.input['id']
        activty_todel=Activity.objects.get(id=id)
        if activty_todel:
            activty_todel.status=-1
            activty_todel.save()
            #清空活动的票
        else:
            raise ValidateError('不存在这个活动!')

class Createactivity(APIView):
    def post(self):
        self.check_input('name', 'key','place','description','picUrl','startTime','endTime','bookStart','bookEnd','totalTickets','status')
        if self.request.user.is_authenticated():
            data=Activity(name=self.input['name'],
                key=self.input['key'],
                place=self.input['place'],
                description=self.input['description'],
                pic_url=self.input['picUrl'],
                start_time=self.input['startTime'],
                end_time=self.input['endTime'],
                book_start=self.input['bookStart'],
                book_end=self.input['bookEnd'],
                total_tickets=self.input['totalTickets'],
                status=self.input['status'],
                remain_tickets=self.input['totalTickets'])
            data.save()
            return data.id
        else:
            raise ValidateError('未登录！')

class Imageupload(APIView):
    def post(self):
        self.check_input('image')
        if self.request.user.is_authenticated():
            image=self.input['image'][0]
            imageName=str(int(time.time()))+image.name
            imageFile = open(WeChatTicket.settings.IMAGE_ROOT+imageName,"w+b")
            image=image.read()
            imageFile.write(image)
            imageFile.close()
            return (WeChatTicket.settings.SITE_DOMAIN +WeChatTicket.settings.IMAGE_URL+imageName)
        else:
            raise ValidateError('未登录！')

class Activitydetail(APIView):
    def get(self):
        self.check_input('id')
        if not self.request.user.is_authenticated():
            raise ValidateError("用户未登录!")
        one_activity=Activity.objects.get(id=self.input['id'])
        data={
            'name':one_activity.name,
            'key':one_activity.key,
            'description':one_activity.description,
            'startTime':int(time.mktime(one_activity.start_time.timetuple()))+28800,
            'endTime':int(time.mktime(one_activity.end_time.timetuple()))+28800,
            'place':one_activity.place,
            'bookStart':int(time.mktime(one_activity.book_start.timetuple()))+28800,
            'bookEnd':int(time.mktime(one_activity.book_end.timetuple()))+28800,
            'totalTickets':one_activity.total_tickets,
            'picUrl':one_activity.pic_url,
            'bookedTickets':one_activity.total_tickets-one_activity.remain_tickets,
            'usedTickets':len(Ticket.objects.filter(activity=one_activity,status=Ticket.STATUS_USED)),
            'currentTime':int(time.time()),
            'status':one_activity.status,
            }
        return data

    def post(self):
        self.check_input('id','name','key','place','description','picUrl','startTime','endTime','bookStart','bookEnd','totalTickets','status')
        if not self.request.user.is_authenticated():
            raise ValidateError("用户未登录!")
        one_activity=Activity.objects.get(id=self.input['id'])
        one_activity.name=self.input['name']
        one_activity.key=self.input['key']
        one_activity.place=self.input['place']
        one_activity.description=self.input['description']
        one_activity.pic_url=self.input['picUrl']
        one_activity.start_time=self.input['startTime']
        one_activity.end_time=self.input['endTime']
        one_activity.book_start=self.input['bookStart']
        one_activity.book_end=self.input['bookEnd']
        one_activity.total_tickets=self.input['totalTickets']
        one_activity.status=self.input['status']
        one_activity.save()
        return 0

class Activitymenu(APIView):
    def get(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("用户未登录!")
        activity_list=Activity.objects.all()
        num=1
        data=[]
        for item in activity_list:
            startTime=int(time.mktime(item.book_start.timetuple()))+28800
            endTime=int(time.mktime(item.book_end.timetuple()))+28800
            currentTime=int(time.time())
            print(startTime,endTime,currentTime)
            if item.status==0:
                continue
            if startTime<=currentTime and  endTime>=currentTime:
                temp={
                'id':item.id,
                'name':item.name,
                'menuIndex':num
                }
                num=num+1
            else:
                temp={
                'id':item.id,
                'name':item.name,
                'menuIndex':0
                }
            data.append(temp)
        return data

    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("用户未登录!")
        data=[]
        for id in self.input:
            activity=Activity.objects.get(id=id)
            data.append(activity)
        CustomWeChatView.update_menu(data)

class Activitycheckin(APIView):
    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("用户未登录!")
        self.check_input('actId')
        activity=Activity.objects.get(id=self.input['actId'])
        try:
            if "ticket" in self.input:
                ticket=Ticket.objects.get(activity=activity,unique_id=self.input['ticket'])
            elif 'studentId' in self.input.keys():
                ticket=Ticket.objects.get(activity=activity,student_id=self.input['studentId'])
        except:
            raise ValidateError("用户无此票！")

        if ticket.status == Ticket.STATUS_CANCELLED:
            raise ValidateError("用户已取消此票!")
        elif ticket.status == Ticket.STATUS_USED:
            raise ValidateError("此票已使用！")
        elif ticket.status == Ticket.STATUS_VALID:
            data={
            'ticket':ticket.unique_id,
            'studentId':ticket.student_id
            }
            ticket.status=Ticket.STATUS_USED
            ticket.save()
            return data
        else:
            raise ValidateError("检票失败，请稍后重试!")
