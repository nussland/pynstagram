import os
import unittest


from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.urlresolvers import resolve
from django.core.files.uploadedfile import SimpleUploadedFile

from . import models


User = get_user_model()


class PhotoTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.users = (
            {'username': 'test1', 'password': '12345678'},
            {'username': 'test2', 'password': '12345678'},
        )
        for _user in self.users:
            User.objects.create_user(**_user)

    def _login(self, username, password):
        return self.client.post(
            settings.LOGIN_URL, {'username': username, 'password': password}
        )

    def _add_photo(self, data, follow=True):
        return self.client.post(
            reverse('photos:create_photo'), data=data, follow=follow
        )

    # @unittest.skip()
    def test_create_photo_without_login(self):
        """로그인을 하지 않은 상태에서 게시물 작성
        """
        _form_data = {
            'title': 'test_title',
            'content': 'test content',
        }

        response = self._add_photo(_form_data)
        self.assertEqual(response.resolver_match.func.__name__, 'login')
        self.assertEqual(response.redirect_chain[0][1], 302)

    # @unittest.skip()
    def test_create_photo_with_login(self):
        """로그인 하고 게시물 작성, 이미지 삭제
        """
        _form_data = {
            'title': 'Sjfdlkja23@#$!@SDF title',
            'content': 'FSAD@3@#$!sdflkj content'
        }

        self._login(**self.users[0])
        response = self._add_photo(_form_data)
        latest_photo = models.Photo.objects.latest('pk')
        _view_photo_url = reverse('photos:view_photo', kwargs={'pk':latest_photo.pk})
        self.assertEqual(response.redirect_chain[0][0], _view_photo_url)
        self.assertEqual(response.redirect_chain[0][1], 302)

        self.assertEqual(
            response.resolver_match.func,
            resolve(_view_photo_url)[0]
        )

        response = self.client.get(_view_photo_url)
        self.assertEqual(response.context['photo'].pk, latest_photo.pk)
        self.assertEqual(response.context['photo'].title, _form_data['title'])

    # @unittest.skip()
    def test_create_photo_with_form_errors(self):
        """필수 입력값 검증 동작 확인
        """
        self._login(**self.users[0])

        # title, content 제외
        response = self._add_photo({})
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].has_error('title'))
        self.assertTrue(response.context['form'].has_error('content'))

        # content 제외
        _form = {'title': 'test'}
        response = self._add_photo(_form)
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].has_error('content'))

        # title 제외
        _form = {'content': 'test'}
        response = self._add_photo(_form)
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].has_error('title'))

        # 모두 입력
        _form['title'] = 'test'
        response = self._add_photo(_form)
        self.assertNotIn('form', response.context)

    # @unittest.skip()
    def test_view_photo_not_exist(self):
        """존재하지 않는 게시물 접근
        """
        response = self.client.get(
                reverse('photos:view_photo', kwargs={'pk':9999}), follow=True
        )
        self.assertEqual(response.status_code, 404)

    # @unittest.skip()
    def test_delete_photo_without_login(self):
        """로그인 없이 게시물 삭제
        """
        _form_data = {
            'title': 'Sjfdlkja23@#$!@SDF title',
            'content': 'FSAD@3@#$!sdflkj content',
        }
        self._login(**self.users[0])

        response = self._add_photo(_form_data)
        self.assertIn(response.status_code, (200, 201,))
        latest_photo = models.Photo.objects.latest('pk')

        self.client.get(settings.LOGOUT_URL)

        response = self.client.get(
                reverse('photos:delete_photo', kwargs={'pk':latest_photo.pk}), follow=True
        )
        self.assertEqual(response.resolver_match.func.__name__, 'login')
        self.assertEqual(response.redirect_chain[0][1], 302)

    # @unittest.skip()
    def test_delete_photo_without_permission(self):
        """게시물 삭제 권한 확인
        """
        _form_data = {
            'title': 'Sjfdlkja23@#$!@SDF title',
            'content': 'FSAD@3@#$!sdflkj content',
        }
        # test1 로그인 및 작성
        self._login(**self.users[0])

        response = self._add_photo(_form_data)
        self.assertIn(response.status_code, (200, 201,))
        latest_photo = models.Photo.objects.latest('pk')

        # test1 로그아웃 후 test2 로그인하여 삭제
        self.client.get(settings.LOGOUT_URL)
        self._login(**self.users[1])

        _delete_photo_url = reverse('photos:delete_photo', kwargs={'pk':latest_photo.pk})
        response = self.client.post(_delete_photo_url, follow=True)
        self.assertEqual(response.status_code, 403)

    # @unittest.skip()
    def test_delete_photo(self):
        """게시물 삭제 확인
        """
        _form_data = {
            'title': 'Sjfdlkja23@#$!@SDF title',
            'content': 'FSAD@3@#$!sdflkj content',
        }
        # test1 로그인 및 작성
        self._login(**self.users[0])

        response = self._add_photo(_form_data)
        self.assertIn(response.status_code, (200, 201,))
        latest_photo = models.Photo.objects.latest('pk')

        _delete_photo_url = reverse('photos:delete_photo', kwargs={'pk':latest_photo.pk})

        # 삭제 url GET 접근
        response = self.client.get(_delete_photo_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.resolver_match.func,
            resolve(_delete_photo_url)[0]
        )

        # 삭제 url POST 접근
        response = self.client.post(_delete_photo_url, follow=True)
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(
            response.resolver_match.func,
            resolve(reverse('photos:list_photos'))[0]
        )

        # 삭제한 게시물 접근
        response = self.client.get(reverse('photos:view_photo', kwargs={'pk':latest_photo.pk}))
        self.assertEqual(response.status_code, 404)

        # DB 확인
        _exists = models.Photo.objects.filter(pk=latest_photo.pk).exists()
        self.assertFalse(_exists)

    # @unittest.skip()
    def test_create_photo_with_image(self):
        """이미지 첨부 게시물 작성, 첨부 이미지 삭제
        """
        testimg = os.path.join(settings.BASE_DIR, 'asset') + '/testimg.jpg'
        _suf = SimpleUploadedFile('testimg.jpg', open(testimg, "rb").read())
        _form_data = {
            'title': 'Sjfdlkja23@#$!@SDF title',
            'content': 'FSAD@3@#$!sdflkj content',
            'image': _suf
        }

        self._login(**self.users[0])
        response = self._add_photo(_form_data)
        latest_photo = models.Photo.objects.latest('pk')
        _view_photo_url = reverse('photos:view_photo', kwargs={'pk':latest_photo.pk})
        self.assertEqual(response.redirect_chain[0][0], _view_photo_url)
        self.assertEqual(response.redirect_chain[0][1], 302)

        self.assertEqual(
            response.resolver_match.func,
            resolve(_view_photo_url)[0]
        )

        response = self.client.get(_view_photo_url)
        # 이미지 첨부 확인
        self.assertEqual(
            os.path.isfile(
                os.path.join(settings.MEDIA_ROOT, str(response.context['photo'].image))
            ), True
        )
        # 썸네일 생성 확인
        self.assertEqual(
            os.path.isfile(
                os.path.join(settings.MEDIA_ROOT, str(response.context['photo'].thumb))
            ), True
        )

        # 테스트 이미지 삭제
        latest_photo.image.delete()
        latest_photo.thumb.delete()

        # 삭제 확인
        response = self.client.get(_view_photo_url)
        self.assertEqual(response.context['photo'].image, '')
        self.assertEqual(response.context['photo'].thumb, '')