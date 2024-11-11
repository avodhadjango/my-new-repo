from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from Tourist_apps.forms import BookingForm
from Tourist_apps.models import Booking


# Create your views here.

def home(request):
    return render(request,'index.html')



from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def Register_user(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        cpassword = request.POST.get('password1', '').strip()

        # Debugging: Print statements to check values
        print("Username:", username)
        print("First Name:", first_name)
        print("Last Name:", last_name)
        print("Email:", email)

        # Collect errors
        errors = []

        # Check for required fields
        if not all([username, first_name, email, password, cpassword]):
            errors.append("All fields are required.")

        # Passwords must match
        if password != cpassword:
            errors.append("Passwords do not match.")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            errors.append("This username already exists.")

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            errors.append("This email is already taken.")

        # If there are errors, show them and return to registration form
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'register.html')  # Reload page with error messages

        # Create the user if all checks pass
        try:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            user.save()
            messages.success(request, 'Registration successful')
            return redirect('login')  # Redirect on successful registration
        except ValueError as e:
            # Log the error for debugging
            print("Error while creating user:", e)
            messages.error(request, str(e))
            return render(request, 'register.html')

    return render(request, 'register.html')

from django.contrib import auth, messages
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if both fields are filled
        if not username or not password:
            return render(request, 'login.html', {'error': 'Username and password are required.'})

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('view_bookings')  # Redirect to the desired page after login
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')
def pictures(request):
    bookings = Booking.objects.all()
    return render(request,'pictures.html',{'bookings':bookings})


def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            no_of_people = form.cleaned_data['no_of_people']  # Get the number of people
            booking_type = form.cleaned_data['booking_type']  # Get the selected booking type

            # Define fixed rates for booking types
            BOOKING_RATES = {
                'standard': 300,
                'deluxe': 150,
                'suite': 800
            }

            fixed_rate = BOOKING_RATES[booking_type]  # Get the rate based on the selected booking type
            total_amount = fixed_rate * no_of_people  # Calculate the total

            booking = form.save(commit=False)  # Save the instance without saving to the database yet
            booking.total_amount = total_amount  # Set the total amount
            booking.save()  # Now save the booking instance

            return redirect('view_bookings')  # Redirect to the view bookings page
    else:
        form = BookingForm()

    return render(request, 'create_booking.html', {'form': form})


def view_bookings(request):
    bookings = Booking.objects.all()
    # Define fixed rates for booking types
    BOOKING_RATES = {
        'standard': 100,
        'deluxe': 150,
        'suite': 800
    }

    for booking in bookings:
        # Get the fixed rate based on the booking type
        fixed_rate = BOOKING_RATES.get(booking.booking_type, 0)  # Default to 0 if booking type is not found
        booking.total_amount = booking.no_of_people * fixed_rate  # Calculate total amount based on booking type

    return render(request, 'view_bookings.html', {'bookings': bookings})

def update_booking(request, booking_id):
    # Get the booking instance based on the booking_id
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)  # Bind the form to the instance
        if form.is_valid():
            updated_booking = form.save(commit=False)  # Save the form but don't commit to the database yet

            # Calculate the total amount based on the selected booking type and number of people
            no_of_people = updated_booking.no_of_people
            booking_type = updated_booking.booking_type

            # Define fixed rates for booking types
            BOOKING_RATES = {
                'standard': 300,
                'deluxe': 150,
                'suite': 800
            }

            fixed_rate = BOOKING_RATES.get(booking_type, 0)  # Get the rate based on the booking type
            total_amount = fixed_rate * no_of_people  # Calculate total amount

            updated_booking.total_amount = total_amount  # Set the total amount
            updated_booking.save()  # Save the updated booking instance

            return redirect('view_bookings')  # Redirect to the bookings view page
    else:
        form = BookingForm(instance=booking)  # If not a POST request, create a form with the current booking data

    return render(request, 'update_booking.html', {'form': form, 'booking': booking})
def delete_booking(request, booking_id):
    # Fetch the booking object using the provided booking_id
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        booking.delete()  # Delete the booking
        return redirect('view_bookings')  # Redirect after deletion

    # You can render a confirmation template if needed
    return render(request, 'delete_booking.html', {'booking': booking})


def add_to_cart(request, id):
        bookings = Booking.objects.get(id=id)

        if bookings.no_of_people > 0:
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, item_created = CartItem.objects.get_or_create(cart=cart, bookings=bookings)

            if not item_created:
                cart_item.no_of_people += 1
                cart_item.save()

        return redirect('view')

import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Cart, CartItem


# View to show the cart
def view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item = CartItem.objects.all()
    cart_items = cart.cartitem_set.all()
    total_people = cart_items.count()
    total_price = sum(item.bookings.get_rate() * item.no_of_people for item in cart_items)

    context = {
        'cart_items': cart_items,
        'cart_item':cart_item,
        'total_people': total_people,
        'total_price': total_price,
    }

    return render(request, 'cart.html', context)


# View for empty cart page
def cart_empty_view(request):
    return render(request, 'empty_cart.html')


# Checkout process


def checkout(request):
    cart_items = CartItem.objects.all()

    if cart_items:
        stripe.api_key = settings.STRIPE_SECRET_KEY

        if request.method == 'POST':
            line_items = []

            for cart_item in cart_items:
                if cart_item.bookings:
                    line_item = {
                        'price_data': {
                            'currency': 'INR',
                            'unit_amount': int(cart_item.bookings.get_rate()  * 100),
                            'product_data': {
                                'name': cart_item.bookings.name
                            },
                        },
                        'quantity': cart_item.no_of_people
                    }
                    line_items.append(line_item)

            if line_items:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=line_items,
                    mode='payment',
                    success_url=request.build_absolute_uri(reverse('success')),
                    cancel_url=request.build_absolute_uri(reverse('cancel')),
                )

                return redirect(checkout_session.url, code=303)




def success(request):
    return render(request, 'success.html')  # Create a cancel template

def cancel(request):
    return render(request,'cancel.html')