from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import *
from .forms import *
from django.utils import timezone
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from datetime import datetime
from django.db.models import F
from django.core.mail import send_mail
from django.contrib import messages
import re
import pyotp
from django.contrib.auth.decorators import login_required
import PyPDF2
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from django.http import HttpResponse
from PyPDF2 import PdfReader
from pyhanko.sign import fields
from pyhanko.sign.signers import SimpleSigner
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
# from pyhanko.stamp import ImageStampStyle

# def add_image_signature(request):
#     if request.method == 'POST' and request.FILES['pdf_file'] and request.FILES['image_file']:
#         pdf_file = request.FILES['pdf_file']
#         image_file = request.FILES['image_file']

#         # Saving the uploaded files
#         fs = FileSystemStorage()
#         pdf_filename = fs.save(pdf_file.name, pdf_file)
#         image_filename = fs.save(image_file.name, image_file)

#         # Open the PDF file
#         pdf_input = open(fs.path(pdf_filename), 'rb')
#         pdf_reader = PyPDF2.PdfReader(pdf_input)
#         pdf_writer = PyPDF2.PdfWriter()

#         # Choose a page to add the image signature
#         page_num = 0  # Change this to your desired page number

#         # Open the image file
#         img = open(fs.path(image_filename), 'rb')

#         # Get the PDF page and merge the image
#         page = pdf_reader.getPage(page_num)
#         page.merge_page(PyPDF2.PdfReader(img).getPage(0))
#         pdf_writer.addPage(page)

#         # Save the modified PDF
#         output_filename = 'output.pdf'
#         with open(output_filename, 'wb') as output:
#             pdf_writer.write(output)

#         pdf_input.close()
#         img.close()

#         return render(request, 'success.html', {'output_filename': output_filename})

#     return render(request, 'add_image_signature.html')

# def add_image_signature(request):
#     try:
#         # Paths to PDF and image file
#         pdf_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', 'System-Development-Method-With-The-Prototype-Method.pdf')
#         image_path = os.path.join(settings.MEDIA_ROOT, 'signatures', 'astra_avatar.png')

#         output_filename = 'output.pdf'

#         # Open the PDF file
#         pdf_input = open(pdf_path, 'rb')
#         pdf_reader = PyPDF2.PdfReader(pdf_input)
#         pdf_writer = PyPDF2.PdfWriter()

#         # Choose a page to add the image signature
#         page_num = 0  # Change this to your desired page number

#         # Open the image file
#         img = open(image_path, 'rb')

#         # Get the PDF page and merge the image
#         page = pdf_reader.pages[page_num]
#         img_page = PyPDF2.PdfReader(img).getPage(0)
        
#         # Ensure the image page has the required dimensions
#         img_page.mediaBox.upperRight = (
#             page.mediaBox.getUpperRight_x(),
#             page.mediaBox.getUpperRight_y()
#         )

#         page.merge_page(img_page)
#         pdf_writer.addPage(page)

#         # Save the modified PDF
#         output_path = os.path.join(settings.MEDIA_ROOT, output_filename)
#         with open(output_path, 'wb') as output:
#             pdf_writer.write(output)

#         pdf_input.close()
#         img.close()

#         output_url = os.path.join(settings.MEDIA_URL, output_filename)

#         return render(request, 'success.html', {'output_url': output_url})

#     except Exception as e:
#         # Handle exceptions, log errors, or display an error message
#         return render(request, 'esign/error.html', {'error_message': str(e)})

# def add_image_signature(request):
#     try:
#         # Paths to the main PDF and the watermark PDF
#         main_pdf_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', 'Tunku_Abdul_Rahman_University_of_Management_and_Technology_TAR_UMT_-_Student_Intran_Xs7fVdR.pdf')
#         watermark_pdf_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', 'watermark.pdf')

#         output_filename = 'output_with_watermark.pdf'

#         # Open the main PDF file
#         main_pdf_input = open(main_pdf_path, 'rb')
#         main_pdf_reader = PyPDF2.PdfReader(main_pdf_input)
#         main_pdf_writer = PyPDF2.PdfWriter()

