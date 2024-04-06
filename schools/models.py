from __future__ import annotations

from django.db import models

from schools.domain.entities import SchoolEntity


class Schools(models.Model):
    id = models.SmallAutoField(primary_key=True)
    owner = models.ForeignKey('users.Users', on_delete=models.DO_NOTHING, db_index=True)
    name = models.CharField(max_length=20, null=False)
    city = models.CharField(max_length=30, null=False)
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
