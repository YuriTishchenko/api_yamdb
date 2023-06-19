from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CommentViewSet, ReviewViewSet, UserViewSet, signup, token

app_name = 'api'

router_v1 = DefaultRouter()


router_v1.register(
    r'titles/(?P<title_id>[\d]+)/reviews', ReviewViewSet, basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet,
    basename='comment'
)
router_v1.register(
    'users',
    UserViewSet,
    basename='users'
)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', signup),
    path('v1/auth/token/', token),
]
