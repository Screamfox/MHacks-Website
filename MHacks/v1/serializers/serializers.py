from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.fields import CharField, ChoiceField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from MHacks.models import Announcement as AnnouncementModel, \
    Event as EventModel, Location as LocationModel, \
    ScanEvent as ScanEventModel, MHacksUser as MHacksUserModel
from MHacks.v1.serializers.util import UnixEpochDateField, DurationInSecondsField


class MHacksModelSerializer(ModelSerializer):
    def to_representation(self, instance):
        if getattr(instance, 'deleted', False):
            # noinspection PyProtectedMember
            return {instance._meta.pk.name: str(instance.pk), 'deleted': True}
        return super(MHacksModelSerializer, self).to_representation(instance)


class AnnouncementSerializer(MHacksModelSerializer):
    id = CharField(read_only=True)
    broadcast_at = UnixEpochDateField()

    class Meta:
        model = AnnouncementModel
        fields = ('id', 'title', 'info', 'broadcast_at', 'category', 'approved')


class EventSerializer(MHacksModelSerializer):
    id = CharField(read_only=True)
    start = UnixEpochDateField()
    locations = PrimaryKeyRelatedField(many=True, pk_field=CharField(),
                                       queryset=LocationModel.objects.all().filter(deleted=False))
    duration = DurationInSecondsField()
    category = ChoiceField(choices=EventModel.CATEGORIES)

    class Meta:
        model = EventModel
        fields = ('id', 'name', 'info', 'start', 'duration', 'locations', 'category', 'approved')


class LocationSerializer(MHacksModelSerializer):
    id = CharField(read_only=True)

    class Meta:
        model = LocationModel
        fields = ('id', 'name', 'latitude', 'longitude')


class ScanEventSerializer(MHacksModelSerializer):
    id = CharField(read_only=True)
    expiry_date = UnixEpochDateField()

    class Meta:
        model = ScanEventModel
        fields = ('id', 'name', 'expiry_date')


class MHacksUserSerializer(MHacksModelSerializer):
    id = CharField(read_only=True)

    class Meta:
        model = MHacksUserModel
        fields = ('id', 'first_name', 'last_name', 'email')


class AuthSerializer(AuthTokenSerializer):
    # Extends auth token serializer to accommodate push notifs

    token = serializers.CharField(required=False)
    is_gcm = serializers.BooleanField(required=False)

    def validate(self, attributes):
        attributes = super(AuthSerializer, self).validate(attributes)

        # Optionally add the token if it exists
        if 'token' in attributes.keys() and 'is_gcm' in attributes.keys():
            token = attributes.get('token')
            is_gcm = attributes.get('is_gcm')
            preference = attributes.get('preference', '63')
            if not isinstance(preference, str):
                preference = str(preference)
            attributes['push_notification'] = {
                'token': token,
                'is_gcm': is_gcm,
                'preference': preference
            }

        return attributes

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
