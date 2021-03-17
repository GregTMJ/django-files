from django.db import models
from BackEndNewsPaper import Author, Category, Post, PostCategory, Comment
from django.contrib.auth.models import User

#Create 2 Users
user_1 = User.objects.create_user(username='niceone', email='django_master@django.com',
                                  password='NiceOne1')
user_2 = User.objects.create_user(username='leavemealone', email='something@django.com',
                                  password='noammo1')

#Create 2 Authors
Author_1 = Author.objects.create(author=user_1)
Author_2 = Author.objects.create(author=user_2)

#Add 4 categories
Category_1 = Category.objects.create(category_name = 'category 1')
Category_2 = Category.objects.create(category_name='category 2')
Category_3 = Category.objects.create(category_name='category 3')
Category_4 = Category.objects.create(category_name='category 4')

#Add 2 articles and news

article1 = Post.objects.create(author=Author_1,
                               post_type=Post.article,
                               post_title='Title 1',
                               post_content='Text 1',
                               )
article2 = Post.objects.create(author=Author_1,
                               post_type=Post.article,
                               post_title='Title 2',
                               post_content='Text 2',
                               )
news1 = Post.objects.create(author=Author_2,
                            post_type=Post.news,
                            post_title='Title 1',
                            post_content='Text 1',
                            )

article1.post_category.add(Category_1)
article1.post_category.add(Category_2)
article2.post_category.add(Category_3)
news1.post_category.add(Category_4)


comment1 = Comment.objects.create(post=article1,
                                  user=user_1,
                                  comment_text='comment 1')
comment2 = Comment.objects.create(post=article1,
                                  user=user_2,
                                  comment_text='comment 2')
comment3 = Comment.objects.create(post=article2,
                                  user=user_1,
                                  comment_text='comment 3')
comment4 = Comment.objects.create(post=news1,
                                  user=user_2,
                                  comment_text='comment 4')

comment1.like()
comment2.like()
comment3.like()
comment4.like()
comment1.like()
comment2.like()
comment3.like()
comment1.like()
comment2.like()
comment1.like()
comment1.dislike()
comment4.dislike()
comment3.dislike()
comment1.dislike()
article1.like()
article1.like()
article1.like()
article1.like()
article1.like()
article2.like()
article2.like()
article2.like()
news1.dislike()

Author_1.update_rating()
Author_2.update_rating()

Post.objects.all().values('author', 'post_title')
Post.objects.filter(author=Author_2)
Post.objects.filter(post_title='Title 1').values('author')
Comment.objects.filter(post=article1).values('comment_text')
Comment.objects.filter(comment_text='comment 2').values('comment_rating')
Author.objects.filter(id=1)
Author.objects.all().values('author', 'id')
Comment.objects.all().values('post', 'user')
