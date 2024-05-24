from django.test import TestCase
from unittest import TestCase
from unittest.mock import patch
from .models import *

class EmployeeModelTest(TestCase):

    def test_first_name_label(self):
        employee = Employee.objects.get(id=1)
        field_label = employee.user._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_label(self):
        employee = Employee.objects.get(id=1)
        field_label = employee.user._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_first_name_max_length(self):
        employee = Employee.objects.get(id=1)
        max_length = employee.user._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 150)

    def test_last_name_max_length(self):
        employee = Employee.objects.get(id=1)
        max_length = employee.user._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 150)
        

class ClientModelTest(TestCase):
        
    def test_first_name_label(self):
        client = Client.objects.get(id=7)
        field_label = client._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_label(self):
        client = Client.objects.get(id=7)
        field_label = client._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')
        
class JobModelTest(TestCase):

    def test_str_method(self):
        job = Job.objects.get(id=1)
        expected_object_name = job.title
        self.assertEqual(str(job), expected_object_name)

    def test_description_text(self):
        job = Job.objects.get(id=1)
        expected_text = 'The dirty worker'
        self.assertEqual(job.description, expected_text)
        
class FAQModelTest(TestCase):

    def test_str_method(self):
        faq = FAQ.objects.get(id=1)
        expected_object_name = faq.question
        self.assertEqual('Whats your name?', expected_object_name)

    def test_question_text(self):
        faq = FAQ.objects.get(id=1)
        expected_text = 'Whats your name?'
        self.assertEqual(faq.question, expected_text)

    def test_answer_text(self):
        faq = FAQ.objects.get(id=1)
        expected_text = 'Jackson'
        self.assertEqual(faq.answer, expected_text)