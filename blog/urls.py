from . import views
from django.urls import path

urlpatterns = [
    path('', views.HomeView, name='home'),
    path('index/', views.PostList.as_view(), name='post_list'),
    path('post/<int:pk>', views.DetailPostView.as_view(), name='post_detail'),
    path('post-like/<int:pk>', views.PostLike, name="post_like"),
    path('post/<int:pk>/comment/', views.AddComment, name='add_comment'),
    path('add_post/', views.AddPostView.as_view(), name='add_post'),
    path('post/edit/<int:pk>', views.UpdatePostView.as_view(), name='update_post'),
    path('post/<int:pk>/remove', views.DeletePostView.as_view(), name='delete_post'),
    # path('add_category/', views.AddCategoryView.as_view(), name='add_category'),
    path('category/<slug:tag_slug>/', views.TagView, name='tags'),
    # path('search/', views.SearchResultsView.as_view(), name='search_results'),
    path('searchbar/', views.SearchBar, name='search_bar'),


]
