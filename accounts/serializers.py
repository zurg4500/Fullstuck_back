from rest_framework import serializers
from rest_framework import status
from django.contrib.auth import get_user_model, authenticate
from .utils import send_activation_code, create_activation_code, send_drop_password_code


User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(max_length=200, write_only=True)

    class Meta:
        model = User
        fields = ("alcohol-anonimus_name", "email", "password", "password_confirm")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    # .is_valid()
    def validate(self, attrs: dict):
        password = attrs.get("password")
        password_confirm = attrs.pop("password_confirm")
        if password != password_confirm:
            raise serializers.ValidationError(
                {"message": "Пароли не совпадают, опохмелись"}, code=status.HTTP_400_BAD_REQUEST
            )
        return attrs

    # attrs -> validated_data
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        create_activation_code(user)
        send_activation_code(user)
        return user


class ActivationSerializer(serializers.Serializer):
    activation_code = serializers.CharField(max_length=10)

    def validate_activation_code(self, activation_code):
        code_exists = User.objects.filter(activation_code=activation_code).exists()
        if code_exists:
            return activation_code
        raise serializers.ValidationError(
            {"message": "Неправильно указан код активациио, тебе нужно опохмелиться"},
            code=status.HTTP_400_BAD_REQUEST,
        )

    def activate(self):
        code = self.validated_data.get("activation_code")
        user = User.objects.get(activation_code=code)
        user.is_active = True
        user.activation_code = ""
        user.save()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=128)

    def validate_username(self, username):
        user = User.objects.filter(username=username).exists()
        if not user:
            raise serializers.ValidationError(
                {"message": f"User with {username} alcohol_anonimus_name not found"},
                code=status.HTTP_400_BAD_REQUEST,
            )
        return username

    def validate(self, attrs: dict):
        request = self.context.get("request")
        username = attrs.get("alcohol_anonimus_name")
        password = attrs.get("password")
        if not (username and password):
            raise serializers.ValidationError(
                {"message": "Alcohol_anonimus_name and password are required"},
                code=status.HTTP_400_BAD_REQUEST,
            )
        user = authenticate(username=username, password=password, request=request)
        if user is None:
            raise serializers.ValidationError(
                {"message": "Неправильно указан alcohol_anonimus_name или password"}
            )
        attrs["user"] = user
        return attrs



class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128)
    password_confirm = serializers.CharField(max_length=128)

    def validate_current_password(self, current_password):
        user = self.context.get('request').user
        if user.check_password(current_password):
            return current_password
        raise serializers.ValidationError('Wrong password')
    
    def validate(self, attrs: dict):
        new_pass = attrs.get('new_password')
        pass_confirm = attrs.get('password_confirm')
        if new_pass != pass_confirm:
            raise serializers.ValidationError('Пароли не совпадают, опохмелись')
        return attrs
    
    def set_new_password(self):
        new_password = self.validated_data.get('new_password')
        user = self.context.get('request').user
        user.set_password(new_password)
        user.save()


class DropPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email does not exist')
        return email
    
    def send_activation_code(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        create_activation_code(user)
        send_drop_password_code(email, user.activation_code)


class ChangeForgottenPassword(serializers.Serializer):
    code = serializers.CharField(max_length=10)
    new_password = serializers.CharField(max_length=128)
    password_confirm = serializers.CharField(max_length=128)

    def validate_code(self, code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Wrong code')
        return code

    def validate(self, attrs: dict):
        new_pass = attrs.get('new_password')
        pass_confirm = attrs.get('password_confirm')
        if new_pass != pass_confirm:
            raise serializers.ValidationError('Пароли не совпадают, сколько пальцев на одной руке?')
        return attrs

    def set_new_password(self):
        code = self.validated_data.get('code')
        new_password = self.validated_data.get('new_password')
        user = User.objects.get(activation_code=code)
        user.set_password(new_password)
        user.activation_code = ''
        user.save()
