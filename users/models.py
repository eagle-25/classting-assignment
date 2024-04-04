from __future__ import annotations

from django.db import models

from users.domain.entities import UserEntity
from users.domain.values import UserType


class Users(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(
        max_length=100, unique=True, db_index=True
    )  # 로그인 시 사용
    password = models.CharField(max_length=100)  # 해싱된 값이 저장 되어야 함
    user_type = models.CharField(max_length=20)  # UserType['PUBLISHER', 'SUBSCRIBER']
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"

    @classmethod
    def from_entity(cls, user_entity: UserEntity) -> Users:
        return cls(
            id=user_entity.id,
            email=user_entity.email,
            user_type=user_entity.user_type.value,
            password=user_entity.password,
        )

    def to_entity(self) -> UserEntity:
        return UserEntity(
            id=self.id,
            email=self.email,
            user_type=UserType(self.user_type),
            password=self.password,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
