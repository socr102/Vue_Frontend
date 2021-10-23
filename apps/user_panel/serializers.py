from django.contrib.auth.models import Group

from .models import CustomUser
from .mixins import EmailValidationMixin
from rest_framework import serializers
from backend.settings import MERCHANT_ADMIN, MERCHANT_WORKER


class TrimUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email')


class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', )


class UserListSerializer(EmailValidationMixin, serializers.ModelSerializer):
    created_by = TrimUserSerializer(read_only=True)
    groups = GroupsSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ('email',
                  'password',
                  'id',
                  'is_staff',
                  'is_superuser',
                  'is_active',
                  'organization',
                  'delete_request',
                  'created_by',
                  'groups',
                  )

        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')

        self.email_check(validated_data)
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.created_by_id = self.context['request'].user.id
        request_context, group = self.context['request'], None

        if request_context.user.is_superuser or\
            request_context.user.is_staff and not\
            validated_data['is_staff']:
            group = Group.objects.get(name=MERCHANT_ADMIN)

        if request_context.user.groups.filter(name=MERCHANT_ADMIN).exists():
            group = Group.objects.get(name=MERCHANT_WORKER)
            user.organization_id = request_context.user.organization_id

        user.save()
        if group: group.user_set.add(user)
        return user


class UserDetailSerializer(EmailValidationMixin, serializers.ModelSerializer):
    created_by = TrimUserSerializer(read_only=True)
    groups = GroupsSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        extra_kwargs = {'password': {'write_only': True},
                        'delete_request': {'read_only': True},
                        'is_active': {'read_only': True}}
        fields = ('id',
                  'email',
                  'is_active',
                  'password',
                  'first_name',
                  'last_name',
                  'is_staff',
                  'delete_request',
                  'social_security',
                  'phone',
                  'allow_contact',
                  'contact_way',
                  'organization',
                  'is_superuser',
                  'created_by',
                  'groups'
                  )

    def update(self, user, validated_data):
        password = validated_data.pop('password', None)
        self.email_check(validated_data)

        if password:
            user.set_password(password)

        user = super().update(user, validated_data)
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True,
                                         required=True)
    old_password = serializers.CharField(write_only=True,
                                         required=True)
    confirm_password = serializers.CharField(write_only=True,
                                             required=True)

    class Meta:
        model = CustomUser
        fields = ('old_password', 'new_password', 'confirm_password')

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            error = "Current password is not correct"
            raise serializers.ValidationError(error)
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            error = {"new_password": "Password fields didn't match."}
            raise serializers.ValidationError(error)
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
