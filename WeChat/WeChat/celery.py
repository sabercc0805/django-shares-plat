import os
from celery import Celery
from django.conf import settings

# 设置celery的环境变量和django-celery的工作目录
os.environ.setdefault("DJANGO_SETTINGS_MODULE","WeChat.settings")
# 实例化celery应用，传入服务器名称
app = Celery("WeChat",broker='redis://127.0.0.1:6379/0',include=['User.tasks','User.wechatpay'])#include重点
# 加载celery配置
app.config_from_object("django.conf:settings")

# 如果在项目中，创建了task.py,那么celery就会沿着app去查找task.py来生成任务
app.autodiscover_tasks(lambda :settings.INSTALLED_APPS)

from datetime import timedelta
from celery.schedules import crontab
#定时任务
app.conf.beat_schedule = {
    'add_spread_entry': {
        'task': 'User.tasks.spread_entry',          #项目地址/脚本.方法
        #'schedule': timedelta(seconds=10),
        'schedule': crontab(hour=9, minute=0),             #每天早8点执行该命令
    },
    'add_wechat_payment': {
        'task': 'User.tasks.excutetaskcash',  # 任务名
        'schedule': timedelta(seconds=2),
    },

    'add_wechat_paycheck': {
        'task': 'User.tasks.excutetaskresearch',  # 任务名
        'schedule': timedelta(minutes=10),
    },
    'add_recoverdaytimes': {
        'task': 'User.tasks.recovertaskdaytimes',          #项目地址/脚本.方法
        'schedule': crontab(hour=9, minute=0),             #每天早9点执行该命令
    },
    'add_recovermonthtimes': {
        'task': 'User.tasks.recovertaskmonthtimes',          #项目地址/脚本.方法
        'schedule': crontab(hour=9, minute=0,day_of_month=1),   #每月1日早9点执行该命令
    },
    'add_recoverappstate': {
        'task': 'User.tasks.recovertaskappstate',          #项目地址/脚本.方法
         'schedule': crontab(hour=0, minute=0),   #每天早0点执行该命令
    },
    'update_plat_tocken': {
        'task': 'User.tasks.get_task_plattocken',  # 更新第三方平台tocken，1分钟查一次，失效或没有直接更新，其次100分钟更新一次
        'schedule': timedelta(minutes=1),
    },
}

if __name__ == '__main__':
    app.start()
'''
app.conf.update(
CELERY_BEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'tasks.add',       #任务名
        'schedule':timedelta(seconds=1), #每一秒执行一次该任务
    },
}
)
'''

