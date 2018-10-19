from django.test import TestCase
import json
from wechat.models import *
from django.contrib import auth
#from userpage.views import *
# Create your tests here.

STATUS_DELETED = -1
STATUS_SAVED = 0
STATUS_PUBLISHED = 1
picUrl = "http://pic14.nipic.com/20110605/1369025_165540642000_2.jpg"

def get_response_object(response):
    ''' 向client发送get_message,返回一个object对象 '''
    response_json = response.content.decode('utf-8')
    return json.loads(response_json)

url='/wechat?signature=0dbdfc356a8418762d8ecc57547f374fa6760ea9&timestamp=1539837340&nonce=445616432&openid=123456'

validUser = User(open_id='123456', student_id='2015012358')
superUserCorrect = {'username': 'superuser', 'email': 'superuser@test.com', 'password': 'iamsuperuser'}

activityBookingNotStartedSql = Activity(name ='activity_published', key = 'publishednotstart', description = 'The booking has not started!',
                                start_time = '2018-12-15T17:01:00.000Z', end_time = '2018-12-30T17:01:00.000Z', place = 'anywhere',
                                book_start = '2018-12-10T17:01:00.000Z', book_end = '2018-12-15T17:01:00.000Z',
                                status= STATUS_PUBLISHED, pic_url=picUrl, total_tickets = 10, remain_tickets = 10)

activityBookingAvailableSql = Activity(name ='activity_published', key = 'publishedavailable', description = 'The booking is available now!',
                                start_time = '2018-12-15T17:01:00.000Z', end_time = '2018-12-30T17:01:00.000Z', place = 'anywhere',
                                book_start = '2018-10-01T17:01:00.000Z', book_end = '2018-12-15T17:01:00.000Z',
                                status= STATUS_PUBLISHED, pic_url=picUrl, total_tickets = 10, remain_tickets = 9)

activityBookingRepeatedlySql = Activity(name ='activity_published', key = 'publishedrepeated', description = 'The booking is repeated!',
                                start_time = '2018-12-15T17:01:00.000Z', end_time = '2018-12-30T17:01:00.000Z', place = 'anywhere',
                                book_start = '2018-10-01T17:01:00.000Z', book_end = '2018-12-15T17:01:00.000Z',
                                status= STATUS_PUBLISHED, pic_url=picUrl, total_tickets = 10, remain_tickets = 9)


activitySoldOutSql = Activity(name ='activity_published', key = 'publishedsoldout', description = 'The tictets has been sold out!',
                                start_time = '2018-12-15T17:01:00.000Z', end_time = '2018-12-30T17:01:00.000Z', place = 'anywhere',
                                book_start = '2018-10-01T17:01:00.000Z', book_end = '2018-12-15T17:01:00.000Z',
                                status= STATUS_PUBLISHED, pic_url=picUrl, total_tickets = 10, remain_tickets = 0)

activityBookingFinishedSql =  Activity(name ='activity_published', key = 'publishedfinished', description = 'The booking has finished!',
                                start_time = '2018-12-15T17:01:00.000Z', end_time = '2018-12-30T17:01:00.000Z', place = 'anywhere',
                                book_start = '2018-10-01T17:01:00.000Z', book_end = '2018-10-03T17:01:00.000Z',
                                status= STATUS_PUBLISHED, pic_url=picUrl, total_tickets = 10, remain_tickets = 2)

bookTicketCommand = '<xml><ToUserName><![CDATA[toUser]]></ToUserName>\n' \
          '<FromUserName><![CDATA[123456]]></FromUserName>\n' \
          '<CreateTime>1539926562</CreateTime>\n' \
          '<MsgType><![CDATA[text]]></MsgType>\n' \
          '<Content><![CDATA[抢票 %s]]></Content>\n' \
          '<MsgId>6613934222456865082</MsgId>\n' \
          '</xml>'

cancelTicketCommand = '<xml><ToUserName><![CDATA[toUser]]></ToUserName>\n' \
          '<FromUserName><![CDATA[123456]]></FromUserName>\n' \
          '<CreateTime>1539926562</CreateTime>\n' \
          '<MsgType><![CDATA[text]]></MsgType>\n' \
          '<Content><![CDATA[退票 %s]]></Content>\n' \
          '<MsgId>6613934222456865082</MsgId>\n' \
          '</xml>'


