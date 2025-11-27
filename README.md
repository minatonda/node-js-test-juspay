# Notes Service API

REST API for text notes management - Juspay Brazil Assignment

## 📋 Description

Backend service developed with NestJS that allows creating, listing, updating, deleting and searching text notes. Implements pagination, keyword search, tag filtering and soft delete.

## 🚀 Technologies

- **NestJS** - Node.js framework
- **TypeORM** - Database ORM
- **SQLite (in-memory)** - In-memory database
- **Swagger** - API documentation
- **TypeScript** - Programming language

## 📦 Installation

```bash
# Install dependencies
npm install

# Configure environment variables
cp .env.example .env
# Edit .env with your settings
```

## REDDIS Settings on Docker
docker run -d --name redis-dev -p 6379:6379 redis:7.4-alpine

## 🗄️ Database Configuration

The project uses **in-memory SQLite** (`:memory:`), which means:

- ✅ **Zero configuration**: No need to install or configure any database server
- ✅ **Simplified setup**: Just install dependencies and run the application
- ⚠️ **Data does not persist**: All data is lost when the application is restarted (ideal for development and testing)

Migrations are executed automatically on application startup.

## 🏃 Running the Application

```bash
# Development
npm run start:dev

# Production
npm run build
npm run start:prod
```

The application will be available at `http://localhost:3000`

## 📚 Swagger Documentation

After starting the application, access the interactive documentation at:
- **Swagger UI**: http://localhost:3000/docs

## 🔌 Endpoints

### Create Note
```
POST /notes
```

### List Notes
```
GET /notes?page=1&limit=20&search=keyword&tags[]=tag1&sortBy=createdAt&sortOrder=DESC
```

### Get Note by ID
```
GET /notes/:id
```

### Update Note
```
PATCH /notes/:id
```

### Delete Note
```
DELETE /notes/:id
```

### Health Check
```
GET /health
```

## 📝 Features

### Essential
- ✅ Create note (title, body, optional tags)
- ✅ List notes with pagination
- ✅ Update note (partial or complete)
- ✅ Delete note (soft delete)
- ✅ Search by keywords (title/body)

### Optional
- ✅ Tag filtering
- ✅ Soft delete
- ✅ Server-side sorting (createdAt, updatedAt, title)

## 🛠️ Available Scripts

```bash
# Development
npm run start:dev        # Start in watch mode
npm run start:debug      # Start in debug mode

# Build
npm run build            # Compile the project

# Migrations
npm run migration:generate  # Generate new migration
npm run migration:run       # Run migrations
npm run migration:revert    # Revert last migration

# Tests
npm run test             # Run unit tests (Jest)
npm run test:watch       # Run tests in watch mode
npm run test:cov         # Run tests with coverage
npm run test:e2e         # Run E2E tests (Python) - requires API running
npm run test:e2e:base    # Run E2E tests with custom URL

# Linting
npm run lint             # Run ESLint
npm run format           # Format code with Prettier
```

## 📋 Project Structure

```
src/
├── common/                          # Shared abstractions and utilities
│   ├── base/
│   │   ├── base-entity.ts          # Base entity with id, timestamps
│   │   └── soft-deletable-entity.ts # Base entity with soft delete
│   ├── dto/
│   │   ├── pagination-query.dto.ts  # Base pagination query DTO
│   │   └── pagination-response.dto.ts # Base pagination response DTO
│   ├── interfaces/
│   │   └── soft-deletable.interface.ts # Soft deletable interface
│   ├── pipes/
│   │   └── uuid-validation.pipe.ts  # UUID validation pipe (404 instead of 400)
│   └── utils/
│       ├── pagination.util.ts      # Pagination utilities
│       ├── uuid.util.ts            # UUID validation utilities
│       └── soft-delete.util.ts     # Soft delete utilities
├── notes/
│   ├── dto/
│   │   ├── create-note.dto.ts
│   │   ├── update-note.dto.ts
│   │   ├── list-notes-query.dto.ts
│   │   └── list-notes-response.dto.ts
│   ├── note.entity.ts
│   ├── notes.controller.ts
│   ├── notes.service.ts
│   └── notes.module.ts
├── database/
│   ├── config/
│   │   └── typeorm.config.ts
│   └── migrations/
│       └── 1770000000000-CreateNotesTable.ts
├── app.module.ts
└── main.ts
```

