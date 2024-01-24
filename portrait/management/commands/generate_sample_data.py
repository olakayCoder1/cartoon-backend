# yourapp/management/commands/create_sample_data.py

from django.core.management.base import BaseCommand
from faker import Faker
from portrait.models import CartoonImage
from account.models import User , NewsLetterUser
from admin_user.models import FAQ
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile
from uuid import uuid4

class Command(BaseCommand):
    help = 'Populate the CartoonImage model with sample data'

    def generate_image_file(self):
        image = SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        return image

    def handle(self, *args, **kwargs):
        fake = Faker()

        for _ in range(20):
            unique_uuid = str(uuid4())
            CartoonImage.objects.create(
                uuid=unique_uuid,  
                image=self.generate_image_file(),
                description=fake.text(),
                price=fake.pydecimal(left_digits=3, right_digits=2, positive=True),
                likes_count=fake.random_int(min=0, max=100),
                saves_count=fake.random_int(min=0, max=100),
                comments_count=fake.random_int(min=0, max=100),
                is_active=fake.boolean(),
                is_featured=fake.boolean(),
            )


        for _ in range(10):
            unique_uuid = str(uuid4())
            User.objects.create(
                uuid=unique_uuid,
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                image=self.generate_image_file(),
                is_active=True,
                is_verify=True,
                is_staff=False,
                is_admin=False,
                is_google=False,
                is_superuser=False,
            )

        for _ in range(40):
            unique_uuid = str(uuid4())
            NewsLetterUser.objects.create(
                uuid=unique_uuid,
                email=fake.email(),
            )


        for _ in range(10):
            unique_uuid = str(uuid4())
            FAQ.objects.create(
                uuid=unique_uuid, 
                question=fake.text(),
                answer=fake.text()
            )

        self.stdout.write(self.style.SUCCESS('Sample data created successfully.'))
