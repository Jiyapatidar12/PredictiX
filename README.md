# PredictiX — Medical Disease Prediction Platform

PredictiX ek full-stack web application hai jo machine learning models ka use karke 4 major diseases predict karta hai. Users apna medical data ya images upload karte hain aur prediction ke saath PDF report generate kar sakte hain.

---

## Project Overview

| Feature | Details |
|---|---|
| Disease Predictions | Breast Cancer, Lung Cancer, Heart Disease, Diabetes |
| Prediction Types | Image-based (CNN) + Parameter-based (ML) |
| Authentication | JWT-based with access & refresh tokens |
| Report Generation | PDF reports with pre-built templates |
| Deployment | Vercel (Frontend + Backend) + MongoDB Atlas |

---

## Tech Stack

### Frontend
- **React 18** + **Vite** — UI framework
- **React Router DOM v6** — Client-side routing
- **Axios** — API calls
- **Styled Components** — CSS-in-JS styling
- **PDF-lib** — Client-side PDF generation
- **React Toastify** — Notifications
- **React Leaflet** — Map integration
- **React Spinners / React Loader Spinner** — Loading states

### Backend
- **Node.js** + **Express.js** — REST API server
- **Mongoose** — MongoDB ODM
- **JWT (jsonwebtoken)** — Authentication tokens
- **Bcrypt** — Password hashing
- **Multer** — File upload handling
- **Child Process** — Python ML script integration
- **Cookie Parser** — HTTP-only cookie management
- **CORS** — Cross-origin request handling

### Machine Learning
- **Python** — ML scripts
- **TensorFlow/Keras** — Deep learning models (.h5)
- **Scikit-learn** — Classical ML models (.pkl)

### Database
- **MongoDB** (MongoDB Atlas) — Cloud database
- **Mongoose ODM** — Schema & query management

### DevOps / Deployment
- **Vercel** — Frontend + Backend hosting
- **Cloudinary** — Cloud image/file storage
- **Nodemon + Concurrently** — Development tooling

---

## ML Models

| Disease | Input Type | Model Format | Output |
|---|---|---|---|
| Heart Disease | 13 medical parameters | `.pkl` (scikit-learn) | 0 = Healthy, 1 = Disease |
| Diabetes | 8 medical parameters | `.pkl` + scaler | 0 = No Diabetes, 1 = Diabetes |
| Lung Cancer | CT scan image | `.h5` (Keras CNN) | Cancerous / Non-Cancerous |
| Breast Cancer | Histology image | `.h5` (Keras CNN) | Cancerous / Non-Cancerous |

ML scripts Python mein likhe hain aur Node.js `child_process.spawn()` ke through call hote hain.

---

## Database Schema

**Collection: `users`**

```js
{
  username: String,   // unique, indexed
  email: String,      // unique
  fullname: String,
  password: String,   // bcrypt hashed
  refreshToken: String,
  createdAt: Date,
  updatedAt: Date
}
```

---

## Project Structure

