from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User, auth
from datetime import datetime
from .models import Contact
from .models import Register
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login as user_login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from home.models import Tour, Tag, Program, Gallary, Subject, Profile, Register, TourBooking, Payment
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages
import random
import string
import stripe


# Create your views here.
#All pages Links.
# razorpay_client = razorpay.Client(
#     auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def index(request):
    return render(request, "index.html",{})

def About(request):
    return render(request, "about.html",{})

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('registerFirstName')
        print('===========>>>>>>>>>>>first_name>>>>>>>>>',first_name)
        last_name = request.POST.get('registerLastName')
        email = request.POST.get('registerEmail')
        username = request.POST.get('registerUsername')
        password = request.POST.get('registerPassword')
        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error_message': 'Username is already taken'})
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error_message': 'Email is already use'})

        # Create the user
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            return redirect('login')  # Redirect to the login page after successful registration

    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('loginUsername')
        password = request.POST.get('loginPassword')
        user = authenticate(username=username, password=password)
        if user is not None:
            # user_login(self.request, user):
            user_login(request,user)
            if user.is_superuser:
                # Redirect superuser to admin panel
                return redirect('/admin/')
            return redirect('index')  # Redirect to the home page after successful login
        else:
            return render(request, "login.html", {'error_message': 'Invalid username or password'})
    return render(request, "login.html")

def profile(request):
    return render(request, 'profile.html')

def thankyou(request):
    return render(request, 'thankyou.html')


@login_required
def profile(request):
    if request.method == "POST":
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        username = request.POST.get('username')
        image = request.FILES.get('image_up_lode')
        email = request.POST.get('email')
        # dob = request.POST.get('d_o_b')
        # Update User model
        user = User.objects.get(username=request.user.username)
        user.first_name = firstname
        user.last_name = lastname
        user.username = username
        user.email = email
        user.save()

        # Update or create Profile instance
        profile_instance, created = Profile.objects.get_or_create(user=request.user)
        print(image)
        if image:
            profile_instance.profile_picture = image
        profile_instance.save()
        return redirect('index')
    # contex of profile page
    context = {
    }
    return render(request, 'profile.html',context)

def Logout(request):
    logout(request)
    return redirect('login')

