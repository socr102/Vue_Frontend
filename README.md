# DJANGO `.env` file example
```bash
DEBUG=1
SECRET_KEY=123
ALLOWED_HOSTS=localhost 127.0.0.1
POSTGRES_DB=crm
POSTGRES_USER=crm_user
POSTGRES_PASSWORD=strong_password_123
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

REDIS_URL=redis://127.0.0.1:6379/0

SERVICE_ACCOUNT_EMAIL = 'app@app.gserviceaccount.com'
SERVICE_ACCOUNT_PKCS12_FILE_PATH = 'credentials.p12'
DOMAIN = 'domain.com'
DELEGATED_EMAIL = 'admin@domain.com'
SERVICE_ACCOUNT_PKCS12_FILE_PWD='notasecret'
```

# Git Branch Naming Conventions

- Feature branches have the name feature/[id]-[#]
- Bug branches have the name bug/[id]-[#]
- Release branches have the name release/v[#] where v[#] is the associated version
- Hotfix branches have the name hotfix/[id]-[#]

 __*where [#] is a short descriptor of the task and use hyphens as separators*__

Example: feature/7-add-new-app


## Receipt Data Structure
- [Receipt example](https://developer.storebox.com/pos-api.html#operation/uploadReceipt)
- [Receipt ART POS standart](https://github.com/SwedishPaymentAndECRGroup/digital-receipt-standard/blob/master/ArtsDR200WithSwedishExtensions/resources/docs/ARTS_DR200_with_Swedish_extension.md)

## How to generate fake members
`python manage.py populate_members --count 10 --orgId 1`

where `--count` indicates how much members should be created
where `--orgId` is an organization which will be assigned to member

## How to generate fake receipts
Go to project root folder and run command:

`python manage.py populate_receipts --stores 10 --categories 10 --products 100 --receipts 1000 --articles 500 --merchantId 1 --members 1,2,3`

where `--stores` count of unique stores in result dataset

where `--categories` count of unique categories in result dataset

where `--products` count of unique products in result dataset

where `--receipts` count of unique receipts in result dataset

where `--articles` count of unique articles in result dataset

where `--merchantId` merchant user from Database for whome assign generated data. If it's not provided take first metchant from Database

where `--members` members from Database. If it's not provided take all existing members from Database


## How to start celery beat with worker
Go to the root of a project and execute
`celery -A backend worker -B -l info`
