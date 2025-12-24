param(
    [switch]$CreateSuperUser
)

Write-Host "Setting up Kayabaşı Naturel local dev environment..."

# Ensure .env exists
python .\generate_env.py

# create venv if missing
if (-not (Test-Path -Path .\.venv)) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
}

Write-Host "Activating virtual environment..."
.\.venv\Scripts\Activate.ps1

Write-Host "Installing requirements..."
pip install -r requirements.txt

Write-Host "Applying migrations..."
python manage.py migrate

if ($CreateSuperUser) {
    # create superuser non-interactively if env vars present
    $admin_user = $env:DJANGO_SUPERUSER_USERNAME
    $admin_email = $env:DJANGO_SUPERUSER_EMAIL
    $admin_pass = $env:DJANGO_SUPERUSER_PASSWORD
    if ($admin_user -and $admin_pass) {
        Write-Host "Creating superuser $admin_user"
        python manage.py createsuperuser --noinput --username $admin_user --email $admin_email
uybi         # set password by writing a temporary python script and running it (avoids quoting issues)
        $tmp = [System.IO.Path]::Combine($PWD.Path, '._set_su_tmp.py')
        $py = @"
    from django.contrib.auth import get_user_model
    User = get_user_model()
    u = User.objects.get(username='$admin_user')
u.set_password('$admin_pass')
u.save()
"@
        $py | Out-File -Encoding utf8 -FilePath $tmp
        python $tmp
        Remove-Item $tmp -Force
    } else {
        Write-Host "DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD env vars not set; skipping superuser creation."
    }
}

Write-Host "Setup complete. To start the development server, run:`n .\.venv\Scripts\Activate.ps1`n python manage.py runserver"
