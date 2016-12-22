from django.contrib import admin
from app.models import SignUp,User,PrimaryAdmin,SecondaryAdmin,Waste
admin.site.register(SignUp)
admin.site.register(User)
admin.site.register(Waste)
admin.site.register(PrimaryAdmin)
admin.site.register(SecondaryAdmin)
# Register your models here.