#         # Open the watermark PDF file
#         watermark_pdf = open(watermark_pdf_path, 'rb')
#         watermark_pdf_reader = PyPDF2.PdfReader(watermark_pdf)
#         watermark_page = watermark_pdf_reader.pages[0]

#         # Merge each page of the main PDF on top of the watermark
#         for page_num in range(len(main_pdf_reader.pages)):
#             main_page = main_pdf_reader.pages[page_num]
#             main_page.merge_page(watermark_page)
#             main_pdf_writer.add_page(main_page)

#         # Save the modified PDF with the main content over the watermark
#         output_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', output_filename)
#         with open(output_path, 'wb') as output:
#             main_pdf_writer.write(output)

#         main_pdf_input.close()
#         watermark_pdf.close()

#         output_url = os.path.join(settings.MEDIA_URL, 'pdfs', output_filename)

#         return render(request, 'esign/success.html', {'output_url': output_url})

#     except Exception as e:
#         return render(request, 'error.html', {'error_message': str(e)})

# def add_signature_to_pdf(request):
#     # Paths to your PDF and signature image
#     pdf_path = 'media/pdfs/default.pdf'
#     signature_image_path = 'media/signature/astra_avatar.png'

#     signer = SimpleSigner.load(request.user.certificate_path, request.user.private_key_path, chain_path=request.user.chain_path)

#     writer = IncrementalPdfFileWriter(open(pdf_path, 'rb'))
#     sig_field_name = 'signature_field_name'  # Replace with the field name in your PDF where you want to add the signature

#     # Load the PDF field where the signature will be placed
#     field = fields.SignatureFormField(sig_field_name)
#     field.embedder = writer
#     field.prepare_general(writer.reader)

#     # Prepare the image for the signature
#     signature_image = ImageStampStyle.from_file(signature_image_path)

#     # Sign the PDF
#     sig_field_appearance = signer.sign(
#         writer, field, signature_image=signature_image, existing_fields_only=True
#     )

#     # Save the modified PDF
#     with open('path/to/save/modified_document.pdf', 'wb') as modified_pdf:
#         writer.write_in_place(modified_pdf)
    
#     return HttpResponse('Signature added successfully')

from PyPDF2 import PdfReader
from pyhanko.sign import fields, signers
from pyhanko.sign.signers import SimpleSigner
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
# from pyhanko.stamp import ImageStampStyle

# def add_image_signature(request):
#     # Paths to your PDF and signature image
#     pdf_path = 'media/pdfs/default.pdf'
#     signature_image_path = 'media/signature/astra_avatar.png'

#     signer = SimpleSigner.load(request.user.certificate_path, request.user.private_key_path, chain_path=request.user.chain_path)

#     writer = IncrementalPdfFileWriter(open(pdf_path, 'rb'))
#     sig_field_name = 'signature_field_name'  # Replace with the field name in your PDF where you want to add the signature

#     # Load the PDF field where the signature will be placed
#     field = fields.SignatureFormField(sig_field_name)
#     field.embedder = writer
#     field.prepare_general(writer.reader)

#     # Prepare the image for the signature
#     signature_image = ImageStampStyle.from_file(signature_image_path)

#     # Sign the PDF
#     sig_field_appearance = signer.sign(
#         writer, field, signature_image=signature_image, existing_fields_only=True
#     )

#     # Save the modified PDF
#     with open('media/pdfs//modified_document.pdf', 'wb') as modified_pdf:
#         writer.write_in_place(modified_pdf)
    
#     return HttpResponse('Signature added successfully')

from pyhanko import stamp
from pyhanko.pdf_utils import text, images
from pyhanko.pdf_utils.font import opentype
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign import fields, signers
from pyhanko.pdf_utils.layout import SimpleBoxLayoutRule, Margins, AxisAlignment
from pyhanko.pdf_utils.content import RawContent
from pyhanko.pdf_utils.reader import PdfFileReader
from pyhanko.sign.fields import SigFieldSpec


