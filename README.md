# Test app

## Run app

### Build

```commandline
docker compose build
```

### Run (database volumes will be created at `~/app_postgres` directory)

```commandline
docker compose up
```

## Available methods

### GET /api/v1/categories/filter/

1. *title* - categories with the same title
2. *title__contains* - categories containing substring in the title

#### Return categories UUID

### GET /api/v1/categories/\<UUID>/

#### Return category by UUID

### POST /api/v1/categories/

1. *title* - category title

#### Create new category

### PUT /api/v1/categories/\<UUID>/

1. *title* - category title

#### Edit category by UUID

### DELETE /api/v1/categories/\<UUID>/

#### Delete category by UUID

### GET /api/v1/products/filter/

1. *category_uuid* - filter by category UUID
2. *title__contains* - filter by substring in product title
3. *cost__lower_than* - filter by cost lower than
4. *other* filter

#### Return products UUID

### GET /api/v1/products/\<UUID>/

#### Return product by UUID

### POST /api/v1/products/

1. *title* - product title
2. *description* - product description
3. *cost* - product cost
4. *category_uuid* - product category

#### Create new product

### PUT /api/v1/products/\<UUID>/

1. *title* - product title
2. *description* - product description
3. *cost* - product cost
4. *category_uuid* - product category

#### Edit product by UUID

### DELETE /api/v1/products/\<UUID>/

#### Delete product by UUID