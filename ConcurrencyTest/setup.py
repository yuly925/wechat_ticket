'''
在数据库中生成初始用户和活动,用于并发测试
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

    # 生成100个用户，将其写入数据库，并将openid写入本地文件
    f = open("user.csv", "w")
    for i in range(10000,20000):
        user = User(open_id=str(i),student_id=str(i))
        user.save()
        f.write(str(i))
        f.write("\n")
    f.close()

    # 生成一个活动
    picUrl = "http://pic14.nipic.com/20110605/1369025_165540642000_2.jpg"
    activitySql = Activity(name='activity_published', key='1',
                           description='The booking is available now!',
                           start_time='2018-12-15T17:01:00.000Z', end_time='2018-12-30T17:01:00.000Z',
                           place='anywhere',
                           book_start='2018-10-01T17:01:00.000Z', book_end='2018-12-15T17:01:00.000Z',
                           status=1, pic_url=picUrl, total_tickets=1000, remain_tickets=1000)
    activitySql.save()

