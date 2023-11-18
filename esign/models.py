from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib import admin
import hashlib

def validate_pdf_extension(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError('Only PDF files are allowed.')

def default_pdf_path():
    # Replace 'default.pdf' with the actual path to your default PDF file
    return 'pdfs/default.pdf'

class Organization(models.Model):
    orgID = models.CharField(max_length=6, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    address = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=15, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.orgID:
            # Get the latest organization
            latest_org = Organization.objects.order_by('-orgID').first()

            if latest_org:
                # Extract the numeric part, increment, and format the new ID
                new_id = int(latest_org.orgID[3:]) + 1
                self.orgID = 'COM' + str(new_id).zfill(3)
            else:
                # If there are no organizations, start with COM001
                self.orgID = 'COM001'

        super(Organization, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    userID = models.CharField(max_length=6, primary_key=True)
    orgID = models.ForeignKey(Organization, on_delete=models.CASCADE)
    position = models.CharField(max_length=50)

    # Add related_name to avoid clashes
    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set', blank=True)

    def save(self, *args, **kwargs):
        if not self.userID:
            # Get the latest organization
            latest_user = CustomUser.objects.order_by('-userID').first()

            if latest_user:
                # Extract the numeric part, increment, and format the new ID
                new_id = int(latest_user.userID[3:]) + 1
                self.userID = 'USE' + str(new_id).zfill(3)
            else:
                # If there are no organizations, start with COM001
                self.userID = 'USE001'

        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.username
    
class DocPermission(models.Model):
    dpID = models.CharField(max_length=6, primary_key=True)
    userID = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # docID = models.ForeignKey('Document', on_delete=models.CASCADE)
    type = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if not self.dpID:
            # Get the latest organization
            latest_dp = DocPermission.objects.order_by('-dpID').first()

            if latest_dp:
                # Extract the numeric part, increment, and format the new ID
                new_id = int(latest_dp.dpID[3:]) + 1
                self.dpID = 'DPE' + str(new_id).zfill(3)
            else:
                # If there are no organizations, start with COM001
                self.dpID = 'DPE001'

        super(DocPermission, self).save(*args, **kwargs)

class URL(models.Model):
    urlID = models.CharField(max_length=6, primary_key=True)
    docID = models.ForeignKey('Document', on_delete=models.CASCADE)
    dpID = models.ForeignKey('DocPermission', on_delete=models.CASCADE)
    userID = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.urlID:
            # Assuming you have the logic to generate a unique urlID
            # Get the latest organization
            latest_urlID = URL.objects.order_by('-urlID').first()

            if latest_urlID:
                # Extract the numeric part, increment, and format the new ID
                new_id = int(latest_urlID.urlID[3:]) + 1
                self.urlID = 'URL' + str(new_id).zfill(3)
            else:
                # If there are no organizations, start with COM001
                self.urlID = 'URL001'

            # Concatenate urlID and userID
            data_to_hash = f"{self.urlID}{self.userID}"

            # Create a SHA256 hash object
            # sha256 = hashlib.sha256()

            # Update the hash object with the concatenated string
            # sha256.update(concatenated_string.encode('utf-8'))

            # Get the hexadecimal digest of the hash
            hashed_url = hashlib.sha256(data_to_hash.encode()).hexdigest()

            # Assign the hashed URL to the 'url' field
            self.url = hashed_url

        super(URL, self).save(*args, **kwargs)


class Document(models.Model):
    docID = models.CharField(max_length=6, primary_key=True)
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(
        upload_to='pdfs/',
        validators=[validate_pdf_extension],
        default=default_pdf_path
    )

    def save(self, *args, **kwargs):
        if not self.docID:
            # Get the latest organization
            latest_doc = Document.objects.order_by('-docID').first()

            if latest_doc:
                # Extract the numeric part, increment, and format the new ID
                new_id = int(latest_doc.docID[3:]) + 1
                self.docID = 'DOC' + str(new_id).zfill(3)
            else:
                # If there are no organizations, start with COM001
                self.docID = 'DOC001'

        super(Document, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Signature(models.Model):
    docID = models.ForeignKey('Document', on_delete=models.CASCADE)
    signature = models.ImageField(upload_to='signatures')
    signed_at = models.DateTimeField(auto_now_add=True)