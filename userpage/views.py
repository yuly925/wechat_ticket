from codex.baseerror import *
from codex.baseview import APIView

from wechat.models import User,Activity,Ticket
import re
import json
import time,os,datetime

class UserBind(APIView):

    def validate_user(self):
        """
        input: self.input['student_id'] and self.input['password']
        raise: ValidateError when validating failed
        """
        id =self.input['student_id']
        if re.match('^201[1-8]\d{6}$',id):
            return 0

        raise ValidateError('student ID is invalid')
        #raise NotImplementedError('You should implement UserBind.validate_user method')

    def get(self):
        self.check_input('openid')
        return User.get_by_openid(self.input['openid']).student_id

    def post(self):
        self.check_input('openid', 'student_id', 'password')
        user = User.get_by_openid(self.input['openid'])
        self.validate_user()
        user.student_id = self.input['student_id']
        user.save()

        #return 0

class activityDetail(APIView):

    def get(self):
        self.check_input('id')
        activity=Activity.objects.get(id=self.input['id'])
        if activity.status==Activity.STATUS_PUBLISHED:
            response = {
                'name':activity.name,
                'key':activity.key,
                'description':activity.description,
                'startTime':int(time.mktime(activity.start_time.timetuple()))+28800,
                'endTime':int(time.mktime(activity.end_time.timetuple()))+28800,
                'place':activity.place,
                'bookStart':int(time.mktime(activity.book_start.timetuple()))+28800,
                'bookEnd':int(time.mktime(activity.book_end.timetuple()))+28800,
                'totalTickets':activity.total_tickets,
                'picUrl':activity.pic_url,
                'remainTickets':activity.remain_tickets,
                'currentTime':int(time.time()),
            }
            return response
        else:
            raise LogicError('活动不处于发布状态')


class ticketDetail(APIView):

    def get(self):
        self.check_input('openid','ticket')
        ticket=Ticket.objects.get(unique_id=self.input['ticket'])
        activity=ticket.activity
        response = {
            'activityName': activity.name,
            'activityKey': activity.key,
            'startTime': int(time.mktime(activity.start_time.timetuple())) + 28800,
            'endTime': int(time.mktime(activity.end_time.timetuple())) + 28800,
            'place': activity.place,
            'currentTime': int(time.time()),
            'uniqueId':ticket.unique_id,
            'status':ticket.status
        }
        return response



