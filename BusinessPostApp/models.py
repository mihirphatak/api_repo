from django.db import models
from UserApp.models import User
# Create your models here.


class BusinessCategory(models.Model):
    english_name = models.CharField(max_length=50, )
    marathi_name = models.CharField(max_length=50, null=True)
    alias1 = models.CharField(max_length=50, null=True)
    alias2 = models.CharField(max_length=50, null=True)
    alias3 = models.CharField(max_length=50, null=True)
    alias4 = models.CharField(max_length=50, null=True)
    alias5 = models.CharField(max_length=50, null=True)
    class FieldNames:
        ENGLISH_NAME = "english_name"
        MARATHI_NAME = "marathi_name"
        ALIAS1 = "alias1"
        ALIAS2 = "alias2"
        ALIAS3 = "alias3"
        ALIAS4 = "alias4"
        ALIAS5 = "alias5"


class BusinessPoints(models.Model):
    abbreviation = models.CharField(max_length=50)
    english = models.CharField(max_length=100)
    marathi = models.CharField(max_length=100)
    class FieldNames:
        ENGLISH = "english"
        MARATHI = "marathi"
        ABBREVIATION = "abbreviation"


class BusinessPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business_category = models.ForeignKey(BusinessCategory, on_delete=models.PROTECT)
    business_type = models.CharField(max_length=20)
    business_name_english = models.CharField(max_length=100)
    business_name_marathi = models.CharField(max_length=100,null=True)
    business_contact_number = models.CharField(max_length=10)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    # weekly_off will contain comma separated 0s and 1s. Example: 1,0,0,0,0,0,1. Week start from Sunday.
    weekly_off = models.CharField(max_length=15, null=True)
    business_point_1 = models.CharField(max_length=150, null=True)
    business_point_2 = models.CharField(max_length=150, null=True)
    business_point_3 = models.CharField(max_length=150, null=True)
    business_address = models.CharField(max_length=100, null=True)
    discount = models.PositiveSmallIntegerField(null=True)
    email = models.EmailField(null=True)
    business_image = models.ImageField(upload_to='business_images', null=True)
    likes_counter = models.PositiveIntegerField(default=0)
    city = models.CharField(max_length=50, null=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=6, null=True)
    is_payment_made = models.BooleanField(default=False)
    payment_amount = models.PositiveIntegerField(null=True)
    valid_till = models.DateTimeField(null=True)
    are_details_complete = models.BooleanField(default=False)
    # can be set by user to enable/disable add
    is_active = models.BooleanField(default=False)
    # will be set by moderator
    #is_approved = models.BooleanField(default=False)
    # will be set by moderator
    #is_blocked = models.BooleanField(default=False)
    class FieldNames:
        BUSINESS_CATEGORY = "business_category"
        BUSINESS_TYPE = "business_type"
        BUSINESS_NAME_ENGLISH = "business_name_english"
        BUSINESS_NAME_MARATHI = "business_name_marathi"
        BUSINESS_CONTACT_NUMBER = "business_contact_number"
        START_TIME = "start_time"
        END_TIME = "end_time"
        WEEKLY_OFF = "weekly_off"
        BUSINESS_POINTS = "business_points"
        BUSINESS_ADDRESS = "business_address"
        DISCOUNT = "discount"
        EMAIL = "email"
        BUSINESS_IMAGE = "business_image"
        LIKES_COUNTER = "likes_counter"
        CITY = "city"
        LATITUDE = "latitude"
        LONGITUDE = "longitude"
        IS_PAYMENT_MADE = "is_payment_made"
        PAYMENT_AMOUNT = "payment_amount"
        VALID_TILL = "valid_till"

class PaymentTransactions(models.Model):
    business_post = models.ForeignKey(BusinessPost, on_delete=models.CASCADE)
    # payment_id is the transaction id from the payment gateway
    payment_id = models.CharField(max_length=100)
    amount = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    success = models.BooleanField(default=False)
    failure_reason = models.CharField(max_length=200, null=True)
    class FieldNames:
        BUSINESS_POST = "business_post"
        PAYMENT_ID = "payment_id"
        AMOUNT = "amount"
        DATE = "date"
        TIME = "time"
        SUCCESS = "success"
        FAILURE_REASON = "failure_reason"
