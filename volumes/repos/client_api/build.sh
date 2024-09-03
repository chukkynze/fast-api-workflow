

# Migrations
cd app/database/migrations || exit
alembic -n clientdb upgrade head
alembic -n customerdb upgrade head
#alembic -n clientcache upgrade head

cd /var/www/json || exit

# Seeders
cd app/database/seeders || exit
python3 seeder.py dev