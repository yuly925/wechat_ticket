
# -*- coding: utf-8 -*-
#
from django.conf.urls import url

from adminpage.views import *


__author__ = "Epsirom"


urlpatterns = [
    url(r'^login?$', Login.as_view()),
    url(r'^logout?$', Logout.as_view()),
    url(r'^activity/list?$', Activitylist.as_view()),
    url(r'^activity/delete?$', Activitydelete.as_view()),
    url(r'^activity/create?$', Createactivity.as_view()),
    url(r'^image/upload?$', Imageupload.as_view()),
    url(r'^activity/detail?$', Activitydetail.as_view()),
    url(r'^activity/menu?$', Activitymenu.as_view()),
    url(r'^activity/checkin?$', Activitycheckin.as_view()),
]
