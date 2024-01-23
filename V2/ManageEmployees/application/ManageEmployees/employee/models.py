from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission


#_________________________ Department
class Department(models.Model):
    ADMINISTRATION = 'Administration'
    IT = 'Information Technology'
    HR = 'Human Resources'
    FINANCE = 'Finance'

    DEPARTMENT_CHOICES = [
        (ADMINISTRATION, 'Administration'),
        (IT, 'Information Technology (IT)'),
        (HR, 'Human Resources (HR)'),
        (FINANCE, 'Finance'),
    ]

    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=255, choices=DEPARTMENT_CHOICES)

    def __str__(self):
        return self.department_name
        
#_________________________ Position
class Position(models.Model):
    ADMIN = 'admin'
    RH = 'RH'
    REGULAR_EMPLOYEE = 'regular_employee'

    POSITION_CHOICES = [
        (ADMIN, 'Admin'),
        (RH, 'RH'),
        (REGULAR_EMPLOYEE, 'Regular Employee'),
    ]

    position_id = models.AutoField(primary_key=True)
    position_name = models.CharField(
        max_length=50,
        choices=POSITION_CHOICES,
        default=REGULAR_EMPLOYEE,
    )

    def __str__(self):
        return self.get_position_name_display()

#_________________________ Employee
class EmployeeManager(BaseUserManager):
    def create_user(self, email, name, position, department, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, position=position, department=department, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, position, department, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
         #   This line will be deleted 
        default_position, _ = Position.objects.get_or_create(position_name='regular_employee')

        return self.create_user(email, name, position, department, password, **extra_fields)

class Employee(AbstractBaseUser, PermissionsMixin):
    employee_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='employees')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Note: In practice, use a more secure way to store passwords
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    joined_date = models.DateField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender = models.CharField(max_length=10, choices=gender_choices, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)

    objects = EmployeeManager()

    groups = models.ManyToManyField(Group, blank=True, related_name='employee_groups')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='employee_permissions')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'position', 'department']

    def __str__(self):
        return self.name
#_________________________ EmployeeProfile

#_____ Documents
class Document(models.Model):
    CERTIFICATION = 'Certification'
    CV = 'CV'
    PORTFOLIO = 'Portfolio'

    DOCUMENT_CHOICES = [
        (CERTIFICATION, 'Certification'),
        (CV, 'CV'),
        (PORTFOLIO, 'Portfolio'),
    ]

    document_type = models.CharField(max_length=50, choices=DOCUMENT_CHOICES)
    document_file = models.FileField(upload_to='employee_documents/')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.upload_date}"

#_____ Profile
class EmployeeProfile(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, primary_key=True)
    skills = models.TextField(blank=True)
    qualifications = models.TextField(blank=True)

    # Relationship with documents
    documents = models.ManyToManyField(Document, blank=True, related_name='employee_documents')

    def __str__(self):
        return f"Profile of {self.employee.name}"