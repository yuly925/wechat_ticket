
from django.test import TestCase

# Create your tests here.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.auth.models import User
from wechat.models import *
from adminpage.views import *
import json
import time, datetime
import copy, os

# Create your tests here.
STATUS_DELETED = -1
STATUS_SAVED = 0
STATUS_PUBLISHED = 1

superUserCorrect = {'username': 'superuser', 'email': 'superuser@test.com', 'password': 'iamsuperuser'}
superUserBlankUser = {'username': '', 'email': 'superuser@test.com', 'password': 'iamsuperuser'}
superUserBlankPassword = {'username': 'superuser', 'email': 'superuser@test.com', 'password': ''}
superUserWrongUser = {'username': 'notsuperuser', 'email': 'superuser@test.com', 'password': 'iamsuperuser'}
superUserWrongPassword = {'username': 'superuser', 'email': 'superuser@test.com', 'password': 'iamsuperuserwithwrongpassword'}

#1##############################################################################
class loginStatusTest(TestCase):

    def setUp(self):
        User.objects.create_superuser(username=superUserCorrect['username'],
                                      email=superUserCorrect['email'],
                                      password=superUserCorrect['password'])

    def test_noLogin(self):
        response = self.client.get('/api/a/login')
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 3)

    def test_login(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.get('/api/a/login')
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)

    def tearDown(self):
        pass


#2#############################################################################
class loginTest(TestCase):

    def setUp(self):
        User.objects.create_superuser(username=superUserCorrect['username'],
                                      email=superUserCorrect['email'],
                                      password=superUserCorrect['password'])

    def test_success(self):
        response = self.client.post('/api/a/login', superUserCorrect)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)

    def test_blankUser(self):
        response = self.client.post('/api/a/login', superUserBlankUser)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 3)

    def test_blankPassword(self):
        response = self.client.post('/api/a/login', superUserBlankPassword)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 3)


    def test_wrongUser(self):
        response = self.client.post('/api/a/login', superUserWrongUser)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 3)

    def test_wrongPassword(self):
        response = self.client.post('/api/a/login', superUserWrongPassword)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 3)

    def tearDown(self):
        pass



