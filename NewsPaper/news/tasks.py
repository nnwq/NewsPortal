from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from datetime import date, timedelta
from models import Post, SubscribedUsers
from django.db.models import Q


@shared_task
def send_email_to_subscribers(user, category, title, text, receivers_id, url):
    for _ in receivers_id:
        to_send = User.objects.filter(id=_['user_id']).values('first_name', 'last_name', 'username', 'email')
        html_content = render_to_string(
            'news_created.html',
            {
                    'title': title,
                    'text': text,
                    'cur_user': user,
                    'category': category,
                    'url': url,
                    'user': f"{to_send[0]['first_name']} {to_send[0]['last_name']} ({to_send[0]['username']})"
            }
        )
        msg = EmailMultiAlternatives(
                subject=title,
                body=text[:50],
                from_email='dmitrypomishin@gmail.com',
                to=[to_send[0]['email']],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return


@shared_task()
def send_email_every_week():
    print('')
    date_from = date.today()-timedelta(days=8)
    date_to = date.today()-timedelta(days=1)
    post_source = Post.objects.filter(Q(creation__gte=date_from) & Q(creation__lt=date_to))
    users = SubscribedUsers.objects.all().values('user_id').distinct()
    title = f''

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
#            print(html_content)
            msg = EmailMultiAlternatives(
                subject=title,
                body=f'New posts from {date_from} по {date_to}.',
                from_email='dmitrypomishin@gmail.com',
                to=[user[0]['email']],
            )

            msg.attach_alternative(html_content, "text/html")
            msg.send()

    print('Mailing finished')
