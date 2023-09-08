from django.contrib import admin
from .models import Chemical, Plant, XRef, Drug

admin.site.register(Chemical)
admin.site.register(Plant)
admin.site.register(XRef)
admin.site.register(Drug)
