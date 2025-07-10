"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Admin Id :- super@123
# Admin Pass :- super111

from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('about/', views.About, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.Logout, name='logout'),
    path('Packages/', views.packages, name='packages'),
    path('booking/<int:pk>/', views.Booking, name='booking'),
    path('bookings/', views.booking, name='bookings'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('thankyou/', views.thankyou, name='thankyou'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path('packages/<str:slug>', views.Packages, name='packages_details'),
    path('ForgotPassword/', views.ForgotPassword, name='forgot_password'),
    path('stripe/<int:amount>/', views.stripe_payment_page, name='stripe_page'),
    path('stripe/create-checkout-session/<int:amount>/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.success, name="success"),
    path('cancel/', views.cancel, name="cancel"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
