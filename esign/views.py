from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import *
from .forms import *
from django.utils import timezone
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from datetime import datetime
from django.db.models import F

def index(request):
    user_id = request.session['user_id']
    documents = Document.objects.all()
    return render(request, 'esign/index.html', {'documents': documents, 'user_id': user_id})

def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            # Set session for logged-in user ID
            request.session['user_id'] = user.userID
            user_id = request.session['user_id']
            return redirect('esign:index')
        else:
            # Check for the presence of the 'logout' query parameter
            show_logout_modal = 'logout' in request.GET
            if show_logout_modal:
                # If not, return to login page again
                return render(request, 'esign/user_login.html', {'show_logout_modal': show_logout_modal})
            else:
                return render(request, 'esign/user_login.html', context)
    else:
        # Check for the presence of the 'logout' query parameter
        show_logout_modal = 'logout' in request.GET
        if show_logout_modal:
            # If not, return to login page again
            return render(request, 'esign/user_login.html', {'show_logout_modal': show_logout_modal})
        else:
            return render(request, 'esign/user_login.html', context)

def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)

    # Redirect user back to the login page with a query parameter
    # Redirect to the login page with a query parameter
    return redirect(reverse('esign:login') + '?logout=1')

def check_session(request):
    session_expired = not request.user.is_authenticated
    return JsonResponse({'session_expired': session_expired})

def handler403(request, exception, template_name='403.html'):
    return render(request, template_name, status=403)

def handler404(request, exception, template_name='404.html'):
    return render(request, template_name, status=404)

def handler500(request, template_name='500.html'):
    return render(request, template_name, status=500)



def save_pdf_to_db(request):
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_file = request.FILES['pdf_file']
        # Save the file and create a document in the database
        # Example code for saving the file to a Document model
        document = Document(title=pdf_file, pdf_file=pdf_file)
        document.save()

        user_id = request.session['user_id']
        # Create DocPermission object for the user
        doc_permission = DocPermission(userID_id=user_id, docID_id=document.docID, type='Owner')
        doc_permission.save()

        # Create URL object for the user
        url = URL(docID_id=document.docID, dpID_id=doc_permission.dpID, userID_id=user_id)
        url.save()
        
        # Return the primary key of the newly created document as JSON
        return JsonResponse({'newURL': url.url})
    else:
        return JsonResponse({'error': 'File upload failed'}, status=400)



    
###########     MANAGEMENT     ###########

def management(request, hashed_url):
    user_id = request.session['user_id']
    url = URL.objects.get(url=hashed_url)
    # Check if the hashed_url exists in the database
    if not url:
        return render(request, '404.html', status=404)
    
    # Check if the user is authorized to view the document
    if url.userID_id != user_id:
        return render(request, '403.html', status=403)
        # document = Document.objects.get(pk=url.docID_id)
        # return render(request, 'esign/test.html', {'url': url.userID_id, 'document': document, 'user_id': user_id})
    
    # Get the document object from the database
    document = Document.objects.get(pk=url.docID_id)
    docID = document.docID
    docCreate = document.created_date.strftime('%Y-%m-%dT%H:%M')
    docDue = document.due_date.strftime('%Y-%m-%dT%H:%M')
    # permission = DocPermission.objects.filter(docID_id=url.docID_id)

    # Get all unique UserIDs from DocPermission
    permission = DocPermission.objects.filter(docID_id=url.docID_id)
    unique_user_ids = permission.values_list('userID_id', flat=True).distinct()

    # Fetch all CustomUser objects with the unique_user_ids
    users = CustomUser.objects.filter(userID__in=unique_user_ids)
    
    # Fetching companies corresponding to unique_user_ids
    company_names = Organization.objects.filter(customuser__in=users).annotate(user_id=F('customuser__userID')).values_list('user_id', 'name').distinct()

    # Creating a dictionary with user_id as keys and company names as values
    user_company_names = {user_id: company_name for user_id, company_name in company_names}

    # Fetching roles corresponding to unique_user_ids
    role = DocPermission.objects.filter(docID_id=url.docID_id, userID_id__in=unique_user_ids)

    user_data = []

    for user_id in unique_user_ids:
        comps = user_company_names.get(user_id, 'No Company')  # Get the company name or set a default value

        # Fetching other user details as before
        user_details = CustomUser.objects.get(userID=user_id)
        username = user_details.username
        email = user_details.email
        role_for_user = role.filter(userID_id=user_id)

        # Appending the user data to the user_data list
        user_data.append((user_id, comps, username, email, role_for_user))



    companies = Organization.objects.all()  # Fetch all companies from the database
    return render(request, 'esign/manage.html', {'docID': docID, 'docCreate': docCreate, 'docDue': docDue, 'document': document, 'user_data': user_data, 'companies': companies, 'user_id': user_id})



def get_names_emails_for_company(request):
    # company_id = 'COM002'
    company_ids = request.POST.getlist('company_id')

    # return JsonResponse({'names': company_id})
    if company_ids:
        names = []
        for company_id in company_ids:
            try:
                # organization = Organization.objects.get(pk=company_id)
                # Fetch employees related to the company
                employees = CustomUser.objects.filter(orgID=company_id)
                # fetch customuser related to the company
                

                # Extract names and emails from employees
                names.extend([{'value': employee.pk, 'text': f'{employee.username} ({employee.email})'} for employee in employees])
                # emails = [{'value': employee.id, 'text': employee.email} for employee in employees]

                
            except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'CustomUser not found'})
        return JsonResponse({'names': names})
    else:
        return JsonResponse({'error': 'Company ID not provided'})



def update_document_title(request, document_id):
    if request.method == 'POST':
        new_title = request.POST.get('new_title')
        document = Document.objects.get(pk=document_id)
        document.title = new_title
        document.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def update_due(request):
    if request.method == 'POST':
        new_due = request.POST.get('new_due')
        document_id = request.POST.get('document_id')
        document = Document.objects.get(pk=document_id)

        # Assuming the new_due is in string format ('YYYY-MM-DDTHH:MM')
        new_due_datetime = datetime.strptime(new_due, '%Y-%m-%dT%H:%M')

        # Ensure new_due_datetime is timezone-aware
        new_due_timezone = timezone.make_aware(new_due_datetime, timezone=timezone.utc)

        # Set the document's due date to the adjusted time zone
        document.due_date = new_due_timezone
        document.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def update_permission(request):
    if request.method == 'POST':
        user_id = request.POST.get('selectedID')
        document_id = request.POST.get('document_id')
        new_role = request.POST.get('selectedRole')
        # Get the DocPermission object
        # Create DocPermission object for the user
        doc_permission = DocPermission(userID_id=user_id, docID_id=document_id, type=new_role)
        doc_permission.save()

        # Create URL object for the user
        url = URL(docID_id=document_id, dpID_id=doc_permission.dpID, userID_id=user_id)
        url.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})




def detail(request, pk):
    document = Document.objects.get(pk=pk)
    signatures = Signature.objects.filter(docID=document)
    return render(request, 'esign/detail.html', {'document': document, 'signatures': signatures})

def sign(request, pk):
    document = Document.objects.get(pk=pk)
    if request.method == 'POST':
        form = SignatureForm(request.POST, request.FILES)
        if form.is_valid():
            signature = form.save(commit=False)
            signature.document = document
            signature.signed_at = timezone.now()
            signature.save()
            return redirect('detail', pk=document.pk)
    else:
        form = SignatureForm()
    return render(request, 'esign/sign.html', {'form': form})