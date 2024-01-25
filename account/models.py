from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin ,BaseUserManager
from django.contrib.auth.models import Group , Permission
# Create your models here.
from uuid import uuid4 



def upload_to(instance, filename):
    return 'profiles/{filename}'.format(filename=filename)


class UserManager(BaseUserManager):

    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model( email=email , **extra_fields)
        user.set_password(password)
        user.save()
        return user
    

    def create_superuser(self,email,password, **extra_fields):

        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_admin',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('superuser must be given is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser must be given is_superuser=True')
        return self.create_user(email,password,**extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    """
    """
    uuid = models.CharField(max_length=100 , unique=True)
    first_name = models.CharField(max_length=100, null=True , blank=True)
    last_name = models.CharField(max_length=100 , null=True , blank=True) 
    email = models.EmailField(unique=True)
    image = models.ImageField( 
        upload_to=upload_to , null=True , blank=True ,
        help_text=_(
            "This image will be gotten from the bvn data return"
        ),
    )
    is_active = models.BooleanField(default=True)
    is_verify = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_google = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to.'),
        related_name='account_user_groups',  # Add or change this line
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='account_user_permissions',  # Add or change this line
    )

    


    objects= UserManager()

    USERNAME_FIELD = "email"  


    def save(self, *args, **kwargs):
        # Generate a new unique uuid if it's not set
        if not self.uuid:
            self.uuid = str(uuid4())

        super().save(*args, **kwargs)



    def __str__(self) -> str:
        return self.email


    @classmethod
    def check_email(cls, email:str):
        exist = cls.objects.filter(email=email).first()
        return exist if exist else False


    @classmethod
    def disabled_user(cls):
        return cls.objects.filter(is_active=False , is_staff=False).count()


    @classmethod
    def active_user(cls):
        return cls.objects.filter(is_active=True , is_staff=False).count()
    
    def serialized_user_data(self):
        data = dict(
            id=self.uuid,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            is_admin=self.is_admin,
            created_at=self.created_at
        )
        if self.image:
            data['image'] = self.image.url
        else:
            data['image'] = None

        profile = UserProfile.objects.filter(user__id=self.id).first()
        data['profile'] = profile.serialized_user_data()
        return data

  
class UserProfile(models.Model):
    uuid = models.CharField(max_length=100 , unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField( max_length=20, null=True)
    """
    The field that is related to the user address and location starts
    """
    country = models.CharField(max_length=50, null=True , blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True) 
    lga = models.CharField(
        max_length=100, null=True, blank=True,
        help_text=_('Local government area of the user location')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        # Generate a new unique uuid if it's not set
        if not self.uuid:
            self.uuid = str(uuid4())

        super().save(*args, **kwargs)

    def serialized_user_data(self):
        data = dict(
            phone=self.phone,
            country=self.country,
            state=self.state,
            city=self.city,
            address=self.address,
            lga=self.lga,
        )
        return data




class NewsLetterUser(models.Model):
    uuid = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    


    def save(self, *args, **kwargs):
        # Generate a new unique uuid if it's not set
        if not self.uuid:
            self.uuid = str(uuid4())

        super().save(*args, **kwargs)




class LeedUser(models.Model):
    uuid = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    


    def save(self, *args, **kwargs):
        # Generate a new unique uuid if it's not set
        if not self.uuid:
            self.uuid = str(uuid4())

        super().save(*args, **kwargs)






class OrderItem(models.Model):

    uuid = models.CharField(max_length=100 , unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='cartoon_images')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_water_mark = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=100, default='pending', 
        choices=[
            ("pending","Pending"), 
            ("delivered","Delivered") , 
            ("cancelled","Cancelled")
            ]
        )
    payment_status = models.CharField(
        max_length=100, default='pending', 
        choices=[
            ("pending","Pending"), 
            ("successful","Successful") , 
            ("failed","Failed")
            ]
        )
    
    first_name=models.CharField(max_length=64, null=True)
    last_name=models.CharField(max_length=64, null=True)
    phone=models.CharField(max_length=20, null=True)
    email = models.EmailField()
    additional_info=models.TextField(null=True)
    



    def save(self, *args, **kwargs):
        if not self.uuid:self.uuid = str(uuid4())
        super().save(*args, **kwargs)
    





class PaymentTransaction(models.Model):
    AVAILABLE_STATUS = (
        ('success','success'),
        ('failed','failed'),
        ('pending','pending')
    )
    uuid = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    token = models.CharField(max_length=100,unique=True, null=True)
    status = models.CharField(max_length=10,choices=AVAILABLE_STATUS, default='pending')
    price = models.DecimalField(max_digits=10,decimal_places=2)
    order = models.OneToOneField(OrderItem, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)





    def save(self, *args, **kwargs):
        if not self.uuid:self.uuid = str(uuid4())
        super().save(*args, **kwargs)