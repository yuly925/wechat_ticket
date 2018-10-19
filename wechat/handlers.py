# -*- coding: utf-8 -*-
#
from wechat.wrapper import WeChatHandler
from wechat.models import Activity,Ticket,User
from django.utils import timezone
import uuid
import re,time
__author__ = "Epsirom"


class ErrorHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        return self.reply_text('对不起，服务器现在有点忙，暂时不能给您答复 T T')


class DefaultHandler(WeChatHandler):

    def check(self):
        return True

    def handle(self):
        return self.reply_text('对不起，没有找到您需要的信息:(')


class HelpOrSubscribeHandler(WeChatHandler):

    def check(self):
        return self.is_text('帮助', 'help') or self.is_event('scan', 'subscribe') or \
               self.is_event_click(self.view.event_keys['help'])

    def handle(self):
        return self.reply_single_news({
            'Title': self.get_message('help_title'),
            'Description': self.get_message('help_description'),
            'Url': self.url_help(),
        })


class UnbindOrUnsubscribeHandler(WeChatHandler):

    def check(self):
        return self.is_text('解绑') or self.is_event('unsubscribe')

    def handle(self):
        self.user.student_id = ''
        self.user.save()
        return self.reply_text(self.get_message('unbind_account'))


class BindAccountHandler(WeChatHandler):

    def check(self):
        return self.is_text('绑定') or self.is_event_click(self.view.event_keys['account_bind'])

    def handle(self):
        return self.reply_text(self.get_message('bind_account'))


class BookEmptyHandler(WeChatHandler):

    def check(self):
        return self.is_event_click(self.view.event_keys['book_empty'])

    def handle(self):
        return self.reply_text(self.get_message('book_empty'))

#消息框输入文本"取票 XXXXX"
class PickTicketHandler(WeChatHandler):
    def check(self):
        return self.is_query('取票')

    def handle(self):
        # 未绑定先绑定
        if not self.user.student_id:
            return self.reply_text(self.get_message('bind_account'))
        else:
            words = re.findall('^\S{2}\s+(\S+)$', str(self.input['Content']))
            if not words:
                return self.reply_text('输入有误')
            key = words[0]

            try:
                ac = Activity.objects.get(key=key,status=Activity.STATUS_PUBLISHED)
            except Activity.DoesNotExist:
                return self.reply_text('对不起！没有查找到发布的活动')
            try:
                tk =Ticket.objects.get(activity=ac,student_id=self.user.student_id,status=Ticket.STATUS_VALID)
            except Ticket.DoesNotExist:
                return self.reply_text('对不起！您没有该活动的票')
            #print(ac.remain_tickets)
            return self.reply_single_news({'Title': ac.name, 'Description': ac.description,
                                     'PicUrl':ac.pic_url,'Url':self.url_ticket(tk.unique_id)
                                     })


#消息框输入文本"退票 XXXXX"
class CancelTicketHandler(WeChatHandler):
    def check(self):
        return self.is_query('退票')

    def handle(self):
        # 未绑定先绑定
        if not self.user.student_id:
            return self.reply_text(self.get_message('bind_account'))
        else:
            words=re.findall('^\S{2}\s+(\S+)$',str(self.input['Content']))
            if not words:
                return self.reply_text('输入有误')
            key=words[0]

            try:
                ac = Activity.objects.get(key=key,status=Activity.STATUS_PUBLISHED)
            except Activity.DoesNotExist:
                return self.reply_text('对不起！没有查找到发布的活动')
            try:
                tk =Ticket.objects.get(activity=ac,student_id=self.user.student_id,status=Ticket.STATUS_VALID)
            except Ticket.DoesNotExist:
                return self.reply_text('对不起！您没有该活动的票')

            tk.status=Ticket.STATUS_CANCELLED
            tk.save()
            ac.remain_tickets+=1
            ac.save()
            return self.reply_text('退票成功！')



