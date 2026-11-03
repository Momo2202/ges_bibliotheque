from rest_framework import serializers

from apps.members.models import Member


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
            "registration_date",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "registration_date", "created_at", "updated_at"]