#3#############################################################################
class logoutTest(TestCase):

    def setUp(self):
        User.objects.create_superuser(username=superUserCorrect['username'],
                                      email=superUserCorrect['email'],
                                      password=superUserCorrect['password'])

    def test_noLogin(self):
        response = self.client.post('/api/a/logout', superUserCorrect)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 3)

    def test_login(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/logout', superUserCorrect)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)

    def tearDown(self):
        pass


###############################################################################
###############################################################################



activitySaved = {'name':'activity_saved', 'key':'saved', 'description' :'This is a saved activity!',
                'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-30T17:01:00.000Z', 'place' : 'anywhere',
                'bookStart' : '2018-11-01T17:01:00.000Z', 'bookEnd' : '2018-12-01T17:01:00.000Z', 'status' : STATUS_SAVED,
                'picUrl' :'./testSource/1.png', 'totalTickets' : 10}


activityPublished = {'name':'activity_published', 'key':'published', 'description' :'This is a published activity!',
                    'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-30T17:01:00.000Z', 'place' : 'anywhere',
                    'bookStart' : '2018-11-01T17:01:00.000Z', 'bookEnd' : '2018-12-01T17:01:00.000Z', 'status' : STATUS_PUBLISHED,
                    'picUrl' :'./testSource/1.png', 'totalTickets' : 10}


activityDeleted = {'name':'activity_deleted', 'key':'deleted', 'description' :'This is a deleted activity!',
                    'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-30T17:01:00.000Z', 'place' : 'anywhere',
                    'bookStart' : '2018-11-01T17:01:00.000Z', 'bookEnd' : '2018-12-01T17:01:00.000Z', 'status' : STATUS_DELETED,
                    'picUrl' :'./testSource/1.png', 'totalTickets' : 10}

activitySavedTime1 = {'name':'activity_saved_time1', 'key':'saved_time1', 'description' :'This is a saved activity! endTime < startTIme',
                    'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-14T17:01:00.000Z', 'place' : 'anywhere',
                    'bookStart' : '2018-11-01T17:01:00.000Z', 'bookEnd' : '2018-12-01T17:01:00.000Z', 'status' : STATUS_SAVED,
                    'picUrl' :'./testSource/1.png', 'totalTickets' : 10}

activitySavedTime2 = {'name':'activity_saved_time2', 'key':'saved_time2', 'description' :'This is a saved activity! bookEnd < bookStart',
                    'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-30T17:01:00.000Z', 'place' : 'anywhere',
                    'bookStart' : '2018-11-01T17:01:00.000Z', 'bookEnd' : '2018-10-01T17:01:00.000Z', 'status' : STATUS_SAVED,
                    'picUrl' :'./testSource/1.png', 'totalTickets' : 10}

activitySavedTime3 = {'name':'activity_saved_time3', 'key':'saved_time3', 'description' :'This is a saved activity! bookEnd > startTime',
                    'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-30T17:01:00.000Z', 'place' : 'anywhere',
                    'bookStart' : '2018-11-01T17:01:00.000Z', 'bookEnd' : '2018-12-21T17:01:00.000Z', 'status' : STATUS_SAVED,
                    'picUrl' :'./testSource/1.png', 'totalTickets' : 10}

activitySavedTime4 = {'name':'activity_saved_time4', 'key':'saved_time4', 'description' :'This is a saved activity! bookStart < currentTime',
                    'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-30T17:01:00.000Z', 'place' : 'anywhere',
                    'bookStart' : time.strftime("%Y-%m-%dT%H:%M:00.000Z"), 'bookEnd' : '2018-12-21T17:01:00.000Z', 'status' : STATUS_SAVED,
                    'picUrl' :'./testSource/1.png', 'totalTickets' : 10}

activitySavedImgURL = {'name':'activity_saved_url', 'key':'saved_url', 'description' :'This is a saved activity! bookStart < currentTime',
                    'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-30T17:01:00.000Z', 'place' : 'anywhere',
                    'bookStart' : '2018-11-01T17:01:00.000Z', 'bookEnd' : '2018-12-01T17:01:00.000Z', 'status' : STATUS_SAVED,
                    'picUrl' :'./testSource/2.png', 'totalTickets' : 10}

activitySavedKey = {'name':'activity_saved_key', 'key':'saved', 'description' :'This is a saved activity! bookStart < currentTime',
                    'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-30T17:01:00.000Z', 'place' : 'anywhere',
                    'bookStart' : '2018-11-01T17:01:00.000Z', 'bookEnd' : '2018-12-01T17:01:00.000Z', 'status' : STATUS_SAVED,
                    'picUrl' :'./testSource/1.png', 'totalTickets' : 10}

activitySavedNoTicket = {'name':'activity_saved_no_ticket', 'key':'saved_no_tickets', 'description' :'This is a saved activity! TotalTickets=0',
                        'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-30T17:01:00.000Z', 'place' : 'anywhere',
                        'bookStart' : '2018-11-01T17:01:00.000Z', 'bookEnd' : '2018-12-01T17:01:00.000Z', 'status' : STATUS_SAVED,
                        'picUrl' :'./testSource/1.png', 'totalTickets' : 0}


activityPublishedTime1 = {'name':'activity_published_time1', 'key':'published_time1', 'description' :'This is a published activity! endTime < startTIme',
                    'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-14T17:01:00.000Z', 'place' : 'anywhere',
                    'bookStart' : '2018-11-01T17:01:00.000Z', 'bookEnd' : '2018-12-01T17:01:00.000Z', 'status' : STATUS_PUBLISHED,
                    'picUrl' :'./testSource/1.png', 'totalTickets' : 10}

activityPublishedTime2 = {'name':'activity_published_time2', 'key':'published_time2', 'description' :'This is a published activity! bookEnd < bookStart',
                    'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-30T17:01:00.000Z', 'place' : 'anywhere',
                    'bookStart' : '2018-11-01T17:01:00.000Z', 'bookEnd' : '2018-10-01T17:01:00.000Z', 'status' : STATUS_PUBLISHED,
                    'picUrl' :'./testSource/1.png', 'totalTickets' : 10}

activityPublishedTime3 = {'name':'activity_published_time3', 'key':'published_time3', 'description' :'This is a published activity! bookEnd > startTime',
                    'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-30T17:01:00.000Z', 'place' : 'anywhere',
                    'bookStart' : '2018-11-01T17:01:00.000Z', 'bookEnd' : '2018-12-21T17:01:00.000Z', 'status' : STATUS_PUBLISHED,
                    'picUrl' :'./testSource/1.png', 'totalTickets' : 10}

activityPublishedTime4 = {'name':'activity_published_time4', 'key':'published_time4', 'description' :'This is a published activity! bookStart < currentTime',
                    'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-30T17:01:00.000Z', 'place' : 'anywhere',
                    'bookStart' : time.strftime("%Y-%m-%dT%H:%M:00.000Z"), 'bookEnd' : '2018-12-21T17:01:00.000Z', 'status' : STATUS_PUBLISHED,
                    'picUrl' :'./testSource/1.png', 'totalTickets' : 10}

activityPublishedImgURL = {'name':'activity_published_url', 'key':'published_url', 'description' :'This is a published activity! bookStart < currentTime',
                    'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-30T17:01:00.000Z', 'place' : 'anywhere',
                    'bookStart' : '2018-11-01T17:01:00.000Z', 'bookEnd' : '2018-12-01T17:01:00.000Z', 'status' : STATUS_PUBLISHED,
                    'picUrl' :'./testSource/2.png', 'totalTickets' : 10}

activityPublishedKey = {'name':'activity_published_key', 'key':'published', 'description' :'This is a published activity! bookStart < currentTime',
                    'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-30T17:01:00.000Z', 'place' : 'anywhere',
                    'bookStart' : '2018-11-01T17:01:00.000Z', 'bookEnd' : '2018-12-01T17:01:00.000Z', 'status' : STATUS_PUBLISHED,
                    'picUrl' :'./testSource/1.png', 'totalTickets' : 10}


activityPublishedNoTicket = {'name':'activity_published_no_ticket', 'key':'published_no_tickets', 'description' :'This is a published activity! TotalTickets=0',
                'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-30T17:01:00.000Z', 'place' : 'anywhere',
                'bookStart' : '2018-11-01T17:01:00.000Z', 'bookEnd' : '2018-12-01T17:01:00.000Z', 'status' : STATUS_PUBLISHED,
                'picUrl' :'./testSource/1.png', 'totalTickets' : 0}

'''
activityActing = {'id':7, 'name':'activity_published4', 'description' : 'This is a published activity!',
                                'startTime' : time.strftime("%Y-%m-%dT00:00:00.000Z"), 'endTime': '2018-12-30T17:01:00.000Z', 'place': 'anywhere',
                                'bookStart' : '2018-09-15T17:01:00.000Z', 'bookEnd':'2018-09-25T17:01:00.000Z', 
                                'status': STATUS_PUBLISHED, 'pic_url': './testSource/1.png', 'totalTickets':10}


activityActed = {'id':8, 'name':'activity_published5', 'description': 'This is a published activity!',
                                'startTime' : '2018-09-26T17:01:00.000Z', 'endTime' : '2018-09-27T17:01:00.000Z', 'place' : 'anywhere',
                                'bookStart' : '2018-09-15T17:01:00.000Z', 'bookEnd' : '2018-09-25T17:01:00.000Z', 
                                'status': STATUS_PUBLISHED, 'picUrl':'./testSource/1.png', 'totalTickets' : 10}
'''

activitySavedSql = Activity(name ='activity_saved', key = 'saved', description = 'This is a saved activity!',
                            start_time = '2018-12-15T17:01:00.000Z', end_time = '2018-12-30T17:01:00.000Z', place = 'anywhere',
                            book_start = '2018-11-01T17:01:00.000Z', book_end = '2018-12-01T17:01:00.000Z', 
                            status= 0, pic_url='./testSource/1.png', total_tickets = 10, remain_tickets = 10)

activityPublishedSql = Activity(name ='activity_published', key = 'published', description = 'This is a published activity!',
                                start_time = '2018-12-15T17:01:00.000Z', end_time = '2018-12-30T17:01:00.000Z', place = 'anywhere',
                                book_start = '2018-11-01T17:01:00.000Z', book_end = '2018-12-01T17:01:00.000Z', 
                                status= STATUS_PUBLISHED, pic_url='./testSource/1.png', total_tickets = 10, remain_tickets = 10)

activityDeletedSql = Activity(name ='activity_deleted', key = 'deleted', description = 'This is a deleted activity!',
                            start_time = '2018-12-15T17:01:00.000Z', end_time = '2018-12-30T17:01:00.000Z', place = 'anywhere',
                            book_start = '2018-11-01T17:01:00.000Z', book_end = '2018-12-01T17:01:00.000Z', 
                            status= STATUS_DELETED, pic_url='./testSource/1.png', total_tickets = 10, remain_tickets = 10)

activityTicketingSql = Activity(name ='activity_published1', key = 'published1', description = 'This is a published activity!',
                                start_time = '2018-12-15T17:01:00.000Z', end_time = '2018-12-30T17:01:00.000Z', place = 'anywhere',
                                book_start = time.strftime("%Y-%m-%dT%H:%M:00.000Z"), book_end = '2018-12-01T17:01:00.000Z', 
                                status= STATUS_PUBLISHED, pic_url='./testSource/1.png', total_tickets = 10, remain_tickets = 10)

activityTicketedSql = Activity(name ='activity_published2', key = 'published2', description = 'This is a published activity!',
                                start_time = '2019-12-15T17:01:00.000Z', end_time = '2019-12-30T17:01:00.000Z', place = 'anywhere',
                                book_start = time.strftime("%Y-%m-01T00:00:00.000Z"), book_end = time.strftime("%Y-%m-%dT%H:%M:00.000Z"), 
                                status= STATUS_PUBLISHED, pic_url='./testSource/1.png', total_tickets = 10, remain_tickets = 10)

activityWaitActSql = Activity(name ='activity_published3', key = 'published3', description = 'This is a published activity!',
                                start_time = '2019-09-26T17:01:00.000Z', end_time = '2019-12-30T17:01:00.000Z', place = 'anywhere',
                                book_start = '2018-09-15T17:01:00.000Z', book_end = '2018-09-25T17:01:00.000Z', 
                                status= STATUS_PUBLISHED, pic_url='./testSource/1.png', total_tickets = 10, remain_tickets = 10)

activityActingSql = Activity(name ='activity_published4', key = 'published4', description = 'This is a published activity!',
                                start_time = time.strftime("%Y-%m-%dT00:00:00.000Z"), end_time = '2018-12-30T17:01:00.000Z', place = 'anywhere',
                                book_start = '2018-09-15T17:01:00.000Z', book_end = '2018-09-25T17:01:00.000Z', 
                                status= STATUS_PUBLISHED, pic_url='./testSource/1.png', total_tickets = 10, remain_tickets = 10)

activityActedSql = Activity(name ='activity_published5', key = 'published5', description = 'This is a published activity!',
                                start_time = '2018-09-26T17:01:00.000Z', end_time = '2018-09-27T17:01:00.000Z', place = 'anywhere',
                                book_start = '2018-09-15T17:01:00.000Z', book_end = '2018-09-25T17:01:00.000Z', 
                                status= STATUS_PUBLISHED, pic_url='./testSource/1.png', total_tickets = 10, remain_tickets = 10)

#4#############################################################################
class getActivityListTest(TestCase):

    def setUp(self):
        User.objects.create_superuser(username=superUserCorrect['username'],
                                      email=superUserCorrect['email'],
                                      password=superUserCorrect['password'])
        activitySavedSql.save()
        activityPublishedSql.save()
        activityDeletedSql.save()
        
    def test_noLogin(self):
        response = self.client.get('/api/a/activity/list')
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 3)

    def test_getActivityList(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.get('/api/a/activity/list')
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)
        #print(response_obj['data'])
        self.assertEqual(len(response_obj['data']), 2)
        self.assertEqual(response_obj['data'][0]['id'], 1)
        self.assertEqual(response_obj['data'][1]['id'], 2)

    def tearDown(self):
        Activity.objects.all().delete()


