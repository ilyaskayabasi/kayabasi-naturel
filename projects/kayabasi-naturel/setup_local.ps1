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
        # set password via Django shell
        $py = @'
from django.contrib.auth import get_user_model
User = get_user_model()
u = User.objects.get(username="' + $admin_user + '")
u.set_password("' + $admin_pass + '")
u.save()
'@
        python - <<EOF
$py
EOF
    } else {
        Write-Host "DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD env vars not set; skipping superuser creation."
    }
}

Write-Host "Starting development server (Ctrl+C to stop)..."
python manage.py runserver
