from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import root_route, logout_route

urlpatterns = [
    path('', root_route),
    path('admin/', admin.site.urls),

    # For session authentication in the web browsable API interface
    path('api-auth/', include('rest_framework.urls')),

    path(
        'api-auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'api-auth/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),

    # `dj_rest_auth` provides authentication endpoints
    # the login path is typically `dj-rest-auth/login/`
    path('dj-rest-auth/', include('dj_rest_auth.urls')),

    # our logout route has to be above the default one to be matched first
    # path('dj-rest-auth/logout/', LogoutView.as_view(), name='rest_logout'),

    path(
        'dj-rest-auth/registration/',
        include('dj_rest_auth.registration.urls')
    ),
    
    path('', include('profiles.urls')),
    path('', include('posts.urls')),
    path('', include('comments.urls')),
    path('', include('likes.urls')),
    path('', include('followers.urls')),
]
