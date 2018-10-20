from django.shortcuts import render

# Create your views here.
from codex.baseerror import *
from codex.baseview import APIView
from wechat.models import Activity,Ticket
from wechat.views import CustomWeChatView
import WeChatTicket.settings
import time,os
from datetime import datetime, timedelta, timezone
import pytz
import re
import django.utils.timezone as timezone

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout

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

        if not username:
            raise ValidateError('用户名为空！')
        if not password:
            raise ValidateError('密码为空！')
        if not User.objects.filter(username=username):
            raise ValidateError('用户名不存在！')
        if not user:
            raise ValidateError('密码错误！')

        if user.is_active:
            login(self.request,user)


class Logout(APIView):
    def post(self):
        if self.request.user.is_authenticated():
            logout(self.request)
        else:
            raise ValidateError('用户注销失败！')

class ActivityList(APIView):
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
                'startTime':int(time.mktime(item.start_time.astimezone(pytz.timezone('Asia/Shanghai')).timetuple())) ,
                'endTime':int(time.mktime(item.end_time.astimezone(pytz.timezone('Asia/Shanghai')).timetuple())) ,
                'place':item.place,
                'bookStart':int(time.mktime(item.book_start.astimezone(pytz.timezone('Asia/Shanghai')).timetuple())) ,
                'bookEnd':int(time.mktime(item.book_end.astimezone(pytz.timezone('Asia/Shanghai')).timetuple())) ,
                'currentTime':int(time.time()),
                'status':item.status,
                }
                data.append(temp)
            else:
                continue
        return data

class ActivityDelete(APIView):
    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError('用户未登录！')
        self.check_input('id')
        id=self.input['id']

        try:
            activity=Activity.objects.get(id=id)
        except:
            raise LogicError('删除不存在的活动!')
        if activity.status==-1:
            raise LogicError('删除已删除的活动!')

        bookStart=int(time.mktime(activity.book_start.astimezone(pytz.timezone('Asia/Shanghai')).timetuple()))
        endTime=int(time.mktime(activity.end_time.astimezone(pytz.timezone('Asia/Shanghai')).timetuple()))
        currentTime=int(time.time())
        if currentTime<=endTime and currentTime >=bookStart:
            raise LogicError('活动已开始，无法删除!')

        #更新微信界面
        menu=CustomWeChatView.get_book_btn()
        modification=False
        for item in menu['sub_button']:
            if item['name']==activity.name:
                modification=True
                break
            else:
                continue
        if modification:
            data=[]
            for item in menu['sub_button']:
                id=int(item['key'][17:])
                temp_activity=Activity.objects.get(id=id)
                if temp_activity.name==activity.name:
                    continue
                else:
                    data.append(temp_activity)
            CustomWeChatView.update_menu(data)

        activity.status=-1
        activity.save()

class CreateActivity(APIView):
    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError('用户未登录！')
        self.check_input('name', 'key','place','description','picUrl','startTime','endTime','bookStart','bookEnd','totalTickets','status')
        if not(int(self.input['status'])==0 or int(self.input['status'])==1):
            raise LogicError('活动状态错误！')

        currentTime=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
        if self.input['endTime']<=self.input['startTime']:
            raise LogicError('活动结束时间早于活动开始时间！')
        if self.input['bookEnd']<=self.input['bookStart']:
            raise LogicError('订票结束时间早于订票开始时间！')
        if self.input['startTime']<=self.input['bookEnd']:
            raise LogicError('活动开始时间早于订票结束时间！')
        if self.input['bookStart']<=currentTime:
            raise LogicError('订票开始时间早于当前时间！')

        pattern=re.match(r'(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?',self.input['picUrl'],re.IGNORECASE)
        if not pattern:
            raise LogicError('图片url格式错误！')
        if Activity.objects.filter(key=self.input['key']):
            raise LogicError('活动key值已存在！')
        if int(self.input['totalTickets'])<=0:
            raise LogicError('活动票数应当为正数！')

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