## 🏗️ Architecture Patterns & Abstractions

This project implements several reusable patterns and abstractions to ensure consistency, maintainability, and code reusability across all endpoints.

### 📄 Pagination Pattern

All list endpoints follow a standardized pagination pattern.

#### Components

- **`PaginationQueryDto`** (`src/common/dto/pagination-query.dto.ts`)
  - Base DTO for pagination query parameters
  - Fields: `page` (default: 1, min: 1), `limit` (default: 20, min: 1)
  - Includes validation and Swagger documentation

- **`PaginationResponseDto<T>`** (`src/common/dto/pagination-response.dto.ts`)
  - Generic base DTO for paginated responses
  - Structure: `{ items: T[], total: number, page: number, limit: number, pageCount: number }`

- **Pagination Utilities** (`src/common/utils/pagination.util.ts`)
  - `normalizePaginationParams()`: Normalizes and validates pagination parameters
  - `calculatePageCount()`: Calculates total number of pages
  - `createPaginationResponse()`: Creates consistent paginated response

#### Usage Example

```typescript
// Query DTO extends PaginationQueryDto
export class ListItemsQueryDto extends PaginationQueryDto {
  // Add specific fields (search, filters, etc.)
}

// Service uses utilities
const { page, limit } = normalizePaginationParams(query.page, query.limit)
// ... query builder ...
return createPaginationResponse(items, total, page, limit)
```

### 🔑 UUID Validation Pattern

Consistent UUID validation that returns 404 (Not Found) instead of 400 (Bad Request) for invalid UUIDs, providing better UX.

#### Components

- **`UuidValidationPipe`** (`src/common/pipes/uuid-validation.pipe.ts`)
  - Custom pipe that validates UUID v4 format
  - Throws `NotFoundException` (404) for invalid UUIDs
  - Factory function: `createUuidValidationPipe(entityName)`

- **UUID Utilities** (`src/common/utils/uuid.util.ts`)
  - `isValidUUID()`: Validates UUID v4 format
  - `validateUUIDOrThrow()`: Validates and throws NotFoundException
  - `UUID_V4_REGEX`: UUID v4 validation regex

#### Usage Example

```typescript
// Controller
@Get(':id')
async findOne(@Param('id', createUuidValidationPipe('Note')) id: string) {
  return this.service.findOne(id)
}
```

### 🗑️ Soft Delete Pattern

Standardized soft delete implementation that excludes deleted entities from queries automatically.

#### Components

- **`SoftDeletableEntity`** (`src/common/base/soft-deletable-entity.ts`)
  - Base entity class with `deletedAt` field
  - Extends `BaseEntity` (includes `id`, `createdAt`, `updatedAt`)
  - Includes index on `deletedAt` for performance

- **`ISoftDeletable`** (`src/common/interfaces/soft-deletable.interface.ts`)
  - Interface for entities that support soft delete
  - Type guard: `isSoftDeletable()`

- **Soft Delete Utilities** (`src/common/utils/soft-delete.util.ts`)
  - `applySoftDeleteFilter()`: Applies soft delete filter to query builder
  - `excludeDeleted()`: Adds soft delete condition to where clause
  - `performSoftDelete()`: Sets `deletedAt` to current date
  - `isSoftDeleted()`: Checks if entity is soft deleted

#### Usage Example

