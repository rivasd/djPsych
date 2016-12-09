from rest_framework.test import APIRequestFactory, APITestCase
from django.contrib.auth import get_user_model
from djexperiments.models import Experiment
# Create your tests here.


class RestFrameworkTests(APITestCase):
    fixtures = ['fulldb.json'] # do the tests with full database
    
    def setUp(self):
        self.factory = APIRequestFactory()
        self.researcher = get_user_model().objects.create(username = "tester", password="password") # create a true researcher
        
        # fetch an experiment to use
        self.experiment = Experiment.objects.all()[0]
        # make our researcher a member of this experiment
        self.researcher.groups.add(self.experiment.research_group)
        
    
    def test_config_post(self):
        # start by logging in our Client
        self.client.login(username="tester", password="password")
        response = self.client.post()