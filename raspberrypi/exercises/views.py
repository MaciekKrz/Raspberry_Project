from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, AddUserForm
from .models import TemperatureReading
from chartit import DataPool, Chart
from .serializers import TempSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.db.models import Max, Min, Avg
from datetime import timedelta
from django.utils import timezone


class StartView(View):

    def get(self, request):

        return render(request,
                      template_name="base.html")


class IntroView(View):
        def get(self, request):
            return render(request,
                          template_name="intro.html")


#######################LOGIN######################################


class LoginUserView(View):
    def get(self, request):
        form = LoginForm()
        ctx = {
            "form": form
        }
        return render(
            request,
            "login.html",
            ctx
        )

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse("Loged")
            else:
                return HttpResponse("Try again")


class LogoutUserView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return redirect(reverse("index"))


class AddUserView(View):
    def get(self, request):
        form = AddUserForm()
        ctx = {
            'form': form
        }
        return render(
            request,
            "add_user.html",
            ctx
        )

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            if User.objects.filter(username=login).exists():
                form.add_error('login', "Taki login jest już zajęty")
            if password != password2:
                form.add_error('password', "Hasło musi być identyczne")
            if not form.errors:
                User.objects.create_user(login,
                                         email,
                                         password,
                                         first_name=first_name,
                                         last_name=last_name)
                return HttpResponse("Udało utworzyć się nowego użytkownika")
        ctx = {
            'form': form
        }
        return render(
            request,
            "add_user.html",
            ctx
        )


class ContactView(View):
    def get(self, request):
        return render(
            request,
            "contact.html",
        )
####################################END-LOGIN#################################################

####################################TEMPERATURE###############################################


class TempView(View):
    def get(self, request):

        last_temp = TemperatureReading.objects.last()

        ctx = {
            'last_temp': last_temp
        }
        return render(
            request,
            "actual_temp.html",
            ctx
        )

##############################CHARTS ###################################################


class ChartView(View):

    def get(self, request):
        # Step 1: Create a DataPool with the data we want to retrieve.

        all_filter = TemperatureReading.objects.all()

        weatherdata = \
            DataPool(
                series=
                [{'options': {
                    'source': all_filter},
                    'terms': [
                        'creation_date',
                        'tempC',
                        'tempF']}
                ])

        # Step 2: Create the Chart object
        #Celsius Chart
        chart_1 = Chart(
            datasource=weatherdata,
            series_options=
            [{'options': {
                'type': 'line',
                'stacking': False},
                'terms': {
                    'creation_date': [
                        'tempC']
                }}],
            chart_options=
            {'title': {
                'text': 'Temperature measurment in °C'},
                'xAxis': {
                    'title': {
                        'text': 'Date'}}})
        #Fahrenheit Chart
        chart_2 = Chart(
            datasource=weatherdata,
            series_options=
            [{'options': {
                'type': 'line',
                'stacking': False},
                'terms': {
                    'creation_date': [
                        'tempF']
                }}],
            chart_options=
            {'title': {
                'text': 'Temperature measurment in °F'},
                'xAxis': {
                    'title': {
                        'text': 'Date'}}})

        ctx = {
            'chart_list': [chart_1, chart_2]
        }

        # Step 3: Send the chart object to the template.
        return render(
            request,
            "chart.html",
            ctx
        )
##################Cahrt in one HOURS ########################################
class Chart2View(View):
    def get(self, request):

        # Step 1: Create a DataPool with the data we want to retrieve.
        this_hour = timezone.localtime(timezone.now()).replace(minute=0, second=0, microsecond=0)
        one_hour_earlier = this_hour - timedelta(hours=1)
        hour_filter = TemperatureReading.objects.filter(creation_date__range=(one_hour_earlier, this_hour))

        weatherdata2 = \
            DataPool(
                series=
                [{'options': {
                    'source': hour_filter},
                    'terms': [
                        'creation_date',
                        'tempC',
                        'tempF']}
                ])

        # Celsius Chart One Hour
        chart2_1 = Chart(
            datasource=weatherdata2,
            series_options=
            [{'options': {
                'type': 'line',
                'stacking': False},
                'terms': {
                    'creation_date': [
                        'tempC']
                }}],
            chart_options=
            {'title': {
                'text': 'Temperature measurment in °C'},
                'xAxis': {
                    'title': {
                        'text': 'Date'}}})

        ctx = {
            'chart_list': chart2_1
        }

        # Step 3: Send the chart object to the template.
        return render(
            request,
            "chart2.html",
            ctx
        )