@login_required()
def Booking(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    # Store tour ID in session
    request.session['tour_id'] = pk
    
    guide_fee = 350
    insurance_fee = 250
    tax_percent = 12
    discount_percent = tour.discount

    # Get number of people from POST request or default to 1
    num_people = int(request.POST.get('num_people', 1))

    # Calculate base price for all people
    base_price = tour.price * num_people

    # Subtotal (including guide fee and insurance fee per person)
    subtotal = base_price + (guide_fee * num_people) + (insurance_fee * num_people)

    # Tax calculation
    tax = (tax_percent / 100) * subtotal

    # Total after tax
    total_with_tax = subtotal + tax

    # Discount
    discount = (discount_percent / 100) * total_with_tax

    # Final price
    final_total = round(total_with_tax - discount, 2)

    return render(request, "booking.html", {
        "tour": tour,
        "guide_fee": guide_fee,
        "insurance_fee": insurance_fee,
        "tax_percent": tax_percent,
        "tax_amount": round(tax, 2),
        "discount_percent": discount_percent,
        "discount_amount": round(discount, 2),
        "final_total": final_total,
        "num_people": num_people,
        "base_price": base_price
    })





    
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        contact = Contact(name=name, email=email, message=message, date=datetime.today())
        # return redirect('contact')
        contact.save()
        return redirect('contact')
    return render(request, "contact.html",{})

def faq(request):
    return render(request, "faq.html",{})

def testimonial(request):
    return render(request, "testimonial-page.html",{})

def packages(request):

    tour = Tour.objects.all()

    return render(request, "packages.html", context={'tour' : tour})

def Packages(request, slug):

    tour = Tour.objects.get(slug = slug)
    context = {
        "tour" : tour
    }
    return render(request, "package-detail.html", context=context)


def booking(request):
    if request.method == 'POST':
        firstname_booking = request.POST.get('firstname_booking')
        lastname_booking = request.POST.get('lastname_booking')
        email_booking = request.POST.get('email_booking')
        phone_number = request.POST.get('phone_number')
        check_in = request.POST.get('check_in_booking')
        check_out = request.POST.get('check_out_booking')
        num_people = int(request.POST.get('num_people', 1))
        
        # Get the tour from the session or request
        tour_id = request.session.get('tour_id')
        if tour_id:
            tour = get_object_or_404(Tour, pk=tour_id)
            
            # Calculate prices
            guide_fee = 350
            insurance_fee = 250
            tax_percent = 12
            discount_percent = tour.discount
            
            # Calculate base price for all people
            base_price = tour.price * num_people
            
            # Subtotal (including guide fee and insurance fee per person)
            subtotal = base_price + (guide_fee * num_people) + (insurance_fee * num_people)
            
            # Tax calculation
            tax = (tax_percent / 100) * subtotal
            
            # Total after tax
            total_with_tax = subtotal + tax
            
            # Discount
            discount = (discount_percent / 100) * total_with_tax
            
            # Final price
            final_total = round(total_with_tax - discount, 2)
            
            # Save booking
            booking = TourBooking(
                firstname_booking=firstname_booking,
                lastname_booking=lastname_booking,
                email_booking=email_booking,
                phone_number=phone_number,
                check_in=check_in,
                check_out=check_out,
                num_people=num_people,
                tour=tour,
                total_amount=final_total
            )
            booking.save()
            
            # Store booking ID in session for payment reference
            request.session['booking_id'] = booking.id
            
            # Redirect to stripe payment page with the final total
            return redirect('stripe_page', amount=int(final_total))
        else:
            # If no tour ID in session, redirect to packages page
            return redirect('packages')
    
    # GET request - render the booking form
    tour_id = request.session.get('tour_id')
    if tour_id:
        tour = get_object_or_404(Tour, pk=tour_id)
        return render(request, 'booking.html', {
            'tour': tour,
            'num_people': 1  # Default value
        })
    return redirect('packages')


def generate_strong_password(length=6):
    return ''.join(random.choice(string.digits) for _ in range(length))

def ForgotPassword(request):
    if request.method == "POST":
        email = request.POST.get("email")
        print("Email:", email)

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            print("User Exists")

            new_password = generate_strong_password()
            user.set_password(new_password)
            user.save()

            subject = "Your New Password"
            message = f"""Hello {user.username},

Your password has been reset. Here is your new password:

{new_password}

Please log in using this password and change it immediately.

If you did not request this password reset, please contact support.

Best regards,
Your Website Team"""

            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]

            try:
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                messages.success(request, "A new password has been sent to your email.")
                return redirect('login')
            except Exception as e:
                print(e)
                messages.error(request, "Error sending email.")
        else:
            messages.error(request, "Email does not exist.")

        return render(request, 'forgot_password.html')

    return render(request, 'forgot_password.html')
# def NewPasswordPage(request):
#     if request.method =="POST":



# payment


stripe.api_key = settings.STRIPE_SECRET_KEY


def stripe_payment_page(request, amount):
    # Ensure amount is an integer
    amount = int(amount)
    
    context = {
        'amount': amount,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'payment_stripe.html', context)


def create_checkout_session(request, amount):
    # Ensure amount is an integer
    amount = int(amount)
    
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': 'Tour Booking Payment',
                },
                'unit_amount': amount * 100,  # INR in paise
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://127.0.0.1:8000/success/?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='http://127.0.0.1:8000/cancel/',
    )
    return redirect(session.url, code=303)



def success(request):
    session_id = request.GET.get('session_id')

    if not session_id:
        return HttpResponse("Session ID missing", status=400)

    try:
        session = stripe.checkout.Session.retrieve(session_id)

        # You can get email & amount from the session object
        customer_email = session.customer_details.email
        amount_paid = session.amount_total / 100  # convert paise to INR

        # Save payment info to DB
        Payment.objects.create(
            email=customer_email,
            amount=amount_paid,
            stripe_session_id=session.id,
            status=session.payment_status
        )

        return render(request, 'success.html', {
            'email': customer_email,
            'amount': amount_paid
        })

    except Exception as e:
        return HttpResponse(f"Failed to retrieve session: {str(e)}", status=500)


def cancel(request):
    return render(request, 'cancel.html')    