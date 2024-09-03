import sys
from app.database.seeders.development.posts_table_seeder import posts_table_seeder as dev_1_posts_table_seeder
from app.database.seeders.test.posts_table_seeder import posts_table_seeder as test_1_posts_table_seeder
from app.database.seeders.qa.posts_table_seeder import posts_table_seeder as qa_1_posts_table_seeder

env = sys.argv[1]

if env in ["dev", "development"]:
    print(f'Seeding for {env}')
    dev_1_posts_table_seeder()
elif env in ["test", "testing"]:
    print(f'Seeding for {env}')
    test_1_posts_table_seeder()
elif env in ["qa", "acceptance"]:
    print(f'Seeding for {env}')
    qa_1_posts_table_seeder()
else:
    raise Exception(f"Invalid environment '{env}' selected. Data going to production goes in a migration, not a seeder.")