from django.db import models
from django.core.validators import RegexValidator

class Order(models.Model):
    # Status choices
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Existing fields
    order_name = models.CharField(max_length=250)
    order_number = models.CharField(max_length=50, unique=True)
    expected_date = models.DateField()
    actual_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # New fields
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    customer_name = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.order_number} - {self.order_name} - {self.customer_name}"

class Invoice(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='invoices')
    order_details = models.TextField()  # Fixed field name to follow Python conventions
    invoice_number = models.CharField(max_length=50, unique=True)
    issue_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.invoice_number

class Courier(models.Model):
    courier_fullname = models.CharField(max_length=250)
    courier_phoneno = models.CharField(
        max_length=20,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )]
    )
    courier_vehicle_detail = models.CharField(max_length=250)
    courier_license = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.courier_fullname

class Delivery(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PACKING = 'PACKING', 'Packing'
        OUT_FOR_DELIVERY = 'OUT_FOR_DELIVERY', 'Out for Delivery'
        DELIVERY_RETURN = 'DELIVERY_RETURN', 'Delivery Return'
        FAILED_TO_DELIVERY = 'FAILED_TO_DELIVERY', 'Failed to Delivery'
        CANCELED = 'CANCELED', 'Canceled'

    courier = models.ForeignKey(Courier, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='deliveries')
    order_details = models.TextField()
    delivery_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order.order_number} - {self.get_status_display()}"

class Asset(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    serial_number = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50)
    location = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.serial_number})"
    
class Report(models.Model):
    STATUS_CHOICES = [
        ('Good', 'Good'),
        ('Bad', 'Bad'),
    ]

    temp_no = models.CharField(max_length=250, unique=True, blank=True)
    asset_name = models.CharField(max_length=250)
    serial_number = models.CharField(max_length=6, unique=True, blank=True)
    asset_code = models.CharField(max_length=10, unique=True)
    depreciation = models.FloatField()  # Depreciation percentage
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Good')
    location = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.serial_number:
            self.serial_number = self.generate_serial_number()
        if not self.temp_no:
            self.temp_no = self.generate_temp_no()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_serial_number():
        """Generate a unique 6-digit serial number."""
        while True:
            serial = str(uuid.uuid4().int)[:6]
            if not Report.objects.filter(serial_number=serial).exists():
                return serial

    @staticmethod
    def generate_temp_no():
        """Generate temp_no using the current month abbreviation and a counter."""
        month_abbr = now().strftime("%b").upper()  # E.g., "JAN" for January
        last_entry = Report.objects.filter(temp_no__startswith=month_abbr).order_by('-id').first()
        if last_entry:
            last_number = int(last_entry.temp_no[-4:]) + 1
        else:
            last_number = 1
        return f"{month_abbr}{str(last_number).zfill(4)}"

    def __str__(self):
        return f"{self.asset_name} ({self.temp_no})"