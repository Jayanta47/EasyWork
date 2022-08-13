from rest_framework import serializers

from .models import FuncCategory

class FuncCategorySerializer(serializers.Serializer):
    title = serializers.CharField(max_length = 200, required=False)
    expected_time = serializers.IntegerField(required=False)
    man_hour_per_week = serializers.IntegerField(required=False)
    allocated_budget = serializers.IntegerField(required=False)
    
    def create(self, validated_data):
        return FuncCategory.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.expected_time = validated_data.get('expected_time', instance.expected_time)
        instance.man_hour_per_week = validated_data.get('man_hour_per_week', instance.man_hour_per_week)
        instance.allocated_budget = validated_data.get('allocated_budget', instance.allocated_budget)
        instance.save()
        return instance
        
    class Meta:
        model = FuncCategory
        fields = [
            "id",
            "title",
            "expected_time",
            "man_hour_per_week",
            "allocated_budget"
        ]