import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student

import random



@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        student_set = baker.prepare(Student, _quantity=15)
        courses = baker.make(Course, students=student_set, make_m2m=True, *args, **kwargs)
        return courses

    return factory

@pytest.mark.django_db
def test_get_first_course(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)
    course_id = courses[0].id
    course_name = courses[0].name
    # Act
    response = client.get(f'/api/v1/courses/{course_id}/')

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert course_id == data['id']
    assert course_name == data['name']


@pytest.mark.django_db
def test_get_course_list(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)

    # Act
    response = client.get('/api/v1/courses/')

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)

@pytest.mark.django_db
def test_get_course_by_id(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)
    course_id  = courses[0].id
    course_name = courses[0].name

    # Act
    response = client.get(f'/api/v1/courses/?id={course_id}')

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert course_id == data[0]['id']
    assert course_name == data[0]['name']

@pytest.mark.django_db
def test_get_course_by_name(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)
    course_id  = courses[0].id
    course_name = courses[0].name

    # Act
    response = client.get(f'/api/v1/courses/?name={course_name}')

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert course_id == data[0]['id']
    assert course_name == data[0]['name']

@pytest.mark.django_db
def test_create_course(client):
    response = client.post('/api/v1/courses/', {'name': 'test'})
    data = response.json()

    assert response.status_code == 201

    course = Course.objects.values()

    assert course[0]['id'] == data['id']
    assert course[0]['name'] == data['name']


@pytest.mark.django_db
def test_update_course(client, course_factory):
    courses = course_factory(_quantity=10)
    course_id  = courses[0].id
    test_update_name = 'test'

    response = client.patch(f'/api/v1/courses/{course_id}/', {'name': test_update_name})
    assert  response.status_code == 200

    # Act
    response = client.get(f'/api/v1/courses/{course_id}/')

    # Assert
    assert response.status_code == 200
    data = response.json()


    assert courses[0].id == data['id']
    assert data['name']== test_update_name

@pytest.mark.django_db
def test_delete_course(client, course_factory):
    courses = course_factory(_quantity=10)
    course_id  = courses[0].id

    response = client.delete(f'/api/v1/courses/{course_id}/')
    assert  response.status_code == 204

    # Act
    response = client.get(f'/api/v1/courses/{course_id}/')

    # Assert
    assert response.status_code == 404

@pytest.mark.django_db
def test_max_student_pass(client, course_factory,settings):
    max_student = settings.MAX_STUDENTS_PER_COURSE = 20
    courses = course_factory(_quantity=10)

    c = Course.objects.all()
    for course in c:
        assert course.students.count() <= max_student

@pytest.mark.django_db
def test_max_student_fail(client, course_factory,settings):
    max_student = settings.MAX_STUDENTS_PER_COURSE = 10
    courses = course_factory(_quantity=10)

    c = Course.objects.all()
    for course in c:
        assert course.students.count() > max_student


