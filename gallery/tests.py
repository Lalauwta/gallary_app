import io
import tempfile

from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from PIL import Image

from .models import Album, Photo


def make_image_file(name='test.png'):
    """Build a tiny in-memory PNG suitable for an ImageField upload."""
    buffer = io.BytesIO()
    Image.new('RGB', (10, 10), color='red').save(buffer, format='PNG')
    buffer.seek(0)
    return SimpleUploadedFile(name, buffer.read(), content_type='image/png')


class PublicPageTests(TestCase):
    """Pages reachable without logging in."""

    def test_home_renders(self):
        self.assertEqual(self.client.get(reverse('home')).status_code, 200)

    def test_home_search(self):
        self.assertEqual(self.client.get(reverse('home'), {'q': 'sunset'}).status_code, 200)

    def test_album_list_renders(self):
        self.assertEqual(self.client.get(reverse('album-list')).status_code, 200)

    def test_login_page_renders(self):
        self.assertEqual(self.client.get(reverse('login')).status_code, 200)

    def test_register_page_renders(self):
        self.assertEqual(self.client.get(reverse('register')).status_code, 200)

    def test_missing_photo_404(self):
        self.assertEqual(self.client.get(reverse('photo-detail', args=[999])).status_code, 404)

    def test_missing_album_404(self):
        self.assertEqual(self.client.get(reverse('album-detail', args=[999])).status_code, 404)


class LoginRequiredTests(TestCase):
    """Protected views must redirect anonymous users to the login page."""

    def test_upload_redirects_anonymous(self):
        resp = self.client.get(reverse('upload'))
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/accounts/login/', resp.url)

    def test_my_photos_redirects_anonymous(self):
        self.assertEqual(self.client.get(reverse('my-photos')).status_code, 302)

    def test_create_album_redirects_anonymous(self):
        self.assertEqual(self.client.get(reverse('album-create')).status_code, 302)


class AuthFlowTests(TestCase):
    """Registration, login and logout."""

    def test_register_creates_and_logs_in_user(self):
        resp = self.client.post(reverse('register'), {
            'username': 'alice',
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice@example.com',
            'password1': 'Sup3rSecret!42',
            'password2': 'Sup3rSecret!42',
        })
        self.assertRedirects(resp, reverse('home'))
        self.assertTrue(User.objects.filter(username='alice').exists())
        # Authenticated session -> protected page now returns 200
        self.assertEqual(self.client.get(reverse('upload')).status_code, 200)

    def test_login_and_logout(self):
        User.objects.create_user('bob', password='Sup3rSecret!42')
        login_resp = self.client.post(reverse('login'), {
            'username': 'bob',
            'password': 'Sup3rSecret!42',
        })
        self.assertRedirects(login_resp, reverse('home'))
        logout_resp = self.client.get(reverse('logout'))
        self.assertRedirects(logout_resp, reverse('login'))


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class PhotoAndAlbumTests(TestCase):
    """Core gallery features: upload, detail, like, delete, albums."""

    def setUp(self):
        self.user = User.objects.create_user('carol', password='Sup3rSecret!42')
        self.other = User.objects.create_user('dave', password='Sup3rSecret!42')

    def test_upload_photo(self):
        self.client.force_login(self.user)
        resp = self.client.post(reverse('upload'), {
            'title': 'Mountain',
            'description': 'A nice view',
            'image': make_image_file(),
        })
        photo = Photo.objects.get(title='Mountain')
        self.assertRedirects(resp, reverse('photo-detail', args=[photo.pk]))
        self.assertEqual(photo.owner, self.user)

    def test_photo_detail_renders(self):
        self.client.force_login(self.user)
        photo = Photo.objects.create(owner=self.user, title='Sea', image=make_image_file())
        self.assertEqual(self.client.get(reverse('photo-detail', args=[photo.pk])).status_code, 200)

    def test_like_toggles(self):
        self.client.force_login(self.user)
        photo = Photo.objects.create(owner=self.other, title='Forest', image=make_image_file())
        self.client.get(reverse('photo-like', args=[photo.pk]))
        self.assertEqual(photo.total_likes(), 1)
        self.client.get(reverse('photo-like', args=[photo.pk]))
        self.assertEqual(photo.total_likes(), 0)

    def test_owner_can_delete_photo(self):
        self.client.force_login(self.user)
        photo = Photo.objects.create(owner=self.user, title='Doomed', image=make_image_file())
        resp = self.client.post(reverse('photo-delete', args=[photo.pk]))
        self.assertRedirects(resp, reverse('home'))
        self.assertFalse(Photo.objects.filter(pk=photo.pk).exists())

    def test_non_owner_cannot_delete_photo(self):
        self.client.force_login(self.other)
        photo = Photo.objects.create(owner=self.user, title='Safe', image=make_image_file())
        resp = self.client.post(reverse('photo-delete', args=[photo.pk]))
        self.assertEqual(resp.status_code, 404)
        self.assertTrue(Photo.objects.filter(pk=photo.pk).exists())

    def test_create_album_and_detail(self):
        self.client.force_login(self.user)
        resp = self.client.post(reverse('album-create'), {
            'title': 'Holiday',
            'description': 'Trip pics',
        })
        album = Album.objects.get(title='Holiday')
        self.assertRedirects(resp, reverse('album-detail', args=[album.pk]))
        self.assertEqual(self.client.get(reverse('album-detail', args=[album.pk])).status_code, 200)

    def test_my_photos_lists_only_own(self):
        self.client.force_login(self.user)
        Photo.objects.create(owner=self.user, title='Mine', image=make_image_file())
        Photo.objects.create(owner=self.other, title='Theirs', image=make_image_file())
        resp = self.client.get(reverse('my-photos'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Mine')
        self.assertNotContains(resp, 'Theirs')
