from ...models import Task
from accounts.models import Profile
from rest_framework import serializers
from datetime import datetime, timezone, timedelta


class TaskSerializer(serializers.ModelSerializer):
    snippet = serializers.ReadOnlyField(source="get_snippet")
    relative_url = serializers.URLField(source="get_absolute_api_url", read_only=True)
    absolute_url = serializers.SerializerMethodField(method_name="get_absolute_url")

    class Meta:
        model = Task
        fields = [
            "author",
            "title",
            "snippet",
            "relative_url",
            "absolute_url",
            "status",
            "created_date",
            "updated_date",
        ]
        read_only_fields = ["author"]

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get("request")
        rep["author"] = Profile.objects.get(user=request.user).user.email
        rep["state"] = "list"
        # print(request.__dict__)
        if request.parser_context.get("kwargs").get("pk"):
            rep["state"] = "single"
            rep.pop("snippet", None)
            rep.pop("relative_url", None)
            rep.pop("absolute_url", None)
        rep.pop("state", None)
        return rep

    def create(self, validated_data):
        validated_data["author"] = Profile.objects.get(
            user=self.context.get("request").user.id
        )
        return super().create(validated_data)

    def validate(self, attrs):
        if self.instance and self.context["request"].method == "PATCH":
            allowed_fields = {
                "status"
            }  # limitation for status field in only PATCH method
            disallowed_fields = set(attrs.keys()) - allowed_fields
            if disallowed_fields:
                raise serializers.ValidationError(
                    f"These fields cannot be updated: {', '.join(disallowed_fields)}"
                )
        return attrs


# Weather:
class WeatherSerializer(serializers.Serializer):
    city = serializers.CharField(source="name")
    country = serializers.CharField(source="sys.country")
    coordinates = serializers.SerializerMethodField()
    weather = serializers.SerializerMethodField()
    temperature = serializers.SerializerMethodField()
    pressure = serializers.IntegerField(source="main.pressure")
    humidity = serializers.IntegerField(source="main.humidity")
    wind = serializers.SerializerMethodField()
    clouds = serializers.IntegerField(source="clouds.all")
    visibility = serializers.IntegerField()
    sunrise = serializers.SerializerMethodField()
    sunset = serializers.SerializerMethodField()
    timezone = serializers.IntegerField()

    def get_coordinates(self, obj):
        return {
            "lon": obj.get("coord", {}).get("lon"),
            "lat": obj.get("coord", {}).get("lat"),
        }

    def get_weather(self, obj):
        weather_list = obj.get("weather", [])
        if weather_list and isinstance(weather_list, list):
            first = weather_list[0]
            return {
                "main": first.get("main"),
                "description": first.get("description"),
            }
        return {}

    def get_temperature(self, obj):
        main = obj.get("main", {})
        return {
            "current": main.get("temp"),
            "feels_like": main.get("feels_like"),
            "min": main.get("temp_min"),
            "max": main.get("temp_max"),
        }

    def get_wind(self, obj):
        wind = obj.get("wind", {})
        return {
            "speed": wind.get("speed"),
            "degree": wind.get("deg"),
        }

    def _convert_unix_to_iso(self, unix_ts, tz_offset):
        if unix_ts is None or tz_offset is None:
            return None
        tz = timezone(timedelta(seconds=tz_offset))
        dt = datetime.fromtimestamp(unix_ts, tz)
        return dt.isoformat()

    def get_sunrise(self, obj):
        return self._convert_unix_to_iso(
            obj.get("sys", {}).get("sunrise"), obj.get("timezone")
        )

    def get_sunset(self, obj):
        return self._convert_unix_to_iso(
            obj.get("sys", {}).get("sunset"), obj.get("timezone")
        )
