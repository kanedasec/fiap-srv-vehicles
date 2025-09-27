# 🚗 FIAP Service - Vehicles

Microserviço de **cadastro e gestão de veículos** desenvolvido em **Python + FastAPI**, utilizando **Arquitetura Hexagonal (Ports & Adapters)** e **PostgreSQL** para persistência.

---

## 🏛️ Arquitetura

A aplicação segue princípios de **Arquitetura Hexagonal**, também conhecida como **Ports & Adapters**:

- **Domain (`src/domain`)**  
  Entidades e regras de negócio puras (`Vehicle`, `VehicleStatus`).

- **Ports (`src/ports`)**  
  Contratos/Protocolos de comunicação (ex.: `VehicleRepository`).

- **Application (`src/application`)**  
  Casos de uso que orquestram a lógica de negócio (`create_vehicle`).

- **Adapters (`src/adapters`)**  
  - **db/** → Implementa persistência usando **SQLAlchemy** e **PostgreSQL**.  
  - **http/** → Exposição da API via **FastAPI** (endpoints REST).

- **main.py**  
  Ponto de entrada da aplicação, inicializa o FastAPI e conecta os routers.

📐 **Vantagens dessa abordagem**:
- Independência do banco de dados.
- Facilidade para adicionar novas interfaces (ex.: CLI, gRPC).
- Separação clara entre **regra de negócio** e **infraestrutura**.

---

## 🛢️ Banco de Dados

O serviço utiliza **PostgreSQL 15** pelas seguintes razões:

- **Confiabilidade e maturidade** em ambientes críticos.  
- **Suporte robusto a transações**.  
- Integração sólida com **SQLAlchemy** e **Alembic** (migrações).  

### 🔄 Migrações
As migrações são gerenciadas com **Alembic**:

```bash
# Criar nova migration
alembic revision --autogenerate -m "descrição"

# Aplicar migrations
alembic upgrade head
```

---

## 🐳 Executando o Projeto

1. **Subir containers com Docker Compose**:
   ```bash
   docker compose up -d --build
   ```

2. **Acessar a API**:  
   - API: [http://localhost:8000](http://localhost:8000)  
   - Documentação Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)  
   - Banco PostgreSQL: `localhost:5432`  

3. **Encerrar serviços**:
   ```bash
   docker compose down
   ```

---

## 📡 Endpoints da API

### 🔍 Healthcheck
- `GET /healthz` → Verifica se a API está rodando.  
- `GET /readyz` → Testa conectividade com o banco.

### 🚘 Vehicles

#### Criar veículo
`POST /vehicles`

**Request Body**:
```json
{
  "brand": "Toyota",
  "model": "Corolla",
  "year": 2020,
  "color": "Prata",
  "price": 85000.00
}
```

**Response**:
```json
{
  "id": "uuid-gerado",
  "brand": "Toyota",
  "model": "Corolla",
  "year": 2020,
  "color": "Prata",
  "price": 85000.0,
  "status": "available"
}
```

#### Listar veículos
`GET /vehicles?status={status}`

Parâmetro `status` pode ser:
- `available`
- `reserved`
- `sold`

**Exemplo**:
```http
GET http://localhost:8000/vehicles?status=available
```

---

