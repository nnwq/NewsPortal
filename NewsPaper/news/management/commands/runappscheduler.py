import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from apscheduler.jobstores.base import BaseJobStore
from django_apscheduler.models import DjangoJobExecution
from django.db.models import Q
from datetime import date, timedelta
from NewsPaper.news.models import Post, SubscribedUsers, User
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

logger = logging.getLogger(__name__)

def inform_for_new_posts():
    #  Your job processing logic here...
    print('News in a week')
    date_from = date.today()-timedelta(days=8)
    date_to = date.today()-timedelta(days=1)
    post_source = Post.objects.filter(Q(creation__gte=date_from) & Q(creation__lt=date_to))
    users = SubscribedUsers.objects.all().values('user_id').distinct()
    title = f'News in a week'

    for i in range(users.count()):
        categories = SubscribedUsers.objects.filter(user_id=users[i]['user_id']).values('category_id', 'category_id__name')
        user = User.objects.filter(id=users[i]['user_id']).values('first_name', 'last_name', 'username', 'email')
        user_name = f"{user[0]['first_name']} {user[0]['last_name']} ({user[0]['username']})"
        for c in range(categories.count()):
            category_name = categories[c]['category_id__name']
#            print(user)
#            print(category_name)
            posts = post_source.filter(category__id=categories[c]['category_id'])
            if posts.count() == 0:
                continue
#            print(posts)
            html_content = render_to_string(
                        'post_digest.html',
                        {
                            'date_from': date_from,
                            'date_to': date_to,
                            'title': title,
                            'user': user_name,
                            'category': category_name,
                            'posts': posts,
                            'url_start': 'http://127.0.0.1:8000/',
                        }
                    )

            msg = EmailMultiAlternatives(
                subject=title,
                body=f'News in a week from {date_from} to {date_to}.',
                from_email='dmitrypomishin@gmail.com',
                to=[user[0]['email']]
            )

            msg.attach_alternative(html_content, "text/html")
            msg.send()

    print('Email send finished')


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs NEW POST INFORMER."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(BaseJobStore(), "default")

        scheduler.add_job(
            inform_for_new_posts,
            trigger=CronTrigger(week="*/1"),
            id="Post Informer",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'New posts informer'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")