```typescript
// Entity extends SoftDeletableEntity
export class MyEntity extends SoftDeletableEntity {
  // Only specific fields
}

// Service
// Query builder
applySoftDeleteFilter(queryBuilder, 'myEntity')

// FindOne
const entity = await this.repository.findOne({
  where: excludeDeleted({ id }),
})

// Soft delete
performSoftDelete(entity)
await this.repository.save(entity)
```

### 🏛️ Base Entity Pattern

Common entity structure to avoid code duplication and ensure consistency.

#### Components

- **`BaseEntity`** (`src/common/base/base-entity.ts`)
  - Abstract base class with common fields:
    - `id`: UUID (auto-generated)
    - `createdAt`: Creation timestamp (auto-managed)
    - `updatedAt`: Update timestamp (auto-managed)
  - Includes Swagger documentation

- **`SoftDeletableEntity`** (`src/common/base/soft-deletable-entity.ts`)
  - Extends `BaseEntity`
  - Adds `deletedAt` field for soft delete support
  - Includes index on `deletedAt`

#### Usage Example

```typescript
// Entity with soft delete
@Entity({ name: 'items' })
export class ItemEntity extends SoftDeletableEntity {
  @Column()
  name: string
  // Automatically has: id, createdAt, updatedAt, deletedAt
}

// Entity without soft delete
@Entity({ name: 'categories' })
export class CategoryEntity extends BaseEntity {
  @Column()
  name: string
  // Automatically has: id, createdAt, updatedAt
}
```

### 📦 Benefits of These Patterns

1. **Consistency**: All endpoints follow the same patterns
2. **Reusability**: Base classes and utilities can be used across all modules
3. **Maintainability**: Changes in one place affect all endpoints
4. **Type Safety**: Strong typing throughout the application
5. **Documentation**: Automatic Swagger documentation
6. **Less Code**: Reduced duplication and boilerplate
7. **Better UX**: Consistent error handling (404 for invalid UUIDs)
8. **Scalability**: Easy to add new endpoints following the same patterns

### 🔄 How to Use in New Endpoints

When creating a new endpoint, follow these patterns:

1. **Entity**: Extend `BaseEntity` or `SoftDeletableEntity`
2. **Query DTO**: Extend `PaginationQueryDto` for list endpoints
3. **Response DTO**: Extend `PaginationResponseDto<T>` for paginated responses
4. **Controller**: Use `createUuidValidationPipe()` for UUID parameters
5. **Service**: Use pagination and soft delete utilities

## 🔒 Validation

The API uses `class-validator` for automatic input data validation. All DTOs have appropriate validations.

## 📊 Logging

The service uses NestJS `Logger` to log important operations:
- Note creation
- Note updates
- Note deletion
- Errors

## 🧪 E2E Tests

The project includes an E2E test suite in Python that validates all API functionalities.

### Prerequisites

- Python 3.9 or higher
- API running (default at `http://localhost:3000`)

### Installation

```bash
cd tests
pip install -r requirements.txt
# or
pip3 install -r requirements.txt
```

### Execution

```bash
# Run tests (API must be running)
npm run test:e2e

# Or directly
cd tests
python3 run_tests.py

# With custom URL
python3 run_tests.py --base http://localhost:3000
```

### What is tested

- ✅ Health check
- ✅ Complete note CRUD
- ✅ Required field validation
- ✅ Pagination and sorting
- ✅ Keyword search
- ✅ Tag filtering
- ✅ Soft delete

For more details, see `tests/README.md`.

## 🧪 Usage Examples

### Create a note
```bash
curl -X POST http://localhost:3000/notes \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My first note",
    "body": "This is the note content",
    "tags": ["work", "important"]
  }'
```

### List notes with search
```bash
curl "http://localhost:3000/notes?page=1&limit=20&search=important&tags[]=work"
```

### Update a note
```bash
curl -X PATCH http://localhost:3000/notes/{id} \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated title",
    "body": "Updated content"
  }'
```

## 📄 License

UNLICENSED

