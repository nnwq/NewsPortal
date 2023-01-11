from NewsPaper.news.models import *

User1 = User.objects.create_user('Dmitry')
User2 = User.objects.create_user('Oleg')

Author1 = Author.objects.create(user_id=1)
Author2 = Author.objects.create(user_id=2)

Category1 = Category.objects.create(category_name='Books')
Category2 = Category.objects.create(category_name='Programming')
Category3 = Category.objects.create(category_name='Travel')
Category4 = Category.objects.create(category_name='Games')

News1 = Post.objects.create(author_id=1, post_type='news')
Blog1 = Post.objects.create(author_id=1)                    # default post type is blog
Blog2 = Post.objects.create(author_id=1)

News1.category.set([Category1, Category2])
Blog1.category.set([Category4])
Blog2.category.set([Category3])

comment1 = Comment.objects.create(post_id=1, user_id=1, comment_text='Nice article, thanks!')
comment2 = Comment.objects.create(post_id=2, user_id=2, comment_text='Nice article, thanks!')
comment3 = Comment.objects.create(post_id=3, user_id=1, comment_text='Nice article, thanks!')
comment4 = Comment.objects.create(post_id=3, user_id=2, comment_text='Thank you for the news!')

comment1 = like()