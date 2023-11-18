from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from .forms import *
from django.utils import timezone
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse

def index(request):
    documents = Document.objects.all()
    return render(request, 'esign/index.html', {'documents': documents})

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

def handler404(request, exception, template_name='404.html'):
    return render(request, template_name, status=404)




def save_pdf_to_db(request):
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_file = request.FILES['pdf_file']
        # Save the file and create a document in the database
        # Example code for saving the file to a Document model
        document = Document(title=pdf_file, pdf_file=pdf_file)
        document.save()
        
        # Return the primary key of the newly created document as JSON
        return JsonResponse({'newest_pk': document.pk})
    else:
        return JsonResponse({'error': 'File upload failed'}, status=400)


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
    


def management(request, pk):
    document = Document.objects.get(pk=pk)
    companies = Organization.objects.all()  # Fetch all companies from the database
    return render(request, 'esign/manage.html', {'document': document, 'companies': companies})

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