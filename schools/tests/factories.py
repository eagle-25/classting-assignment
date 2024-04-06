import factory

from schools.models import Schools


class SchoolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Schools

    name = factory.Faker('name')
    city = factory.Faker('city')
