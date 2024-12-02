from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase 


# Create your tests here.
class PostListViewTests(APITestCase):
    def setUp(self):
        # create user
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


# Users can retrieve a post with valid ID,
# Users can’t retrieve a post with invalid ID,
# Users can update the posts that they own
# Users can’t update the posts that they don't own.

class PostDetailViewTests(APITestCase):
    def setUp(self):
        # create two users
        adam = User.objects.create_user(username='adam', password='pass')
        brian = User.objects.create_user(username='brian', password='pass')
        # create a post for each user
        Post.objects.create(
            owner=adam,
            title='a title', 
            content='adams content'
        )
        Post.objects.create(
            owner=brian,
            title='a title',
            content='brians conent'
        )

    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get('/posts/1/')  # retrieve post
        print(response.status_code)
        self.assertEqual(response.data['title'], 'a title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_post_using_invalid_id(self):
        response = self.client.get('/posts/999/')  # retrieve post
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_user_can_update_own_post(self):
        self.client.login(username='adam', password='pass')
        # send a put request to  a url with post’s ID
        response = self.client.put('/posts/1/', {'title': 'a new title'})
        # fetch that post  from the database by ID
        post = Post.objects.filter(pk=1).first()
        # test if the post change has been persisted
        self.assertEqual(post.title, 'a new title')
        # make sure the 200 OK code is sent to the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_post(self):
        self.client.login(username='adam', password='pass')
        # send a put request to a url with post’s ID of another user (Brian's ID=2)
        response = self.client.put('/posts/2/', {'title': 'a new title'})
        # make sure the 200 OK code is sent to the response
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

