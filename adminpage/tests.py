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
                'picUrl' :'http://host.net/testSource/1.png', 'totalTickets' : 10}


activityPublished = {'name':'activity_published', 'key':'published', 'description' :'This is a published activity!',
                    'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-30T17:01:00.000Z', 'place' : 'anywhere',
                    'bookStart' : '2018-11-01T17:01:00.000Z', 'bookEnd' : '2018-12-01T17:01:00.000Z', 'status' : STATUS_PUBLISHED,
                    'picUrl' :'http://host.net/testSource/1.png', 'totalTickets' : 10}


activityDeleted = {'name':'activity_deleted', 'key':'deleted', 'description' :'This is a deleted activity!',
                    'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-30T17:01:00.000Z', 'place' : 'anywhere',
                    'bookStart' : '2018-11-01T17:01:00.000Z', 'bookEnd' : '2018-12-01T17:01:00.000Z', 'status' : STATUS_DELETED,
                    'picUrl' :'http://host.net/testSource/1.png', 'totalTickets' : 10}

activitySavedWrongTime = {'name':'activity_saved_time1', 'key':'saved_wrong_time', 'description' :'This is a saved activity! endTime < startTIme',
                    'startTime' : '2018-12-14T17:01:00.0wq00Z', 'endTime' : '2018-12-10T17:01:00.000Z', 'place' : 'anywhere',
                    'bookStart' : '2018-11-01T17:01:00.0wq00Z', 'bookEnd' : '2018-12-01T17:01:00.000Z', 'status' : STATUS_SAVED,
                    'picUrl' :'http://host.net/testSource/1.png', 'totalTickets' : 10}

activitySavedTime1 = {'name':'activity_saved_time1', 'key':'saved_time1', 'description' :'This is a saved activity! endTime < startTIme',
                    'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-14T17:01:00.000Z', 'place' : 'anywhere',
                    'bookStart' : '2018-11-01T17:01:00.000Z', 'bookEnd' : '2018-12-01T17:01:00.000Z', 'status' : STATUS_SAVED,
                    'picUrl' :'http://host.net/testSource/1.png', 'totalTickets' : 10}

activitySavedTime2 = {'name':'activity_saved_time2', 'key':'saved_time2', 'description' :'This is a saved activity! bookEnd < bookStart',
                    'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-30T17:01:00.000Z', 'place' : 'anywhere',
                    'bookStart' : '2018-11-01T17:01:00.000Z', 'bookEnd' : '2018-10-01T17:01:00.000Z', 'status' : STATUS_SAVED,
                    'picUrl' :'http://host.net/testSource/1.png', 'totalTickets' : 10}

activitySavedTime3 = {'name':'activity_saved_time3', 'key':'saved_time3', 'description' :'This is a saved activity! bookEnd > startTime',
                    'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-30T17:01:00.000Z', 'place' : 'anywhere',
                    'bookStart' : '2018-11-01T17:01:00.000Z', 'bookEnd' : '2018-12-21T17:01:00.000Z', 'status' : STATUS_SAVED,
                    'picUrl' :'http://host.net/testSource/1.png', 'totalTickets' : 10}

activitySavedTime4 = {'name':'activity_saved_time4', 'key':'saved_time4', 'description' :'This is a saved activity! bookStart < currentTime',
                    'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-30T17:01:00.000Z', 'place' : 'anywhere',
                    'bookStart' : datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:00.000Z"), 'bookEnd' : '2018-12-21T17:01:00.000Z', 'status' : STATUS_SAVED,
                    'picUrl' :'http://host.net/testSource/1.png', 'totalTickets' : 10}

activitySavedKey = {'name':'activity_saved_key', 'key':'saved', 'description' :'This is a saved activity! bookStart < currentTime',
                    'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-30T17:01:00.000Z', 'place' : 'anywhere',
                    'bookStart' : '2018-11-01T17:01:00.000Z', 'bookEnd' : '2018-12-01T17:01:00.000Z', 'status' : STATUS_SAVED,
                    'picUrl' :'http://host.net/testSource/1.png', 'totalTickets' : 10}

