from django.contrib import admin
from django.urls import path, include  # new

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('account/', include('django.contrib.auth.urls')),
    path('account/', include('account.urls')),

]