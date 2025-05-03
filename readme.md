# Personal CRM API

The **Personal CRM API** is a backend system designed to manage contacts, extract and organize data from business cards, and integrate with LinkedIn profiles. It provides functionality for user authentication, contact creation and management, business card OCR processing, and LinkedIn profile data extraction. This API is built using Django and Django REST Framework.

---

## Features

1. **User Authentication**:
   - Register users.
   - Login users with JWT-based authentication (using `SimpleJWT`).
   - Secure endpoints with token-based authentication.

2. **Contact Management**:
   - Add, update, delete, and retrieve contacts.
   - Associate notes, LinkedIn profiles, and interactions with contacts.

3. **Business Card OCR**:
   - Upload and process business card images.
   - Extract contact information from images using OCR (powered by Tesseract).
   - Convert extracted data into structured contact records.

4. **LinkedIn Integration**:
   - Fetch LinkedIn profile data for contacts.
   - Retrieve mutual connections, posts, and professional details.

---

## API Endpoints

### Authentication Endpoints

| HTTP Method | Endpoint                   | Description                       |
|-------------|----------------------------|-----------------------------------|
| `POST`      | `/api/auth/register/`      | Register a new user.             |
| `POST`      | `/api/auth/login/`         | Login and obtain access tokens.  |
| `POST`      | `/api/auth/token/refresh/` | Refresh an expired access token. |

### Contact Management Endpoints

| HTTP Method | Endpoint              | Description                           |
|-------------|-----------------------|---------------------------------------|
| `POST`      | `/api/contacts/`      | Create a new contact.                |
| `GET`       | `/api/contacts/`      | Retrieve all contacts.               |
| `GET`       | `/api/contacts/{id}/` | Retrieve a specific contact by ID.   |
| `PUT`       | `/api/contacts/{id}/` | Update a specific contact by ID.     |
| `DELETE`    | `/api/contacts/{id}/` | Delete a specific contact by ID.     |

### Business Card OCR Endpoints

| HTTP Method | Endpoint                      | Description                           |
|-------------|-------------------------------|---------------------------------------|
| `POST`      | `/api/ocr-images/`            | Upload a business card image.        |
| `POST`      | `/api/ocr-images/{id}/process/` | Process an uploaded image with OCR.  |
| `POST`      | `/api/ocr-images/{id}/extract_contacts/` | Extract contact data from OCR result. |

### LinkedIn Integration Endpoints

| HTTP Method | Endpoint                              | Description                           |
|-------------|---------------------------------------|---------------------------------------|
| `POST`      | `/api/linkedin-profiles/fetch_linkedin_data/` | Fetch LinkedIn data for a contact. |

---

## Project Structure

The project follows the standard Django structure with additional directories for REST API functionality.

```
project_root/
├── accounts/                # App for user authentication and registration
│   ├── views.py             # Views for registration and login
│   ├── urls.py              # URLs for authentication endpoints
│   └── serializers.py       # Serializers for user data
├── contacts/                # App for managing contacts
│   ├── views.py             # Views for contact CRUD operations
│   ├── models.py            # Contact models
│   ├── urls.py              # URLs for contact endpoints
│   └── serializers.py       # Serializers for contact data
├── ocr/                     # App for OCR-related functionality
│   ├── views.py             # Views for OCR image upload and processing
│   ├── models.py            # Models for OCR image data
│   ├── urls.py              # URLs for OCR endpoints
│   ├── services.py          # OCR processing logic (Tesseract wrapper)
│   └── serializers.py       # Serializers for OCR data
├── linkedin/                # App for LinkedIn profile data integration
│   ├── views.py             # Views for LinkedIn data fetching
│   ├── urls.py              # URLs for LinkedIn endpoints
│   └── serializers.py       # Serializers for LinkedIn profile data
├── project_root/
│   ├── settings.py          # Django project settings
│   ├── urls.py              # Root URL configuration
│   └── wsgi.py              # WSGI entry point
└── requirements.txt         # Project dependencies
```

---

## How It Works

### 1. User Authentication
- Users register with a username, email, and password.
- Login provides a JWT token for authentication.
- Tokens are required to access all protected endpoints.

### 2. Contact Management
- Users can add, edit, and delete contacts.
- Contacts are stored with fields such as name, email, phone number, company, job title, and LinkedIn profile.
- Contacts can have notes, interactions, and other associated metadata.

### 3. Business Card OCR
- Users upload images of business cards.
- The system processes the image using Tesseract OCR to extract text.
- Extracted text is parsed into contact fields (e.g., name, email, phone number).
- Users can verify and save extracted data as new contacts.

### 4. LinkedIn Integration
- Users provide a LinkedIn username or URL for a contact.
- The system fetches profile details, work history, and mutual connections.
- Data is saved and can be associated with existing contacts.

---

## Setup Instructions

### Prerequisites
- Python 3.8+
- Django 4.x
- PostgreSQL or SQLite
- Tesseract OCR installed on the system.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sarthaksnh5/MIT-Hackathon-Submission---Innovengers
   cd personal-crm-api
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables for database and secret keys in `.env`:
   ```bash
   SECRET_KEY=your_secret_key
   DEBUG=True
   DATABASE_URL=sqlite:///db.sqlite3
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

---

## Usage

### Register a User
```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "password": "securepassword",
  "password_confirm": "securepassword"
}
```

### Add a Contact
```http
POST /api/contacts/
Authorization: Bearer <your_access_token>
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone_number": "+1234567890",
  "company": "Acme Inc.",
  "job_title": "Product Manager"
}
```

### Upload a Business Card
```http
POST /api/ocr-images/
Authorization: Bearer <your_access_token>
Content-Type: multipart/form-data

{
  "image": [BINARY_DATA],
  "image_type": "BUSINESS_CARD",
  "location": "New York"
}
```

### Fetch LinkedIn Profile Data
```http
POST /api/linkedin-profiles/fetch_linkedin_data/
Authorization: Bearer <your_access_token>
Content-Type: application/json

{
  "contact_id": 1,
  "username": "johndoe"
}
```

---

## Dependencies

- **Django**: High-level Python web framework.
- **Django REST Framework**: Toolkit for building APIs.
- **SimpleJWT**: For JWT-based authentication.
- **Tesseract OCR**: For text extraction from images.
- **Pillow**: For image handling.

---

## Future Enhancements

- Add support for importing contacts from CSV files.
- Enhance OCR accuracy with pre-processing algorithms.
- Add APIs for calendar and meeting integrations.
- Build a React Native frontend for mobile access.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.
