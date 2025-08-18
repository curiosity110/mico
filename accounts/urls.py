from django.urls import path

from accounts.views import (
    GetMeView,
    LoginView,
    RefreshTokenView,
    UsersListView,
    GetMeOrdersView, GroupsListView, CreateUserView, UsersDeleteView, UpdateUserGroupsView,
)

urlpatterns = [
    path("auth/login/", LoginView.as_view(), name="token_obtain_pair"),
    path("auth/refresh-token/", RefreshTokenView.as_view(), name="token_refresh"),
    path("me/", GetMeView.as_view(), name="get_me"),
    path("me/orders/", GetMeOrdersView.as_view(), name="get_me_orders"),
    path("users/", UsersListView.as_view(), name="users_list"),
    path("groups/", GroupsListView.as_view(), name="groups_list"),
    path("users/create/", CreateUserView.as_view(), name="create_user"),
    path("users/<int:pk>/", UsersDeleteView.as_view(), name="delete_user"),
    path("users/<int:pk>/groups/", UpdateUserGroupsView.as_view(), name="update_user_permissions"),

]
