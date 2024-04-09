from django.core.cache import cache
from django.db import IntegrityError

from common import settings
from schools.domain.commands import SearchSchoolsCmd
from schools.domain.entities import SchoolNewsEntity
from schools.domain.exceptions import (
    SchoolAlreadyExists,
    SchoolNewsNotFound,
    SchoolNotFound,
)
from schools.domain.interfaces import ISchoolRepo
from schools.domain.values import SchoolDTO
from schools.models import SchoolNews, Schools


class DjangoOrmSchoolsRepo(ISchoolRepo):
    def create_school(self, owner_id: int, school_name: str, city: str) -> None:
        """
        학교를 생성한다.
        """
        try:
            Schools.objects.create(owner_id=owner_id, name=school_name, city=city)
        except IntegrityError:
            raise SchoolAlreadyExists

    def search_schools(self, cmd: SearchSchoolsCmd) -> list[SchoolDTO]:
        """
        조건에 맞는 학교를 검색한다. id 기준 오름차순으로 정렬한다.
        """
        schools = Schools.objects.all()
        if cmd.school_name:
            schools = schools.filter(name__icontains=cmd.school_name)
        if cmd.city:
            schools = schools.filter(city__icontains=cmd.city)
        if cmd.owner_id:
            schools = schools.filter(owner_id=cmd.owner_id)
        return [school.to_dto() for school in schools]

    def list_schools(self, user_id: int) -> list[SchoolDTO]:
        """
        유저가 소유한 학교 목록을 반환한다.
        """
        return [x.to_dto() for x in Schools.objects.filter(owner_id=user_id)]

    def create_school_news(self, school_id: int, content: str) -> None:
        """
        학교 소식을 생성한다.
        """
        news = SchoolNews(school_id=school_id, content=content)
        news.save()

        cache_key = settings.SCHOOL_NEWS_LIST_CACHE_KEY.format(school_id)
        if (cached_news := cache.get(cache_key)) is not None:

            cache_news = {news.id: news.to_entity(), **cached_news}
            cache.set(cache_key, cache_news)

    def list_school_news(self, school_id: int) -> list[SchoolNewsEntity]:
        """
        학교의 소식을 최신순으로 반환한다..
        """
        try:
            school = Schools.objects.get(id=school_id)
        except Schools.DoesNotExist:
            raise SchoolNotFound

        cache_key = settings.SCHOOL_NEWS_LIST_CACHE_KEY.format(school_id)
        if (school_news := cache.get(cache_key)) is None:
            news = {x.id: x.to_entity() for x in SchoolNews.objects.filter(school=school).order_by('-id')}
            cache.set(cache_key, news)
            return list(news.values())
        else:
            return list(school_news.values())

    def update_school_news(self, news_id: int, content: str) -> SchoolNewsEntity:
        """
        학교 소식의 내용을 수정한다.
        """
        try:
            news = SchoolNews.objects.get(id=news_id)
            news.content = content
            news.save()
        except SchoolNews.DoesNotExist:
            raise SchoolNotFound

        cache_key = settings.SCHOOL_NEWS_LIST_CACHE_KEY.format(news.school.id)
        if (cache_news := cache.get(cache_key)) is not None:
            cache_news[news_id] = news.to_entity()
            cache.set(cache_key, cache_news)

        return news.to_entity()

    def delete_school_news(self, news_id: int) -> None:
        """
        학교 소식을 삭제한다.
        """
        try:
            news = SchoolNews.objects.get(id=news_id)
            news.delete()
        except SchoolNews.DoesNotExist:
            raise SchoolNotFound

        cache_key = settings.SCHOOL_NEWS_LIST_CACHE_KEY.format(news.school.id)
        if (cache_news := cache.get(cache_key)) is not None:
            cache_news.pop(news_id)
            cache.set(cache_key, cache_news)

    def is_owned_news(self, owner_id: int, news_id: int) -> bool:
        """
        학교 소식이 유저의 것인지 확인한다.
        """
        try:
            news: SchoolNews = SchoolNews.objects.get(id=news_id)
        except SchoolNews.DoesNotExist:
            raise SchoolNewsNotFound
        return news.school.owner.id == owner_id

    def is_owned_school(self, owner_id: int, school_id: int) -> bool:
        """
        학교가 유저의 것인지 확인한다.
        """
        try:
            school: Schools = Schools.objects.get(id=school_id)
        except Schools.DoesNotExist:
            raise SchoolNotFound
        return school.owner.id == owner_id
