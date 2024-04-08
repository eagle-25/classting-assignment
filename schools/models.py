from __future__ import annotations

from django.db import models

from schools.domain.entities import SchoolEntity, SchoolNewsEntity
from schools.domain.values import SchoolDTO


class Schools(models.Model):
    id = models.SmallAutoField(primary_key=True)
    owner = models.ForeignKey('users.Users', on_delete=models.DO_NOTHING, db_index=True)
    name = models.CharField(max_length=20, null=False, db_index=True)
    city = models.CharField(max_length=30, null=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'schools'
        unique_together = ('name', 'city')

    @classmethod
    def from_entity(cls, entity: SchoolEntity) -> Schools:
        return cls(
            owner_id=entity.owner_id,
            name=entity.name,
            city=entity.city,
        )

    def to_entity(self) -> SchoolEntity:
        return SchoolEntity(
            id=self.id, owner_id=self.owner.id, name=self.name, city=self.city, created_at=self.created_at
        )

    def to_dto(self) -> SchoolDTO:
        return SchoolDTO(
            id=self.id,
            name=self.name,
            city=self.city,
            owner_id=self.owner.id,
            owner_email=self.owner.email,
            created_at=self.created_at,
        )


class SchoolNews(models.Model):
    id = models.SmallAutoField(primary_key=True)
    school = models.ForeignKey(Schools, on_delete=models.DO_NOTHING, db_index=True)
    content = models.TextField(max_length=1000, null=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'school_news'

    @classmethod
    def from_entity(cls, entity: SchoolNewsEntity) -> SchoolNews:
        return cls(
            school_id=entity.school_id,
            content=entity.content,
        )

    def to_entity(self) -> SchoolNewsEntity:
        return SchoolNewsEntity(
            id=self.id,
            school_id=self.school.id,
            content=self.content,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
