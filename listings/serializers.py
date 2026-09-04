from django.contrib.auth.models import User
from rest_framework import serializers

from listings.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации.
        Вызывается при создании и обновлении.
        Не больше 10 открытых объявлений у пользователя

        """

        request = self.context.get('request')

        # Проверяем, аутентифицирован ли пользователь
        if request and request.user.is_authenticated:
            # Проверяем, меняется ли статус на OPEN
            if data.get('status') == 'OPEN':
                # Считаем открытые объявления пользователя
                open_ads = Advertisement.objects.filter(
                    creator=request.user,
                    status='OPEN'
                )

                # Если это обновление, то исключаем текущее объявление
                if self.instance:
                    open_ads = open_ads.exclude(id=self.instance.id)

                # Если объявлений 10 или больше, возникает ошибка
                if open_ads.count() >= 10:
                    raise serializers.ValidationError(
                        "У пользователя не может быть больше 10 открытых объявлений"
                    )

        return data
