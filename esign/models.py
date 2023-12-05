from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib import admin
import hashlib
import datetime
from .managers import CustomUserManager
import pytz

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
    MFA = models.BooleanField(default=True)

    # Add related_name to avoid clashes
    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set', blank=True)

    REQUIRED_FIELDS = ('email', 'orgID', 'position')

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
    objects = CustomUserManager()

    def __str__(self):
        return self.username

class Document(models.Model):
    docID = models.CharField(max_length=6, primary_key=True)
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(
        upload_to='pdfs/',
        validators=[validate_pdf_extension],
        default=default_pdf_path
    )
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    email_sent = models.BooleanField(default=False)
    assigned_users = models.ManyToManyField(CustomUser, related_name='assigned_documents')

    def save(self, *args, **kwargs):
        print(f"Before save - created_date: {self.created_date} - due_date: {self.due_date}")
        
        singapore_tz = pytz.timezone('Asia/Singapore')
        self.created_date = timezone.now().astimezone(singapore_tz)
        
        if not self.created_date:
            self.created_date = timezone.now()
        self.created_date = self.created_date.astimezone(singapore_tz)
        
        if not self.due_date:
            # Set a very old date if due_date is not set
            self.due_date = datetime.datetime(1900, 1, 1, tzinfo=singapore_tz)  # Set to January 1, 1900 as an example
        else:
            self.due_date = self.due_date.astimezone(singapore_tz)

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
        print(f"After save - created_date: {self.created_date} - due_date: {self.due_date}")

    def get_status(self):
        now = timezone.now()
        if now > self.due_date:
            return 'expired'
        else:
            return 'assigned'

    def __str__(self):
        return self.title

class PersonalDoc(models.Model):
    pdocID = models.CharField(max_length=6, primary_key=True)
    dpID = models.ForeignKey('DocPermission', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(
        upload_to='signed/',
        validators=[validate_pdf_extension],
        default=default_pdf_path,
        null=True,
        blank=True
    )
    created_date = models.DateTimeField(auto_now_add=True)
    email_sent = models.BooleanField(default=False)
    page = models.IntegerField(default=0)
    reference = models.CharField(max_length=6, null=True, blank=True)

    def save(self, *args, **kwargs):

        if not self.pdocID:
            # Get the latest organization
            latest_doc = PersonalDoc.objects.order_by('-pdocID').first()

            if latest_doc:
                # Extract the numeric part, increment, and format the new ID
                new_id = int(latest_doc.pdocID[3:]) + 1
                self.pdocID = 'PDO' + str(new_id).zfill(3)
            else:
                # If there are no organizations, start with COM001
                self.pdocID = 'PDO001'

        super(PersonalDoc, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class DocPermission(models.Model):
    dpID = models.CharField(max_length=6, primary_key=True)
    userID = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    docID = models.ForeignKey('Document', on_delete=models.CASCADE)
    priority = models.IntegerField(null=True, blank=True)
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

class Remark(models.Model):
    remarkID = models.CharField(max_length=6, primary_key=True)
    docID = models.ForeignKey('Document', on_delete=models.CASCADE)
    userID = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.remarkID:
            # Get the latest remark
            latest_remark = Remark.objects.order_by('-remarkID').first()

            if latest_remark:
                # Extract the numeric part, increment, and format the new ID
                new_id = int(latest_remark.remarkID[3:]) + 1
                self.remarkID = 'REM' + str(new_id).zfill(3)
            else:
                # If there are no remarks, start with REM001
                self.remarkID = 'REM001'

        super(Remark, self).save(*args, **kwargs)


class Signature(models.Model):
    docID = models.ForeignKey('Document', on_delete=models.CASCADE)
    signature = models.ImageField(upload_to='signatures')
    signed_at = models.DateTimeField(auto_now_add=True)





class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    photo = models.ImageField(blank=True, upload_to='photos')
    bio = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"profile of {self.user.username}"
    
class Log(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    photo = models.ImageField(upload_to='logs')
    is_correct = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)