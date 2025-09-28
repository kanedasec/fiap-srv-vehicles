# FIAP SRV Veículos

Serviço de gerenciamento de veículos construído em **FastAPI** com arquitetura **Hexagonal (Ports & Adapters)**, utilizando **PostgreSQL** como banco de dados e **Docker Compose** para orquestração dos serviços.

---

## 🏗️ Arquitetura

A aplicação segue os princípios de **Domain-Driven Design (DDD)** e **Hexagonal Architecture**:

- **Domain (`src/domain`)**  
  Contém as entidades centrais (`Vehicle`, `VehicleStatus`) e regras de negócio.

- **Application (`src/application`)**  
  Define os casos de uso (`create_vehicle`, `reserve_vehicle`, `sell_vehicle`, `unreserve_vehicle`).

- **Ports (`src/ports`)**  
  Protocolos/interfaces que definem contratos de repositórios.

- **Adapters (`src/adapters`)**  
  - **DB (`src/adapters/db`)**: implementação usando SQLAlchemy.  
  - **HTTP (`src/adapters/http`)**: exposição dos endpoints via FastAPI.

- **Infraestrutura**  
  Banco de dados PostgreSQL rodando em container Docker.

---

## 🗄️ Banco de Dados

- Banco escolhido: **PostgreSQL**
- Motivos:
  - Robustez e confiabilidade
  - Bom suporte a tipos enumerados (enums), usado para `VehicleStatus`
  - Integração nativa com SQLAlchemy
- Migrações gerenciadas com **Alembic**

---

## 🚀 Como rodar o projeto

### 1. Subir containers

```bash
sudo docker compose up --build -d
```

### 2. Aplicar migrações

```bash
alembic upgrade head
```

### 3. Acessar API

A aplicação roda em:  
👉 [http://localhost:8001](http://localhost:8001)

---

## 📚 Endpoints

### Health

- `GET /healthz` → Verifica se a API está viva  
- `GET /readyz` → Verifica conectividade com o banco

---

### Vehicles

- **Criar veículo**

```http
POST /vehicles
Content-Type: application/json

{
  "brand": "Ford",
  "model": "Fiesta",
  "year": 2018,
  "color": "blue",
  "price": 45000.0
}
```

- **Listar veículos por status**

```http
GET /vehicles?status=available
GET /vehicles?status=reserved
GET /vehicles?status=sold
```

- **Reservar veículo**

```http
POST /vehicles/{id}/reserve
Content-Type: application/json

{
  "reserved_by": "kaneda"
}
```

- **Cancelar reserva**

```http
POST /vehicles/{id}/unreserve
Content-Type: application/json

{
  "reserved_by": "kaneda"
}
```

- **Marcar como vendido**

```http
POST /vehicles/{id}/sell
```

---

## 🧪 Testes rápidos (curl)

```bash
# Saúde
curl -s http://localhost:8001/healthz
curl -s http://localhost:8001/readyz

# Listar disponíveis
curl -s "http://localhost:8001/vehicles?status=available"

# Criar
curl -s -X POST http://localhost:8001/vehicles   -H "Content-Type: application/json"   -d '{"brand":"Ford","model":"Fiesta","year":2018,"color":"blue","price":45000.0}'

# Reservar
curl -s -X POST http://localhost:8001/vehicles/{id}/reserve   -H "Content-Type: application/json"   -d '{"reserved_by":"kaneda"}'

# Cancelar reserva
curl -s -X POST http://localhost:8001/vehicles/{id}/unreserve

# Vender
curl -s -X POST http://localhost:8001/vehicles/{id}/sell
```

---

## 📂 Estrutura de Pastas

```
src/
 ├── adapters/
 │   ├── db/         # ORM, repositorios, base SQLAlchemy
 │   └── http/       # Endpoints FastAPI
 │   └── messaging/  # Serviços de mensageria
 ├── application/    # Casos de uso (usecases)
 │   └── usecases/   # Casos de uso (usecases)
 ├── domain/         # Entidades e enums centrais
 ├── ports/          # Interfaces de repositório
 └── main.py         # Ponto de entrada da API
```

---

## 🔑 Decisões de Design

1. **Arquitetura hexagonal** para garantir isolamento entre camadas e facilidade de testes.  
2. **PostgreSQL** escolhido pela robustez, compatibilidade com enums e uso em produção real.  
3. **FastAPI** para endpoints REST, validação automática com Pydantic e documentação embutida (`/docs`).  
4. **Docker Compose** para subir todo o stack com um único comando.  