#5#######################################################################
class deleteActivityTest(TestCase):

    def setUp(self):
        User.objects.create_superuser(username=superUserCorrect['username'],
                                      email=superUserCorrect['email'],
                                      password=superUserCorrect['password'])
        activityDeletedSql.save()
        activitySavedSql.save()
        activityPublishedSql.save()
        activityTicketingSql.save()
        activityTicketedSql.save()
        activityWaitActSql.save()
        activityActingSql.save()
        activityActedSql.save()

    def test_noLogin(self):
        response = self.client.post('/api/a/activity/delete', {'id' : 1})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 3)

    def test_delDeletedActivity(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/delete', {'id' : 1})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_delSavedActivity(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/delete', {'id' : 2})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)

    def test_delBeforeTicketActivity(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/delete',{'id' : 3})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)
        #self.assertEqual(Activity.objects.filter(id = 2), [])

    def test_delTicketingActivity(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/delete',{'id' : 4})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)
        #self.assertEqual(Activity.objects.filter(id = 2), [])

    def test_delAfterTicketActivity(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/delete',{'id' : 5})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)
        #self.assertEqual(Activity.objects.filter(id = 2), [])

    def test_delBeforeActActivity(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/delete',{'id' : 6})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)
        #self.assertEqual(Activity.objects.filter(id = 2), [])

    def test_delActingActivity(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/delete',{'id' : 7})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)
        #self.assertEqual(Activity.objects.filter(id = 2), [])

    def test_delAfterActActivity(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/delete',{'id' : 8})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)
        #self.assertEqual(Activity.objects.filter(id = 2), [])

    def test_delNotExistActivity(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/delete', {'id' : 100})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def tearDown(self):
        Activity.objects.all().delete()


#6##################################################################################
class createActivityTest(TestCase):

    def setUp(self):
        User.objects.create_superuser(username=superUserCorrect['username'],
                                      email=superUserCorrect['email'],
                                      password=superUserCorrect['password'])

    def test_noLogin(self):
        response = self.client.post('/api/a/activity/create', activitySaved)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 3)

    def test_createDeleted(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/create', activityDeleted)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_savedSuccess(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/create', activitySaved)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)

    def test_savedTime1(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/create', activitySavedTime1)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_savedTime2(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/create', activitySavedTime2)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_savedTime3(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/create', activitySavedTime3)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_savedTime4(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/create', activitySavedTime4)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_savedImgURL(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/create', activitySavedImgURL)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_savedKeyConflict(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/create', activitySaved)
        response = self.client.post('/api/a/activity/create', activitySavedKey)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_savedNoTicket(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/create', activitySavedNoTicket)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_publishedSuccess(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/create', activityPublished)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)

    def test_publishedTime1(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/create', activityPublishedTime1)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_publishedTime2(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/create', activityPublishedTime2)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_publishedTime3(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/create', activityPublishedTime3)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_publishedTime4(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/create', activityPublishedTime4)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_publishedImgURL(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/create', activityPublishedImgURL)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_publishedKeyConflict(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/create', activityPublished)
        response = self.client.post('/api/a/activity/create', activityPublishedKey)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_publishedNoTicket(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/create', activityPublishedNoTicket)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def tearDown(self):
        Activity.objects.all().delete()



#7###################################################################################
class getActivityDetail(TestCase):

    def setUp(self):
        User.objects.create_superuser(username=superUserCorrect['username'],
                                      email=superUserCorrect['email'],
                                      password=superUserCorrect['password'])
        activitySavedSql.save()
        activityPublishedSql.save()
        activityDeletedSql.save()

    def test_noLogin(self):
        response = self.client.get('/api/a/activity/detail', {'id':1})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 3)

    def test_savedActivity(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.get('/api/a/activity/detail', {'id' : 1})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)

    def test_publishedActivity(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.get('/api/a/activity/detail', {'id' : 2})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)

    def test_DeletedActivity(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.get('/api/a/activity/detail', {'id' : 3})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_notExistID(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.get('/api/a/activity/detail', {'id' : 100})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def tearDown(self):
        Activity.objects.all().delete()


#8##############################################################################
class editActivityDetail(TestCase):

    def setUp(self):
        User.objects.create_superuser(username=superUserCorrect['username'],
                                      email=superUserCorrect['email'],
                                      password=superUserCorrect['password'])
        activityDeletedSql.save()
        activitySavedSql.save()
        activityPublishedSql.save()
        activityTicketingSql.save()
        activityTicketedSql.save()
        activityWaitActSql.save()
        activityActingSql.save()
        activityActedSql.save()

    def test_noLogin(self):
        activityEdited = copy.deepcopy(activitySaved)
        activityEdited['id']=2
        del activityEdited['key']
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 3)

    def test_editDeleted(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityEdited = copy.deepcopy(activityDeleted)
        activityEdited['name'] = 'deletedEdit'
        activityEdited['id']=1
        del activityEdited['key']
        #print(activityEdited)
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_editSaved(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityEdited = {'id':2, 'name':'activity_save12d', 'description' :'This i12s a saved activity!',
                          'startTime' : '2018-12-15T17:02:00.000Z', 'endTime' : '2018-12-30T17:02:00.000Z', 'place' : 'anywWQWhere',
                          'bookStart' : '2018-11-01T17:02:00.000Z', 'bookEnd' : '2018-12-01T17:02:00.000Z', 'status' : STATUS_PUBLISHED,
                          'picUrl' :'./testSource/3.png', 'totalTickets' : 8}
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)

    def test_editPublished1(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityEdited = copy.deepcopy(activityPublished)
        activityEdited['id']=3
        activityEdited['description'] = 'ssss'
        activityEdited['url']='./testSource/3.png'
        del activityEdited['key']
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)

    def test_editPublished2(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityEdited = copy.deepcopy(activityPublished)
        activityEdited['id']=3
        activityEdited['name'] = 'ssss'
        del activityEdited['key']
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_editPublished3(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityEdited = copy.deepcopy(activityPublished)
        activityEdited['place']='sssss'
        activityEdited['id']=3
        del activityEdited['key']
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_editPublished4(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityEdited = copy.deepcopy(activityPublished)
        activityEdited['id']=3
        activityEdited['bookStart'] = '2018-09-14T17:01:00.000Z'
        del activityEdited['key']
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_editPublished5(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityTemp = Activity.objects.filter(id=8)[0]
        activityEdited={'id':activityTemp.id, 'place':activityTemp.place,'description':activityTemp.description,
                        'startTime':activityTemp.start_time, 'endTime':activityTemp.end_time, 
                        'bookStart':activityTemp.book_start, 'bookEnd':activityTemp.book_end,
                        'picUrl':activityTemp.pic_url, 'status':activityTemp.status, 
                        'name':activityTemp.name, 'totalTickets':activityTemp.total_tickets}
        activityEdited['startTime']='2018-12-14T17:01:00.000Z'
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_editPublished6(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityTemp = Activity.objects.filter(id=8)[0]
        activityEdited={'id':activityTemp.id, 'place':activityTemp.place,'description':activityTemp.description,
                        'startTime':activityTemp.start_time, 'endTime':activityTemp.end_time, 
                        'bookStart':activityTemp.book_start, 'bookEnd':activityTemp.book_end,
                        'picUrl':activityTemp.pic_url, 'status':activityTemp.status, 
                        'name':activityTemp.name, 'totalTickets':activityTemp.total_tickets}
        activityEdited['endTime']='2018-12-29T17:01:00.000Z'
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)
    
    def test_editPublished7(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityTemp = Activity.objects.filter(id=7)[0]
        activityEdited={'id':activityTemp.id, 'place':activityTemp.place,'description':activityTemp.description,
                        'startTime':activityTemp.start_time, 'endTime':activityTemp.end_time, 
                        'bookStart':activityTemp.book_start, 'bookEnd':activityTemp.book_end,
                        'picUrl':activityTemp.pic_url, 'status':activityTemp.status, 
                        'name':activityTemp.name, 'totalTickets':activityTemp.total_tickets}
        activityEdited['startTime']='2018-10-29T17:01:00.000Z'
        activityEdited['endTime']='2018-12-29T17:01:00.000Z'
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)


    def test_editPublished8(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityTemp = Activity.objects.filter(id=7)[0]
        activityEdited={'id':activityTemp.id, 'place':activityTemp.place,'description':activityTemp.description,
                        'startTime':activityTemp.start_time, 'endTime':activityTemp.end_time, 
                        'bookStart':activityTemp.book_start, 'bookEnd':activityTemp.book_end,
                        'picUrl':activityTemp.pic_url, 'status':activityTemp.status, 
                        'name':activityTemp.name, 'totalTickets':activityTemp.total_tickets}
        activityEdited['bookEnd']='2018-9-29T17:01:00.000Z'
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)


    def test_editPublished9(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityTemp = Activity.objects.filter(id=6)[0]
        activityEdited={'id':activityTemp.id, 'place':activityTemp.place,'description':activityTemp.description,
                        'startTime':activityTemp.start_time, 'endTime':activityTemp.end_time, 
                        'bookStart':activityTemp.book_start, 'bookEnd':activityTemp.book_end,
                        'picUrl':activityTemp.pic_url, 'status':activityTemp.status, 
                        'name':activityTemp.name, 'totalTickets':activityTemp.total_tickets}
        activityEdited['bookEnd']='2018-9-25T17:02:10.000Z'
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)

    def test_editPublished10(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityTemp = Activity.objects.filter(id=3)[0]
        activityEdited={'id':activityTemp.id, 'place':activityTemp.place,'description':activityTemp.description,
                        'startTime':activityTemp.start_time, 'endTime':activityTemp.end_time, 
                        'bookStart':activityTemp.book_start, 'bookEnd':activityTemp.book_end,
                        'picUrl':activityTemp.pic_url, 'status':activityTemp.status, 
                        'name':activityTemp.name, 'totalTickets':activityTemp.total_tickets}
        activityEdited['totalTickets']=9
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)

    def test_editPublished10(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityTemp = Activity.objects.filter(id=4)[0]
        aactivityEdited={'id':activityTemp.id, 'place':activityTemp.place,'description':activityTemp.description,
                        'startTime':activityTemp.start_time, 'endTime':activityTemp.end_time, 
                        'bookStart':activityTemp.book_start, 'bookEnd':activityTemp.book_end,
                        'picUrl':activityTemp.pic_url, 'status':activityTemp.status, 
                        'name':activityTemp.name, 'totalTickets':activityTemp.total_tickets}
        activityEdited['totalTickets']=9
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_editPublished10(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityTemp = Activity.objects.filter(id=3)[0]
        activityEdited={'id':activityTemp.id, 'place':activityTemp.place,'description':activityTemp.description,
                        'startTime':activityTemp.start_time, 'endTime':activityTemp.end_time, 
                        'bookStart':activityTemp.book_start, 'bookEnd':activityTemp.book_end,
                        'picUrl':activityTemp.pic_url, 'status':activityTemp.status, 
                        'name':activityTemp.name, 'totalTickets':activityTemp.total_tickets}
        activityEdited['totalTickets']=9
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)

    def test_savedToPublished(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityEdited = copy.deepcopy(activitySaved)
        activityEdited['state'] = STATUS_PUBLISHED
        activityEdited['id']=2
        del activityEdited['key']
        #print(activityEdited)
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)

    def test_publishedToSaved(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityEdited = copy.deepcopy(activityPublished)
        activityEdited['state'] = STATUS_SAVED
        activityEdited['id']=3
        del activityEdited['key']
        #print(activityEdited)
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)


    def tearDown(self):
        #print(Activity.objects.all().delete())
        Activity.objects.all().delete()

'''
#9#################################################################################
class getActivityMenu(TestCase):

    def setUp(self):
        User.objects.create_superuser(username=superUserCorrect['username'],
                                      email=superUserCorrect['email'],
                                      password=superUserCorrect['password'])
        activitySavedSql.save()
        activityPublishedSql.save()
        activityDeletedSql.save()

    def test_noLogin(self):
        response = self.client.get('/api/a/activity/menu')
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 3)

    def test_success(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.get('/api/a/activity/menu')
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)
        #self.assertEqual(len(response_obj['data']), 1)

    def tearDown(self):
        #print(Activity.objects.all().delete())
        Activity.objects.all().delete()


#10##########################################################################
class adjustActivityMenu(TestCase):

    def setUp(self):
        User.objects.create_superuser(username=superUserCorrect['username'],
                                      email=superUserCorrect['email'],
                                      password=superUserCorrect['password'])
        activityDeletedSql.save()
        activitySavedSql.save()
        activityPublishedSql.save()
        activityTicketingSql.save()
        activityTicketedSql.save()

    def test_noLogin(self):
        response = self.client.post('/api/a/activity/menu', {'items':[4]})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 3)

    def test_addDeleted(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/menu', {[1]})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_addSaved(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/menu', {2:2})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_addPublishedBeforeTicket(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/menu', {3:3})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_addPublishedTicketing(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/menu', {4:4})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)

    def test_addPublishedAfterTicket(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/menu', {5:5})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)
    
    def tearDown(self):
        Activity.objects.all().delete()
'''
################################################################################
################################################################################

imgCorrect={'image': './testSource/1.png'}
imgNotExist={'image': './testSource/2.png'}

#11#############################################################################
class uploadImgTest(TestCase):
    def setUp(self):
        User.objects.create_superuser(username=superUserCorrect['username'],
                                      email=superUserCorrect['email'],
                                      password=superUserCorrect['password'])


    def test_onLogin(self):
        #imgPath = os.path.join(settings.BASE_DIR, './testSource/1.png')
        with open('./testSource/1.png', 'rb') as pic:
            response = self.client.post('/api/a/image/upload', {'image': pic})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 3)


    def test_success(self):
        self.client.post('/api/a/login', superUserCorrect)
        #imgPath = os.path.join(settings.BASE_DIR, './testSource/1.png')
        with open('./testSource/1.png', 'rb') as pic:
            response = self.client.post('/api/a/image/upload', {'image': pic})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)

    '''
    def test_noImg(self):
        self.client.post('/api/a/login', superUserCorrect)
        #imgPath = os.path.join(settings.BASE_DIR, './testSource/2.png')
        with open('./testSource/2.png', 'rb') as pic:
            response = self.client.post('/api/a/image/upload', {'image': pic})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)
    '''

#############################################################################
#############################################################################

STATUS_CANCELLED = 0
STATUS_VALID = 1
STATUS_USED = 2

ticketCorrect1 = {'actId': 1, 'ticket': 'iamuniqueid'}
ticketCorrect2 = {'actId': 1,'studentId':123456}
ticketWrongActId = {'actId': 10, 'ticket': 'iamuniqueid222'}
ticketWrongTicket = {'actId': 1,'ticket': 'iamuniqueid222'}
ticketWrongStudentId =  {'actId': 1,'studentId':1234567}

ticketUsed={'actId': 1, 'ticket': 'iamuniqueid2'}
ticketCancelled={'actId': 1, 'ticket': 'iamuniqueid3'}


activityTicketedSql1 = Activity(id=1, name ='activity_published2', key = 'published2', description = 'This is a published activity!',
                                start_time = '2019-12-15T17:01:00.000Z', end_time = '2019-12-30T17:01:00.000Z', place = 'anywhere',
                                book_start = time.strftime("%Y-%m-01T00:00:00.000Z"), book_end = time.strftime("%Y-%m-%dT%H:%M:00.000Z"), 
                                status= STATUS_PUBLISHED, pic_url='./testSource/1.png', total_tickets = 10, remain_tickets = 10)

ticketUsedSql=Ticket(student_id=654321, unique_id='iamuniqueid2', 
                activity=activityTicketedSql1, status=STATUS_USED)
ticketValidSql=Ticket(student_id=123456, unique_id='iamuniqueid', 
                activity=activityTicketedSql1, status=STATUS_VALID)
ticketCancelledSql=Ticket(student_id=111111, unique_id='iamuniqueid3', 
                activity=activityTicketedSql1, status=STATUS_CANCELLED)


#12#########################################################################
class checkTicket(TestCase):

    def setUp(self):
        User.objects.create_superuser(username=superUserCorrect['username'],
                                      email=superUserCorrect['email'],
                                      password=superUserCorrect['password'])
        activityTicketedSql1.save()
        ticketValidSql.save()
        ticketUsedSql.save()
        ticketCancelledSql.save()

    def test_notLogin(self):
        response = self.client.post('/api/a/activity/checkin', ticketCorrect1)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 3)

    def test_Ticket(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/checkin', ticketCorrect1)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)

    def test_StudentTicket(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/checkin', ticketCorrect2)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)

    def test_wrongActId(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/checkin', ticketWrongActId)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_wrongTicket(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/checkin', ticketWrongTicket)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_wrongStudentId(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/checkin', ticketWrongStudentId)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)
    
    def test_ticketUsed(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/checkin', ticketUsed)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)
    
    def test_ticketCancelled(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/checkin', ticketCancelled)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)


    def tearDown(self):
        Activity.objects.all().delete()
        Ticket.objects.all().delete()

