# Alembic Multi DB resource Setup & Usage

1. Determine the data resources you want to simultaneously interact with using migrations, their alias and the tech. 
    Examples could be:
   1. Customer Relational Data - "custdb" - MySql RDBMS
   2. Customer Data Cache - "cachestore" - Redis
   3. Customer Document Database - "docdb" - Mongo
   4. Customer Deep Object Database - "objectdb" - PostgreSql RDBMS

    For this project, I'm using migrations with the following data resources:
   1. Client Relational Data - "clientdb" - MySql
   2. Customer Relational Data - "customerdb" - Postgres
   3. Client Data Cache - "clientcache" - Redis

    Ensure that each resource has the proper drivers and dependencies installed on the machine/device
    as well as for pip. Also, consider that SqlAlchemy has different connections and different connection requirements
    for each connection & resource. You'll have to work this out for the actual migration code as well.

2. Initialize (MultiDB) migrations in app 
   ```text
   cd to the migrations folder: 'cd app/database/migrations'
   RUN alembic init multidb
   ```
3. In the newly created 'multidb' folder:
   1. Convert the README file to a README.md file
   2. Delete the versions folder. It will be replaced.
   3. Modify the alembic.ini file to reflect your chosen data resources
      1. Under the `[alembic]` section, add a 'databases' key with a comma 
         separated list of the aliases you chose for your resources:
         `databases = clientdb, customerdb, clientcache`
      2. Add sections for each resource: `[resource-alias]`
         ```text
         [clientdb]
         ...
         
         [customerdb]
         ...
         
         [clientcache]
         ...
         ```
      3. In each resource section, specify a `sqlalchemy.url` key and a `version_locations` key:
         ```text
         [clientdb]
         sqlalchemy.url = mysql://clientdbuser:secret123@host.docker.internal/clientdb
         version_locations = ./multidb/clientdb/versions
         ```
         Of course, do not hard code the url values but pull them from an environmentally aware config
      4. Add a `[DEFAULT]` section (Not [default] but [DEFAULT]) and place all the values that won't change
         for a resource. If you want a value to change for a resource, add it to the resource's section:
         ```text
         [DEFAULT]
         script_location = multidb
         file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s
         prepend_sys_path = .
         timezone = UTC
         # version_path_separator = os.pathsep
         # truncate_slug_length = 40
         # revision_environment = false
         # sourceless = false
         # recursive_version_locations = false
         # output_encoding = utf-8
         ```
      5. The rest you can tweak as you desire. I change all the logging to DEBUG on local to see as much output as possible.

4. Now, migrations are interacted with based on the resource.
5. To make a new migration, navigate to the migrations folder (wherever the alembic.ini file is located) and ... 
   1. for the 'clientdb'    resource: `alembic -n clientdb revision -m "create posts table"`
   2. for the 'customerdb'  resource: `alembic -n customerdb revision -m "create posts table"`
   3. for the 'clientcache' resource: `alembic -n clientcache revision -m "store initial posts"`
6. Migrations will be created in the `version_locations` folder. The current structure allows you to keep resource specific
   files in easy to locate directories such as a csv or xml file that your migration can reference in code without clashing
   with another resource. Creating migrations does not depend on any connection to the actual resource.
7. To connect with a resource, alembic will use the `sqlalchemy.url` key in the resource section, to connect. But, 
   instead of having that hard coded in the ini, you can have that injected into the alembic process from a config.
   To do this 
8. To run your completed migration
   1. for the 'clientdb'    resource: `alembic -n clientdb upgrade head`
   2. for the 'customerdb'  resource: `alembic -n customerdb upgrade head`
   3. for the 'clientcache' resource: `alembic -n clientcache upgrade head`
9. Other commands:
   1. `alembic upgrade +-X` where x is the number of 
   2. `alembic upgrad <rev string>+X`