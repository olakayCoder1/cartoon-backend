import stripe
from threading import Thread
from django.conf import settings
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from admin_user.models import FAQ
from portrait.models import PurchaseImage
from .serializers import PaymentCheckoutSerializer ,PaymentCheckoutConfirmSerializer,LeedUserJoinSerializer,  UserJoinNewsletterSerializer , AnonymousPaymentCheckoutSerializer
from account.models import PaymentTransaction , NewsLetterUser , OrderItem , LeedUser
# Create your views here.
from helpers.mail import MailServices




class LeadUserJoinApiView(generics.GenericAPIView):
    serializer_class = LeedUserJoinSerializer


    def post(self,request):
        serialiser = self.serializer_class(data=request.data)
        serialiser.is_valid(raise_exception=True)

        try:
            email = serialiser.validated_data['email'].lower()
            name = serialiser.validated_data['name']
            exist_mail = LeedUser.objects.filter(email=email).first()
            if exist_mail:
                return Response(dict(status=False,detail='The provided email already exist'),status=status.HTTP_400_BAD_REQUEST)
            LeedUser.objects.create(email=email,name=name)
            Thread(target=MailServices.come_back_mail, kwargs={
                        'email': email , 'name': name
                    }).start()
            return Response(dict(status=True,detail='Email successfully register for newsletter'),status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(dict(status=False,detail='An error occured'),status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserJoinNewsletterApiView(generics.GenericAPIView):
    serializer_class = UserJoinNewsletterSerializer


    def post(self,request):
        serialiser = self.serializer_class(data=request.data)
        serialiser.is_valid(raise_exception=True)

        try:
            email = serialiser.validated_data['email'].lower()
            exist_mail = NewsLetterUser.objects.filter(email=email).first()
            if exist_mail:
                return Response(dict(status=False,detail='Email already signup for newsletter'),status=status.HTTP_400_BAD_REQUEST)
            NewsLetterUser.objects.create(email=email)
            Thread(target=MailServices.come_back_mail, kwargs={
                        'email': email
                    }).start()
            return Response(dict(status=True,detail='Email successfully register for newsletter'),status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(dict(status=False,detail='An error occured'),status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AllFAQ(APIView):
    def get(self, request):
        records = [ dict(
                # id=val.id,
                question=val.question,
                answer=val.answer
                ) for val in FAQ.objects.filter(is_featured=True)]
        return Response(dict(status=True,data=records),status=status.HTTP_200_OK)
    



stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeCheckoutView(APIView):

    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serialiser = PaymentCheckoutSerializer(data=request.data)
        serialiser.is_valid(raise_exception=True)

        purchase_id = serialiser.validated_data['purchase_id']
        purchase = PurchaseImage.objects.filter(uuid=purchase_id).first()

        if purchase == None:
            return Response(dict(statu=False, detail='Record not found'), status=status.HTTP_404_NOT_FOUND)



        if not purchase.is_custom:
            line_items = [
                {
                    "price_data": {
                        "currency": 'USD',
                        "product_data": {
                            "name": purchase.image.description,
                            "images": ['https://avatars.githubusercontent.com/u/95700260?v=4']
                        },
                        "unit_amount": int(float(purchase.image.price) * 100),
                    },
                    "quantity": purchase.quantity,
                }
            ]
        else:
            price = purchase.price
            if purchase.is_frame:
                price += purchase.frame.price
            line_items = [
                {
                    "price_data": {
                        "currency": 'USD',
                        "product_data": {
                            "name": 'Custome purchase',
                            "images": ['https://avatars.githubusercontent.com/u/95700260?v=4']
                        },
                        "unit_amount": int(float(price) * 100),
                    },
                    "quantity": purchase.quantity,
                }
            ]
        
        try:
            stripe_payment = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=line_items,
                mode="payment",
                success_url=settings.BASE_FRONTEND_URL + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.BASE_FRONTEND_URL + '/?canceled=true',
                metadata={"reference": purchase.uuid, "user": purchase.user.uuid }
            )
            
            return  redirect(stripe_payment.url)
        
        except stripe.error.InvalidRequestError as err:
            print(err)
            # TODO log error
            # invalid parameters were supplied to Stripe's API
            return Response(dict(status=False,detail=f"Amount must not exceed USD 999,999.99"),status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            # TODO log error
            return Response(dict(status=False,detail="Could not initialize payment"),status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class AnonymousStripeCheckoutView(generics.GenericAPIView):

    serializer_class = AnonymousPaymentCheckoutSerializer


    def post(self, request):
        serialiser = self.serializer_class(data=request.data)
        serialiser.is_valid(raise_exception=True)


        first_name = serialiser.validated_data.get('first_name')
        last_name = serialiser.validated_data.get('last_name')
        email = serialiser.validated_data.get('email')
        phone = serialiser.validated_data.get('phone')
        image = serialiser.validated_data.get('image')
        water_mark = serialiser.validated_data.get('watermark')
        additional_info = serialiser.validated_data.get('note','')

        water_mark = False if water_mark == 'no' else True


        water_mark = True

        image_price = 100

        water_mark_price = 0

        if water_mark:
            water_mark_price += 10

        price = image_price  + water_mark_price


        price = format(price, ".2f")
        order_item = OrderItem.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            price=price,
            phone=phone,
            image=image,
            is_water_mark=water_mark,
            additional_info=additional_info
        )
        
        print(email)
        
        transaction = PaymentTransaction.objects.create(email=email,price=price, order=order_item)


        line_items = [
                {
                    "price_data": {
                        "currency": 'USD',
                        "product_data": {
                            "name": 'Olaka',
                            "images": ['https://avatars.githubusercontent.com/u/95700260?v=4']
                        },
                        "unit_amount": int(float(price) * 100),
                    },
                    "quantity": 1,
                }
        ]

        try:
            stripe_payment = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=line_items,
                mode="payment",
                success_url=settings.BASE_FRONTEND_URL + '/payment?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.BASE_FRONTEND_URL + '/payment?canceled=true',
                metadata={"txn_ref": transaction.uuid,"order_ref": order_item.uuid,  "user": transaction.email }
            )
            
            return  Response(dict(status=True,redirect_url=stripe_payment.url),status=200)
        
        except stripe.error.InvalidRequestError as err:
            print(err)
            # TODO log error
            # invalid parameters were supplied to Stripe's API
            return Response(dict(status=False,detail=f"Amount must not exceed USD 999,999.99"),status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            # TODO log error
            return Response(dict(status=False,detail="Could not initialize payment"),status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ConfimStripeCheckoutPaymentView_2(APIView):
    def get(self,request):
        session_id = request.GET.get('session_id')

        try:
            # Retrieve the payment session from Stripe
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == 'paid':
                metadata = session.metadata
                txn_ref = metadata['txn_ref']
                order_ref = metadata['order_ref']
                txn = PaymentTransaction.objects.get(uuid=txn_ref)
                order = OrderItem.objects.get(uuid=order_ref)
                order.payment_status = 'successful'
                order.save()
                if txn.status != 'success':
                    txn.status = 'success'
                    txn.save()
                    Thread(target=MailServices.send_successfully_order_mail, kwargs={
                        'email': order.email ,
                        'name': f"{order.first_name} {order.last_name }",
                        'order_id': order_ref , 
                        'txn_id':txn_ref,
                        'water_mark':order.is_water_mark
                    }).start()
                # Payment is successful, update your database or perform any other actions
                return Response({'status': True , 'detail': 'Payment successfull'},status=status.HTTP_200_OK)
            else:
                metadata = session.metadata
                txn_ref = metadata['txn_ref']
                order_ref = metadata['order_ref']
                txn = PaymentTransaction.objects.get(uuid=txn_ref)
                txn.status = 'failed'
                txn.save()
                order = OrderItem.objects.get(uuid=order_ref)
                order.payment_status = 'failed'
                order.save()
                # Payment is not successful
                return Response({'status': False , 'detail': 'Payment not  successfull'}, status=status.HTTP_400_BAD_REQUEST)
            
        except stripe.error.StripeError as e:
            # Handle Stripe errors
            return Response({'detail': str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except Exception as e:
            # Handle Stripe errors
            return Response({'detail': str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ConfimStripeCheckoutPaymentView(APIView):

    def post(self, request):
        serialiser = PaymentCheckoutConfirmSerializer(data=request.data)
        serialiser.is_valid(raise_exception=True)

        try:
            charge = stripe.Charge.create(
                amount=float(10) * 100,
                currency='USD',
                source=serialiser.validated_data['token'],
                description="Portrait Purchase",
                statement_descriptor="CartoonVerse",
                metadata={"reference": 'purchase.uuid', "user": 'purchase.user.uuid' },
            )
            print(charge)
            # Only confirm a funding after status: succeeded
            if charge["status"] == "succeeded":
                return Response(dict(status=True,detail="Transaction successful"),status=status.HTTP_200_OK)
            else:
                return Response(dict(status=False,detail="Could not verify transaction"),status=status.HTTP_400_BAD_REQUEST)
            
        except stripe.error.CardError as e:
            # TODO log error
            body = e.json_body
            err = body.get("error", {})
            return Response(dict(status=False,detail=err.get("message")),status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.RateLimitError as e:
            print(e)
            # TODO Log error
            return Response(dict(status=False,detail="Could not verify your transaction at the moment"),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except stripe.error.InvalidRequestError as e:
            print(e)
            # TODO Log error
            # invalid parameters were supplied to Stripe's API
            return Response(dict(status=False,detail="Could not verify your transaction at the moment"),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except stripe.error.AuthenticationError as e:
            print(e)
            # TODO Log error
            # Authentication with Stripe's API failed
            return Response(dict(status=False,detail="Could not verify your transaction at the moment"),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except stripe.error.APIConnectionError as e:
            print(e)
            # TODO Log error
            # Network communication with Stripe failed
            return Response(dict(status=False,detail="Network communication failed, try again."),status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.StripeError as e:
            print(e)
            # TODO Log error
            # send yourself an email
            return Response(dict(status=False,detail="Internal Error, contact support."),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Something else happened, completely unrelated to Stripe
        except Exception as e:
            print(e)
            # TODO Log error
            return Response(dict(status=False,detail="Could not verify your transaction at the moment"),status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@csrf_exempt
@require_POST
def stripe_webhook(request):
    """"
        Stripe payment verification webhook
        URL to be registered using stripe CLI
    """
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        # TODO LOG ERROR HERE
        return Response({"detail": e}, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        # TODO LOG ERROR HERE
        return Response({"detail": e}, status=400)
    # Handle the checkout.session.completed event

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        purchase_id = session["metadata"]["reference"]
        try:
            purchase = PurchaseImage.objects.get(pk=purchase_id)
        except Exception as e:
            print(e)
            return Response(dict(statu=False), status=status.HTTP_404_NOT_FOUND)
        
        reference = session["id"]
        amount = float(session['amount_total']) / 100

        purchase.status = 'successful'
        purchase.save()
        

    return Response(status=200)
