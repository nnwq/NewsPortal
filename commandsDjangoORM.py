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


Post.like(Post.objects.get(id=1))
Comment.like(Comment.objects.get(id=3))
Post.like(Post.objects.get(id=2))
Comment.like(Comment.objects.get(id=3))
Comment.like(Comment.objects.get(id=2))
Comment.like(Comment.objects.get(id=5))
Post.like(Post.objects.get(id=3))
Post.dislike(Post.objects.get(id=1))
Comment.dislike(Comment.objects.get(id=2))


Author.update_rating(Author.objects.get(id=1))
Author.update_rating(Author.objects.get(id=2))


Author.objects.all().order_by('-rating').values('user__username', 'rating')[0]


Post.objects.all().order_by('-rating').values('time_created', 'author', 'author_id', 'id', 'rating', 'object_title')
Post.preview(Post.objects.all())

Comment.objects.filter(id=1).values('comment_text', 'id', 'time_created', 'user')
