from django.db import IntegrityError

from schools.domain.entities import SchoolEntity, SchoolNewsEntity
from schools.domain.exceptions import (
    SchoolCreateFailed,
    SchoolNewsNotFound,
    SchoolNotFound,
)
from schools.domain.interfaces import ISchoolRepo
from schools.models import SchoolNews, Schools


class DjangoOrmSchoolsRepo(ISchoolRepo):
    def create_school(self, entity: SchoolEntity) -> None:
        try:
            Schools.from_entity(entity=entity).save()
        except IntegrityError:
            raise SchoolCreateFailed(detail="Already exists")

    def list_school(self, owner_id: int) -> list[SchoolEntity]:
        try:
            return [x.to_entity() for x in Schools.objects.filter(owner_id=owner_id).order_by('id')]
        except Schools.DoesNotExist:
            raise SchoolNotFound

    def create_school_news(self, entity: SchoolNewsEntity) -> None:
        SchoolNews.from_entity(entity=entity).save()

    def list_school_news(self, school_id: int) -> list[SchoolNewsEntity]:
        return [x.to_entity() for x in SchoolNews.objects.filter(school_id=school_id).order_by('-id')]

    def update_school_news(self, news_id: int, content: str) -> SchoolNewsEntity:
        try:
            news = SchoolNews.objects.get(id=news_id)
            news.content = content
            news.save()
            return news.to_entity()
        except SchoolNews.DoesNotExist:
            raise SchoolNotFound

    def delete_school_news(self, news_id: int) -> None:
        try:
            SchoolNews.objects.get(id=news_id).delete()
        except SchoolNews.DoesNotExist:
            raise SchoolNotFound

    def is_owned_news(self, owner_id: int, news_id: int) -> bool:
        try:
            news: SchoolNews = SchoolNews.objects.get(id=news_id)
        except SchoolNews.DoesNotExist:
            raise SchoolNewsNotFound
        return news.school.owner.id == owner_id

    def is_owned_school(self, owner_id: int, school_id: int) -> bool:
        try:
            school: Schools = Schools.objects.get(id=school_id)
        except Schools.DoesNotExist:
            raise SchoolNotFound
        return school.owner.id == owner_id
