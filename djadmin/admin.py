from django.contrib import admin

# Register your models here.

class GenericAdmin(admin.ModelAdmin):
    """
    The grandfather modelAdmin from which all the modelAdmins of all our models will inherit. Should implement hiding of models
    """
    
    