import json

from django.contrib.auth.models import User, Group
from django.db.utils import IntegrityError
from django.http.response import JsonResponse, HttpResponse
from django.views.defaults import bad_request
from rest_framework import viewsets, status
from rest_framework.decorators import api_view

from api.models import Employee, Guest
from api.serializers import EmployeeSerializer, GuestSerializer
import values

"""
Section: API list functions
"""

@api_view(['GET'])
def list_participants(request):
    """
    List all employees
    :param request:
    :return:
    """
    participants = Employee.objects.all()
    print(participants)
    serializer = EmployeeSerializer(participants, many=True)
    return JsonResponse({'participants': serializer.data}, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
def list_guests(request):
    """
    List all guests
    :param request:
    :return:
    """
    guests = Guest.objects.all()
    serializer = GuestSerializer(guests, many=True)
    return JsonResponse({'guests': serializer.data}, safe=False, status=status.HTTP_200_OK)

"""
Section: Deleting
"""
@api_view(['DELETE'])
def delete_employee(request, email):
    try:
        employee = Employee.objects.get(email=email)
    except:
        return HttpResponse(status=404)
    employee.delete()
    return JsonResponse({'success' : "Participante removido"}, safe=False, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_guest(request, email):
    try:
        guest = Guest.objects.get(email=email)
    except:
        return HttpResponse(status=404)
    guest.delete()
    return JsonResponse({'success' : "Convidado removido"}, safe=False, status=status.HTTP_200_OK)

"""
Section: add participants
"""

@api_view(['POST'])
def participate(request):
    try:
        employee = request.data.get('employee')
        employeeSerializer = EmployeeSerializer(data=employee)
        if employeeSerializer.is_valid():
            employeeSerializer.save()
        else:
            return JsonResponse({'error': "Objetos não criados"}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return JsonResponse({'employee': employeeSerializer.data}, safe=False, status=status.HTTP_201_CREATED)
    except IntegrityError:
        return bad_request(request)
    except Exception as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def add_guest(request):
    employeeEmail = request.data.get('employeeEmail')
    try:
        employee = Employee.objects.get(email=employeeEmail)
        guest = request.data.get('guest')
        guest = Guest.objects.create(employee=employee, **guest)
        return JsonResponse({'employee': employee}, safe=False, status=status.HTTP_201_CREATED)
    except IntegrityError:
        return bad_request(request)
    except:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

"""
Section: Financial status
"""
@api_view(['GET'])
def finance(request):
    employees = Employee.objects.all()
    food_total = 0
    drinks_total = 0
    for e in employees:
        food_total += values.food_fee
        if e.isDrinking:
            drinks_total += values.drinking_fee
        if e.guest:
            food_total += values.food_fee
            if e.guest.isDrinking:
                drinks_total += values.drinking_fee
    return JsonResponse({'total': food_total + drinks_total, 'drinkingTotal': drinks_total, 'foodTotal': food_total},
                        safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)