import os
import urllib.request
import urllib.error
import urllib.parse
import json
import logging
from django.core.files.storage import Storage, FileSystemStorage
from django.core.files.base import ContentFile
from django.utils.deconstruct import deconstructible

logger = logging.getLogger(__name__)

@deconstructible
class SupabaseStorage(Storage):
    """
    Custom Django Storage backend that integrates with Supabase Storage.
    If credentials are not configured in environment variables, it gracefully
    falls back to Django's standard FileSystemStorage.
    """
    def __init__(self, bucket_name=None, supabase_url=None, supabase_key=None):
        self.supabase_url = supabase_url or os.environ.get("SUPABASE_URL")
        # Strip trailing slash and quotes from URL if present
        if self.supabase_url:
            self.supabase_url = self.supabase_url.strip('"\'').rstrip('/')
            
        self.supabase_key = supabase_key or os.environ.get("SUPABASE_KEY")
        if self.supabase_key:
            self.supabase_key = self.supabase_key.strip('"\'')
            
        self.bucket_name = bucket_name or os.environ.get("SUPABASE_BUCKET_NAME", "Portfolio_bucket")
        if self.bucket_name:
            self.bucket_name = self.bucket_name.strip('"\'')

        
        # Check if we have the minimum configuration for Supabase
        if not self.supabase_url or not self.supabase_key or self.supabase_key == "your_service_role_key_here":
            self.is_fallback = True
            self.fallback_storage = FileSystemStorage()
            logger.warning(
                "Supabase Storage credentials not configured or set to default placeholder. "
                "Falling back to local FileSystemStorage."
            )
        else:
            self.is_fallback = False

    def _get_headers(self, with_content_type=False, content_type='application/octet-stream'):
        headers = {
            "Authorization": f"Bearer {self.supabase_key}",
            "apikey": self.supabase_key,
        }
        if with_content_type:
            headers["Content-Type"] = content_type
        return headers

    def _quote_path(self, name):
        """
        Normalize separators and URL-encode path segments to handle spaces and special characters.
        """
        name = name.replace('\\', '/')
        parts = [urllib.parse.quote(part) for part in name.split('/')]
        return '/'.join(parts)

    def _open(self, name, mode='rb'):
        if self.is_fallback:
            return self.fallback_storage._open(name, mode)
            
        quoted_name = self._quote_path(name)
        url = f"{self.supabase_url}/storage/v1/object/{self.bucket_name}/{quoted_name}"
        req = urllib.request.Request(url, headers=self._get_headers())
        try:
            with urllib.request.urlopen(req) as response:
                return ContentFile(response.read())
        except urllib.error.URLError as e:
            raise IOError(f"Could not open file {name} from Supabase Storage: {e}")

    def _save(self, name, content):
        if self.is_fallback:
            return self.fallback_storage._save(name, content)
            
        quoted_name = self._quote_path(name)
        url = f"{self.supabase_url}/storage/v1/object/{self.bucket_name}/{quoted_name}"
        
        content_type = getattr(content, 'content_type', 'application/octet-stream')
        headers = self._get_headers(with_content_type=True, content_type=content_type)
        headers["x-upsert"] = "true"  # Automatically overwrite if file exists
        
        # Read content bytes
        data = content.read()
        
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        try:
            with urllib.request.urlopen(req) as response:
                response.read()
        except urllib.error.HTTPError as e:
            error_msg = e.read().decode('utf-8')
            raise IOError(f"Failed to save file to Supabase Storage: {error_msg} (Status {e.code})")
        except urllib.error.URLError as e:
            raise IOError(f"Failed to connect to Supabase: {e}")
            
        return name

    def exists(self, name):
        if self.is_fallback:
            return self.fallback_storage.exists(name)
            
        quoted_name = self._quote_path(name)
        # Try retrieving object info
        url = f"{self.supabase_url}/storage/v1/object/info/public/{self.bucket_name}/{quoted_name}"
        req = urllib.request.Request(url, headers=self._get_headers())
        try:
            with urllib.request.urlopen(req) as response:
                return response.status == 200
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return False
            # In case of other errors (e.g. permission issues or API version mismatches), return False
            return False
        except Exception:
            return False

    def url(self, name):
        if self.is_fallback:
            return self.fallback_storage.url(name)
            
        quoted_name = self._quote_path(name)
        # Public URL structure: https://<ref>.supabase.co/storage/v1/object/public/<bucket>/<path>
        return f"{self.supabase_url}/storage/v1/object/public/{self.bucket_name}/{quoted_name}"

    def delete(self, name):
        if self.is_fallback:
            return self.fallback_storage.delete(name)
            
        quoted_name = self._quote_path(name)
        url = f"{self.supabase_url}/storage/v1/object/{self.bucket_name}/{quoted_name}"
        req = urllib.request.Request(url, headers=self._get_headers(), method='DELETE')
        try:
            with urllib.request.urlopen(req) as response:
                response.read()
        except urllib.error.HTTPError as e:
            # If the file is already gone, count it as a success
            if e.code != 404:
                error_msg = e.read().decode('utf-8')
                raise IOError(f"Failed to delete file from Supabase Storage: {error_msg} (Status {e.code})")
        except urllib.error.URLError as e:
            raise IOError(f"Failed to connect to Supabase: {e}")

    def size(self, name):
        if self.is_fallback:
            return self.fallback_storage.size(name)
            
        quoted_name = self._quote_path(name)
        url = f"{self.supabase_url}/storage/v1/object/info/public/{self.bucket_name}/{quoted_name}"
        req = urllib.request.Request(url, headers=self._get_headers())
        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                metadata = data.get('metadata', {})
                # Size might be at the root or within metadata
                return data.get('size') or metadata.get('size') or 0
        except Exception:
            return 0
