from django.db import models

class ContactUsModel(models.Model):
    SUBJECT_CHOICES = (
        ('Order Inquiry', 'Order Inquiry'),
        ('Product Feedback', 'Product Feedback'),
        ('Account Issue', 'Account Issue'),
        ('General Inquiry', 'General Inquiry'),
        ('Other', 'Other'),
    )
    name       = models.CharField(max_length=100,null=True)
    email      = models.EmailField(null=True)
    subject    = models.CharField(max_length=50, choices=SUBJECT_CHOICES,null=True)
    message    = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    

    def __str__(self):
        return self.name
