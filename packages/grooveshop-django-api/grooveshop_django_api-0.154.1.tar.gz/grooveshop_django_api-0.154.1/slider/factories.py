import importlib

import factory
from django.apps import apps
from django.conf import settings
from django.db.models import Count
from django.utils import timezone

from slider.models import Slide
from slider.models import Slider

available_languages = [lang["code"] for lang in settings.PARLER_LANGUAGES[settings.SITE_ID]]


def get_or_create_slider():
    if apps.get_model("slider", "Slider").objects.exists():
        return (
            apps.get_model("slider", "Slider")
            .objects.annotate(num_slides=Count("slides"))
            .order_by("num_slides")
            .first()
        )
    else:
        slider_factory_module = importlib.import_module("slider.factories")
        slider_factory_class = getattr(slider_factory_module, "SliderFactory")
        return slider_factory_class.create()


class SliderTranslationFactory(factory.django.DjangoModelFactory):
    language_code = factory.Iterator(available_languages)
    name = factory.Faker("word")
    url = factory.Faker("url")
    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph")
    master = factory.SubFactory("slider.factories.SliderFactory")

    class Meta:
        model = apps.get_model("slider", "SliderTranslation")
        django_get_or_create = ("language_code", "master")


class SliderFactory(factory.django.DjangoModelFactory):
    image = factory.django.ImageField(
        filename="slider_image.jpg",
        color=factory.Faker("color"),
        width=1920,
        height=1080,
    )
    thumbnail = factory.django.ImageField(
        filename="slider_thumbnail.jpg",
        color=factory.Faker("color"),
        width=1280,
        height=720,
    )
    video = factory.django.FileField(filename="slider_video.mp4")

    class Meta:
        model = Slider
        skip_postgeneration_save = True

    @factory.post_generation
    def num_slides(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            SlideFactory.create_batch(extracted, slider=self)

    @factory.post_generation
    def translations(self, create, extracted, **kwargs):
        if not create:
            return

        translations = extracted or [
            SliderTranslationFactory(language_code=lang, master=self) for lang in available_languages
        ]

        for translation in translations:
            translation.master = self
            translation.save()


class SlideTranslationFactory(factory.django.DjangoModelFactory):
    language_code = factory.Iterator(available_languages)
    name = factory.Faker("word")
    url = factory.Faker("url")
    title = factory.Faker("sentence", nb_words=3)
    subtitle = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph")
    button_label = factory.Faker("word")
    master = factory.SubFactory("slider.factories.SlideFactory")

    class Meta:
        model = apps.get_model("slider", "SlideTranslation")
        django_get_or_create = ("language_code", "master")


class SlideFactory(factory.django.DjangoModelFactory):
    slider = factory.LazyFunction(get_or_create_slider)
    discount = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    show_button = factory.Faker("boolean")
    date_start = factory.LazyFunction(timezone.now)
    date_end = factory.LazyFunction(lambda: timezone.now() + timezone.timedelta(days=180))
    image = factory.django.ImageField(
        filename="slide_image.jpg",
        color=factory.Faker("color"),
        width=1920,
        height=1080,
    )
    thumbnail = factory.django.ImageField(
        filename="slide_thumbnail.jpg",
        color=factory.Faker("color"),
        width=1280,
        height=720,
    )

    class Meta:
        model = Slide
        django_get_or_create = ("slider",)
        skip_postgeneration_save = True

    @factory.post_generation
    def translations(self, create, extracted, **kwargs):
        if not create:
            return

        translations = extracted or [
            SlideTranslationFactory(language_code=lang, master=self) for lang in available_languages
        ]

        for translation in translations:
            translation.master = self
            translation.save()
