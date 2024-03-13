from django.test import SimpleTestCase
from django.urls import reverse, resolve, Resolver404
from users.views import register


class TestUrls(SimpleTestCase):
    def test_register_url(self):
        try:
            url = reverse('user-register')
            print(resolve('app-home'))
        # self.assertEquals(resolve('user-register').func, register)
        except Resolver404:
            self.fail("Couldn't resolve the url")