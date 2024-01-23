from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
#from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

#_________________________ Registration
def registerPage(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('login')  
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'accounts/authentification/register.html', context)

#_________________________ Login
def loginPage(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print(f'Form data: {form.data}')

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Explicitly print the provided credentials
            print(f'Email: {email}, Password: {password}')

            # Authenticate the user
            user = authenticate(request, email=email, password=password)

            # Print debug information
            if user is not None:
                print(f'User authenticated: {user}')
                print(f'User position: {user.position.position_name}')
            else:
                print('Authentication failed. User is None.')

            if user is not None and user.is_active:
                # Log in the user
                login(request, user)

                if user.position.position_name == 'admin':
                    return redirect('admin_dashboard')  # Replace with your admin dashboard URL
                elif user.position.position_name == 'RH':
                    return redirect('listEmployees')  # Replace with your RH dashboard URL
                else:
                    return redirect('employee_dashboard')  # Replace with your employee dashboard URL

        else:
            print(f'Form errors: {form.errors}')

    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'accounts/authentification/login.html', context)
#---RH
def rh_dashboard(request):
    return  render(request, 'accounts/RH/welcome.html',)
 
#_________________________ Logout
        #complete the necessary code


#_________________________ AdminViews
    #_________ListOfEmployees
    #@login_required(login_url='login')  # Ensure the user is logged in
def listEmployees(request):
    #if request.user.position.position_name == 'admin':
        employees = Employee.objects.filter(position__position_name__in=['RH', 'regular_employee'])

        context = {'employees': employees}
        return render(request, 'accounts/admin/listOfEmployees.html', context)
    #else:
        #return render(request, 'accounts/unauthorized_access.html')

def filter_employees(request, position):
    if position == 'all':
        employees = Employee.objects.all()
    else:
        employees = Employee.objects.filter(position__position_name=position)

    context = {'employees': employees}
    html = render(request, 'accounts/admin/employee_table_body.html', context).content
    return JsonResponse({'html': html.decode('utf-8')})

    # _________DeleteEmployee
def deleteEmployee(request, employee_id):
    # Retrieve the employee object
    employee = get_object_or_404(Employee, pk=employee_id)

    if request.method == 'POST':
        # Perform deletion logic here (e.g., employee.delete())
        employee.delete()
        return redirect('listEmployees')  # Redirect to the employee list page

    # If the request method is not POST, render a confirmation page
    context = {'employee': employee}
    return render(request, 'accounts/admin/delete_confirmation.html', context)
    
    # _________UpdateEmployee
def updateEmployee(request, employee_id):
    employee = get_object_or_404(Employee, employee_id=employee_id)
    form = EmployeeUpdateForm(request.POST or None, instance=employee)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('listEmployees')

    return render(request, 'accounts/admin/updateEmployee.html', {'form': form, 'employee': employee})


#_________________________ AllEmployees
    #_________ ProfileEmployees 
def create_profile(request):
    if request.method == 'POST':
        form = EmployeeProfileForm(request.POST)
        if form.is_valid():
            # Save the profile
            profile = form.save(commit=False)
            profile.employee = request.user
            profile.save()
            return redirect('profile_detail')  # Replace with the appropriate URL
    else:
        # Pass the user instance to the form
        form = EmployeeProfileForm(user_instance=request.user)

    return render(request, 'accounts/employees/create_profile.html', {'form': form})