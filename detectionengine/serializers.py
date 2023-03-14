from rest_framework import serializers
from .models import ProcessedData


# remember to import the File model


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class SaveFileSerializer(serializers.Serializer):

    class Meta:
        model = ProcessedData
        fields = "__all__"


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedData
        fields = "__all__"
