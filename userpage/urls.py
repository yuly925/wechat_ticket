# -*- coding: utf-8 -*-
#
from django.conf.urls import url

from userpage.views import *


__author__ = "Epsirom"


urlpatterns = [
    url(r'^user/bind/?$', UserBind.as_view()),
    url(r'^activity/detail/?$', activityDetail.as_view()),
    url(r'^ticket/detail/?$', ticketDetail.as_view()),
]
