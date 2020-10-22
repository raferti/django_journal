from rest_framework import serializers

from django_journal.settings import STUDENT
from journal.models import Score, Grade
from people.models import User, Teacher


class ScoreSerializer(serializers.ModelSerializer):
    """Сериализатор оценок."""
    created = serializers.DateField(label='Дата создания')
    updated = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S', read_only=True)

    def create(self, validated_data):
        score = Score(**validated_data)
        score.teacher = self.context['request'].user
        score.save()
        return score

    def update(self, instance, validated_data):
        validated_data['teacher'] = self.context['request'].user
        return super(ScoreSerializer, self).update(instance, validated_data)

    def validate(self, attrs):
        if not Teacher.objects.prefetch_related('lessons')\
                .filter(user=self.context['request'].user, lessons=attrs['lesson']).exists():
            raise serializers.ValidationError(
                {'lesson': f'В доступе отказанно, вы не можете ставить оценки по {attrs["lesson"]}.'}
            )

        if not Grade.objects.filter(group=attrs['group'], lessons=attrs['lesson']).exists():
            raise serializers.ValidationError(
                {'lesson': f'У класса: {attrs["group"]} нет предмета: {attrs["lesson"]}.'}
            )

        if not User.objects.select_related('student')\
                .filter(student__group=attrs['group'], username=attrs['student'], user_status=STUDENT).exists():
            raise serializers.ValidationError(
                {'student_field': f'Пользователь: {attrs["student"]} не состоит в классе: {attrs["group"]}.'}
            )
        return attrs

    class Meta:
        model = Score
        fields = ['id', 'score', 'score_status', 'lesson', 'student', 'teacher', 'group', 'created', 'updated']
        extra_kwargs = {'teacher': {'read_only': True}}