```
PredictiX/
├── Frontend/                        # React + Vite app
│   ├── src/
│   │   ├── pages/                   # All page components
│   │   │   ├── HomePage.jsx
│   │   │   ├── LoginPage.jsx
│   │   │   ├── SignupPage.jsx
│   │   │   ├── PredictorsPage.jsx
│   │   │   ├── HeartPage.jsx
│   │   │   ├── DiabetesPage.jsx
│   │   │   ├── BreastPage.jsx
│   │   │   └── LungPage.jsx
│   │   ├── components/              # Reusable components
│   │   │   ├── Navbar.jsx
│   │   │   ├── Hero.jsx
│   │   │   └── Card.jsx
│   │   ├── context/
│   │   │   └── UserContext.jsx      # Global auth state
│   │   └── App.jsx                  # Route definitions
│   └── public/
│       └── ReportTemplate/          # PDF templates per disease
│
├── Backend/                         # Express.js API
│   ├── routes/
│   │   ├── user.routes.js           # Auth routes
│   │   ├── prediction.routes.js     # Prediction routes
│   │   └── pdf.routes.js            # PDF routes
│   ├── controllers/
│   │   ├── user.controller.js       # Auth logic
│   │   ├── pred.controller.js       # ML prediction logic
│   │   └── pdf.controller.js        # PDF scraping
│   ├── models/
│   │   └── user.model.js            # MongoDB schema
│   ├── middlewares/
│   │   ├── auth.middleware.js       # JWT verification
│   │   └── multer.middlewares.js    # File upload config
│   ├── ML/                          # Python ML scripts + models
│   │   ├── Heart Disease Prediction/
│   │   ├── Diabetes Prediction/
│   │   ├── Lung Cancer Prediction/
│   │   └── Breast Cancer Prediction/
│   ├── utils/
│   │   ├── ApiError.js
│   │   ├── ApiResponse.js
│   │   ├── asyncHandler.js
│   │   └── cloudinary.js
│   └── db/
│       └── index.js                 # MongoDB connection
│
└── Medical Reports/                 # Dataset images
    ├── Breast Cancer/dataset/
    └── Lung Cancer/dataset/
```

---

## API Endpoints

### User Routes — `/api/v1/users`
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/register` | No | User registration |
| POST | `/login` | No | User login |
| POST | `/logout` | Yes | User logout |
| POST | `/refresh-token` | No | Refresh access token |
| POST | `/change-password` | Yes | Change password |
| GET | `/current-user` | Yes | Get logged-in user |
| PATCH | `/update-account` | Yes | Update profile |

### Prediction Routes — `/api/v1/predict`
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/heart-pred` | Yes | Heart disease prediction |
| POST | `/diabetes-pred` | Yes | Diabetes prediction |
| POST | `/lung-pred` | Yes | Lung cancer (image upload) |
| POST | `/breast-pred` | Yes | Breast cancer (image upload) |

---

## Data Flow

```
User Login → JWT Token (HTTP-only cookie)
     ↓
Select Disease Predictor
     ↓
Input Parameters / Upload Image
     ↓
Express API → Multer (for images) → Python Script (child_process)
     ↓
ML Model runs → Returns prediction
     ↓
Frontend shows result → Generate PDF Report
```

---

## Environment Variables

Backend ke liye `.env` file mein ye variables chahiye:

```env
PORT=8000
MONGODB_URI=mongodb+srv://<user>:<password>@cluster.mongodb.net/predictix
CORS_ORIGIN=http://localhost:5173
ACCESS_TOKEN_SECRET=<secret>
ACCESS_TOKEN_EXPIRY=1d
REFRESH_TOKEN_SECRET=<secret>
REFRESH_TOKEN_EXPIRY=10d
CLOUDINARY_CLOUD_NAME=<name>
CLOUDINARY_API_KEY=<key>
CLOUDINARY_API_SECRET=<secret>
```

---

## Getting Started

### Prerequisites
- Node.js v18+
- Python 3.8+
- MongoDB Atlas account

### Installation

```bash
# Clone the repo
git clone <repo-url>
cd PredictiX

# Install backend dependencies
cd Backend
npm install

# Install frontend dependencies
cd ../Frontend
npm install

# Install Python dependencies
pip install tensorflow scikit-learn numpy pillow
```

### Run Development Server

```bash
# From Backend folder — starts both frontend and backend
cd Backend
npm run dev
```

Frontend: `http://localhost:5173`  
Backend API: `http://localhost:8000`

---

## Security

- Passwords hashed with **bcrypt** (salt rounds: 10)
- **JWT** access + refresh token strategy
- Tokens stored in **HTTP-only cookies** (XSS protection)
- **CORS** restricted to allowed origins
- Protected routes via `verifyJWT` middleware

---

## Author

**Rhitam Chaudhury**
