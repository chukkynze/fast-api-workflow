GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;

-- local clientdbuser
DROP USER clientdbuser;
FLUSH PRIVILEGES;
CREATE USER 'clientdbuser'@'%'         IDENTIFIED BY 'secret123';
CREATE USER 'clientdbuser'@'0.0.0.0'   IDENTIFIED BY 'secret123';
CREATE USER 'clientdbuser'@'127.0.0.1' IDENTIFIED BY 'secret123';
CREATE USER 'clientdbuser'@'localhost' IDENTIFIED BY 'secret123';
FLUSH PRIVILEGES;

GRANT ALL PRIVILEGES ON *.* TO 'clientdbuser'@'%';
GRANT ALL PRIVILEGES ON *.* TO 'clientdbuser'@'0.0.0.0';
GRANT ALL PRIVILEGES ON *.* TO 'clientdbuser'@'127.0.0.1';
GRANT ALL PRIVILEGES ON *.* TO 'clientdbuser'@'localhost';
FLUSH PRIVILEGES;

-- Read Only grafana user
-- GRANT SELECT ON *.* TO 'grafana'@'%'         IDENTIFIED BY 'grafana123';
-- GRANT SELECT ON *.* TO 'grafana'@'0.0.0.0'   IDENTIFIED BY 'grafana123';
-- GRANT SELECT ON *.* TO 'grafana'@'127.0.0.1' IDENTIFIED BY 'grafana123';
-- GRANT SELECT ON *.* TO 'grafana'@'localhost' IDENTIFIED BY 'grafana123';
-- GRANT SELECT ON *.* TO 'grafana'@'mysql'     IDENTIFIED BY 'grafana123';

--  PMM user
-- GRANT ALL PRIVILEGES ON *.* TO 'pmm'@'%'         IDENTIFIED BY 'academystack123';
-- GRANT ALL PRIVILEGES ON *.* TO 'pmm'@'0.0.0.0'   IDENTIFIED BY 'academystack123';
-- GRANT ALL PRIVILEGES ON *.* TO 'pmm'@'127.0.0.1' IDENTIFIED BY 'academystack123';
-- GRANT ALL PRIVILEGES ON *.* TO 'pmm'@'localhost' IDENTIFIED BY 'academystack123';
-- GRANT ALL PRIVILEGES ON *.* TO 'pmm'@'mysql'     IDENTIFIED BY 'academystack123';

FLUSH PRIVILEGES;