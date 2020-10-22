from rest_framework import serializers

from journal.models import GroupStudent, Lesson
from people.models import Student


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор школьных предметов."""

    class Meta:
        model = Lesson
        fields = ['id', 'name']


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор школьных классов."""
    grade = serializers.CharField()

    class Meta:
        model = GroupStudent
        fields = ['id', 'grade', 'create_group']


class GroupStudentSerializer(serializers.ModelSerializer):
    """Сериализатор учеников в группе."""
    user_id = serializers.StringRelatedField(source='user.id')
    full_name = serializers.StringRelatedField(source='user.get_full_name')

    class Meta:
        model = Student
        fields = ['user_id', 'full_name']


class GroupDetailSerializer(serializers.ModelSerializer):
    """Сериализатор данных школьной группы."""
    lessons = LessonSerializer(source='grade.lessons', many=True)
    students = GroupStudentSerializer(many=True)
    grade = serializers.CharField()

    class Meta:
        model = GroupStudent
        fields = ['id', 'grade', 'create_group', 'lessons', 'students']