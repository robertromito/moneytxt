CREATE DATABASE IF NOT EXISTS grafana;
USE grafana;
GRANT USAGE ON *.* TO 'grafana'@'%' IDENTIFIED BY 'grafana';
GRANT ALL PRIVILEGES ON grafana.* TO 'grafana'@'%';
FLUSH PRIVILEGES;
SET PASSWORD FOR 'grafana'@'%' = PASSWORD('grafana');

CREATE DATABASE IF NOT EXISTS metricstxt;
USE metricstxt;
GRANT USAGE ON *.* TO 'metricstxt'@'%' IDENTIFIED BY 'metricstxt';
GRANT ALL PRIVILEGES ON metricstxt.* TO 'metricstxt'@'%';
FLUSH PRIVILEGES;
SET PASSWORD FOR 'metricstxt'@'%' = PASSWORD('metricstxt');