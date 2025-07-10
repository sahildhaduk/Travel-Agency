from django.contrib import admin
from home.models import *
from home.models import Contact, Register, Tour, Tag, Program, Gallary, Subject, Profile, TourBooking, Payment

# Register your models here.
admin.site.register(Contact)
admin.site.register(Register)
admin.site.register(Profile)
admin.site.register(TourBooking)
admin.site.register(Payment)



class TagAdmin(admin.TabularInline):
    model = Tag
class ProgramAdmin(admin.TabularInline):
    model = Program
class GallaryAdmin(admin.TabularInline):
    model = Gallary

class SubjectAdmin(admin.TabularInline):
    model = Subject

class TourAdmin(admin.ModelAdmin):
    inlines = [TagAdmin, ProgramAdmin, GallaryAdmin, SubjectAdmin]

admin.site.register(Tour, TourAdmin)

