# Django Image Hosting App

A web-based image hosting application built with Django. It allows users to register, upload and manage images, with support for storage limits and admin moderation.

## 🚀 Features

* 🔐 User registration and authentication
* 📄 Image upload with title
* 📁 Personal image gallery with pagination
* 🗑️ Image deletion and title editing
* 📀 Storage quota limits (5 GB for regular users, 15 GB for premium)
* ⚙️ Admin/staff can view all user galleries
* 🛆 Automatic image cleanup via Django signals

## 🧱 Tech Stack

* Python 3.12.10
* Django 5.1
* SQLite
* Pillow (image processing)
* Pipenv (dependency management)

## 📂 Project Structure

```
imghost/
├── account/             # Custom user model and authentication
│   ├── forms.py
│   ├── models.py
│   ├── views.py
│   └── ...
├── imghostapp/          # Main image upload and gallery logic
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── utils/
│   │   └── storage.py
│   └── signals.py
├── templates/
│   ├── imghostapp/
│   ├── gallery/
│   └── account/
├── tests/
│   ├── account/
│   │   └── test_forms.py
│   ├── imghostapp/
│   │   └── test_views.py
│   └── ...
├── static/
├── manage.py
├── Pipfile
├── Pipfile.lock
└── README.md
```

## ⚙️ Setup Instructions (Pipenv)

### 1. Clone the repository

```bash
git clone https://github.com/tha-broski/imghost.git
cd imghost
```

### 2. Install Pipenv (if not installed)

```bash
pip install pipenv
```

### 3. Install dependencies and activate shell

```bash
pipenv install
pipenv shell
```

### 4. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Run development server

```bash
python manage.py runserver
```

Then visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)


## 🧪 Running Tests

Run all tests with:

```bash
python manage.py test
```

Organized by app:

* `tests/account/` – registration & authentication
* `tests/imghostapp/` – views, models, utils, and signal tests

## 🖼️ File Storage

Uploaded images are stored under:

```
MEDIA_ROOT/user_<username>/<filename>
```

File size is calculated to enforce storage quotas per user.

## 🧠 Signals

* Image files are automatically deleted from disk when the corresponding database record is removed.

## 📄 License

MIT License – feel free to use, modify, and share.

---

**Author:** Marcin Dabrowski
**Contact:** \[[dabrowskimarcin2001@gmail.com](mailto:your@email.com)]
