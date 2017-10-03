from django.core.urlresolvers import reverse


class BaseViewSetTestMixin:

    def test_list(self):
        url_base = '%s:%s' % (self.namespace, self.url_name)
        url = reverse(url_base + '-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_retrieve(self):
        url_base = '%s:%s' % (self.namespace, self.url_name)
        url = reverse(url_base + '-detail', kwargs={'pk': self.item.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        url_base = '%s:%s' % (self.namespace, self.url_name)
        url = reverse(url_base + '-list')
        data = self.post_data
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')

        response.render()
        self.assertEqual(response.status_code, 201)

    def test_update(self):
        url_base = '%s:%s' % (self.namespace, self.url_name)
        url = reverse(url_base + '-detail', kwargs={'pk': self.item.pk})
        data = self.update_data
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data, format='json')

        response.render()
        self.assertEqual(response.status_code, 200)
