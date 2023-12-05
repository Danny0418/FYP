from django.shortcuts import render, redirect
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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .utils import is_ajax, classify_face
import base64
from django.core.files.base import ContentFile

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
from django.contrib.gis.geoip2 import GeoIP2
from ipware import get_client_ip
from datetime import datetime, timedelta
import pytz

def add_image_signature(request):
    if request.method == 'POST':
        # Get the user's IP address
        client_ip = request.META.get('HTTP_X_FORWARDED_FOR', '180.75.247.19')
        # client_ip, _ = get_client_ip(request)

        # Get geolocation information based on the IP address
        if client_ip:
            geoip = GeoIP2()
            location = geoip.city(request.META.get('HTTP_X_FORWARDED_FOR', '180.75.247.19'))
            #  location = geoip.city(client_ip)
            geolocation_info = {
                'IP Address': client_ip,
                'City': location.get('city', ''),
                'Country': location.get('country_name', ''),
                'Region': location.get('region', ''),
            }
        else:
            geolocation_info = {
                'IP Address': 'N/A',
                'City': 'N/A',
                'Country': 'N/A',
                'Region': 'N/A',
            }
        
        # Add geolocation and IP information to the PDF
        # info_text = "\n".join(f"{key}: {value}" for key, value in geolocation_info.items())

        # Get the current UTC time and convert it to UTC+08
        current_utc_time = datetime.now(pytz.utc)
        utc_plus_8 = pytz.timezone('Asia/Shanghai')  # You can adjust this to any UTC+08 timezone
        current_time_utc_plus_8 = current_utc_time.astimezone(utc_plus_8)

        # Format the time
        formatted_time = current_time_utc_plus_8.strftime('%I:%M:%S %p UTC+08')

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
            margins=Margins(0, 0, 0, 50)  # Adjust margins as needed
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
                    stamp_text='Signed by: %(signer)s\nTime: ' + formatted_time +'\n' + 'IP Address: ' + geolocation_info['IP Address'] + '\nRegion: ' + geolocation_info['City'] + ', ' + geolocation_info['Country'],
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






###############      ERROR PAGES      ################
# Error page for non-logged in users
def xlogin(request):
    return render(request, 'esign/xlogin.html')

# Error 403 page
def handler403(request, exception, template_name='403.html'):
    return render(request, template_name, status=403)

# Error 404 page
def handler404(request, exception, template_name='404.html'):
    return render(request, template_name, status=404)

# Error 500 page
def handler500(request, template_name='500.html'):
    return render(request, template_name, status=500)
###############      ERROR PAGES      ################


###############      Authentication + MFA      ################

# Login module
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

# generate TOTP redirect and send email notification
def send_totp_email(email, totp_code):
    subject = 'Your TOTP Code'
    message = f'Your TOTP code is: {totp_code}'
    from_email = 'd34482807@gmail.com'
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)

# Regenerate TOTP code
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

# MFA page
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

# Logout module
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)

    # Redirect to the login page with a query parameter
    return redirect(reverse('esign:login') + '?logout=1')

# session checking
def check_session(request):
    session_expired = not request.user.is_authenticated
    return JsonResponse({'session_expired': session_expired})
###############      Authentication + MFA      ################


