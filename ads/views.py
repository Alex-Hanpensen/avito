from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ads.models import Ads, Categories
from django.views import View
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
import json


def index(request):
    return HttpResponse({"status": "ok"})


@method_decorator(csrf_exempt, name='dispatch')
class CategoriesViews(View):
    def get(self, request):
        categories = Categories.objects.all()
        response = [{"id": cat.id, "name": cat.name} for cat in categories]
        return JsonResponse(response, safe=False)

    def post(self, request):
        categories_data = json.loads(request.body)
        categories = Categories()
        categories.name = categories_data['name']
        categories.save()
        return JsonResponse({"id": categories.id, "name": categories.name})


@method_decorator(csrf_exempt, name='dispatch')
class AsdViews(View):
    def get(self, request):
        ads_all = Ads.objects.all()
        response = [
            {"id": ads.id, "name": ads.name, 'author': ads.author, 'price': ads.price, 'description': ads.description,
             'address': ads.address, 'is_published': ads.is_published} for ads in ads_all]
        return JsonResponse(response, safe=False)

    def post(self, request):
        ads_data = json.loads(request.body)
        ads = Ads()
        ads.name = ads_data['name']
        ads.author = ads_data['author']
        ads.price = ads_data['price']
        ads.description = ads_data['description']
        ads.address = ads_data['address']
        ads.is_published = ads_data['is_published']
        ads.save()
        return JsonResponse(
            {"id": ads.id, "name": ads.name, 'author': ads.author, 'price': ads.price, 'description': ads.description,
             'address': ads.address, 'is_published': ads.is_published})


class CategoryDetailView(DetailView):
    model = Categories

    def get(self, request, *args, **kwargs):
        category = self.get_object()
        return JsonResponse({"id": category.id, "name": category.name})


class AdsDetailView(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        ads = self.get_object()
        return JsonResponse(
            {"id": ads.id, "name": ads.name, 'author': ads.author, 'price': ads.price, 'description': ads.description,
             'address': ads.address, 'is_published': ads.is_published})