activitySavedNoTicket = {'name':'activity_saved_no_ticket', 'key':'saved_no_tickets', 'description' :'This is a saved activity! TotalTickets=0',
                        'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-30T17:01:00.000Z', 'place' : 'anywhere',
                        'bookStart' : '2018-11-01T17:01:00.000Z', 'bookEnd' : '2018-12-01T17:01:00.000Z', 'status' : STATUS_SAVED,
                        'picUrl' :'http://host.net/testSource/1.png', 'totalTickets' : 0}

activityPublishedWrongTime = {'name':'activity_published_time1', 'key':'published_rwong_time', 'description' :'This is a published activity! endTime < startTIme',
                            'startTime' : '2018-12-5T17:01:000Z', 'endTime' : '2018-12-14T17:01:00.000Z', 'place' : 'anywhere',
                            'bookStart' : '2018-11-01T17:01:00.000Z', 'bookEnd' : '2018-12-01T17:01:00.000Z', 'status' : STATUS_PUBLISHED,
                            'picUrl' :'http://host.net/testSource/1.png', 'totalTickets' : 10}

activityPublishedTime1 = {'name':'activity_published_time1', 'key':'published_time1', 'description' :'This is a published activity! endTime < startTIme',
                    'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-14T17:01:00.000Z', 'place' : 'anywhere',
                    'bookStart' : '2018-11-01T17:01:00.000Z', 'bookEnd' : '2018-12-01T17:01:00.000Z', 'status' : STATUS_PUBLISHED,
                    'picUrl' :'http://host.net/testSource/1.png', 'totalTickets' : 10}

activityPublishedTime2 = {'name':'activity_published_time2', 'key':'published_time2', 'description' :'This is a published activity! bookEnd < bookStart',
                    'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-30T17:01:00.000Z', 'place' : 'anywhere',
                    'bookStart' : '2018-11-01T17:01:00.000Z', 'bookEnd' : '2018-10-01T17:01:00.000Z', 'status' : STATUS_PUBLISHED,
                    'picUrl' :'http://host.net/testSource/1.png', 'totalTickets' : 10}

activityPublishedTime3 = {'name':'activity_published_time3', 'key':'published_time3', 'description' :'This is a published activity! bookEnd > startTime',
                    'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-30T17:01:00.000Z', 'place' : 'anywhere',
                    'bookStart' : '2018-11-01T17:01:00.000Z', 'bookEnd' : '2018-12-21T17:01:00.000Z', 'status' : STATUS_PUBLISHED,
                    'picUrl' :'http://host.net/testSource/1.png', 'totalTickets' : 10}

activityPublishedTime4 = {'name':'activity_published_time4', 'key':'published_time4', 'description' :'This is a published activity! bookStart < currentTime',
                    'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-30T17:01:00.000Z', 'place' : 'anywhere',
                    'bookStart' : datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:00.000Z"), 'bookEnd' : '2018-12-21T17:01:00.000Z', 'status' : STATUS_PUBLISHED,
                    'picUrl' :'http://host.net/testSource/1.png', 'totalTickets' : 10}

activityPublishedKey = {'name':'activity_published_key', 'key':'published', 'description' :'This is a published activity! bookStart < currentTime',
                    'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-30T17:01:00.000Z', 'place' : 'anywhere',
                    'bookStart' : '2018-11-01T17:01:00.000Z', 'bookEnd' : '2018-12-01T17:01:00.000Z', 'status' : STATUS_PUBLISHED,
                    'picUrl' :'http://host.net/testSource/1.png', 'totalTickets' : 10}

activityPublishedNoTicket = {'name':'activity_published_no_ticket', 'key':'published_no_tickets', 'description' :'This is a published activity! TotalTickets=0',
                'startTime' : '2018-12-15T17:01:00.000Z', 'endTime' : '2018-12-30T17:01:00.000Z', 'place' : 'anywhere',
                'bookStart' : '2018-11-01T17:01:00.000Z', 'bookEnd' : '2018-12-01T17:01:00.000Z', 'status' : STATUS_PUBLISHED,
                'picUrl' :'http://host.net/testSource/1.png', 'totalTickets' : 0}


