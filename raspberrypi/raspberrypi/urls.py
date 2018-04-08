"""raspberrypi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from exercises.views import (StartView, LoginUserView, LogoutUserView,
                             AddUserView, ChartView, StatisticsView, IntroView, TempView,
                             TempList, TempApiView, ContactView, Chart2View, Chart3View, Chart4View)


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^start_page/$', StartView.as_view(), name="index"),
    url(r'^intro/$', IntroView.as_view(), name="intro"),
    ###########LOGIN#########################
    url(r'^login/$', LoginUserView.as_view(),
        name="login"),
    url(r'^logout/$', LogoutUserView.as_view(),
        name="logout"),
    url(r'^add_user/$', AddUserView.as_view(),
        name="add_user"),
    url(r'^contact/$', ContactView.as_view(),
        name="contact"),
    ################TEMPERATURE######################
    url(r'^actual_temp/$', TempView.as_view(),
        name="temp"),
    url(r'^chartit/$', ChartView.as_view(),
        name="chart"),
    url(r'^chartit2/$', Chart2View.as_view(),
        name="chart2"),
    url(r'^chartit3/$', Chart3View.as_view(),
        name="chart3"),
    url(r'^chartit4/$', Chart4View.as_view(),
        name="chart4"),
    url(r'^statistics/$', StatisticsView.as_view(),
        name="statistics"),
    #####################API VIEW#####################
    url(r'^api_temps/$', TempList.as_view(),
        name="api_temps"),
    url(r'^api_temp/(?P<id>(\d)+)', TempApiView.as_view(),
        name="api_temp"),

]