def add_image_signature(request):
    if request.method == 'POST':
        page_num = int(request.POST.get('page_num'))  # Get the page number from the submitted form data
        pdf_path = request.POST.get('pdf_path')  # Get the path to the PDF file from the submitted form data

        # Assuming 'pdf_file' is the uploaded PDF file from a Django form
        pdf_file = os.path.join(settings.MEDIA_ROOT, pdf_path)
        image_path = os.path.join(settings.MEDIA_ROOT, 'signatures', 'astra_avatar.png')

        # Setup the signature configuration
        # (Refer to PyHanko documentation for the exact configuration)
        signer = signers.SimpleSigner.load('media/cert/private_key.pem', "media/cert/certificate.pem", key_passphrase=b"12345")
        

        # Determine the dimensions of the PDF (assuming A4 size for this example)
        pdf_width, pdf_height = 595, 842  # A4 dimensions in points
        signature_box_width, signature_box_height = 200, 100  # Adjust as needed

        # Calculate the bottom right coordinates
        llx = pdf_width - signature_box_width  # Lower-left x-coordinate
        lly = 0  # Lower-left y-coordinate
        urx = pdf_width  # Upper-right x-coordinate
        ury = signature_box_height  # Upper-right y-coordinate

        # Adjust the layout rule for the stamp
        layout_rule = SimpleBoxLayoutRule(
            x_align=AxisAlignment.ALIGN_MID,  # or LEFT/RIGHT as per your need
            y_align=AxisAlignment.ALIGN_MIN,  # Aligns content to the top
            margins=Margins(0, 0, 0, 40)  # Adjust margins as needed
        )

        inner_layout_rule = SimpleBoxLayoutRule(
            x_align=AxisAlignment.ALIGN_MID,  # or LEFT/RIGHT as per your need
            y_align=AxisAlignment.ALIGN_MIN,  # Aligns content to the top
            margins=Margins(0, 0, 0, 0)  # Adjust margins as needed
        )

        # Read the PDF file
        with open(pdf_file, 'rb') as pdf_input:
            reader = PdfFileReader(pdf_input)
            pdf_reader = PyPDF2.PdfReader(pdf_input)
            w = IncrementalPdfFileWriter(pdf_input)
            # Loop through each page and add a signature field
            # for page_num in range(len(pdf_reader.pages)):
                # Calculate signature field position for each page
                # Adjust these values as needed
            signature_meta = signers.PdfSignatureMetadata(field_name=f'Signature_{page_num}')
            fields.append_signature_field(
                w, sig_field_spec=SigFieldSpec(
                    f'Signature_{page_num}', box=(llx, lly, urx, ury), on_page=page_num-1
                )
            )
            pdf_signer = signers.PdfSigner(
                signature_meta, signer=signer, stamp_style=stamp.TextStampStyle(
                    # the 'signer' and 'ts' parameters will be interpolated by pyHanko, if present
                    stamp_text='This is custom text!\nSigned by: %(signer)s\nTime: %(ts)s',
                    text_box_style=text.TextBoxStyle(
                        font=opentype.GlyphAccumulatorFactory('media/font/NotoSans-Regular.ttf')
                    ),
                    background=images.PdfImage(image_path),
                    background_layout=layout_rule,
                    inner_content_layout=inner_layout_rule,
                    border_width=0
                ),
            )
            with open('media/signed/document-signed.pdf', 'wb') as outf:
                pdf_signer.sign_pdf(w, output=outf)

        return JsonResponse({'status': 'success', 'message': 'Page signed successfully'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})





@login_required(login_url='esign:xlogin')
def index(request):
    user_id = request.session['user_id']
    # Get all documents for the user
    documents = []
    # documents = Document.objects.filter(docID__in=DocPermission.objects.filter(userID_id=user_id).values_list('docID_id', flat=True))

    # get all the url for the documents
    urls = URL.objects.filter(userID_id=user_id).values_list('url', flat=True)

    for user_id in urls:
        # get documents for the user
        documents.append(Document.objects.get(docID=URL.objects.get(url=user_id).docID_id))

    user_id = request.session['user_id']

    # zip the documents and urls together
    documents_urls = zip(documents, urls)
    return render(request, 'esign/index.html', {'documents_urls': documents_urls, 'user_id': user_id})

# Error page for non-logged in users
def xlogin(request):
    return render(request, 'esign/xlogin.html')

