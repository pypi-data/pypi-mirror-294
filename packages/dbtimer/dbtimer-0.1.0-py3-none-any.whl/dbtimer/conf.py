from django.conf import settings
"""
Enter configuration for DBTimer here
"""

# Example media url for bucket

STORAGE_URL = f"https://{settings.LINODE_BUCKET}.{settings.LINODE_BUCKET_REGION}.{settings.LINODE_URL}"

