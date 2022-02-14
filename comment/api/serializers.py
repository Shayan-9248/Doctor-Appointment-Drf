from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from rest_framework import serializers

from comment.models import Comment
from appointment.models import Appointment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content",)
    
    def create(self, validated_data):
        instance = get_object_or_404(Appointment, pk=self.context.get("appointment_id"))
        user_id = self.context.get("user_id")

        Comment.objects.create(
            author_id=user_id,
            content=validated_data.get("content"),
            content_type=instance.get_content_type,
            object_id=instance.id,
        )
        return validated_data
