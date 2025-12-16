#!/usr/bin/env python
import os
import sys
import django

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()
    
    from django.contrib.auth.models import User
    
    # Demo hesabı
    if not User.objects.filter(username='demo').exists():
        User.objects.create_user(
            username='demo',
            email='demo@example.com',
            password='demo1234',
            first_name='Demo',
            last_name='Kullanıcı'
        )
        print('✓ Demo hesabı oluşturuldu')
    else:
        print('✓ Demo hesabı zaten var')
    
    # Admin hesabı
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print('✓ Admin hesabı oluşturuldu')
    else:
        print('✓ Admin hesabı zaten var')