def bookTicketFrom(client, activitySql):
    key = activitySql.key
    reqBody = (bookTicketCommand % key).encode('utf-8')
    response = client.post(url, reqBody, content_type='text/xml')
    #print(response.context)
    return response.context


def cancelTicketFrom(client, activitySql):
    key = activitySql.key
    reqBody = (cancelTicketCommand % key).encode('utf-8')
    response = client.post(url, reqBody, content_type='text/xml')
    return response.context


class bookingTicketsTest(TestCase):

    def setUp(self):
        validUser.save()
        activityBookingNotStartedSql.save()
        activityBookingAvailableSql.save()
        activitySoldOutSql.save()
        activityBookingFinishedSql.save()
        activityBookingRepeatedlySql.save()

    def test_bookingNotStarted(self):
        remainTickets = activityBookingNotStartedSql.remain_tickets
        print(bookTicketFrom(self.client, activityBookingNotStartedSql))
        self.assertEqual(remainTickets,
                         Activity.objects.get(id=activityBookingNotStartedSql.id).remain_tickets)

    def test_bookingAvailable(self):
        remainTickets = activityBookingAvailableSql.remain_tickets
        print(bookTicketFrom(self.client,activityBookingAvailableSql))
        self.assertEqual(remainTickets-1,
                         Activity.objects.get(id=activityBookingAvailableSql.id).remain_tickets)

    def test_bookingRepeatedly(self):
        remainTickets = activityBookingRepeatedlySql.remain_tickets
        print(bookTicketFrom(self.client,activityBookingRepeatedlySql))
        print(bookTicketFrom(self.client,activityBookingRepeatedlySql))
        self.assertEqual(remainTickets-1,
                         Activity.objects.get(id=activityBookingRepeatedlySql.id).remain_tickets)

    def test_ticketsSoldOut(self):
        print(bookTicketFrom(self.client,activitySoldOutSql))
        self.assertEqual(0,
                         Activity.objects.get(id=activitySoldOutSql.id).remain_tickets)

    def test_bookingFinished(self):
        remainTickets = activityBookingFinishedSql.remain_tickets
        print(bookTicketFrom(self.client,activityBookingFinishedSql))
        self.assertEqual(remainTickets,
                         Activity.objects.get(id=activityBookingFinishedSql.id).remain_tickets)

    def tearDown(self):
        Activity.objects.all().delete()
        User.objects.all().delete()
        Ticket.objects.all().delete()


