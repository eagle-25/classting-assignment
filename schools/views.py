import dataclasses

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View

from common.decorators import jwt_login
from common.exceptions import ValueNotFound
from common.utils import parse_body
from schools.adapters.repos.school_repo import DjangoOrmSchoolsRepo
from schools.usecases.school_usecase import (
    create_school_news_usecase,
    create_school_usecase,
    delete_school_news_usecase,
    list_school_news_usecase,
    list_schools_usecase,
    update_school_news_usecase,
)


class SchoolView(View):
    @method_decorator(jwt_login)
    def post(self, request: HttpRequest, user_id: int) -> HttpResponse:
        """
        학교를 생성하는 API View
        """
        if (school_name := request.POST.get('school_name')) is None:
            raise ValueNotFound(detail="school_name")
        if (city := request.POST.get('city')) is None:
            raise ValueNotFound(detail="city")
        if (owner_id := request.POST.get('owner_id')) is None:
            raise ValueNotFound(detail="owner_id")
        create_school_usecase(school_repo=DjangoOrmSchoolsRepo(), owner_id=int(owner_id), name=school_name, city=city)
        return HttpResponse(status=201)

    @method_decorator(jwt_login)
    def get(self, request: HttpRequest, user_id: int) -> HttpResponse:
        """
        owner가 가지는 학교들을 조회하는 API View
        """
        if (owner_id := request.GET.get('owner_id')) is None:
            raise ValueNotFound(detail="owner_id")
        schools = list_schools_usecase(school_repo=DjangoOrmSchoolsRepo(), owner_id=int(owner_id))
        schools = [dataclasses.asdict(school) for school in schools]
        return JsonResponse(data={'schools': schools}, status=200)


class SchoolNewsView(View):
    @method_decorator(jwt_login)
    def post(self, request: HttpRequest, user_id: int, school_id: int) -> HttpResponse:
        """
        학교 소식을 생성하는 API View
        """
        if (content := request.POST.get('content')) is None:
            raise ValueNotFound(detail="content")
        school_repo = DjangoOrmSchoolsRepo()
        create_school_news_usecase(school_repo=school_repo, owner_id=user_id, school_id=school_id, content=content)
        return HttpResponse(status=201)

    @method_decorator(jwt_login)
    def get(self, request: HttpRequest, user_id: int, school_id: int) -> HttpResponse:
        """
        학교별 소식들을 조회하는 API View
        """
        school_news = list_school_news_usecase(school_repo=DjangoOrmSchoolsRepo(), school_id=int(school_id))
        school_news = [dataclasses.asdict(news) for news in school_news]
        return JsonResponse(data={'school_news': school_news}, status=200)

    @method_decorator(jwt_login)
    def patch(self, request: HttpRequest, user_id: int, news_id: int) -> HttpResponse:
        """
        학교 소식을 수정하는 API View. 필드 추가되는 경우 대비해 patch로 구현
        """
        body = parse_body(request)
        if (content := body.get('content')) is None:
            raise ValueNotFound(detail="content")
        school_repo = DjangoOrmSchoolsRepo()
        res = update_school_news_usecase(school_repo=school_repo, owner_id=user_id, news_id=news_id, content=content)
        return JsonResponse(data=dataclasses.asdict(res), status=200)

    @method_decorator(jwt_login)
    def delete(self, request: HttpRequest, user_id: int, news_id: int) -> HttpResponse:
        """
        학교 소식을 삭제하는 API View
        """
        school_repo = DjangoOrmSchoolsRepo()
        delete_school_news_usecase(school_repo=school_repo, owner_id=user_id, news_id=news_id)
        return HttpResponse(status=204)
