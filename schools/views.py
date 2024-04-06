import dataclasses

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View

from common.decorators import jwt_login
from common.exceptions import ValueNotFound
from schools.adapters.repos.django_school_repo import DjangoOrmSchoolsRepo
from schools.usecases.school_usecase import create_school_usecase, list_schools_usecase


class SchoolView(View):
    @method_decorator(jwt_login())
    def post(self, request: HttpRequest, user_id: int):
        if (name := request.POST.get('name')) is None:
            raise ValueNotFound(detail="name")
        if (city := request.POST.get('city')) is None:
            raise ValueNotFound(detail="city")
        if (owner_id := request.POST.get('owner_id')) is None:
            raise ValueNotFound(detail="owner_id")
        create_school_usecase(school_repo=DjangoOrmSchoolsRepo(), owner_id=int(owner_id), name=name, city=city)
        return HttpResponse(status=201)

    @method_decorator(jwt_login())
    def get(self, request: HttpRequest, user_id: int):
        if (owner_id := request.GET.get('owner_id')) is None:
            raise ValueNotFound(detail="owner_id")
        schools = list_schools_usecase(school_repo=DjangoOrmSchoolsRepo(), owner_id=int(owner_id))
        schools = [dataclasses.asdict(school) for school in schools]
        return JsonResponse(data={'schools': schools}, status=200)
