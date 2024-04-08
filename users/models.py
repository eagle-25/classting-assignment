from __future__ import annotations

from django.db import models

from users.domain.entities import UserEntity


class Users(models.Model):
    id = models.SmallAutoField(primary_key=True)
    email = models.EmailField(max_length=100, unique=True, db_index=True)  # 로그인 시 사용
    password = models.CharField(max_length=100)  # 해싱된 값이 저장 되어야 함
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"

    def to_entity(self) -> UserEntity:
        return UserEntity(
            id=self.id,
            email=self.email,
            password=self.password,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
