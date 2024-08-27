-- local customerdbuser
GRANT pg_read_all_data TO customerdbuser;
GRANT pg_write_all_data TO customerdbuser;
GRANT ALL ON SCHEMA public TO customerdbuser;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO customerdbuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO customerdbuser;