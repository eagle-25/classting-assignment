from django.db import IntegrityError

from schools.domain.entities import SchoolEntity
from schools.domain.exceptions import SchoolCreateFailed, SchoolNotFound
from schools.domain.interfaces import ISchoolRepo
from schools.models import Schools


class DjangoOrmSchoolsRepo(ISchoolRepo):
    def create(self, entity: SchoolEntity) -> None:
        try:
            Schools.from_entity(entity=entity).save()
        except IntegrityError:
            raise SchoolCreateFailed(detail="Already exists")

    def list(self, owner_id: int) -> list[SchoolEntity]:
        try:
            return [x.to_entity() for x in Schools.objects.filter(owner_id=owner_id).order_by('id')]
        except Schools.DoesNotExist:
            raise SchoolNotFound
