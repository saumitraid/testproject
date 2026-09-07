from django.shortcuts import render
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


User = get_user_model()


# Create your views here.

def index(request):
    return render(request, 'home.html')



# =========================================================
# REGISTER
# =========================================================

def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        mobile = request.POST.get("mobile")

        # Basic validation
        if not username or not email or not password:
            messages.error(
                request,
                "Please fill all required fields."
            )
            return redirect("register")

        if password != confirm_password:
            messages.error(
                request,
                "Passwords do not match."
            )
            return redirect("register")

        # Check username
        if User.objects.filter(username=username).exists():
            messages.error(
                request,
                "Username already exists."
            )
            return redirect("register")

        # Check email
        if User.objects.filter(email=email).exists():
            messages.error(
                request,
                "Email already registered."
            )
            return redirect("register")

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            mobile=mobile
        )

        # Don't allow login before verification
        user.is_email_verified = False
        user.save()

        # Generate token
        uid = urlsafe_base64_encode(
            force_bytes(user.pk)
        )

        token = default_token_generator.make_token(user)

        # Verification URL
        verification_url = (
            f"http://127.0.0.1:8000/"
            f"verify-email/{uid}/{token}/"
        )

        # Email
        subject = "Verify your email address"

        message = f"""
Hello {user.username},

Thank you for registering.

Please click the link below to verify your email address:

{verification_url}

After verification, you can login to your account.

Thank you.
"""

        try:

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False
            )

            messages.success(
                request,
                "Registration successful. "
                "Please check your email to verify your account."
            )

        except Exception as e:

            # If email sending fails
            user.delete()

            messages.error(
                request,
                f"Unable to send verification email: {e}"
            )

        return redirect("login")

    return render(
        request,
        "register.html"
    )


# =========================================================
# VERIFY EMAIL
# =========================================================

def verify_email(request, uidb64, token):

    try:

        uid = urlsafe_base64_decode(
            uidb64
        ).decode()

        user = User.objects.get(
            pk=uid
        )

    except (
        TypeError,
        ValueError,
        OverflowError,
        User.DoesNotExist
    ):

        user = None

    if user is not None:

        if default_token_generator.check_token(
            user,
            token
        ):

            user.is_email_verified = True
            user.save()

            messages.success(
                request,
                "Your email has been verified successfully. "
                "You can now login."
            )

            return redirect("login")

    messages.error(
        request,
        "The verification link is invalid or has expired."
    )

    return redirect("login")


# =========================================================
# LOGIN
# =========================================================

def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is None:

            messages.error(
                request,
                "Invalid username or password."
            )

            return redirect("login")

        # Check email verification
        if not user.is_email_verified:

            messages.warning(
                request,
                "Please verify your email before logging in."
            )

            return redirect("login")

        login(
            request,
            user
        )

        messages.success(
            request,
            "Login successful."
        )

        return redirect("home")

    return render(
        request,
        "login.html"
    )


# =========================================================
# LOGOUT
# =========================================================

def user_logout(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out."
    )

    return redirect("login")


# =========================================================
# RESEND VERIFICATION EMAIL
# =========================================================

def resend_verification(request):

    if request.method == "POST":

        email = request.POST.get("email")

        try:

            user = User.objects.get(
                email=email
            )

        except User.DoesNotExist:

            messages.error(
                request,
                "No account found with this email."
            )

            return redirect(
                "resend_verification"
            )

        # Already verified
        if user.is_email_verified:

            messages.info(
                request,
                "Your email is already verified."
            )

            return redirect("login")

        # Generate new token
        uid = urlsafe_base64_encode(
            force_bytes(user.pk)
        )

        token = default_token_generator.make_token(
            user
        )

        verification_url = (
            f"http://127.0.0.1:8000/"
            f"verify-email/{uid}/{token}/"
        )

        subject = "Verify your email address"

        message = f"""
Hello {user.username},

Please click the following link to verify your email:

{verification_url}

Thank you.
"""

        try:

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False
            )

            messages.success(
                request,
                "Verification email has been sent."
            )

        except Exception as e:

            messages.error(
                request,
                f"Unable to send email: {e}"
            )

        return redirect("login")

    return render(
        request,
        "resend_verification.html"
    )

