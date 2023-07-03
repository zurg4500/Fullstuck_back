from rest_framework import serializers
from .models import WineImage, Wine


class WineImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WineImage
        exclude = ["wine"]


class WineSerializer(serializers.ModelSerializer):
    image = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Wine
        fields = "__all__"
        extra_kwargs = {
            "user": {"read_only": True},
            "slug": {"read_only": True},
        }

    def create(self, validated_data):
        user = self.context.get("request").user
        validated_data["user"] = user
        images = validated_data.pop("image", None)
        wine = Wine.objects.create(**validated_data)
        if images is not None:
            imgs = []
            for image in images:
                imgs.append(WineImage(wine=wine, image=image))
            WineImage.objects.bulk_create(imgs)
        return wine

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["images"] = WineImageSerializer(
            instance.images.all(), many=True
        ).data
        return representation
