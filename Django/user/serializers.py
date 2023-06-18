from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    user = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, required=True)
    re_password = serializers.CharField(max_length=100, required=True)
    credit = serializers.FloatField(required=False)

    def is_valid(self, *, raise_exception=False):
        if super().is_valid():
            if self.data['password'] == self.data['re_password']:
                return True
        return False


class LoginSerializer(serializers.Serializer):
    user = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, required=True)