###############      LANDING PAGES      ################
@login_required(login_url='esign:xlogin')
def index(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return render(request, '404.html', {'error_message': 'User ID not found'})

    try:
        user = CustomUser.objects.get(userID=user_id)
        # Get all documents assigned to the user
        assigned_documents = Document.objects.filter(docpermission__userID=user)
    except CustomUser.DoesNotExist:
        return render(request, '404.html', {'error_message': 'User not found'})

    documents_per_page = 5
    paginator = Paginator(assigned_documents, documents_per_page)
    page = request.GET.get('page', 1)

    try:
        documents = paginator.page(page)
    except PageNotAnInteger:
        documents = paginator.page(1)
    except EmptyPage:
        documents = paginator.page(paginator.num_pages)

    return render(request, 'esign/main.html', {'documents': documents, 'user_id': user_id})

# Display brief information about the selected document in the landing page
def get_document_details(request):
    if 'doc_id' in request.GET:
        doc_id = request.GET['doc_id']
        try:
            document = Document.objects.get(pk=doc_id)
            assigned_users = DocPermission.objects.filter(docID=document)
            users_info = []

            for permission in assigned_users:
                user_info = {
                    'userID': permission.userID.userID,
                    'username': permission.userID.username,
                    'email': permission.userID.email,
                    'position': permission.userID.position,
                }
                users_info.append(user_info)

            data = {
                'document': {
                    'title': document.title,
                    'created_date': document.created_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'due_date': document.due_date.strftime('%Y-%m-%d %H:%M:%S'),
                },
                'assigned_users': users_info,
            }

            return JsonResponse(data)

        except Document.DoesNotExist:
            print(f"Document with ID {doc_id} does not exist.")
            return JsonResponse({'error': 'Document not found'}, status=404)

    else:
        return JsonResponse({'error': 'Document ID not provided'}, status=400)

# Redirect to management function
def viewDoc(request, docID):
    user_id = request.session['user_id']
    urls = URL.objects.get(docID_id=docID, userID_id=user_id)
    hashed_url = urls.url

    return redirect('esign:management', hashed_url=hashed_url)

# Upload documents
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
###############      LANDING PAGES      ################


    
###############      MANAGEMENT      ################
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

    if chkPermission.type != 'Owner':
        docDue = document.due_date.strftime('%Y-%m-%d %H:%M')
        return render(request, 'esign/signer.html', {'hashed_url': hashed_url, 'docID': docID, 'docCreate': docCreate, 'docDue': docDue, 'document': document, 'user_data': user_data, 'owners_data':owners_data, 'user_id': user_id, 'remark_data': remark_data})

    mail = document.email_sent
    if mail is True:
        docDue = document.due_date.strftime('%Y-%m-%d %H:%M')
        return render(request, 'esign/owner.html', {'hashed_url': hashed_url, 'docID': docID, 'docCreate': docCreate, 'docDue': docDue, 'document': document, 'user_data': user_data, 'owners_data':owners_data, 'user_id': user_id, 'remark_data': remark_data})
    
    user_data = []
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

# Retrieving company members from the database base on selected company
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

# Send email notification to signers
def signer_email(request):
    if request.method == 'POST':
        doc_id = request.POST.get('docID')
        users_with_permission = DocPermission.objects.filter(docID_id=doc_id).select_related('userID')

        subject = 'Document Update'
        from_email = 'd34482807@gmail.com'
        for permission in users_with_permission:
            if permission.type != 'Owner':
                user = permission.userID
                recipient_list = [user.email]

                urlObj = URL.objects.get(dpID_id=permission.dpID)
                message = 'There is an update to the document you have permission to access.\n\n' + 'Link: ' + urlObj.url
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        # Update the Document's email_sent flag
        doc = Document.objects.get(docID=doc_id)
        doc.email_sent = True
        doc.save()
        return JsonResponse({'status': 'success', 'message': 'Emails sent successfully'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

# Send email notification to owners    
def owner_email(request):
    if request.method == 'POST':
        doc_id = request.POST.get('docID')
        user_id = request.POST.get('userID')
        permission = DocPermission.objects.get(docID_id=doc_id, userID_id=user_id)

        subject = 'Document Update'
        from_email = 'd34482807@gmail.com'
        
        user = permission.userID
        recipient_list = [user.email]

        urlObj = URL.objects.get(dpID_id=permission.dpID)
        message = 'There is an update to the document you have permission to access.\n\n' + 'Link: ' + urlObj.url
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        # Update the Document's email_sent flag
        doc = Document.objects.get(docID=doc_id)
        doc.email_sent = True
        doc.save()
        return JsonResponse({'status': 'success', 'message': 'Emails sent successfully'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


# Change document title (Owner)
def update_document_title(request, document_id):
    if request.method == 'POST':
        new_title = request.POST.get('new_title')
        document = Document.objects.get(pk=document_id)
        document.title = new_title
        document.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

# Update due date (Owner)
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

# Create new role (Owner)
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

# Change role (Owner)
def update_role(request):
    if request.method == 'POST':
        user_id = request.POST.get('id')
        document_id = request.POST.get('doc')
        new_role = request.POST.get('role')
        # Get the DocPermission object
        # Create DocPermission object for the user
        doc_permission = DocPermission.objects.get(userID_id=user_id, docID_id=document_id)
        doc_permission.type = new_role
        doc_permission.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

# Remove role (Owner)
def delete_permission(request):
    if request.method == 'POST':
        user_id = request.POST.get('id')
        document_id = request.POST.get('doc')
        
        try:
            # Try to get the existing permission record
            doc_permission = DocPermission.objects.get(userID_id=user_id, docID_id=document_id)
            
            # Delete the permission record
            doc_permission.delete()
            
            return JsonResponse({'success': True, 'message': 'Permission deleted successfully'})
        except DocPermission.DoesNotExist:
            # Permission record does not exist
            return JsonResponse({'success': False, 'message': 'Permission not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

# Remark module
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

###############      MANAGEMENT      ################


###############      ESIGNATURE      ################
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

    if chkPermission.priority == 0:
        return render(request, 'esign/sign.html', {'hashed_url': hashed_url, 'docID': docID, 'document': document, 'user_id': user_id, 'remark_data': remark_data})

    chkPersonalDoc = PersonalDoc.objects.get(dpID_id=chkPermission.dpID)
    chkPage = chkPersonalDoc.page

    if chkPermission.priority == 1:
        return render(request, 'esign/sign.html', {'hashed_url': hashed_url, 'docID': docID, 'document': document, 'user_id': user_id, 'remark_data': remark_data, 'chkPersonalDoc': chkPersonalDoc, 'chkPage': chkPage})
    
    return render(request, 'esign/view.html', {'hashed_url': hashed_url, 'docID': docID, 'document': document, 'user_id': user_id, 'remark_data': remark_data, 'chkPersonalDoc': chkPersonalDoc, 'chkPage': chkPage})

def face_detection_view(request):
    return render(request, 'esign/face_detection.html', {})

@login_required
def homw_view(request):
    return render(request, 'esign/home.html', {})

def draw_signature(request):
    context = {}
    return render(request, 'esign/draw_signature.html', context)

def type_signature(request):
    context = {}
    return render(request, 'esign/type_signature.html', context)
###############      ESIGNATURE      ################


###############      PROFILE      ################
def find_user_view(request):
    if is_ajax(request):
        photo = request.POST.get('photo')
        user_id = request.POST.get('user_id')
        print("Request Photo:", photo)
        print("Request User ID:", user_id)
        
        if photo is not None:
            _, str_img = photo.split(';base64,')
            decoded_file = base64.b64decode(str_img)

            x = Log()
            x.photo = ContentFile(decoded_file, name='upload.png')
            x.save()

            
            res = classify_face(x.photo.path)
            user_exists = CustomUser.objects.filter(username=res).exists()

            if user_exists:
                user = CustomUser.objects.get(username=res)

                if user.userID == user_id:
                    profile = Profile.objects.get(user=user)
                    x.profile = profile
                    x.save()

                    login(request, user)
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({'error': 'User not found'})
            else:
                return JsonResponse({'error': 'Photo not found'})
            
def upload_profile(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        if form.is_valid():
            form.save()
            return redirect('esign:profile')
    else:
        form = ProfileForm(instance=user.profile)

    return render(request, 'esign/upload_profile.html', {'form': form, 'user': user})
    
def profile(request):
    user = request.user

    if hasattr(user, 'profile'):
        profile = user.profile
        return render(request, 'esign/profile.html', {'user': user, 'profile': profile})
    else:
        return render(request, '404.html', {'user': user})
    ###############      PROFILE      ################