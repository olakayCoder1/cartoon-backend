from django.contrib import admin
from django.urls import path , include , re_path
from django.views.static import serve 
from drf_yasg.views import get_schema_view 
from drf_yasg import openapi
from rest_framework import permissions 
from django.conf import settings
from django.conf.urls.static import static
from .views import AllFAQ , StripeCheckoutView , stripe_webhook , ConfimStripeCheckoutPaymentView_2 , UserJoinNewsletterApiView , AnonymousStripeCheckoutView ,ConfimStripeCheckoutPaymentView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


schema_view = get_schema_view(
   openapi.Info(
      title="CartonVerse API",
      default_version='v1',
      description="CartonVerse is an online portait purchase app",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="programmerolakay@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/',include('api.version1')),
    path('api/v1/faq', AllFAQ.as_view()),
    path('api/v1/newsletter', UserJoinNewsletterApiView.as_view()),

   #  path('api/v1/staff/', include('admin_user.urls')),
    path('api/v1/make-payment/session', StripeCheckoutView.as_view()),
    path('api/v1/make-payment/session/sdk', AnonymousStripeCheckoutView.as_view()),
    path('api/v1/validate-payment-sdk', ConfimStripeCheckoutPaymentView_2.as_view()), 
    path('api/v1/validate-payment', ConfimStripeCheckoutPaymentView.as_view()),
    path("api/v1/stripe/webhook", stripe_webhook),
   #  path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   #  path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

   path(f'api/schema/', SpectacularAPIView.as_view(), name='schema'),
   path(f'doc/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
   path(f'api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
   re_path(r'^media/(?P<path>.*)$', serve , {'document_root':settings.MEDIA_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)