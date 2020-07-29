from django.contrib.auth.models import User, Group
from rest_framework import serializers

from api.models import Employee, Guest



class GuestSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Guest
        fields = ['email', 'isDrinking']

class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    guest = GuestSerializer()

    class Meta:
        model = Employee
        fields = ['email', 'isDrinking', 'guest']

    def create(self, validated_data):
        print(validated_data)
        guest = validated_data.pop('guest')
        employee = Employee.objects.create(**validated_data)
        guest = Guest.objects.create(employee=employee, **guest)
        return employee
