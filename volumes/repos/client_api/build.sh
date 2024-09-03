

# Migrations
cd app/database/migrations || exit
pwd
alembic -n clientdb upgrade head
alembic -n customerdb upgrade head
#alembic -n clientcache upgrade head

# Seeders
cd app/database/seeders || exit
pwd
python3 seeder.py dev