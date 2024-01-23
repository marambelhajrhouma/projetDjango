from django.contrib import admin

from django.contrib import admin
from .models import Department, Position, Employee, Document, EmployeeProfile

#By the biblio admin we will register the Department

# Register the Department model
admin.site.register(Department)

# Register the Position model
admin.site.register(Position)

# Register the Employee model
admin.site.register(Employee)

#________________________________
# Register the Documents for Employees 
admin.site.register(Document)

# Register the profile of Employees 
admin.site.register(EmployeeProfile)
#________________________________


