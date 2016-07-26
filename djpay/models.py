from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from djPsych.exceptions import PayoutException
from djcollect.models import Participation
import paypalrestsdk
import datetime
import logging

# Create your models here.

class Payment(models.Model):
    """
    Represents a claim for PayPal monetary compensation for a completed participation
    
    Avoid creating this liberally, only when it could actually be payed. For now only one payment per participation is enforced.
    I guess you could always create dummy Participation objects to circumvent this
    
    SHOULD NEVER BE CREATED IN BULK. Anyway it does not really make sense to do this.
    """
    
    participation = models.OneToOneField(Participation)
    amount= models.FloatField()
    currency = models.CharField(max_length=3, default='CAD')
    time_created = models.DateTimeField(auto_now_add=True)
    time_sent = models.DateTimeField(blank=True, null=True)
    sent = models.BooleanField(default=False)
    payout_item_id = models.CharField(max_length=16, blank=True, null=True)
    transaction_id = models.CharField(max_length=20, blank=True, null=True)
    payout_batch_id = models.CharField(max_length=16, blank=True, null=True)
    time_processed = models.DateTimeField(blank=True, null=True)
    receiver = models.EmailField(null=True)
    status = models.CharField(max_length=16, blank=True)
    
    
    
    @classmethod
    def createPayment(cls, participation, amount, receiver=None, curr='CAD', greedy=None):
        """
        Creates a payment linked to this participation. Default currency canadian dollars
        raises exceptions on failure
        """
        if hasattr(participation, 'payment'):
            raise PayoutException(_("Payment already created for this participation"))
        
        if receiver is None:
            receiver = participation.subject.user.email

        payment = cls(participation=self, amount=amount, receiver=receiver)
        payment.save()
        return payment
    
    def save(self, *args, **kwargs):
        
        self.amount = round(self.amount, 2) # realized amount sometimes return float with crazy decimal developments because computers cannot really represent base-10
        if self.pk is None: # do all the below code only for new instances
            if not self.participation.experiment.compensated:
                raise PayoutException(_("This experiment does not currently offer monetary compensation"))
            
            if self.amount > self.participation.experiment.funds_remaining:
                raise PayoutException(_("Sorry! not enough funds remaining to honor this payment"))
            
            if Payment.objects.filter(participation__experiment=self.participation.experiment, participation__subject=self.participation.subject).count() >= self.participation.experiment.max_payouts:
                raise PayoutException(_("You have exceeded the current limit of payments for this experiment"))
            
            self.participation.experiment.deductFunds(self.amount) # Since a Payment is also a promise to a subject that he/she will get paid, deduct the money immediately on creation
        
        super(Payment, self).save(*args, **kwargs)
    
    def pay(self, request, email=None):
        """
        Attempts to send the funds by PayPal. Since this deals with $$$, exceptions will be thrown if
        inconsistencies occur, make sure to catch them.
        
        Remaining funds are not checked on the Experiment object, they are expected to have been deducted at creation time.
        This means that error codes like INSUFFICIENT_FUNDS returned by PayPal are no joke, it means we did not follow through our promise to pay
        or we added funds that we did not really have.  
        """
        
        if not request.user.is_authenticated():
            raise PayoutException(_("You must be logged in to claim a payment"))
        
        if not self.participation.subject.user == request.user:
            raise PayoutException(_("Payouts must be claimed by the same user who received them"))
        
        if self.sent or self.time_sent is not None or self.time_processed is not None or self.payout_item_id is not None:
            # looks like this has already been paid...
            raise PayoutException(_("Payment already sent. Contact us if this is an error"))
        
        if self.receiver is None:
            raise PayoutException(_("Your account must have an email address confirmed before you can claim payments"))
        
        if email is None:
            email = self.receiver
        
        if settings.PAYPAL_MODE == 'sandbox':
            client_id = self.participation.experiment.paypal_id_sandbox
            secret = self.participation.experiment.paypal_secret_sandbox
        elif settings.PAYPAL_MODE == 'live':
            client_id = self.participation.experiment.paypal_id_live
            secret = self.participation.experiment.paypal_secret_live
        else:
            raise PayoutException(_("Payment configuration error, sorry for the inconvience"))
        
        if client_id is None or secret is None:
            raise PayoutException(_("The researchers of this experiment have not configured their Paypal credentials to be able to send money"))
        

        mypaypalapi = paypalrestsdk.Api({
            'mode': settings.PAYPAL_MODE,
            'client_id': client_id,
            'client_secret': secret
        })
        
        # attempt payout
        payout = paypalrestsdk.Payout({
            "sender_batch_header": {
                "sender_batch_id": "batch_"+str(self.pk+20),
                "email_subject": _("You have a payment from the Cognition Communication Lab at UQAM"),
            },
            "items": [
                {
                    "recipient_type": "EMAIL",
                    "amount": {
                        "value": round(self.amount, 2),
                        "currency": self.currency,
                    },
                    "receiver": email,
                    "note": _("Thank you for your participation in the experiment: ")+self.participation.experiment.verbose_name,
                    "sender_item_id": "item_"+str(self.pk+20)
                }
            ]
        }, api=mypaypalapi)
        
        if payout.create(sync_mode=True):
            # DONE: do stuff to mark this payment as completed
            self.sent = True
            self.participation.experiment.deductFunds(float(payout.batch_header.fees.value)) # don't forget to deduct the paypal fees since we pay them!
            self.time_sent = datetime.datetime.now()
            self.payout_batch_id = payout.batch_header.payout_batch_id
            self.status = payout.items[0].transaction_status
            self.payout_item_id = payout.items[0].payout_item_id
            self.transaction_id = payout.items[0].transaction_id
            self.time_processed = payout.items[0].time_processed
            self.save()
            return payout
        else:
            raise PayoutException(payout.error)