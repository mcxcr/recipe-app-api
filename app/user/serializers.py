from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """ Serializer for users objects """

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """ Create a new user with encrypted pass and return it """
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_date):
        """ Update a user, setting the password correctly and return it """
        password = validated_date.pop('password', None)
        user = super().update(instance, validated_date)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """ Serializer for the user auth object """
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """ Validate and aut the user """
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msj = _('Unable to auth with provided credentials.')
            raise serializers.ValidationError(msj, code='authentication')

        attrs['user'] = user
        return attrs
