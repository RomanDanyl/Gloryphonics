from rest_framework import serializers

from band.models import (
    BandImage,
    Album,
    Follower,
    SocialLinks,
    Genre,
    BandVideo,
    Comment,
    Band,
)


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = (
            "id",
            "title",
            "release_date",
            "cover_image",
        )


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ("id", "name", "email")


class SocialLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLinks
        fields = ("facebook", "instagram", "youtube", "spotify", "youtube_music")


class UserImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BandImage
        fields = ["image"]


class BandImageReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = BandImage
        fields = ["id", "image"]


class BandVideoReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = BandVideo
        fields = ["id", "playlist"]


class BandVideoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BandVideo
        fields = ["band", "playlist"]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["name"]


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = [
            "id",
            "text",
            "created_at",
            "user",
        ]


class BandListSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    images = BandImageReadSerializer(many=True)
    videos = BandVideoReadSerializer(many=True)
    albums = AlbumSerializer(many=True)
    followers = FollowerSerializer(many=True)
    slug = serializers.SerializerMethodField()

    class Meta:
        model = Band
        fields = (
            "id",
            "name",
            "slug",
            "country",
            "description",
            "slogan",
            "genres",
            "cover_image",
            "images",
            "videos",
            "albums",
            "followers",
        )

    def get_slug(self, obj: Band) -> str:
        return obj.get_slug()