class ImageUpload(APIView):
    def post(self):
        self.check_input('image')
        if not self.request.user.is_authenticated():
            raise ValidateError('未登录！')

        image=self.input['image'][0]
        imageName=str(int(time.time()))+image.name
        image=image.read()

        imageFile = open(WeChatTicket.settings.IMAGE_ROOT+imageName,"w+b")
        if not imageFile:
            raise FileError('文件打开错误！')

        imageFile.write(image)
        imageFile.close()
        return (WeChatTicket.settings.SITE_DOMAIN +WeChatTicket.settings.IMAGE_URL+imageName)


class ActivityDetail(APIView):
    def get(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("用户未登录!")
        self.check_input('id')
        try:
            activity=Activity.objects.get(id=self.input['id'])
        except:
            raise LogicError('活动不存在！')
        if activity.status==-1:
            raise LogicError('该活动已删除！')

        data={
            'name':activity.name,
            'key':activity.key,
            'description':activity.description,
            'startTime':int(time.mktime(activity.start_time.astimezone(pytz.timezone('Asia/Shanghai')).timetuple())) ,
            'endTime':int(time.mktime(activity.end_time.astimezone(pytz.timezone('Asia/Shanghai')).timetuple())) ,
            'place':activity.place,
            'bookStart':int(time.mktime(activity.book_start.astimezone(pytz.timezone('Asia/Shanghai')).timetuple())) ,
            'bookEnd':int(time.mktime(activity.book_end.astimezone(pytz.timezone('Asia/Shanghai')).timetuple())) ,
            'totalTickets':activity.total_tickets,
            'picUrl':activity.pic_url,
            'bookedTickets':activity.total_tickets-activity.remain_tickets,
            'usedTickets':len(Ticket.objects.filter(activity=activity,status=Ticket.STATUS_USED)),
            'currentTime':int(time.time()),
            'status':activity.status,
            }
        return data

    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("用户未登录!")
        self.check_input('id','name','place','description','picUrl','startTime','endTime','bookStart','bookEnd','totalTickets','status')
        try:
            activity=Activity.objects.get(id=self.input['id'])
        except:
            raise LogicError('此活动不存在！')

        endTime=int(time.mktime(activity.end_time.astimezone(pytz.timezone('Asia/Shanghai')).timetuple()))
        startTime=int(time.mktime(activity.start_time.astimezone(pytz.timezone('Asia/Shanghai')).timetuple()))
        bookStart=int(time.mktime(activity.book_start.astimezone(pytz.timezone('Asia/Shanghai')).timetuple()))
        currentTime=int(time.time())

        if activity.status==-1:
            raise LogicError('not allowed to edit deleted activity')

        pattern=re.match(r'(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?',self.input['picUrl'],re.IGNORECASE)
        if not pattern:
            raise LogicError('图片url格式错误！')

        pattern=re.match(r'20\d{2}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3,}Z',self.input['bookStart'],re.IGNORECASE)
        if not pattern:
            raise LogicError('订票开始时间错误！')

        pattern=re.match(r'20\d{2}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3,}Z',self.input['bookEnd'],re.IGNORECASE)
        if not pattern:
            raise LogicError('订票结束时间错误！')

        pattern=re.match(r'20\d{2}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3,}Z',self.input['startTime'],re.IGNORECASE)
        if not pattern:
            raise LogicError('活动开始时间错误！')

        pattern=re.match(r'20\d{2}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3,}Z',self.input['endTime'],re.IGNORECASE)
        if not pattern:
            raise LogicError('活动结束时间错误！')

        if(int(self.input['totalTickets'])==0):
            raise LogicError('票数至少为1！')

        if activity.status==1:
            if activity.name!=self.input['name']:
                raise LogicError('不能修改活动名称！')
            if activity.place!=self.input['place']:
                raise LogicError('不能修改活动地点！')
            if (activity.book_start.strftime("%Y-%m-%dT%H:%M:%S.000Z")!=self.input['bookStart']):
                raise LogicError('不能修改开始抢票时间！')
            if (startTime<=currentTime and
                activity.book_end.strftime("%Y-%m-%dT%H:%M:%S.000Z")!=self.input['bookEnd']):
                raise LogicError('已经不能修改抢票结束时间！')
            if (endTime<=currentTime and
                (activity.end_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")!=self.input['endTime'] or
                activity.start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")!=self.input['startTime']
                )):
                raise LogicError('已经不能修改活动时间！')
            if(bookStart<=currentTime and
                int(self.input['totalTickets'])!=activity.total_tickets):
                raise LogicError('已经不能修改总票数！')
            if(int(self.input['status'])!=1):
                raise LogicError('此时状态只能为发布状态！')

        activity.name=self.input['name']
        activity.place=self.input['place']
        activity.description=self.input['description']
        activity.pic_url=self.input['picUrl']
        activity.start_time=self.input['startTime']
        activity.end_time=self.input['endTime']
        activity.book_start=self.input['bookStart']
        activity.book_end=self.input['bookEnd']
        activity.total_tickets=self.input['totalTickets']
        activity.status=self.input['status']
        activity.save()

class ActivityMenu(APIView):
    def get(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("用户未登录!")
        activity_list=Activity.objects.all()
        num=1
        data=[]
        old_id=[]

        #获取微信菜单
        menu=CustomWeChatView.get_book_btn()
        for item in menu['sub_button']:
            id=int(item['key'][17:])
            try:
                temp_activity=Activity.objects.get(id=id)
            except:
                raise LogicError('读取活动菜单出错！')
            old_id.append(id)
            temp={
                'id':temp_activity.id,
                'name':temp_activity.name,
                'menuIndex':num
            }
            num=num+1
            data.append(temp)

        for item in activity_list:
            bookStart=int(time.mktime(item.book_start.astimezone(pytz.timezone('Asia/Shanghai')).timetuple()))
            bookEnd=int(time.mktime(item.book_end.astimezone(pytz.timezone('Asia/Shanghai')).timetuple()))
            currentTime=int(time.time())
            if item.status<=0:
                continue
            if bookStart<=currentTime and  bookEnd>=currentTime:
                temp={
                'id':item.id,
                'name':item.name,
                'menuIndex':0
                }
                if id not in old_id:
                    data.append(temp)
        return data

    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("用户未登录!")
        data=[]
        for id in self.input:
            try:
                newid=int(id)
                activity=Activity.objects.get(id=newid)
            except:
                raise LogicError('没有此项活动！')
            bookStart=int(time.mktime(activity.book_start.astimezone(pytz.timezone('Asia/Shanghai')).timetuple()))
            bookEnd=int(time.mktime(activity.book_end.astimezone(pytz.timezone('Asia/Shanghai')).timetuple()))
            currentTime=int(time.time())
            if activity.status != 1:
                raise LogicError('活动未发布')
            if currentTime<=bookStart or currentTime>=bookEnd:
                raise LogicError('此时不能抢票！')
            data.append(activity)
        CustomWeChatView.update_menu(data)

class ActivityCheckin(APIView):
    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("用户未登录!")
        self.check_input('actId')
        try:
            activity=Activity.objects.get(id=self.input['actId'])
        except:
            raise LogicError('活动ID错误！')
        try:
            if "ticket" in self.input:
                ticket=Ticket.objects.get(activity=activity,unique_id=self.input['ticket'])
            elif 'studentId' in self.input.keys():
                ticket=Ticket.objects.get(activity=activity,student_id=self.input['studentId'])
        except:
            raise LogicError("用户无此票，请检查ID！")

        if ticket.status == Ticket.STATUS_CANCELLED:
            raise LogicError("用户已取消此票!")
        elif ticket.status == Ticket.STATUS_USED:
            raise LogicError("此票已使用！")
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
