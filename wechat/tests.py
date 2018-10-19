from django.test import TestCase
from wechat.views import *
# Create your tests here.
from wechat.models import *
import time,datetime


activityTicketingSql = Activity(name ='activity_published1', key = 'published1', description = 'This is a published activity!',
                                start_time = '2018-12-15T17:01:00.000Z', end_time = '2018-12-30T17:01:00.000Z', place = 'anywhere',
                                book_start = '2018-09-30T17:01:00.000Z', book_end = '2018-12-01T17:01:00.000Z',
                                status= Activity.STATUS_PUBLISHED, pic_url='http://testSource/1.png', total_tickets = 10, remain_tickets = 10)

url='/wechat?signature=0dbdfc356a8418762d8ecc57547f374fa6760ea9&timestamp=1539837340&nonce=445616432&openid=123456'

reqBodyb = b'<xml><ToUserName><![CDATA[gh_df7ce82c5d5f]]></ToUserName>\n<FromUserName><![CDATA[123456]]></FromUserName>\n<CreateTime>1539837340</CreateTime>\n<MsgType><![CDATA[event]]></MsgType>\n<Event><![CDATA[CLICK]]></Event>\n<EventKey><![CDATA[BOOKING_ACTIVITY_'
reqBodya=  b']]></EventKey>\n</xml>'

validUser = User(open_id='123456', student_id='2015012358')

class wechatLibTest(TestCase):

    def setUp(self):
        activityTicketingSql.save()
        validUser.save()

    def test_helpButton(self):
        id = activityTicketingSql.id
        reqBody=reqBodyb+str(id).encode()+reqBodya
        response=self.client.post(url, reqBody, content_type='text/xml')
        print(response.context[0].dicts[1]['Content'])


    def tearDown(self):
        Activity.objects.all().delete()
