from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from djPsych.exceptions import PayoutException
from djcollect.models import Participation
import json
import datetime
import requests

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
        Attempts to send the funds by PayPal. Uses Adaptive Payment, since apparently paypal is too retarded to enable the simple REST API for Payouts in Canada
        """
        
        exp = self.participation.experiment
        
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
            app_id = 'APP-80W284485P519543T'
            uname = 'cognitionlabmtl-facilitator_api1.gmail.com'
            password = 'MD6PBHCRAL4VZH9X'
            signature = 'A2wsm0d1Grf2DPtNCD3y37yNpEx0A3sK5M8zW3I.GFkKB7Gad0bvN3bA'
            endpoint = 'https://svcs.sandbox.paypal.com/AdaptivePayments/Pay'
            sender = "cognitionlabmtl-facilitator@gmail.com"
        elif settings.PAYPAL_MODE == 'live':
            app_id = exp.PayPal_Live_ID
            uname = exp.PayPal_API_Username
            password = exp.PayPal_API_Password
            signature = exp.PayPal_API_Signature
            endpoint = 'https://svcs.paypal.com/AdaptivePayments/Pay'
            sender = exp.PayPal_sender_email
        else:
            raise PayoutException(_("Payment configuration error, sorry for the inconvience"))
        
        if app_id is None or exp.PayPal_API_Signature is None:
            raise PayoutException(_("The researchers of this experiment have not configured their Paypal credentials to be able to send money"))
        

        headers  = {
            'X-PAYPAL-SECURITY-USERID': uname,
            'X-PAYPAL-SECURITY-PASSWORD': password,
            'X-PAYPAL-SECURITY-SIGNATURE': signature,
            'X-PAYPAL-APPLICATION-ID': app_id,
            'X-PAYPAL-REQUEST-DATA-FORMAT': 'JSON',
            'X-PAYPAL-RESPONSE-DATA-FORMAT': 'JSON'
        }
        
        payload = {
            "actionType": 'PAY',
            "currencyCode": self.currency,
            "senderEmail": sender,
            "receiverList":{
                "receiver": [{
                    "amount": str(round(self.amount, 2)),
                    "email": email
                }]
            },
            
            "returnUrl": 'https://cogcommtl.ca',
            "cancelUrl": 'https://cogcommtl.ca/webexp',
            "requestEnvelope":{
                "errorLanguage": "en_US",
                "detailLevel": "ReturnAll"
            }
        }
        
        # attempt payout
        resp = requests.post(endpoint, headers=headers, data=json.dumps(payload))
        payout = resp.json()
        
        if resp.status_code == 200:
            
            if payout['responseEnvelope']['ack'] == 'Failure':
                
                raise PayoutException(_("Payment was refused by PayPal for the following reason: ") + payout['error'][0]['message'])
                #TODO: log the error codes and correlation Id to deal with claims
                
                pass
            elif payout["responseEnvelope"]['ack'] == 'Success':
                
                #we need to find how much we paid in fees
                funding_payload = {
                    'payKey': payout['payKey'],
                    "requestEnvelope":{
                        "errorLanguage": 'en_US',
                        "detailLevel": 'ReturnAll'
                    }
                }
                
                if settings.PAYPAL_MODE == 'sandbox':
                    funding_endpoint = 'https://svcs.sandbox.paypal.com/AdaptivePayments/GetFundingPlans'
                elif settings.PAYPAL_MODE == 'live':
                    funding_endpoint = 'https://svcs.paypal.com/AdaptivePayments/GetFundingPlans'
                    
                
                funding = requests.post(funding_endpoint, headers=headers, data=json.dumps(funding_payload))
                funding - funding.json()
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
            raise PayoutException(_("PayPal servers did not respond. Please try again later"))