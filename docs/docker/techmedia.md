
```
docker compose -f docker/cloud/client/techmedia_in.yml up -d
```

### 6 To open soft-aaran-org in bash
```
docker exec -it techmedia_in bash
```

```
sudo chown -R devops:devops .
```


```
cd /cloud/frappe-bench/sites/techmedia.in
```

```
cd /cloud/frappe-bench
```

```
bench start
```

```
bench migrate
```

```
bench clear-cache
```

```
bench clear-website-cache
```

```
bench clear-website-cache
```


```
bench update --patch
```

bench --site techmedia.in  set-maintenance-mode off

bench --site techmedia.in clear-cache
bench --site techmedia.in destroy-all-sessions



```
{
 "db_host": "mariadb",
 "db_name": "erp_tmnext_db",
 "db_password": "1JEOj5LlSYATfp9m",
 "db_type": "mariadb",
 "db_user": "erp_tmnext_db",
 "encryption_key": "KqMHdGdd40t7kIMi1dQ8QdnHR-B5fSjc6BKwSNmgtiI=",
 "nginx_port": 8000,
 "allow_cors":"*",
 "allow_signup":true,
 "cookie_samesite":"Lax",
 "cookie_secure":true,
 "user_type_doctype_limit": {
  "employee_self_service": 40
 }
}
```


```
server {
    listen 80;
    server_name techmedia.in;

    location / {
        proxy_pass http://127.0.0.1:3005;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

```

```
server {
    listen 80;
    server_name erp.techmedia.in;

    location / {
        proxy_pass http://127.0.0.1:8005;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

```
sudo ln -s /etc/nginx/sites-available/techmedia.in /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/erp.techmedia.in /etc/nginx/sites-enabled/

sudo nginx -t
sudo systemctl reload nginx


```
sudo certbot --nginx
```




curl -I http://techmedia.in

dig -I http://erp.techmedia.in

curl -I -v http://techmedia.in 2>&1 | grep "Connected to"

curl -I -v http://erp.techmedia.in 2>&1 | grep "Connected to"

nslookup techmedia.in 8.8.8.8

nslookup erp.techmedia.in 8.8.8.8

nslookup techmedia.in 1.1.1.1






history -c        # Clear the current session's history
history -w        # Write the empty history to the file

If you also want to remove the history file entirely:


rm ~/.bash_history


