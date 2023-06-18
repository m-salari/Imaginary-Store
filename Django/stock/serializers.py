from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    user = serializers.CharField(max_length=100)
    stockname = serializers.CharField(max_length=100)
    quantity = serializers.IntegerField()