#消息框输入文本"抢票 XXXXX"
class BookTicketTextHandler(WeChatHandler):
    def check(self):
        return self.is_query('抢票')

    def handle(self):
        # 未绑定先绑定
        if not self.user.student_id:
            return self.reply_text(self.get_message('bind_account'))

        else:
            words = re.findall('^\S{2}\s+(\S+)$', str(self.input['Content']))
            if not words:
                return self.reply_text('输入有误')
            key = words[0]

            try:
                ac = Activity.objects.get(key=key,status=Activity.STATUS_PUBLISHED)
            except Activity.DoesNotExist:
                return self.reply_text('对不起！没有查找到发布的活动')

            # 判断是否可以抢票
            startTime = int(time.mktime(ac.book_start.timetuple())) + 28800
            endTime = int(time.mktime(ac.book_end.timetuple())) + 28800
            currentTime = int(time.time())
            if startTime > currentTime:
                return self.reply_text('抢票未开始')
            elif endTime < currentTime:
                return self.reply_text('抢票已结束，下次请谨记时间哦')

            if ac.remain_tickets <=0:
                return self.reply_text('抢票已抢光QAQ')
            else:
                #先判断是否已有票
                existTK=Ticket.objects.filter(activity=ac,student_id=self.user.student_id)
                if not existTK:
                    ac.remain_tickets-=1
                    ac.save()
                    uniId=str(uuid.uuid4())+self.user.open_id
                    tk=Ticket(student_id=self.user.student_id,
                              unique_id=uniId,
                              activity=ac,
                              status=Ticket.STATUS_VALID)
                    tk.save()
                    return self.reply_text('抢票成功')
                elif existTK[0].status == Ticket.STATUS_VALID:
                    return self.reply_text('您已拥有该活动的票！切忌贪心哦')
                else:
                    ac.remain_tickets -= 1
                    ac.save()
                    existTK[0].status=Ticket.STATUS_VALID
                    existTK[0].save()
                    return self.reply_text('抢票成功')

#点击"查票"按钮，返回该用户所有票（VALID、CANCELLED、UESED）的图文链接列表
class GetTicketHandler(WeChatHandler):
    def check(self):
        return self.is_event_click(self.view.event_keys['get_ticket'])

    def handle(self):
        #未绑定先绑定
        if not self.user.student_id:
            return self.reply_text(self.get_message('bind_account'))
        #已绑定
        all_tk=Ticket.objects.filter(student_id=self.user.student_id)
        #过滤出发布的活动
        Tickets=[tk for tk in all_tk if tk.activity.status==Activity.STATUS_PUBLISHED]
        if not len(Tickets):
            return self.reply_text('您还没有电子票')
        else:
            return self.reply_news([{'Title': tk.activity.name, 'Description': tk.activity.description,
                                     'PicUrl':tk.activity.pic_url,'Url':self.url_ticket(tk.unique_id)
                                     } for tk in Tickets[:10]])


#点击"抢啥"按钮，返回最多十个正在抢票的活动，按结束时间排序
class BookWhatHandler(WeChatHandler):
    def check(self):
        return self.is_event_click(self.view.event_keys['book_what'])

    def handle(self):
        #未绑定状态先绑定
        if not self.user.student_id:
            return self.reply_text(self.get_message('bind_account'))
        #已绑定
        Activities=Activity.objects.filter(
            status=Activity.STATUS_PUBLISHED, book_end__gt=timezone.now()
        ).order_by('book_end')[ :10]

        if len(Activities):
            return self.reply_news([{'Title': act.name, 'Description': act.description,
                                     'PicUrl':act.pic_url,'Url':self.url_activity(act.id)
                                     } for act in Activities])
        else:
            return self.reply_text(self.get_message('book_empty'))

#点击抢票按钮，进行抢票
class BookTicketHandler(WeChatHandler):
    def check(self):
        return self.is_event_book()

    def handle(self):
        # 未绑定状态先绑定
        if not self.user.student_id:
            return self.reply_text(self.get_message('bind_account'))
        #已绑定
        else:
            id=self.input['EventKey'][len(self.view.event_keys['book_header']):]
            ac=Activity.objects.get(id=id)
            ###删除或保存的活动是否可以出现在抢票按钮？
            if ac.status == Activity.STATUS_DELETED:
                return self.reply_text('活动已删除')

            #判断是否可以抢票
            startTime =int(time.mktime(ac.book_start.timetuple())) + 28800
            endTime=int(time.mktime(ac.book_end.timetuple())) + 28800
            currentTime=int(time.time())
            if startTime > currentTime:
                return self.reply_text('抢票未开始')
            elif endTime <currentTime:
                return self.reply_text('抢票已结束，下次请谨记时间哦')

            if ac.remain_tickets <= 0:
                return self.reply_text('抢票已抢光QAQ')
            else:
                # 先判断是否已有票
                existTK = Ticket.objects.filter(activity=ac, student_id=self.user.student_id)
                if not existTK:
                    ac.remain_tickets -= 1
                    ac.save()
                    uniId = str(uuid.uuid4()) + self.user.open_id
                    tk = Ticket(student_id=self.user.student_id,
                                unique_id=uniId,
                                activity=ac,
                                status=Ticket.STATUS_VALID)
                    tk.save()
                    return self.reply_text('抢票成功')
                elif existTK[0].status == Ticket.STATUS_VALID:
                    return self.reply_text('您已拥有该活动的票！切忌贪心哦')
                else:
                    ac.remain_tickets -= 1
                    ac.save()
                    existTK[0].status = Ticket.STATUS_VALID
                    existTK[0].save()
                    return self.reply_text('抢票成功')