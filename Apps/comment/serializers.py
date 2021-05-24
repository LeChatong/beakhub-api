from rest_framework import serializers

from Apps.account.serializers import UserSerializer
from Apps.comment.models import CommentJob
from Apps.job.serializers import JobSerializer


class CommentJobSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='comment-job-detail'
    )
    user = UserSerializer(many=False)
    job = JobSerializer(many=False)

    class Meta:
        model = CommentJob
        fields = [
            'url',
            'id',
            'user_id',
            'job_id',
            'commentary',
            'is_active',
            'user',
            'job',
            'created_on',
            'updated_on'
        ]