def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        
        userID = request.POST['UID']
        password = request.POST['psw']

        # Custom validation for member ID format
        if not re.match(r'^USE\d{3}$', userID):
            # Return an error message if the format is incorrect
            context['error'] = "Wrong member ID. Please try again."
            return render(request, 'esign/user_login.html', context)

        user = authenticate(request, userID=userID, password=password)
        if user is not None:
            if user.MFA:  # Check if MFA is enabled for the user
                # If MFA is enabled, proceed to generate OTP and verify
                login(request, user)
                # Generate a TOTP secret key for the user
                totp = pyotp.TOTP(pyotp.random_base32(), interval=60)  # You can change the interval as needed
                
                # Store TOTP secret in session for the user
                request.session['totp_secret'] = totp.secret
                # Calculate TOTP code based on the secret
                totp_code = totp.now()
                # Send TOTP code via email
                send_totp_email(user.email, totp_code)
                request.session['email'] = user.email
                
                return render(request, 'esign/verify_totp.html', {'user_id': user.userID, 'totp_code': totp_code})
            else:
                # If MFA is not enabled, redirect to the index page
                login(request, user)
                request.session['user_id'] = user.userID
                return redirect('esign:index')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')  # Error message if login fails
            return render(request, 'esign/user_login.html', context)
    else:
        # Check for the presence of the 'logout' query parameter
        show_logout_modal = 'logout' in request.GET
        if show_logout_modal:
            # If not, return to login page again
            logout(request)
            return render(request, 'esign/user_login.html', {'show_logout_modal': show_logout_modal})
        else:
            return render(request, 'esign/user_login.html', context)

def send_totp_email(email, totp_code):
    subject = 'Your TOTP Code'
    message = f'Your TOTP code is: {totp_code}'
    from_email = 'd34482807@gmail.com'
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)

