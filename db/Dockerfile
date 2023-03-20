# db/Dockerfile
FROM mysql:5.7

# # Add custom configurations or scripts if needed
# COPY my.cnf /etc/mysql/my.cnf
# COPY init.sql /docker-entrypoint-initdb.d/init.sql

# # Fix permission issue
# USER root
# RUN chmod -R 755 /docker-entrypoint-initdb.d

COPY my.cnf /etc/mysql/conf.d/
COPY init.sql /docker-entrypoint-initdb.d/

# Change ownership of the initdb.d directory
RUN chown -R mysql:mysql /docker-entrypoint-initdb.d/

CMD ["--default-authentication-plugin=mysql_native_password"]