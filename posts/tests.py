from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase 


# Create your tests here.
class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='adam', password='pass')

    # Test if users can list posts present in the database.
    def test_can_list_posts(self):
        adam = User.objects.get(username='adam')
        Post.objects.create(owner=adam, title='title')
        # make a  get request to ‘/posts’ to list all the posts.
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    # Test if a looged in user can create a post
    def test_logged_in_user_can_create_post(self):
        self.client.login(username='adam', password='pass')
        # make a post requests to '/posts/'
        response = self.client.post('/posts/', {'title': 'a title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Test a logget out user cannot create a post
    def test_user_not_logged_in_cant_reate_post(self):
        response = self.client.post('/posts/', {'title': 'a title'})
        # Firts, make the test fail: status.HTTP_200_OK
        # Then, fix the test to make it pass
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
