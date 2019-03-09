from django.test import TestCase
from django.urls import reverse


class WeasyTemplateViewTest(TestCase):
    def test_get(self):
        url = reverse('sample1')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        import ipdb; ipdb.set_trace()
