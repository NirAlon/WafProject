from django.test import TestCase
import user, waf_agent

class userTest(TestCase):

    def test_password_rules(self):
        res = user.check_strong_password('12345678')#missing (Aa,!@)
        self.assertEqual(res, False)

        res = user.check_strong_password('123456Aa')#missing (!@)
        self.assertEqual(res, False)

        res = user.check_strong_password('123Aa!') #missing length < 8
        self.assertEqual(res, False)

        res = user.check_strong_password('12345Aa!')
        self.assertEqual(res, True)

    def test_email_validation(self):
        res = user.validation_email('nir.com')#missing (@__)
        self.assertEqual(res, False)

        res = user.validation_email('nir@.com')#missing (@domain.com)
        self.assertEqual(res, False)

        res = user.validation_email('nir.gmail.com')#missing (@)
        self.assertEqual(res, False)

        res = user.validation_email('nir@gmail')#missing (.com)
        self.assertEqual(res, False)

        res = user.validation_email('nir@gmail.com')
        self.assertEqual(res, True)


    def test_xss_agent(self):
        XSS_THRESHOLD = 0.45

        request.session['Waf_trashold'] = 0.8
        res = waf_agent.xss_proccesor('Hello_World')
        self.assertEqual(res<XSS_THRESHOLD, True)

        res = waf_agent.xss_proccesor('<script>alert(!!)</script>')
        self.assertEqual(res>XSS_THRESHOLD, True)


