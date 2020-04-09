from django.contrib.auth.models import User
from django.test import TestCase

class SignUpValidationTests(TestCase):

    def test_can_take_user_data(self):
        from pasahero.pasahero.forms import UserForm
        form = UserForm(data={'username' : 'foo', 'password' : 'barbar1'})
        self.assertTrue(form.is_valid())

    def test_can_register_new_user(self):
        self.client.post('/login', data={'username' : 'foo', 'password' : 'barabar1'})
        self.assertIs(User.objects.get(username='foo'))

    def test_can_reject_duplicate_user_name(self):
        self.client.post('/login', data={'username': 'foo', 'password': 'barbar1'})
        self.assertIs(User.objects.get(username='foo'))

        from pasahero.pasahero.forms import UserForm
        form = UserForm(data={'username' : 'foo', 'password': 'barbar1'})
        self.assertFalse(form.is_valid())
        self.assertTrue('username' in form.errors.as_data())
        self.assertTrue('duplicate_username' == form.errors.as_data()['username'][0].code)

    def test_can_reject_short_password(self):
        from pasahero.pasahero.forms import UserForm
        form = UserForm(data={'username' : 'foo', 'password' : 'bar1'})
        self.assertFalse(form.is_valid())
        self.assertTrue('password' in form.errors.as_data())
        self.assertTrue('password_length' in form.errors.as_data()['password'][0].code)

    def test_can_reject_weak_password(self):
        from pasahero.pasahero.forms import UserForm
        form = UserForm(data={'username': 'foo', 'password': 'barbar'})
        self.assertFalse(form.is_valid())
        self.assertTrue('password' in form.errors.as_data())
        self.assertTrue('password_strength' == form.errors.as_data()['password'][0].code)







