'''
并发测试的收尾工作
'''
import os
import sys
import django

pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, pathname)
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'WeChatTicket.settings')

django.setup()

from wechat.models import User,Activity,Ticket

if __name__ == '__main__':
    User.objects.all().delete()
    Activity.objects.all().delete()
    Ticket.objects.all().delete()