activitySavedSql = Activity(name ='activity_saved', key = 'saved', description = 'This is a saved activity!',place='anywhere',
                            start_time = (datetime.datetime.utcnow()+datetime.timedelta(days=20)).strftime("%Y-%m-%dT%H:%M:00.000Z"), 
                            end_time = (datetime.datetime.utcnow()+datetime.timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:00.000Z"),
                            book_start = (datetime.datetime.utcnow()+datetime.timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:00.000Z"), 
                            book_end = (datetime.datetime.utcnow()+datetime.timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:00.000Z"),
                            status= 0, pic_url='http://host.net/testSource/1.png', total_tickets = 10, remain_tickets = 10)

activityPublishedSql = Activity(name ='activity_published', key = 'published', description = 'This is a published activity!',place='anywhere',
                                start_time = (datetime.datetime.utcnow()+datetime.timedelta(days=20)).strftime("%Y-%m-%dT%H:%M:00.000Z"), 
                                end_time = (datetime.datetime.utcnow()+datetime.timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:00.000Z"),
                                book_start = (datetime.datetime.utcnow()+datetime.timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:00.000Z"), 
                                book_end = (datetime.datetime.utcnow()+datetime.timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:00.000Z"),
                                status= STATUS_PUBLISHED, pic_url='http://host.net/testSource/1.png', total_tickets = 10, remain_tickets = 10)

activityDeletedSql = Activity(name ='activity_deleted', key = 'deleted', description = 'This is a deleted activity!',place = 'anywhere',
                            start_time = (datetime.datetime.utcnow()+datetime.timedelta(days=20)).strftime("%Y-%m-%dT%H:%M:00.000Z"), 
                            end_time = (datetime.datetime.utcnow()+datetime.timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:00.000Z"),
                            book_start = (datetime.datetime.utcnow()-datetime.timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:00.000Z"), 
                            book_end = (datetime.datetime.utcnow()+datetime.timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:00.000Z"),
                            status= STATUS_DELETED, pic_url='http://host.net/testSource/1.png', total_tickets = 10, remain_tickets = 10)

activityTicketingSql = Activity(name ='activity_published1', key = 'published1', description = 'This is a published activity!',place='anywhere',
                                start_time = (datetime.datetime.utcnow()+datetime.timedelta(days=20)).strftime("%Y-%m-%dT%H:%M:00.000Z"), 
                                end_time = (datetime.datetime.utcnow()+datetime.timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:00.000Z"),
                                book_start = (datetime.datetime.utcnow()-datetime.timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:00.000Z"), 
                                book_end = (datetime.datetime.utcnow()+datetime.timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:00.000Z"),
                                status= STATUS_PUBLISHED, pic_url='http://host.net/testSource/1.png', total_tickets = 10, remain_tickets = 10)

activityTicketedSql = Activity(name ='activity_published2', key = 'published2', description = 'This is a published activity!', place = 'anywhere',
                                start_time = (datetime.datetime.utcnow()+datetime.timedelta(days=20)).strftime("%Y-%m-%dT%H:%M:00.000Z"), 
                                end_time = (datetime.datetime.utcnow()+datetime.timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:00.000Z"),
                                book_start = (datetime.datetime.utcnow()-datetime.timedelta(days=20)).strftime("%Y-%m-%dT%H:%M:00.000Z"), 
                                book_end = (datetime.datetime.utcnow()-datetime.timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:00.000Z"),
                                status= STATUS_PUBLISHED, pic_url='http://host.net/testSource/1.png', total_tickets = 10, remain_tickets = 10)

activityActingSql = Activity(name ='activity_published3', key = 'published3', description = 'This is a published activity!', place = 'anywhere',
                                start_time = (datetime.datetime.utcnow()-datetime.timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:00.000Z"), 
                                end_time = (datetime.datetime.utcnow()+datetime.timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:00.000Z"),
                                book_start = (datetime.datetime.utcnow()-datetime.timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:00.000Z"), 
                                book_end = (datetime.datetime.utcnow()-datetime.timedelta(days=20)).strftime("%Y-%m-%dT%H:%M:00.000Z"),
                                status= STATUS_PUBLISHED, pic_url='http://host.net/testSource/1.png', total_tickets = 10, remain_tickets = 10)

activityActedSql = Activity(name ='activity_published4', key = 'published4', description = 'This is a published activity!',place='anywhere',
                                start_time = (datetime.datetime.utcnow()-datetime.timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:00.000Z"), 
                                end_time = (datetime.datetime.utcnow()-datetime.timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:00.000Z"),
                                book_start = (datetime.datetime.utcnow()-datetime.timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:00.000Z"), 
                                book_end = (datetime.datetime.utcnow()-datetime.timedelta(days=20)).strftime("%Y-%m-%dT%H:%M:00.000Z"),
                                status= STATUS_PUBLISHED, pic_url='http://host.net/testSource/1.png', total_tickets = 10, remain_tickets = 10)

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
        print(response_obj['data'])
        self.assertEqual(len(response_obj['data']), 2)
        self.assertEqual(response_obj['data'][0]['name'], 'activity_saved')
        self.assertEqual(response_obj['data'][1]['name'],'activity_published')

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
        activityActingSql.save()
        activityActedSql.save()

    def test_noLogin(self):
        response = self.client.post('/api/a/activity/delete', {'id' : activitySavedSql.id})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 3)

    def test_delDeletedActivity(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/delete', {'id' : activityDeletedSql.id})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_delSavedActivity(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/delete', {'id' : activitySavedSql.id})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)

    def test_delBeforeTicketActivity(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/delete',{'id' : activityPublishedSql.id})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)
        #self.assertEqual(Activity.objects.filter(id = 2), [])

    def test_delTicketingActivity(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/delete',{'id' : activityTicketingSql.id})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)
        #self.assertEqual(Activity.objects.filter(id = 2), [])

    def test_delAfterTicketActivity(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/delete',{'id' : activityTicketedSql.id})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)
        #self.assertEqual(Activity.objects.filter(id = 2), [])


    def test_delActingActivity(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/delete',{'id' : activityActingSql.id})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)
        #self.assertEqual(Activity.objects.filter(id = 2), [])

    def test_delAfterActActivity(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/delete',{'id' : activityActedSql.id})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)
        #self.assertEqual(Activity.objects.filter(id = 2), [])

    def test_delNotExistActivity(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/delete', {'id' : 1000})
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
        print(activitySaved)
        response = self.client.post('/api/a/activity/create', activitySaved)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)

    def test_savedWrongTimeForm(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/create', activitySavedWrongTime)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

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

    def test_publishedWrongTimeForm(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/create', activityPublishedWrongTime)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

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
        response = self.client.get('/api/a/activity/detail', {'id':activitySavedSql.id})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 3)

    def test_savedActivity(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.get('/api/a/activity/detail', {'id' : activitySavedSql.id})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)

    def test_publishedActivity(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.get('/api/a/activity/detail', {'id' : activityPublishedSql.id})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)

    def test_DeletedActivity(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.get('/api/a/activity/detail', {'id' : activityDeletedSql.id})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_notExistID(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.get('/api/a/activity/detail', {'id' : 1000})
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
        activityActingSql.save()
        activityActedSql.save()

    def test_noLogin(self):
        activityEdited = copy.deepcopy(activitySaved)
        activityEdited['id']=activitySavedSql.id
        del activityEdited['key']
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 3)

    def test_editDeleted(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityTemp = Activity.objects.filter(key='deleted')[0]
        activityEdited={'id':activityTemp.id, 'place':activityTemp.place,'description':activityTemp.description,
                        'startTime':activityTemp.start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'endTime':activityTemp.end_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'bookStart':activityTemp.book_start.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'bookEnd':activityTemp.book_end.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'picUrl':activityTemp.pic_url, 'status':activityTemp.status,
                        'name':activityTemp.name, 'totalTickets':activityTemp.total_tickets}
        activityEdited['name'] = 'deletedEdit'
        #print(activityEdited)
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_editSaved(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityEdited = {'id':activitySavedSql.id, 'name':'activity_save12d', 'description' :'This i12s a saved activity!',
                          'startTime' : '2018-12-15T17:02:00.000Z', 'endTime' : '2018-12-30T17:02:00.000Z', 'place' : 'anywWQWhere',
                          'bookStart' : '2018-11-01T17:02:00.000Z', 'bookEnd' : '2018-12-01T17:02:00.000Z', 'status' : STATUS_PUBLISHED,
                          'picUrl' :'http://host.net/testSource/3.png', 'totalTickets' : 8}
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)

    def test_editSaved_noTicket(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityEdited = {'id':activitySavedSql.id, 'name':'activity_save12d', 'description' :'This i12s a saved activity!',
                          'startTime' : '2018-12-15T17:02:00.000Z', 'endTime' : '2018-12-30T17:02:00.000Z', 'place' : 'anywWQWhere',
                          'bookStart' : '2018-11-01T17:02:00.000Z', 'bookEnd' : '2018-12-01T17:02:00.000Z', 'status' : STATUS_PUBLISHED,
                          'picUrl' :'http://host.net/testSource/3.png', 'totalTickets' : 0}
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)
    
    def test_editSaved_urlInvalid(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityEdited = {'id':activitySavedSql.id, 'name':'activity_save12d', 'description' :'This i12s a saved activity!',
                          'startTime' : '2018-12-15T17:02:00.000Z', 'endTime' : '2018-12-30T17:02:00.000Z', 'place' : 'anywWQWhere',
                          'bookStart' : '2018-11-01T17:02:00.000Z', 'bookEnd' : '2018-12-01T17:02:00.000Z', 'status' : STATUS_PUBLISHED,
                          'picUrl' :'htp://host.net/testSource/3.png', 'totalTickets' : 0}
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)
    
    def test_editSaved_wrongTimeForm(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityEdited = {'id':activitySavedSql.id, 'name':'activity_save12d', 'description' :'This i12s a saved activity!',
                          'startTime' : '2018-12-15T17:02:00.000Z', 'endTime' : '2018-12-30T17:02:00.000Z', 'place' : 'anywWQWhere',
                          'bookStart' : '2018-1101T17:02:00.000Z', 'bookEnd' : '2018-12-01T17:02:00.000Z', 'status' : STATUS_PUBLISHED,
                          'picUrl' :'http://host.net/testSource/3.png', 'totalTickets' : 10}
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)
        

    def test_editPublished1(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityTemp = Activity.objects.filter(key='published')[0]
        activityEdited={'id':activityTemp.id, 'place':activityTemp.place,'description':activityTemp.description,
                        'startTime':activityTemp.start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'endTime':activityTemp.end_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'bookStart':activityTemp.book_start.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'bookEnd':activityTemp.book_end.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'picUrl':activityTemp.pic_url, 'status':activityTemp.status,
                        'name':activityTemp.name, 'totalTickets':activityTemp.total_tickets}
        activityEdited['description'] = 'ssss'
        activityEdited['url']='http://host.net/testSource/3.png'
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)

    def test_editPublished2(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityTemp = Activity.objects.filter(key='published')[0]
        activityEdited={'id':activityTemp.id, 'place':activityTemp.place,'description':activityTemp.description,
                        'startTime':activityTemp.start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'endTime':activityTemp.end_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'bookStart':activityTemp.book_start.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'bookEnd':activityTemp.book_end.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'picUrl':activityTemp.pic_url, 'status':activityTemp.status,
                        'name':activityTemp.name, 'totalTickets':activityTemp.total_tickets}
        activityEdited['name'] = 'ssss'
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_editPublished3(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityTemp = Activity.objects.filter(key='published')[0]
        activityEdited={'id':activityTemp.id, 'place':activityTemp.place,'description':activityTemp.description,
                        'startTime':activityTemp.start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'endTime':activityTemp.end_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'bookStart':activityTemp.book_start.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'bookEnd':activityTemp.book_end.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'picUrl':activityTemp.pic_url, 'status':activityTemp.status,
                        'name':activityTemp.name, 'totalTickets':activityTemp.total_tickets}
        activityEdited['place']='sssss'
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_editPublished4(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityTemp = Activity.objects.filter(key='published')[0]
        activityEdited={'id':activityTemp.id, 'place':activityTemp.place,'description':activityTemp.description,
                        'startTime':activityTemp.start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'endTime':activityTemp.end_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'bookStart':activityTemp.book_start.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'bookEnd':activityTemp.book_end.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'picUrl':activityTemp.pic_url, 'status':activityTemp.status,
                        'name':activityTemp.name, 'totalTickets':activityTemp.total_tickets}
        activityEdited['bookStart'] = '2018-09-14T17:01:00.000Z'
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_editPublished5(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityTemp = Activity.objects.filter(key='published4')[0]
        activityEdited={'id':activityTemp.id, 'place':activityTemp.place,'description':activityTemp.description,
                        'startTime':activityTemp.start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'endTime':activityTemp.end_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'bookStart':activityTemp.book_start.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'bookEnd':activityTemp.book_end.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'picUrl':activityTemp.pic_url, 'status':activityTemp.status,
                        'name':activityTemp.name, 'totalTickets':activityTemp.total_tickets}
        activityEdited['startTime']='2018-12-14T17:01:00.000Z'
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_editPublished6(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityTemp = Activity.objects.filter(key='published4')[0]
        activityEdited={'id':activityTemp.id, 'place':activityTemp.place,'description':activityTemp.description,
                        'startTime':activityTemp.start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'endTime':activityTemp.end_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'bookStart':activityTemp.book_start.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'bookEnd':activityTemp.book_end.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'picUrl':activityTemp.pic_url, 'status':activityTemp.status,
                        'name':activityTemp.name, 'totalTickets':activityTemp.total_tickets}
        activityEdited['endTime']='2018-12-29T17:01:00.000Z'
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_editPublished7(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityTemp = Activity.objects.filter(key='published3')[0]
        activityEdited={'id':activityTemp.id, 'place':activityTemp.place,'description':activityTemp.description,
                        'startTime':activityTemp.start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'endTime':activityTemp.end_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'bookStart':activityTemp.book_start.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'bookEnd':activityTemp.book_end.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
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
        activityTemp = Activity.objects.filter(key='published3')[0]
        activityEdited={'id':activityTemp.id, 'place':activityTemp.place,'description':activityTemp.description,
                        'startTime':activityTemp.start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'endTime':activityTemp.end_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'bookStart':activityTemp.book_start.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'bookEnd':activityTemp.book_end.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'picUrl':activityTemp.pic_url, 'status':activityTemp.status,
                        'name':activityTemp.name, 'totalTickets':activityTemp.total_tickets}
        activityEdited['bookEnd']='2018-09-29T17:01:00.000Z'
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)


    def test_editPublished9(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityTemp = Activity.objects.filter(key='published2')[0]
        activityEdited={'id':activityTemp.id, 'place':activityTemp.place,'description':activityTemp.description,
                        'startTime':activityTemp.start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'endTime':activityTemp.end_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'bookStart':activityTemp.book_start.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'bookEnd':activityTemp.book_end.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'picUrl':activityTemp.pic_url, 'status':activityTemp.status,
                        'name':activityTemp.name, 'totalTickets':activityTemp.total_tickets}
        activityEdited['bookEnd']='2018-09-25T17:02:10.000Z'
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)

    def test_editPublished10(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityTemp = Activity.objects.filter(key='published')[0]
        activityEdited={'id':activityTemp.id, 'place':activityTemp.place,'description':activityTemp.description,
                        'startTime':activityTemp.start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'endTime':activityTemp.end_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'bookStart':activityTemp.book_start.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'bookEnd':activityTemp.book_end.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'picUrl':activityTemp.pic_url, 'status':activityTemp.status,
                        'name':activityTemp.name, 'totalTickets':activityTemp.total_tickets}
        activityEdited['totalTickets']=9
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)

    def test_editPublished11(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityTemp = Activity.objects.filter(key='published1')[0]
        activityEdited={'id':activityTemp.id, 'place':activityTemp.place,'description':activityTemp.description,
                        'startTime':activityTemp.start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'endTime':activityTemp.end_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'bookStart':activityTemp.book_start.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'bookEnd':activityTemp.book_end.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'picUrl':activityTemp.pic_url, 'status':activityTemp.status,
                        'name':activityTemp.name, 'totalTickets':activityTemp.total_tickets}
        activityEdited['totalTickets']=9
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_editPublished12(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityTemp = Activity.objects.filter(key='published')[0]
        activityEdited={'id':activityTemp.id, 'place':activityTemp.place,'description':activityTemp.description,
                        'startTime':activityTemp.start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'endTime':activityTemp.end_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'bookStart':activityTemp.book_start.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'bookEnd':activityTemp.book_end.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'picUrl':activityTemp.pic_url, 'status':activityTemp.status,
                        'name':activityTemp.name, 'totalTickets':activityTemp.total_tickets}
        activityEdited['totalTickets']=9
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)

    def test_savedToPublished(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityTemp = Activity.objects.filter(key='saved')[0]
        activityEdited={'id':activityTemp.id, 'place':activityTemp.place,'description':activityTemp.description,
                        'startTime':activityTemp.start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'endTime':activityTemp.end_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'bookStart':activityTemp.book_start.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'bookEnd':activityTemp.book_end.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'picUrl':activityTemp.pic_url, 'status':activityTemp.status,
                        'name':activityTemp.name, 'totalTickets':activityTemp.total_tickets}
        activityEdited['status'] = STATUS_PUBLISHED
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)

    def test_publishedToSaved(self):
        self.client.post('/api/a/login', superUserCorrect)
        activityTemp = Activity.objects.filter(key='published')[0]
        activityEdited={'id':activityTemp.id, 'place':activityTemp.place,'description':activityTemp.description,
                        'startTime':activityTemp.start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'endTime':activityTemp.end_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'bookStart':activityTemp.book_start.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'bookEnd':activityTemp.book_end.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                        'picUrl':activityTemp.pic_url, 'status':activityTemp.status,
                        'name':activityTemp.name, 'totalTickets':activityTemp.total_tickets}
        activityEdited['status'] = STATUS_SAVED
        response = self.client.post('/api/a/activity/detail', activityEdited)
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)


    def tearDown(self):
        Activity.objects.all().delete()


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
        response = self.client.post('/api/a/activity/menu', {activityTicketingSql.id:activityTicketingSql.id})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 3)

    def test_addDeleted(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/menu', {activityDeletedSql.id:activityDeletedSql.id})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_addSaved(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/menu', {activitySavedSql.id:activitySavedSql.id})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_addPublishedBeforeTicket(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/menu', {activityPublishedSql.id:activityPublishedSql.id})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_addPublishedTicketing(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/menu', {activityTicketingSql.id:activityTicketingSql.id})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)

    def test_addPublishedAfterTicket(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/menu', {activityTicketedSql.id:activityTicketedSql.id})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)

    def test_addManyActivities(self):
        self.client.post('/api/a/login', superUserCorrect)
        response = self.client.post('/api/a/activity/menu', {activityTicketedSql.id: activityTicketedSql.id, activityTicketingSql.id:activityTicketingSql.id})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 2)
    
    def tearDown(self):
        Activity.objects.all().delete()

################################################################################
################################################################################

imgCorrect={'image': 'http://host.net/testSource/1.png'}
imgNotExist={'image': 'http://host.net/testSource/2.png'}

#11#############################################################################
class uploadImgTest(TestCase):
    def setUp(self):
        User.objects.create_superuser(username=superUserCorrect['username'],
                                      email=superUserCorrect['email'],
                                      password=superUserCorrect['password'])


    def test_onLogin(self):
        #imgPath = os.path.join(settings.BASE_DIR, 'http://host.net/testSource/1.png')
        with open('testSource/1.png', 'rb') as pic:
            response = self.client.post('/api/a/image/upload', {'image': pic})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 3)


    def test_success(self):
        self.client.post('/api/a/login', superUserCorrect)
        #imgPath = os.path.join(settings.BASE_DIR, 'http://host.net/testSource/1.png')
        with open('testSource/1.png', 'rb') as pic:
            response = self.client.post('/api/a/image/upload', {'image': pic})
        response_json = response.content.decode('utf-8')
        response_obj = json.loads(response_json)
        self.assertEqual(response_obj['code'], 0)

    '''
    def test_noImg(self):
        self.client.post('/api/a/login', superUserCorrect)
        #imgPath = os.path.join(settings.BASE_DIR, 'http://host.net/testSource/2.png')
        with open('testSource/2.png', 'rb') as pic:
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
                                book_start = datetime.datetime.utcnow().strftime("%Y-%m-01T00:00:00.000Z"), book_end = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:00.000Z"),
                                status= STATUS_PUBLISHED, pic_url='http://host.net/testSource/1.png', total_tickets = 10, remain_tickets = 10)

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
