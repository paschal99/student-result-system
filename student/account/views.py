from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import *



def index(request):
    return render(request, 'index.html')


def register_program(request):
    if request.method == 'POST':
        program_name = request.POST.get('program_name')  # Get data from form
        if program_name:  # Check if there's valid input
            new_program = Program(name=program_name)
            new_program.save()  # Save the new Program to the database
            messages.success(request, 'Program registered successfully!')
            return redirect('register_program')  # Redirect to clear the form
        else:
            messages.error(request, 'Please enter a program name.')

    # Render the HTML template
    return render(request, 'dashboard/register_programm.html', {})


def register_user(request):
    if request.method == 'POST':
        # Get form data from POST request
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Validate input and handle errors
        if not username or not password or not email:
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'signup.html')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'signup.html')

        # Create a new User instance and save it
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        # Log in the user automatically after successful registration
        login(request, user)
        messages.success(request, "Registration successful!")

        # Redirect to a desired page (like 'patient_dashboard' or 'home')
        return redirect('dashboard')

    # If not POST, render the signup page with the form
    return render(request, 'signup.html')

def login_user(request):
    if request.method == 'POST':
        # Get form data from POST request
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Log in the user
            messages.success(request, "Successfully logged in!")
            # Redirect to the desired page after login
            return redirect('dashboard')  # Replace 'home' with your desired page
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')  # Render login page on GET request or failed login



def logout_user(request):
    logout(request)  # Log out the current user
    messages.success(request, "You have been logged out.")  # Feedback message
    return redirect('login')


def dashboard(request):
    # Get the logged-in user's information
    user = request.user
    total_students = Student.objects.count()  # Get the total count of Student objects

    # Calculate the total number of subjects offered
    total_subjects = Subject.objects.count()  # Get the total count of Subject objects

    context = {
        'total_students': total_students,  # Total number of students
        'total_subjects': total_subjects,  # Total number of subjects
    }


    return render(request, 'dashboard/dashboard.html',context)

