
```
docker compose -f docker/cloud/client/techmedia_in.yml up -d
```

### 6 To open soft-aaran-org in bash
```
docker exec -it techmedia_in bash
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
bench build
```

```
bench update --patch
```
