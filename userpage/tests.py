from django.test import TestCase
import json
from wechat.models import Activity
from userpage.views import *
# Create your tests here.

###############################################################################
###############################################################################
STATUS_DELETED = -1
STATUS_SAVED = 0
STATUS_PUBLISHED = 1
picUrl = "http://pic14.nipic.com/20110605/1369025_165540642000_2.jpg"

activitySaved = {'name':'activity_saved', 'key':'saved', 'description' :'This is a saved activity!',
                'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-30T17:01:00.000Z', 'place' : 'anywhere',
                'bookStart' : '2018-11-01T17:01:00.000Z', 'bookEnd' : '2018-12-01T17:01:00.000Z', 'status' : STATUS_SAVED,
                'picUrl' :picUrl, 'totalTickets' : 10}


activityPublished = {'name':'activity_published', 'key':'published', 'description' :'This is a published activity!',
                    'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-30T17:01:00.000Z', 'place' : 'anywhere',
                    'bookStart' : '2018-11-01T17:01:00.000Z', 'bookEnd' : '2018-12-01T17:01:00.000Z', 'status' : STATUS_PUBLISHED,
                    'picUrl' :picUrl, 'totalTickets' : 10}


activityDeleted = {'name':'activity_deleted', 'key':'deleted', 'description' :'This is a deleted activity!',
                    'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-30T17:01:00.000Z', 'place' : 'anywhere',
                    'bookStart' : '2018-11-01T17:01:00.000Z', 'bookEnd' : '2018-12-01T17:01:00.000Z', 'status' : STATUS_DELETED,
                    'picUrl' :picUrl, 'totalTickets' : 10}

activitySavedSql = Activity(name ='activity_saved', key = 'saved', description = 'This is a saved activity!',
                            start_time = '2018-12-15T17:01:00.000Z', end_time = '2018-12-30T17:01:00.000Z', place = 'anywhere',
                            book_start = '2018-11-01T17:01:00.000Z', book_end = '2018-12-01T17:01:00.000Z',
                            status= 0, pic_url=picUrl, total_tickets = 10, remain_tickets = 10)

activityPublishedSql = Activity(name ='activity_published', key = 'published', description = 'This is a published activity!',
                                start_time = '2018-12-15T17:01:00.000Z', end_time = '2018-12-30T17:01:00.000Z', place = 'anywhere',
                                book_start = '2018-11-01T17:01:00.000Z', book_end = '2018-12-01T17:01:00.000Z',
                                status= STATUS_PUBLISHED, pic_url=picUrl, total_tickets = 10, remain_tickets = 10)

activityDeletedSql = Activity(name ='activity_deleted', key = 'deleted', description = 'This is a deleted activity!',
                            start_time = '2018-12-15T17:01:00.000Z', end_time = '2018-12-30T17:01:00.000Z', place = 'anywhere',
                            book_start = '2018-11-01T17:01:00.000Z', book_end = '2018-12-01T17:01:00.000Z',
                            status= STATUS_DELETED, pic_url=picUrl, total_tickets = 10, remain_tickets = 10)

validUser = User(open_id='123456', student_id='')

###############################################################################
###############################################################################


def get_response_object(response):
    ''' 向client发送get_message,返回一个object对象 '''
    response_json = response.content.decode('utf-8')
    return json.loads(response_json)


class userBindTest(TestCase):
    def setUp(self):
        self.openid = '123456' #先随便填写一个openid
        self.get_data = {"openid":self.openid}
        validUser.save()

    def test_noBind(self):
        response_object = get_response_object(self.client.get('/api/u/user/bind', self.get_data))
        self.assertEqual(response_object['code'], 0)
        self.assertEqual(response_object['data'], "")

    def test_falseBind(self):
        false_post_data = {"openid": self.openid, "student_id": "201501118", "password": "233"}
        response_object = get_response_object(self.client.post('/api/u/user/bind', false_post_data))
        self.assertNotEqual(response_object['code'], 0)
        response_object = get_response_object(self.client.get('/api/u/user/bind', self.get_data))
        self.assertEqual(response_object['code'], 0)
        self.assertEqual(response_object['data'], "")

    def test_correctBind(self):
        right_post_data = {"openid": self.openid, "student_id": "2015011584", "password": "233"}
        self.client.post('/api/u/user/bind', right_post_data)
        response_object = get_response_object(self.client.get('/api/u/user/bind', self.get_data))
        self.assertEqual(response_object['code'], 0)
        self.assertNotEqual(response_object['data'], "")



class userActivity(TestCase):
    def setUp(self):
        activityPublishedSql.save()
        activityDeletedSql.save()
        activitySavedSql.save()

    def checkActivityDetail(self, response_data, correct_data, correct_remainTickets):
        self.assertEqual(response_data['remainTickets'], correct_remainTickets)
        test_attributes = ["name", "key", "description","place","totalTickets", "picUrl"]
        for attribute in test_attributes:
            self.assertEqual(response_data[attribute], correct_data[attribute])

    def test_getPublishedActivityDetail(self):
        get_data = {"id": str(activityPublishedSql.id)}
        response_object = get_response_object(self.client.get('/api/u/activity/detail', get_data))
        self.assertEqual(response_object['code'],0)
        self.checkActivityDetail(response_object['data'], activityPublished, activityPublishedSql.remain_tickets)
        # !此处可以增加抢票后对剩余票数的检查

    def test_getSavedActivityDetail(self):
        get_data = {"id": str(activitySavedSql.id)}
        response_object = get_response_object(self.client.get('/api/u/activity/detail', get_data))
        self.assertNotEqual(response_object['code'], 0)

    def test_getDeletedActivityDetail(self):
        get_data = {"id": str(activityDeletedSql.id)}
        response_object = get_response_object(self.client.get('/api/u/activity/detail', get_data))
        self.assertNotEqual(response_object['code'], 0)


