from decouple import config


class EnvironmentVariable:
    """
    @note: This class contains all the access data, common configuration variables
    that used in this application
    """
    
    # Environment
    BACKEND_ENVIRONMENT = config('BACKEND_ENVIRONMENT', 'LOCAL') # LOCAL, DEV, PROD
    BACKEND_PORT = config('PORT', 5000)

    HOST_URL = config('HOST_URL', "http://127.0.0.1:8000")
    FRONTEND_URL = config('FRONTEND_URL', 'http://localhost:3000')
    
    DEFAULT_NETWORK = int(config('DEFAULT_NETWORK', 1))

    # Database
    DATABASE_NAME = config('DATABASE_NAME', 'acquire')
    DATABASE_HOST = config('DATABASE_HOST', 'localhost')
    DATABASE_PORT = config('DATABASE_PORT', '5432')
    DATABASE_USERNAME = config('DATABASE_USERNAME', 'postgres')
    DATABASE_PASSWORD = config('DATABASE_PASSWORD', 'postgres')

    # AWS S3 Configurations
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', 'SCH59NYTBER50DFFKM6')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', '1556bd2e-34d1-4246-81cb-650f6d72f35')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', 'acquire')
    AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', 'nl-ams')
    AWS_S3_BASE_URL = config('AWS_S3_BASE_URL',
                             f'https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.scw.cloud')
    AWS_MEDIA_FOLDER = config('AWS_MEDIA_FOLDER', 'backend-media')

    # JWT Access
    JWT_SECRET_KEY = config('JWT_SECRET_KEY', "34mpKHq5nWPCRyZYtODXlQ")

    # Access configs
    CLIENT_ID = config('CLIENT_ID', 'n3fYB0qMFwYidMx4tkqKMA')
    AES_SECRET_KEY = config('AES_SECRET_KEY', 'v4ttjxwi9qGI0an3DlPnbVWpjJWzsm22')

    # Developer's API Key (Only for testing the APIs)
    API_DEV_SECRET_KEY = config('API_DEV_SECRET_KEY', '9KVvI9QM_98vtE__EYrhCgxFad-6do8fRB9050923uc')
    
    DEBUG = config("DEBUG", "True")