def register_student(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        sex = request.POST.get('sex')
        program_id = request.POST.get('program')

        # Validate the required fields
        if not first_name or not last_name or not sex or not program_id:
            messages.error(request, "All fields are required.")
            return render(request, 'dashboard/register_student.html')

        # Validate that program_id is a valid integer
        try:
            program_id = int(program_id)  # Convert to integer
        except ValueError:
            messages.error(request, "Invalid program ID.")
            return HttpResponseBadRequest("Invalid program ID.")

        # Create a new student
        try:
            program = Program.objects.get(id=program_id)  # Validate program exists
        except Program.DoesNotExist:
            messages.error(request, "Selected program does not exist.")
            return render(request, 'dashboard/register_student.html')

        student = Student(
            first_name=first_name,
            last_name=last_name,
            sex=sex,
            program=program
        )
        student.save()  # Save the new student to the database

        messages.success(request, "Student registered successfully!")
        return redirect('dashboard')  # Redirect after successful registration

    # Retrieve all programs for the dropdown menu
    programs = Program.objects.all()

    return render(request, 'dashboard/register_student.html', {'programs': programs})

def enter_student_marks(request):
    if request.method == 'POST':
        # Extract form data from POST request
        student_id = request.POST.get('student')  # Extract student ID
        subject_id = request.POST.get('subject')  # Extract subject ID
        grade_id = request.POST.get('grade')  # Extract grade ID

        # Validate that all required fields are present
        if not student_id or not subject_id or not request.POST.get('marks') or not grade_id:
            messages.error(request, "All fields are required.")
            return render(request, 'dashboard/enter_student_marks.html', {
                'students': Student.objects.all(),
                'subjects': Subject.objects.all(),
                'grades': Grade.objects.all(),
            })

        # Validate the 'marks' field to ensure it's a valid integer
        try:
            marks = int(request.POST.get('marks'))  # Convert 'marks' to integer
        except ValueError:
            messages.error(request, "Invalid marks value. Please enter a valid number.")
            return render(request, 'dashboard/enter_student_marks.html', {
                'students': Student.objects.all(),
                'subjects': Subject.objects.all(),
                'grades': Grade.objects.all(),
            })

        # Validate marks range
        if marks < 0 or marks > 100:
            messages.error(request, "Marks should be between 0 and 100.")
            return render(request, 'dashboard/enter_student_marks.html', {
                'students': Student.objects.all(),
                'subjects': Subject.objects.all(),
                'grades': Grade.objects.all(),
            })

        # Get the related objects
        try:
            student = Student.objects.get(id=student_id)
            subject = Subject.objects.get(id=subject_id)
            grade = Grade.objects.get(id=grade_id)
        except (Student.DoesNotExist, Subject.DoesNotExist, Grade.DoesNotExist):
            messages.error(request, "Invalid data provided. Ensure the student, subject, and grade are correct.")
            return render(request, 'dashboard/enter_student_marks.html', {
                'students': Student.objects.all(),
                'subjects': Subject.objects.all(),
                'grades': Grade.objects.all(),
            })

        # Create and save the new Marks instance
        mark_entry = Marks(
            student=student,
            subject=subject,
            marks=marks,
            grade=grade
        )
        mark_entry.save()

        messages.success(request, "Marks entered successfully!")
        return redirect('dashboard')  # Redirect on successful entry

    # Handle GET requests to display the form
    context = {
        'students': Student.objects.all(),
        'subjects': Subject.objects.all(),
        'grades': Grade.objects.all(),
    }
    return render(request, 'dashboard/enter_student_marks.html', context)

def view_all_marks(request):
    # Retrieve all marks from the database
    all_marks = Marks.objects.all()  # Get all marks

    # Set up pagination with 10 items per page (adjust as needed)
    paginator = Paginator(all_marks, 10)  # 10 marks per page
    page_number = request.GET.get('page')  # Get the current page from the query parameters
    page = paginator.get_page(page_number)  # Get the data for the current page

    # Pass the paginated data to the template
    context = {
        'page': page,  # The paginated data
    }

    return render(request, 'dashboard/view_all_marks.html', context)  # Template for displaying marks

def edit_marks(request, marks_id):
    # Get the specified Marks record
    marks = get_object_or_404(Marks, id=marks_id)

    if request.method == 'POST':
        # Handle form submission
        form = EditMarksForm(request.POST, instance=marks)  # Bind form to existing Marks record
        if form.is_valid():
            form.save()  # Save the changes
            messages.success(request, "Marks updated successfully!")
            return redirect('view_marks')  # Redirect to the view with all marks
        else:
            messages.error(request, "Please correct the errors below.")

    else:
        # Display the form with existing data (GET request)
        form = EditMarksForm(instance=marks)

    # Pass the form to the template
    context = {'form': form}
    return render(request, 'dashboard/edit_marks.html', context)

def search_students(request):
    # Retrieve query parameters from the request
    query = request.GET.get('query')  # Search by name
    program_id = request.GET.get('program')  # Get the program ID from query params
    sex = request.GET.get('sex')  # Get the sex from query params
    page_number = request.GET.get('page')  # Get the page number for pagination

    # Handle empty or 'None' values explicitly for better clarity and prevent ValueErrors
    if program_id == '' or program_id == 'None':
        program_id = None
    elif program_id is not None:
        try:
            # Convert program_id to integer
            program_id = int(program_id)
        except ValueError:
            # If program_id is not a valid integer, return a bad request
            return HttpResponseBadRequest("Invalid program ID")

    # Initialize the base queryset
    students = Student.objects.all()

    # Apply search by name (if `query` is provided and is not 'None' or empty)
    if query and query.strip().lower() != 'none':
        students = students.filter(
            first_name__icontains=query
        ) | students.filter(
            last_name__icontains=query
        )

    # Apply filtering by program_id (if valid)
    if program_id is not None:
        students = students.filter(program_id=program_id)

    # Apply filtering by sex (if provided and not empty or 'none')
    if sex and sex.strip().lower() != 'none':
        students = students.filter(sex=sex)

    # Set up pagination with proper error handling
    try:
        paginator = Paginator(students, 2)  # 2 items per page
        page = paginator.get_page(page_number)  # Get the current page's data
    except ValueError:
        # Handle invalid page numbers, if needed
        return HttpResponseBadRequest("Invalid page number")

    # Fetch all programs for the context
    programs = Program.objects.all()

    # Set up the context for the template
    context = {
        'page': page,  # Paginated data
        'programs': programs,
        'query': query,
        'selected_program': program_id,
        'selected_sex': sex,
    }

    # Render the template with the context
    return render(request, 'dashboard/search_students.html', context)
# Render the template


def register_subject(request):
    if request.method == 'POST':
        # Extract form data from POST request
        name = request.POST.get('name')  # Subject name
        subject_code = request.POST.get('subject_code')  # Subject code

        # Validate data
        if not name or not subject_code:
            messages.error(request, "Name and Subject Code are required.")  # Error handling
            return render(request, 'dashboard/register_subject.html')  # Re-render the form

        # Check if the subject code is unique
        if Subject.objects.filter(subject_code=subject_code).exists():
            messages.error(request, "Subject Code must be unique.")  # Error handling for unique constraint
            return render(request, 'dashboard/register_subject.html')  # Re-render the form

        # Create and save the new subject
        new_subject = Subject(name=name, subject_code=subject_code)
        new_subject.save()  # Save to the database

        messages.success(request, "Subject registered successfully!")  # Success message
        return redirect('dashboard')  # Redirect after successful registration

    # Render the form for GET requests
    return render(request, 'dashboard/register_subject.html')  # Template for subject registration


def register_grade(request):
    if request.method == 'POST':
        # Extract form data from POST request
        name = request.POST.get('name')  # Grade name (e.g., "A", "B", etc.)

        # Validate data
        if not name:
            messages.error(request, "Grade name is required.")  # Error handling
            return render(request, 'dashboard/register_grade.html')  # Re-render the form

        # Check if the grade name is unique
        if Grade.objects.filter(name=name).exists():
            messages.error(request, "Grade must be unique.")  # Error handling for unique constraint
            return render(request, 'dashboard/register_grade.html')  # Re-render the form

        # Create and save the new grade
        new_grade = Grade(name=name)  # Create the Grade instance
        new_grade.save()  # Save it to the database

        messages.success(request, "Grade registered successfully!")  # Success message
        return redirect('dashboard')  # Redirect after successful registration

    # Render the form for GET requests
    return render(request, 'dashboard/register_grade.html')

def change_password(request):
    if request.method == 'POST':
        # Create a PasswordChangeForm instance with the POST data
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            # Save the new password
            user = form.save()
            # Keep the user logged in after changing the password
            update_session_auth_hash(request, user)
            # Display a success message
            messages.success(request, 'Your password was successfully updated!')
            # Redirect to a desired page after a successful change
            return redirect('dashboard')  # Redirect to the dashboard or other page
        else:
            # Handle form validation errors
            messages.error(request, 'Please correct the errors below.')

    else:
        # Display the password change form
        form = PasswordChangeForm(request.user)  # For GET requests

    return render(request, 'dashboard/change_password.html', {'form': form})



def list_programs(request):
    programs = Program.objects.all()  # Fetch all programs from the database
    return render(request, 'dashboard/list_programs.html', {'programs': programs})


def list_subject(request):
    subjects = Subject.objects.all()  # Fetch all programs from the database
    return render(request, 'dashboard/subject.html', {'subjects': subjects})