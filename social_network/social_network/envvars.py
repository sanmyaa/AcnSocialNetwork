import os

DJANGO_SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "VYhBOlgjoPd54DXudxX2VmSSdLZWzXKSmFPsDPUdARsms9RLTgsPRbg2oucIxHn8vhI",
)
POSTGRES_DB =  os.environ.get("POSTGRES_DB", "sample_db")
POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "password")
POSTGRES_HOST = "sample-db-instance.c58euekkwwfu.eu-north-1.rds.amazonaws.com"
POSTGRES_PORT = "5432" #os.environ.get("POSTGRES_PORT", "5433")
DJANGO_JWT_SIGNING_KEY = os.environ.get(
    "DJANGO_JWT_SIGNING_KEY", "ntz4nU2tGjeE2c-XR0Dqj_hbPuRcaVMW1GvVWo3dzi4=y"
)
