from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_EMPLOYEE_URL = reverse('employee:create')
TOKEN_URL = reverse('employee:token')


def create_employee(**params):
    return get_user_model().objects.create_user(**params)


class PublicEmployeeApiTests(TestCase):
    """Tets the employees API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_employee_success(self):
        """Test creating employee with valid payload is successful"""
        payload = {
            'email': 'joaosilva@host.com.br',
            'password': 'senhateste',
            'name': 'João Silva'
        }

        res = self.client.post(CREATE_EMPLOYEE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        employee = get_user_model().objects.get(**res.data)
        self.assertTrue(employee.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_employee_exists(self):
        """Test creating employee that already exists fails"""
        payload = {
            'email': 'joaosilva@host.com.br',
            'password': 'senhateste',
            'name': 'João Silva',
        }
        create_employee(**payload)

        res = self.client.post(CREATE_EMPLOYEE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password must be more than 5 characters"""
        payload = {
            'email': 'joaosilva@host.com.br',
            'password': 'se',
            'name': 'João Silva',
        }
        res = self.client.post(CREATE_EMPLOYEE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        employee_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(employee_exists)

    def test_create_token_for_employee(self):
        """Test that a token is created for the employee"""
        payload = {
            'email': 'joaosilva@host.com.br',
            'password': 'senhateste',
            'name': 'João Silva',
        }
        create_employee(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_employee(email='joaosilva@host.com.br', password='senhateste')
        payload = {'email': 'joaosilva@host.com.br', 'password': 'senhateste'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_employee(self):
        """Test that token is not created if employee doens't exist"""
        payload = {'email': 'joaosilva@host.com.br', 'password': 'senhateste'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {
            'email': 'joaosilva',
            'password': '',
            })
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