class cancelTicketsTest(TestCase):

    def setUp(self):
        validUser.save()
        activityBookingNotStartedSql.save()
        activityBookingAvailableSql.save()
        activitySoldOutSql.save()
        activityBookingFinishedSql.save()
        activityBookingRepeatedlySql.save()

    def test_cancelNotStarted(self):
        remainTickets = activityBookingNotStartedSql.remain_tickets
        print(cancelTicketFrom(self.client, activityBookingNotStartedSql))
        self.assertEqual(remainTickets,
                         Activity.objects.get(id=activityBookingNotStartedSql.id).remain_tickets)

    def test_cancelAvailable(self):
        remainTickets = activityBookingAvailableSql.remain_tickets
        print(bookTicketFrom(self.client,activityBookingAvailableSql))
        self.assertEqual(remainTickets-1,
                         Activity.objects.get(id=activityBookingAvailableSql.id).remain_tickets)
        print(cancelTicketFrom(self.client, activityBookingAvailableSql))
        self.assertEqual(remainTickets,
                         Activity.objects.get(id=activityBookingAvailableSql.id).remain_tickets)

    def test_cancelRepeatedly(self):#重复退掉同一张票
        remainTickets = activityBookingAvailableSql.remain_tickets
        print(bookTicketFrom(self.client, activityBookingAvailableSql))
        self.assertEqual(remainTickets - 1,
                         Activity.objects.get(id=activityBookingAvailableSql.id).remain_tickets)
        print(cancelTicketFrom(self.client, activityBookingAvailableSql))
        self.assertEqual(remainTickets,
                         Activity.objects.get(id=activityBookingAvailableSql.id).remain_tickets)
        print(cancelTicketFrom(self.client, activityBookingAvailableSql))
        self.assertEqual(remainTickets,
                         Activity.objects.get(id=activityBookingAvailableSql.id).remain_tickets)

    def test_cancelFinishedTickets(self): #退掉过期的票
        remainTickets = activityBookingFinishedSql.remain_tickets
        print(cancelTicketFrom(self.client,activityBookingFinishedSql))
        self.assertEqual(remainTickets,
                         Activity.objects.get(id=activityBookingFinishedSql.id).remain_tickets)

    def test_cancelUsedTickets(self): #退掉已经使用过的票
        remainTickets = activityBookingAvailableSql.remain_tickets
        bookTicketFrom(self.client, activityBookingAvailableSql)  # 先抢票
        unique_id = Ticket.objects.get(student_id=validUser.student_id,
                                       activity=activityBookingAvailableSql).unique_id  # 获取电子票的unique_id
        check_tickets_data = {
            "actId": activityBookingAvailableSql.id,
            "ticket": unique_id,
            ""
            "studentId": validUser.student_id
        }
        # 创建管理员
        auth.models.User.objects.create_superuser(username=superUserCorrect['username'],
                                      email=superUserCorrect['email'],
                                      password=superUserCorrect['password'])
        #管理员登录
        self.client.post('/api/a/login', superUserCorrect)
        self.client.post('/api/a/activity/checkin', check_tickets_data)#检票
        print(activityBookingAvailableSql.status)
        print(cancelTicketFrom(self.client,activityBookingAvailableSql))#再退票
        self.assertEqual(remainTickets-1,
                         Activity.objects.get(id=activityBookingAvailableSql.id).remain_tickets)

    def tearDown(self):
        Activity.objects.all().delete()
        User.objects.all().delete()
        Ticket.objects.all().delete()



class ticketDetailTest(TestCase):

    def setUp(self):
        validUser.save()
        activityBookingAvailableSql.save()
        activityBookingRepeatedlySql.save()

    def test_queryInvalidTicket(self):
        bookTicketFrom(self.client, activityBookingAvailableSql)#先抢票
        cancelTicketFrom(self.client, activityBookingAvailableSql)#然后退票
        unique_id=Ticket.objects.get(student_id=validUser.student_id, activity=activityBookingAvailableSql).unique_id #获取电子票的unique_id
        query_data={"openid":validUser.open_id, "ticket":unique_id}
        response_object = get_response_object(self.client.get("/api/u/ticket/detail", query_data))
        self.assertEqual(response_object['data']['status'], 0)

    def test_queryValidTickets(self):
        bookTicketFrom(self.client, activityBookingAvailableSql)  # 先抢票
        unique_id=Ticket.objects.get(student_id=validUser.student_id, activity=activityBookingAvailableSql).unique_id #获取电子票的unique_id
        query_data = {"openid": validUser.open_id, "ticket": unique_id}
        response_object = get_response_object(self.client.get("/api/u/ticket/detail", query_data))
        self.assertEqual(response_object['data']['status'], 1)
        cancelTicketFrom(self.client, activityBookingAvailableSql)#然后退票

    def test_queryUsedTickets(self):
        bookTicketFrom(self.client, activityBookingRepeatedlySql)  # 先抢票
        unique_id=Ticket.objects.get(student_id=validUser.student_id, activity=activityBookingRepeatedlySql).unique_id #获取电子票的unique_id
        check_tickets_data={
            "actId":activityBookingRepeatedlySql.id,
            "ticket":unique_id,
            "studentId":validUser.student_id
        }
        # 创建管理员
        auth.models.User.objects.create_superuser(username=superUserCorrect['username'],
                                      email=superUserCorrect['email'],
                                      password=superUserCorrect['password'])
        #管理员登录
        self.client.post('/api/a/login', superUserCorrect)
        self.client.post('/api/a/activity/checkin', check_tickets_data)#检票
        query_data = {"openid": validUser.open_id, "ticket": unique_id}
        response_object = get_response_object(self.client.get("/api/u/ticket/detail", query_data))
        self.assertEqual(response_object['data']['status'], 2)

    def tearDown(self):
        Activity.objects.all().delete()
        User.objects.all().delete()
        Ticket.objects.all().delete()


