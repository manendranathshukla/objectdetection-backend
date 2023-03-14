from django.contrib import admin

# Register your models here.


from .models import ProcessedData
# Register your models here.

class ProcessedDataAdmin(admin.ModelAdmin):
    list = ('image_name', 'objects_detected', 'timestamp')

    admin.site.register(ProcessedData)