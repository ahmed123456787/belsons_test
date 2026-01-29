# Belsons News API Documentation

## Overview

The Belsons News API is a RESTful web service that provides access to news articles, sources, categories, languages, and countries. The API supports filtering, searching, and pagination to help clients retrieve news data efficiently.

**Base URL:** `http://localhost:8000/apis/v1/`

**API Version:** v1

**Content-Type:** `application/json`

---

## Table of Contents

1. [Authentication](#authentication)
2. [Rate Limiting](#rate-limiting)
3. [Response Format](#response-format)
4. [Error Handling](#error-handling)
5. [Endpoints](#endpoints)
6. [Query Parameters](#query-parameters)
7. [Filtering & Searching](#filtering--searching)
8. [Pagination](#pagination)
9. [Examples](#examples)

---

## Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible.

---

## Rate Limiting

Rate limiting is not currently implemented. However, it is recommended to implement rate limiting in production environments.

---

## Response Format

All API responses follow a standard JSON format:

### Success Response (2xx)

```json
{
  "count": 10,
  "next": "http://localhost:8000/apis/v1/news/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Article Title",
      "description": "Article Description",
      ...
    }
  ]
}
```

### Error Response (4xx, 5xx)

```json
{
  "error": "Error message describing what went wrong"
}
```

---

## Error Handling

| HTTP Status | Description                               |
| ----------- | ----------------------------------------- |
| 200         | OK - Request successful                   |
| 400         | Bad Request - Invalid query parameters    |
| 404         | Not Found - Resource does not exist       |
| 500         | Internal Server Error - Server-side error |

---

## Endpoints

### 1. List News Articles

**Endpoint:** `GET /news/`

**Description:** Retrieve a paginated list of news articles with support for filtering, searching, and sorting.

**Query Parameters:**

- `page` (integer, optional): Page number for pagination (default: 1)
- `page_size` (integer, optional): Number of results per page (default: 10, max: 100)
- `category` (integer, optional): Filter by category ID
- `country` (integer, optional): Filter by country ID
- `source` (integer, optional): Filter by source ID
- `title` (string, optional): Search in article title
- `ordering` (string, optional): Sort results (e.g., `-published_at`, `title`)

**Response:**

```json
{
  "count": 150,
  "next": "http://localhost:8000/apis/v1/news/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Breaking News: Technology Update",
      "description": "A new tech innovation...",
      "url": "https://example.com/news/1",
      "image_url": "https://example.com/image.jpg",
      "published_at": "2024-01-29T10:30:00Z",
      "source": {
        "id": 5,
        "source_id": "bbc-news",
        "name": "BBC News"
      },
      "category_name": "Technology",
      "country_name": "United Kingdom",
      "language_name": "English",
      "created_at": "2024-01-29T11:00:00Z"
    }
  ]
}
```

**Status Code:** `200 OK`

---

### 2. Retrieve News Article Detail

**Endpoint:** `GET /news/<id>/`

**Description:** Retrieve detailed information about a specific news article.

**Path Parameters:**

- `id` (integer, required): The unique identifier of the news article

**Response:**

```json
{
  "id": 1,
  "title": "Breaking News: Technology Update",
  "description": "A new tech innovation...",
  "url": "https://example.com/news/1",
  "image_url": "https://example.com/image.jpg",
  "published_at": "2024-01-29T10:30:00Z",
  "source": {
    "id": 5,
    "source_id": "bbc-news",
    "name": "BBC News",
    "description": "BBC News is the news division of the British Broadcasting Corporation",
    "url": "https://www.bbc.com/news",
    "category": {
      "id": 1,
      "name": "Technology"
    },
    "language": {
      "id": 1,
      "code": "en",
      "name": "English"
    },
    "country": {
      "id": 1,
      "code": "gb",
      "name": "United Kingdom"
    }
  },
  "category": {
    "id": 1,
    "name": "Technology"
  },
  "language": {
    "id": 1,
    "code": "en",
    "name": "English"
  },
  "country": {
    "id": 1,
    "code": "gb",
    "name": "United Kingdom"
  },
  "created_at": "2024-01-29T11:00:00Z"
}
```

**Status Code:** `200 OK`

**Error Response (404):**

```json
{
  "detail": "Not found."
}
```

---

### 3. List News Sources

**Endpoint:** `GET /sources/`

**Description:** Retrieve a list of all news sources with optional filtering.

**Response:**

```json
[
  {
    "id": 1,
    "source_id": "bbc-news",
    "name": "BBC News",
    "description": "BBC News is the news division of the British Broadcasting Corporation",
    "url": "https://www.bbc.com/news",
    "category": {
      "id": 1,
      "name": "General"
    },
    "language": {
      "id": 1,
      "code": "en",
      "name": "English"
    },
    "country": {
      "id": 1,
      "code": "gb",
      "name": "United Kingdom"
    }
  }
]
```

**Status Code:** `200 OK`

---

### 4. List Categories

**Endpoint:** `GET /categories/`

**Description:** Retrieve all available news categories.

**Response:**

```json
[
  {
    "id": 1,
    "name": "Business"
  },
  {
    "id": 2,
    "name": "Entertainment"
  },
  {
    "id": 3,
    "name": "General"
  },
  {
    "id": 4,
    "name": "Health"
  },
  {
    "id": 5,
    "name": "Science"
  },
  {
    "id": 6,
    "name": "Sports"
  },
  {
    "id": 7,
    "name": "Technology"
  }
]
```

**Status Code:** `200 OK`

---

### 5. List Languages

**Endpoint:** `GET /languages/`

**Description:** Retrieve all supported languages.

**Response:**

```json
[
  {
    "id": 1,
    "code": "en",
    "name": "English"
  },
  {
    "id": 2,
    "code": "fr",
    "name": "French"
  },
  {
    "id": 3,
    "code": "ar",
    "name": "Arabic"
  }
]
```

**Status Code:** `200 OK`

---

### 6. List Countries

**Endpoint:** `GET /countries/`

**Description:** Retrieve all supported countries.

**Response:**

```json
[
  {
    "id": 1,
    "code": "us",
    "name": "United States"
  },
  {
    "id": 2,
    "code": "fr",
    "name": "France"
  },
  {
    "id": 3,
    "code": "eg",
    "name": "Egypt"
  },
  {
    "id": 4,
    "code": "ca",
    "name": "Canada"
  }
]
```

**Status Code:** `200 OK`

---

## Query Parameters

### Common Query Parameters

| Parameter   | Type    | Description                                        |
| ----------- | ------- | -------------------------------------------------- |
| `page`      | integer | Page number for pagination (starts at 1)           |
| `page_size` | integer | Number of results per page (default: 10, max: 100) |

### Filtering Parameters (News Articles Only)

| Parameter  | Type    | Description                    |
| ---------- | ------- | ------------------------------ |
| `category` | integer | Filter articles by category ID |
| `country`  | integer | Filter articles by country ID  |
| `source`   | integer | Filter articles by source ID   |

### Searching Parameters (News Articles Only)

| Parameter | Type   | Description                                                   |
| --------- | ------ | ------------------------------------------------------------- |
| `title`   | string | Search within article titles (case-insensitive partial match) |

### Ordering Parameters (News Articles Only)

| Parameter  | Type   | Description                                                                                                          |
| ---------- | ------ | -------------------------------------------------------------------------------------------------------------------- |
| `ordering` | string | Sort results by field. Prefix with `-` for descending order. Available fields: `published_at`, `created_at`, `title` |

---

## Filtering & Searching

### Filtering by Category

```
GET /news/?category=1
```

### Filtering by Country

```
GET /news/?country=1
```

### Filtering by Source

```
GET /news/?source=5
```

### Combining Multiple Filters

```
GET /news/?category=1&country=1&source=5
```

### Searching by Title

```
GET /news/?title=technology
```

### Sorting Results

Sort by published date (newest first):

```
GET /news/?ordering=-published_at
```

Sort by published date (oldest first):

```
GET /news/?ordering=published_at
```

Sort by title (alphabetical):

```
GET /news/?ordering=title
```

### Combining Filters, Search, and Sorting

```
GET /news/?category=1&title=technology&ordering=-published_at&page=1&page_size=20
```

---

## Pagination

The API uses limit-offset pagination for the news articles endpoint.

### Pagination Parameters

| Parameter   | Type    | Default | Max | Description               |
| ----------- | ------- | ------- | --- | ------------------------- |
| `page`      | integer | 1       | N/A | Page number (starts at 1) |
| `page_size` | integer | 10      | 100 | Results per page          |

### Pagination Response

```json
{
  "count": 150,
  "next": "http://localhost:8000/apis/v1/news/?page=2",
  "previous": null,
  "results": [...]
}
```

### Example Pagination Request

```
GET /news/?page=2&page_size=20
```

---

## Examples

### Example 1: Get Latest Technology News

```bash
curl -X GET "http://localhost:8000/apis/v1/news/?category=1&ordering=-published_at"
```

### Example 2: Get News from United States in English

```bash
curl -X GET "http://localhost:8000/apis/v1/news/?country=1&page_size=50"
```

### Example 3: Search for Articles About "AI"

```bash
curl -X GET "http://localhost:8000/apis/v1/news/?title=AI&ordering=-published_at"
```

### Example 4: Get Single Article Details

```bash
curl -X GET "http://localhost:8000/apis/v1/news/1/"
```

### Example 5: List All Categories

```bash
curl -X GET "http://localhost:8000/apis/v1/categories/"
```

### Example 6: Get All News Sources with Filters

```bash
curl -X GET "http://localhost:8000/apis/v1/sources/"
```

---

## HTTP Status Codes

| Status Code | Meaning                                       |
| ----------- | --------------------------------------------- |
| 200         | OK - Request successful                       |
| 400         | Bad Request - Invalid parameters              |
| 404         | Not Found - Resource does not exist           |
| 500         | Internal Server Error - Server error occurred |

---

## Changelog

### Version 1.0.0 (2024-01-29)

- Initial API release
- Endpoints for news articles, sources, categories, languages, and countries
- Support for filtering, searching, and sorting
- Pagination support

---

## Support

For issues or questions about the API, please contact the development team or open an issue in the project repository.
