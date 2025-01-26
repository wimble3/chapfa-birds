## [Local quickstart]

### 1. Create `.env` file in the root directory, the example `.env.example` file is also in the root folder

### 2. Run the command that launches docker containers

```
docker compose -f .\docker-compose.local.yml up -d --build
```

### 3. To stop containers use

```
docker compose -f .\docker-compose.local.yml down
```

---

## [Local convenient start]

### 1. Create `.env` file in the root directory, the example `.env.example` file is also in the root folder

### 2. Comment out the app and all consumers containers

### 3. Run the command that launches the remaining docker containers

```
docker compose -f .\docker-compose.local.yml up -d --build
```

### 4. Run application

```
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Run alembic command for upgrading database state

```
alembic upgrade head
```

### 6. Run via IDE consumers you need (python scripts at `/management/run/` directory) manually