# #######################CHART IN SEVEN HOURS##########################################
class Chart3View(View):

    def get(self, request):

        this_hour = timezone.localtime(timezone.now()).replace(minute=0, second=0, microsecond=0)
        seven_hour_earlier = this_hour - timedelta(hours=7)
        seven_filter = TemperatureReading.objects.filter(creation_date__range=(seven_hour_earlier, this_hour))

        weatherdata3 = \
            DataPool(
                series=
                [{'options': {
                    'source': seven_filter},
                    'terms': [
                        'creation_date',
                        'tempC',
                        'tempF']}
                ])

        # Celsius Chart Seven Hour
        chart3_1 = Chart(
            datasource=weatherdata3,
            series_options=
            [{'options': {
                'type': 'line',
                'stacking': False},
                'terms': {
                    'creation_date': [
                        'tempC']
                }}],
            chart_options=
            {'title': {
                'text': 'Temperature measurment in °C'},
                'xAxis': {
                    'title': {
                        'text': 'Date'}}})

        ctx = {
            'chart_list': chart3_1
        }

        # Step 3: Send the chart object to the template.
        return render(
            request,
            "chart3.html",
            ctx
        )

# ########################CHART IN ONE DAY #####################################################
class Chart4View(View):

    def get(self, request):
        this_hour = timezone.localtime(timezone.now()).replace(minute=0, second=0, microsecond=0)
        one_day_earlier = this_hour - timedelta(hours=24)
        day_filter = TemperatureReading.objects.filter(creation_date__range=(one_day_earlier, this_hour))

        weatherdata4 = \
            DataPool(
                series=
                [{'options': {
                    'source': day_filter},
                    'terms': [
                        'creation_date',
                        'tempC',
                        'tempF']}
                ])
        # Celsius Chart in One Day
        chart4_1 = Chart(
            datasource=weatherdata4,
            series_options=
            [{'options': {
                'type': 'line',
                'stacking': False},
                'terms': {
                    'creation_date': [
                        'tempC']
                }}],
            chart_options=
            {'title': {
                'text': 'Temperature measurment in °C'},
                'xAxis': {
                    'title': {
                        'text': 'Date'}}})

        ctx = {
            'chart_list': chart4_1
        }
        # Step 3: Send the chart object to the template.
        return render(
            request,
            "chart4.html",
            ctx
        )

########################################StatisticsView################################################

class StatisticsView(View):

    def get(self, request):
        return render(
            request,
            "statistics11.html",
        )

    def post(self, request):
        if request.POST.get("date"):
            date = request.POST['date']
            all_temp = TemperatureReading.objects.filter(creation_date__contains=date)
            if all_temp:
                try:
                    average = all_temp.aggregate(Avg('tempC'))['tempC__avg']
                    max_temp = all_temp.aggregate(Max('tempC'))['tempC__max']
                    min_temp = all_temp.aggregate(Min('tempC'))['tempC__min']
                    amplitude = max_temp - min_temp
                except [TypeError, ValueError]:
                    return HttpResponse("Saved")
                ctx = {
                    'average': average,
                    'max_temp': max_temp,
                    'min_temp': min_temp,
                    'amplitude': amplitude
                }
                return render(
                    request,
                    "statistics11.html",
                    ctx
                )
            else:
                return HttpResponse("No measurements in this day")


###################################API VIEW ################################################33

class TempList(APIView):

    def get(self, request, format=None):
        temps = TemperatureReading.objects.all()
        serializer = TempSerializer(temps, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TempSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TempApiView(APIView):

    def get_object(self, pk):
        try:
            return TemperatureReading.objects.get(pk=pk)
        except TemperatureReading.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        temp = self.get_object(id)
        serializer = TempSerializer(temp, context={"request": request})
        return Response(serializer.data)

    def delete(self, request, id, format=None):
        book = self.get_object(id)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id, format=None):
        temp = self.get_object(id)
        serializer = TempSerializer(temp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, id, format=None):
        pass