def resend_totp(request):
    if request.method == "POST":
        email = request.POST.get('email')  # Assuming you'll send the TOTP to a provided email
        user_id = request.POST.get('user_id')
        
        # Generate a new TOTP code
        totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
        request.session['totp_secret'] = totp.secret
        totp_code = totp.now()

        # Store the new TOTP secret in session
        
        request.session['email'] = email

        # Send the new TOTP code via email
        send_totp_email(email, totp_code)

        # Return a JSON response indicating success
        return JsonResponse({'success': True, 'message': 'TOTP code resent successfully.'})
    else:
        # Return an error message if the request method is not POST
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@login_required(login_url='esign:xlogin')    
def verify_totp(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        email = request.POST.get('email')
        totp_code = request.POST.get('totp_code')
        
        # Retrieve the stored TOTP secret from the session
        stored_secret = request.session.get('totp_secret')
        if stored_secret:
            # Verify the entered TOTP code
            totp = pyotp.TOTP(stored_secret, interval=60)  # Use the same interval as generated before
            if totp.verify(totp_code):
                # TOTP code is valid, proceed with user authentication
                # Set up your login logic here
                request.session['user_id'] = user_id
                return redirect('esign:index')  # Redirect to a success page
            else:
                # TOTP code is invalid
                request.session['totp_secret'] = totp_code
                request.session['email'] = email
                messages.error(request, 'Invalid TOTP code. Please login again.')
                logout(request)
                return redirect('esign:login')
        else:
            # TOTP secret not found in session, handle error
            messages.error(request, 'Error: TOTP secret not found. Please login again.')
            logout(request)
            return redirect('esign:login')  # Redirect to login page with error message
    else:
        # Handle non-POST requests if needed
        pass

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

###############      ERROR PAGES      ################
def handler403(request, exception, template_name='403.html'):
    return render(request, template_name, status=403)

def handler404(request, exception, template_name='404.html'):
    return render(request, template_name, status=404)

def handler500(request, template_name='500.html'):
    return render(request, template_name, status=500)
###############      ERROR PAGES      ################


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
@login_required(login_url='esign:xlogin')
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

    chkPermission = DocPermission.objects.get(docID_id=url.docID_id, userID_id=user_id)

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
    owners_data = []

    remarks = Remark.objects.filter(docID_id=document)

    remark_data = []

    for remark in remarks:
        # Fetch the user associated with the remark
        user = CustomUser.objects.get(pk=remark.userID_id)
        
        # Extract required data from the user and remark objects
        username = user.username
        content = remark.content
        created_date = remark.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Format date as needed
        
        # Create a dictionary with the required data
        remark_info = {
            'username': username,
            'content': content,
            'created_date': created_date
        }
        
        # Append the remark information to the remark_data list
        remark_data.append(remark_info)

    if chkPermission.type != 'Owner':
        for user_id in unique_user_ids:
            comps = user_company_names.get(user_id, 'No Company')  # Get the company name or set a default value

            # Fetching other user details as before
            user_details = CustomUser.objects.get(userID=user_id)
            username = user_details.username
            email = user_details.email
            role_for_user = role.filter(userID_id=user_id)

            # Check if the user has 'Owner' role
            if role_for_user.filter(type='Owner').exists():
                # If the user is an owner, store their data in the owners_data list
                owners_data.append((user_id, comps, username, email, role_for_user))

            else:
                # If the user is not an owner, store their data in the user_data list
                user_data.append((user_id, comps, username, email, role_for_user))

        docDue = document.due_date.strftime('%Y-%m-%d %H:%M')
        return render(request, 'esign/signer.html', {'hashed_url': hashed_url, 'docID': docID, 'docCreate': docCreate, 'docDue': docDue, 'document': document, 'user_data': user_data, 'owners_data':owners_data, 'user_id': user_id, 'remark_data': remark_data})

    for user_id in unique_user_ids:
        comps = user_company_names.get(user_id, 'No Company')  # Get the company name or set a default value

        # Fetching other user details as before
        user_details = CustomUser.objects.get(userID=user_id)
        username = user_details.username
        email = user_details.email
        role_for_user = role.filter(userID_id=user_id)

        user_data.append((user_id, comps, username, email, role_for_user))

    companies = Organization.objects.all()  # Fetch all companies from the database
    return render(request, 'esign/manage.html', {'hashed_url': hashed_url, 'docID': docID, 'docCreate': docCreate, 'docDue': docDue, 'document': document, 'user_data': user_data, 'companies': companies, 'user_id': user_id, 'remark_data': remark_data})



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

def add_remark(request):
    if request.method == 'POST':
        # Extract the remark content from the submitted form data
        remark_content = request.POST.get('remark')
        document_id = request.POST.get('doc_id')  # Pass document ID from the frontend form
        user_id = request.session.get('user_id')  # Get the logged-in user ID from the session

        # Create and save the new Remark instance
        new_remark = Remark(content=remark_content, docID_id=document_id, userID_id=user_id)
        new_remark.save()

        # You can return a success response or handle it as needed
        return JsonResponse({'message': 'Remark added successfully'})

    # Handle invalid requests or methods
    return JsonResponse({'message': 'Invalid request'}, status=400)

###########     MANAGEMENT     ###########


###########     Sign / View     ###########
@login_required(login_url='esign:xlogin')
def sign(request, hashed_url):
        
    user_id = request.session['user_id']
    url = URL.objects.get(url=hashed_url)
    # Check if the hashed_url exists in the database
    if not url:
        return render(request, '404.html', status=404)
    
    # Check if the user is authorized to view the document
    if url.userID_id != user_id:
        return render(request, '403.html', status=403)
    
    # Get the document object from the database
    document = Document.objects.get(pk=url.docID_id)
    docID = document.docID

    chkPermission = DocPermission.objects.get(docID_id=url.docID_id, userID_id=user_id)

    remarks = Remark.objects.filter(docID_id=document)

    remark_data = []

    for remark in remarks:
        # Fetch the user associated with the remark
        user = CustomUser.objects.get(pk=remark.userID_id)
        
        # Extract required data from the user and remark objects
        username = user.username
        content = remark.content
        created_date = remark.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Format date as needed
        
        # Create a dictionary with the required data
        remark_info = {
            'username': username,
            'content': content,
            'created_date': created_date
        }
        
        # Append the remark information to the remark_data list
        remark_data.append(remark_info)

    if chkPermission.type != 'Owner':
        return render(request, 'esign/sign.html', {'hashed_url': hashed_url, 'docID': docID, 'document': document, 'user_id': user_id, 'remark_data': remark_data})

    return render(request, 'esign/view.html', {'hashed_url': hashed_url, 'docID': docID, 'document': document, 'user_id': user_id, 'remark_data': remark_data})