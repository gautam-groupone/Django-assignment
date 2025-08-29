# Problem Statement

We aim to extend an existing Django project that catalogs rock music. The project currently includes models for **Artist**, **Album**, and **Track**, along with **Django Admin** and a **read-only REST API**.

Your task is to implement a **Playlist** feature with backend functionality and a minimal frontend (Django templates/views).  
Playlists should support **CRUD operations**, **track ordering**.

---

## This assignment is designed to test:
- Backend expertise in Django (**models, business logic, admin, REST API using DRF**)
- Frontend integration (**Django templates, form views for playlist management**)

---

## Must Haves

### 1. Playlists CRUD
Implement **Create, Read, Update, and Delete** functionality for playlists.  

Each playlist must have:
- `uuid` (unique identifier)
- `name`
- `0 or more orderable tracks`

---

### 2. Track Ordering
- Allow users to change the **order of tracks** in a playlist.

---

### 3. Business Rules
- Prevent **duplicate tracks** in a playlist.  
- Limit playlists to a maximum of **100 tracks**.  
- Validate that a **track belongs to the album’s artist**.  

---

### 4. Django Admin
- Extend admin to support browsing and managing playlists.

---

### 5. REST API (Django REST Framework)
- Implement **CRUD endpoints** for playlists and playlist tracks.  
- Ensure **ordering, validation, and rules** are enforced at the API level.  
- Use proper **HTTP status codes** and **error handling**.  

---

### 6. Templates / Form Views (UI)
- Provide Django **form views and templates** to view, create, and edit playlists.  
- Use Django forms for **validation and error handling**.  
- Keep the frontend **minimal but user-friendly**.  

---

### 7. Testing
Cover CRUD and business rule edge cases, including:
- Duplicate tracks  
- Playlist size limits  
- Reordering  
- Invalid data

## Developing

You can check your work at any time by running:

```shell
$ make ready
```

This will run the default code linters and the test suite.  You can format your code to what the linters expect with:

```shell
$ make format
```

Please ensure that there are no code format or lint errors.

## Getting started




#### Fork this repository

When you have completed the goals then you can open a Pull Request to this main repository.


Log into the Django admin with your superuser account at:

[http://localhost:8000/admin/](http://localhost:8000/admin/)

Browse the REST API at:

[http://localhost:8000/api/v1/](http://localhost:8000/api/v1/).
# Django-assignment
