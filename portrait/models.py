from uuid import uuid4
from django.db import models
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()



class CartoonImage(models.Model):
    uuid = models.CharField(max_length=100 , unique=True)
    image = models.ImageField(upload_to='cartoon_images')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    likes_count = models.IntegerField(default=0)
    saves_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(uuid4())

        super().save(*args, **kwargs)


    def serialized_data(self):
        data = dict(
            id=self.uuid,
            image=self.image.url,
            description=self.description,
            price=float(self.price),
            likes_count=self.likes_count,
            saves_count=self.saves_count,
            comments_count=self.comments_count,
        )
        return data


    @staticmethod
    def get_all_images(request):
        search = request.GET.get('search')
        records = []
        if search:
            for val in CartoonImage.objects.filter(is_active=True, description__icontains=search).order_by('-created_at'):
                data = dict(
                    id=val.uuid,
                    image=val.image.url,
                    description=val.description,
                    price=float(val.price),
                    likes_count=val.likes_count,
                    saves_count=val.saves_count,
                    comments_count=val.comments_count,
                )
                data['has_like'] = CartoonImageUserLike.objects.filter(portrait=val,user__id=request.user.id).exists()
                data['has_save'] = CartoonImageUserFavourite.objects.filter(portrait=val,user__id=request.user.id).exists()
                records.append(data)
        else:
            for val in CartoonImage.objects.filter().order_by('-created_at'):
                data = dict(
                    id=val.uuid,
                    image=val.image.url,
                    description=val.description,
                    price=float(val.price),
                    likes_count=val.likes_count,
                    saves_count=val.saves_count,
                    comments_count=val.comments_count,
                )
                data['has_like'] = CartoonImageUserLike.objects.filter(portrait=val,user__id=request.user.id).exists()
                data['has_save'] = CartoonImageUserFavourite.objects.filter(portrait=val,user__id=request.user.id).exists()
                records.append(data)
        return records


    @staticmethod
    def admin_get_all_images(request):
        search = request.GET.get('search')
        if search:
            records = [ dict(
                id=val.uuid,
                image=val.image.url,
                description=val.description,
                price=float(val.price),
                likes_count=val.likes_count,
                saves_count=val.saves_count,
                comments_count=val.comments_count,
                ) for val in CartoonImage.objects.filter(description__icontains=search).order_by('-created_at')]
        else:
            records = [ dict(
                id=val.uuid,
                image=val.image.url,
                description=val.description,
                price=float(val.price),
                likes_count=val.likes_count,
                saves_count=val.saves_count,
                comments_count=val.comments_count,
                ) for val in CartoonImage.objects.all().order_by("-created_at")]
        return records



class Frame(models.Model):
    uuid = models.CharField(max_length=100 , unique=True)
    name = models.CharField(max_length=255)
    size = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(uuid4())

        super().save(*args, **kwargs)



class CustomImage(models.Model):
    uuid = models.CharField(max_length=100 , unique=True)
    image = models.ImageField(upload_to='custom_images')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    frame = models.BooleanField(default=False)
    frame_size = models.ForeignKey(Frame, on_delete=models.SET_NULL , null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(uuid4())

        super().save(*args, **kwargs)




class FavouriteImage(models.Model):
    uuid = models.CharField(max_length=100 , unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(CartoonImage, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(uuid4())

        super().save(*args, **kwargs)


    @staticmethod
    def get_favourite(user_id):
        records = FavouriteImage.objects.filter(user__id=user_id).select_related()
        return records
    

    @staticmethod
    def get_user_favourites(user_id):
        cartoon_image_user_likes = FavouriteImage.objects.filter(user__id=user_id).order_by('-created_at')

        portraits = [like.image.serialized_data() for like in cartoon_image_user_likes]

        return portraits





class PurchaseImage(models.Model):
    uuid = models.CharField(max_length=100 , unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    image = models.ForeignKey(CartoonImage, on_delete=models.SET_NULL , null=True)
    custome_image = models.ForeignKey(CustomImage, on_delete=models.SET_NULL , null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    is_custom = models.BooleanField(default=False)
    is_frame = models.BooleanField(default=False)
    frame = models.ForeignKey(Frame, on_delete=models.SET_NULL , null=True)
    quantity = models.IntegerField(default=1)
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



    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.price * self.quantity
            
        if not self.uuid:
            self.uuid = str(uuid4())

        super().save(*args, **kwargs)


    def serialized_user_data(self):
        user = self.user.serialized_user_data()
        data = dict(
            id=self.uuid,
            user=user,
            image=self.image.serialized_data(),
            status=self.status,
            is_custom=self.is_custom,
        )
        return data
    




class CartoonImageUserLike(models.Model):

    uuid = models.CharField(max_length=100 , unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    portrait = models.ForeignKey(CartoonImage, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(uuid4())

        super().save(*args, **kwargs)

    @staticmethod
    def get_user_likes(user_id):
        cartoon_image_user_likes = CartoonImageUserLike.objects.filter(user__id=user_id).order_by('-created_at')

        portraits = [like.portrait.serialized_data() for like in cartoon_image_user_likes]

        return portraits
    



class CartoonImageUserFavourite(models.Model):

    uuid = models.CharField(max_length=100 , unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    portrait = models.ForeignKey(CartoonImage, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(uuid4())

        super().save(*args, **kwargs)

    @staticmethod
    def get_user_favourites(user_id):
        cartoon_image_user_likes = CartoonImageUserFavourite.objects.filter(user__id=user_id).order_by('-created_at')

        portraits = [like.portrait.serialized_data() for like in cartoon_image_user_likes]

        return portraits