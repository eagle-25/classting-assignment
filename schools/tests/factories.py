import factory

from schools.models import SchoolNews, Schools


class SchoolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Schools

    name = factory.Faker('word')
    city = factory.Faker('city')


class SchoolNewsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SchoolNews

    content = factory.Faker('text')
