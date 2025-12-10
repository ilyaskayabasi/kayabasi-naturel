import os
import secrets

HERE = os.path.dirname(__file__)
example = os.path.join(HERE, '.env.example')
dest = os.path.join(HERE, '.env')

if not os.path.exists(example):
    print('.env.example not found')
    raise SystemExit(1)

with open(example, 'r', encoding='utf-8') as f:
    content = f.read()

if 'SECRET_KEY=change-me' in content or 'SECRET_KEY=change-me-for-a-secure-random-value' in content or 'SECRET_KEY=change-me-for-production' in content:
    secret = secrets.token_urlsafe(48)
    content = content.replace('SECRET_KEY=change-me-for-a-secure-random-value', f'SECRET_KEY={secret}')
    content = content.replace('SECRET_KEY=change-me-for-production', f'SECRET_KEY={secret}')
    content = content.replace('SECRET_KEY=change-me', f'SECRET_KEY={secret}')

with open(dest, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Created {dest} with a generated SECRET_KEY. Edit remaining values as needed.')
