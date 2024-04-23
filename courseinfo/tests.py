from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Period, Year, Semester, Course, Instructor, Student, Section, Registration


class InstructorFormTest(TestCase):

    def test_clean_first_name(self):
        form_data = {'first_name': ' Kevin ', 'last_name': 'Trainor', 'disambiguator': ''}
        form = InstructorForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['first_name'], 'Kevin')

    def test_clean_last_name(self):
        form_data = {'first_name': ' Kevin ', 'last_name': 'Trainor', 'disambiguator': ''}
        form = InstructorForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['last_name'], 'Trainor')


class ModelTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(username='testuser', password='password123')

        # Create test instances of each model
        self.period = Period.objects.create(period_sequence=1, period_name='Spring')
        self.year = Year.objects.create(year=2024)
        self.semester = Semester.objects.create(year=self.year, period=self.period)
        self.course = Course.objects.create(course_number='IS101', course_name='Introduction to IS')
        self.instructor = Instructor.objects.create(first_name='John', last_name='Doe')
        self.student = Student.objects.create(first_name='Alice', last_name='Smith')
        self.section = Section.objects.create(section_name='001', semester=self.semester, course=self.course, instructor=self.instructor)
        self.registration = Registration.objects.create(student=self.student, section=self.section)



    def test_period_str_representation(self):
        self.assertEqual(str(self.period), 'Spring')

    def test_year_str_representation(self):
        self.assertEqual(str(self.year), '2024')

    def test_semester_str_representation(self):
        expected_str = '2024 - Spring'
        self.assertEqual(str(self.semester), expected_str)

    def test_course_str_representation(self):
        expected_str = 'IS101 - Introduction to IS'
        self.assertEqual(str(self.course), expected_str)

    def test_instructor_str_representation(self):
        expected_str = 'Doe, John'
        self.assertEqual(str(self.instructor), expected_str)

    def test_student_str_representation(self):
        expected_str = 'Smith, Alice'
        self.assertEqual(str(self.student), expected_str)

    def test_section_str_representation(self):
        expected_str = 'IS101 - 001 (2024 - Spring)'
        self.assertEqual(str(self.section), expected_str)

    def test_registration_str_representation(self):
        expected_str = 'IS101 - 001 (2024 - Spring) / Smith, Alice'
        self.assertEqual(str(self.registration), expected_str)

    def test_unique_semester(self):
        # Attempt to create a duplicate semester
        with self.assertRaises(Exception):
            Semester.objects.create(year=self.year, period=self.period)

    def test_unique_course(self):
        # Attempt to create a duplicate course
        with self.assertRaises(Exception):
            Course.objects.create(course_number='IS101', course_name='Introduction to IS')

    def test_unique_instructor(self):
        # Attempt to create a duplicate instructor
        with self.assertRaises(Exception):
            Instructor.objects.create(user=self.user, first_name='John', last_name='Doe')

    def test_unique_student(self):
        # Attempt to create a duplicate student
        with self.assertRaises(Exception):
            Student.objects.create(user=self.user, first_name='Alice', last_name='Smith')

    def test_unique_section(self):
        # Attempt to create a duplicate section
        with self.assertRaises(Exception):
            Section.objects.create(section_name='001', semester=self.semester, course=self.course, instructor=self.instructor)

    def test_unique_registration(self):
        # Attempt to create a duplicate registration
        with self.assertRaises(Exception):
            Registration.objects.create(student=self.student, section=self.section)
