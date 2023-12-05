from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from ads.models import Categories, User, Ads, Location
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from dj_api.settings import TOTAL_ON_PAGE
from django.db.models import Avg, Count, Q
import json


def index(request):
    return HttpResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoriesListViews(ListView):
    model = Categories

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by('name')

        paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        categories = [{"id": category.id, "name": category.name} for category in self.object_list]

        response = {
            "items": categories,
            "total": paginator.num_pages,
            "per_page": paginator.count,
        }
        return JsonResponse(response, safe=False)


class CategoryDetailView(DetailView):
    model = Categories

    def get(self, request, *args, **kwargs):
        category = self.get_object()
        return JsonResponse({"id": category.id, "name": category.name})


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Categories
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Categories
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)

        category = Categories.objects.create(
            name=category_data["name"])

        return JsonResponse({
            "id": category.id,
            "text": category.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Categories
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        category_data = json.loads(request.body)
        self.object.name = category_data["name"]

        self.object.save()
        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AsdListViews(ListView):
    model = Ads

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        self.object_list = self.object_list.select_related('category_id').order_by('-price')

        ads_item = [
            {"id": ads.id, "name": ads.name, 'autor': ads.author_id.first_name,
             'price': ads.price, 'description': ads.description,
             'is_published': ads.is_published, "category": ads.category_id.name} for ads in self.object_list]

        response = {"items": ads_item, "total": paginator.num_pages, "per_page": paginator.count}

        return JsonResponse(response, safe=False)


class AdsDetailView(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        ads = self.get_object()
        return JsonResponse(
            {"id": ads.id, "name": ads.name, 'author': ads.author_id.first_name, 'price': ads.price,
             'description': ads.description, 'image': ads.image.url,
             'is_published': ads.is_published})


@method_decorator(csrf_exempt, name='dispatch')
class AdsCreateView(CreateView):
    model = Ads
    fields = ["name", "price", "description", "is_published", "category_id", "image", "author_id"]

    def post(self, request, *args, **kwargs):
        ads_data = json.loads(request.body)

        ads = Ads.objects.create(
            name=ads_data["name"],
            author_id=User(ads_data["author_id"]),
            price=ads_data["price"],
            description=ads_data["description"],
            is_published=ads_data["is_published"],
            category_id=Categories(ads_data["category_id"])
        )

        return JsonResponse({
            "id": ads.id,
            "name": ads.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdsDeleteView(DeleteView):
    model = Ads
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdsUpdateView(UpdateView):
    model = Ads
    fields = ["name", "price", "description", "is_published", "category_id", "image", "author_id"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        category_data = json.loads(request.body)
        self.object.name = category_data["name"] if category_data.get("name") else self.object.name
        self.object.author_id = User(category_data['author_id']) if category_data.get(
            "author_id") else self.object.author_id
        self.object.price = category_data['price'] if category_data.get("price") else self.object.price
        self.object.description = category_data['description'] if category_data.get(
            "description") else self.object.description
        self.object.is_published = category_data['is_published'] if category_data.get(
            "is_published") else self.object.is_published
        self.object.category_id = Categories(category_data['category_id']) if category_data.get(
            "category_id") else self.object.category_id
        self.object.image = category_data['image'].url if category_data.get(
            "image") else self.object.image

        self.object.save()

        return JsonResponse(
            {'id': self.object.id, 'name': self.object.name, 'author': self.object.author_id.first_name,
             'price': self.object.price,
             'description': self.object.description,
             'is_published': self.object.is_published,
             'image': self.object.image.url if self.object.image else None})


@method_decorator(csrf_exempt, name='dispatch')
class AdsImageView(UpdateView):
    model = Ads
    fields = ["name", "price", "description", "is_published", "category_id", "image", "author_id"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES['image']
        self.object.save()

        return JsonResponse(
            {'id': self.object.id, 'name': self.object.name, 'author': self.object.author_id.first_name,
             'price': self.object.price,
             'description': self.object.description,
             'is_published': self.object.is_published,
             'image': self.object.image.url if self.object.image.url else None})


@method_decorator(csrf_exempt, name='dispatch')
class UsersListViews(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        counted_users = User.objects.annotate(
            publications=Count('ads', filter=Q(ads__is_published=True)))

        paginator = Paginator(counted_users, TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        self.object_list = counted_users.select_related('location_id').order_by('username')

        users = [{"id": user.id, "name": user.first_name, "last_name": user.last_name, "username": user.username,
                  "password": user.password, "role": user.role, "age": user.age, "locations": user.location_id.name,
                  "total_ads": user.publications}
                 for
                 user in self.object_list]

        response = {
            "items": users,
            "total": paginator.num_pages,
            "per_page": paginator.count,
        }
        return JsonResponse(response, safe=False)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        return JsonResponse(
            {"id": user.id, "name": user.first_name, "last_name": user.last_name, "username": user.username,
             "password": user.password, "role": user.role, "age": user.age, "locations": user.location_id.name})


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ["first_name", "last_name", "username", "password", "role", "age", "location_id"]

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        user = User.objects.create(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            username=user_data["username"],
            password=user_data["password"],
            role=user_data["role"],
            age=user_data["age"],
        )
        user_obj, created = Location.objects.get_or_create(name=', '.join(user_data["locations"]),
                                                           defaults={"is_active": True})
        if created:
            user.location_id = user_obj
        user.save()

        return JsonResponse({
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "age": user.age,
            "locations": user.location_id.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ["first_name", "last_name", "username", "password", "role", "age", "location_id"]

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user_data = json.loads(request.body)
        self.object.first_name = user_data["first_name"] if user_data.get("first_name") else self.object.first_name
        self.object.last_name = user_data['last_name'] if user_data.get(
            "last_name") else self.object.last_name
        self.object.username = user_data['username'] if user_data.get("username") else self.object.username
        self.object.password = user_data['password'] if user_data.get(
            "password") else self.object.password
        self.object.role = user_data['role'] if user_data.get(
            "role") else self.object.role
        self.object.age = user_data['age'] if user_data.get(
            "age") else self.object.age
        user_obj, created = Location.objects.get_or_create(name=', '.join(user_data["locations"]),
                                                           defaults={"is_active": True})
        if created:
            self.object.location_id = user_obj
        self.object.save()

        return JsonResponse(
            {"id": self.object.id, "name": self.object.first_name, "last_name": self.object.last_name,
             "username": self.object.username,
             "password": self.object.password, "role": self.object.role, "age": self.object.age,
             "location_id": self.object.location_id.name})
