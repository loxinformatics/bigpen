from rest_framework import serializers


class ContactUsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    subject = serializers.CharField(max_length=200)
    message = serializers.CharField()

    def validate_email(self, value):
        """Custom email validation if needed"""
        return value

    def validate_message(self, value):
        """Custom message validation if needed"""
        if len(value.strip()) < 10:
            raise serializers.ValidationError(
                "Message must be at least 10 characters long."
            )
        return value
