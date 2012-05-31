# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import sys
from StringIO import StringIO
from django.conf import settings
from django.test import TestCase, Client


class TestBase(TestCase):
    def setUp(self):
        pass


class ViewTests(TestBase):
    def setUp(self):
        self.client = Client()


    def test_send_taf_mail(self):
        r = self.client.get('/taf/', {})
        self.assertEqual(r.status_code, 200)

        sys.stdout = StringIO()
        settings.EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

        sender = 'test@test.ch'
        recipient = 'bastian.ballmann@notch-interactive.ch'
        msg = "Dies ist ein freundlicher Test! :)"

        r = self.client.post('/taf/', {'email_sender': sender, 'message': msg, 'email_recipient': recipient, })

        mail = sys.stdout.getvalue()
        self.assertTrue(mail)
        self.assertIn(sender, mail)
        self.assertIn(recipient, mail)
        self.assertIn(msg, mail)
        self.assertIn('Content-Type: application/pdf\nMIME-Version: 1.0\nContent-Transfer-Encoding: base64\nContent-Disposition: attachment; filename="MANOR_BON_A6_DE-10.pdf"\n\nJVBERi0xLjQNJeLjz9MNCjc2IDAgb2JqDTw8L0xpbmVhcml6ZWQgMS9', mail)
