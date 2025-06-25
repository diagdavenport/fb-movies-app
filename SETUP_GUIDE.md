# FB Movies App - Setup Guide for Collaborators

## 🔧 Prerequisites & Compatibility

### System Requirements
- **Python**: 3.8 - 3.12 ✅
- **Node.js**: 16.x - 18.x ✅ (avoid 19+ for compatibility)
- **Git**: Any recent version
- **VS Code**: Recommended

### ⚠️ Known Compatibility Issues
- **Original requirements.txt**: Outdated (3+ years old)
- **Node.js 19+**: Requires OpenSSL legacy provider
- **Angular 10**: Very old, but functional

---

## 🚀 Quick Setup (Recommended)

### 1. Clone Repository
```bash
git clone [your-repo-url]
cd fb-movies-app
code .  # Open in VS Code
```

### 2. Backend Setup (Django)
```bash
cd movies_backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install modern requirements
pip install -r requirements.txt

# Setup database
python manage.py migrate

# Start backend
python manage.py runserver 8000
```

### 3. Frontend Setup (Angular) - New Terminal
```bash
cd movies-ui-v2

# Install dependencies
npm install

# Note: If you have issues with package-lock.json due to older npm version:
# 1. Update npm: npm install -g npm@latest (recommended)
# 2. OR delete package-lock.json and run npm install

# For Node.js 17+ (if you get OpenSSL errors)
export NODE_OPTIONS="--openssl-legacy-provider"

# Start frontend
npm start
```

---

## 🔗 Access Points

- **Main App**: http://localhost:4200
- **API Server**: http://localhost:8000
- **Django Admin**: http://localhost:8000/admin/

---

## 🛠️ Troubleshooting

### Backend Issues
```bash
# If Django URL import errors:
# Already fixed in latest version

# If missing packages:
pip install django-import-export pandas numpy tablib

# If Python version issues:
# Use Python 3.8-3.12
```

### Frontend Issues
```bash
# OpenSSL error with Node 17+:
export NODE_OPTIONS="--openssl-legacy-provider"

# Peer dependency warnings:
npm install --legacy-peer-deps

# If ng serve fails:
npx ng serve --disable-host-check
```

---

## 📝 Configuration Notes

### Backend URL Configuration
The frontend is configured to use **production backend** by default.

**To use local backend**, edit `movies-ui-v2/src/app/global-constants.ts`:
```typescript
export class GlobalConstants {
    // For local development:
    public static backend_url: string = "http://localhost:8000/";
    
    // For production (current):
    // public static backend_url: string = "http://44.204.168.187/";
}
```

### Recent Improvements
✅ Production URL configuration
✅ Improved survey validation (exactly 5 movies)
✅ Enhanced demographic distribution algorithm
✅ Fixed Django URL compatibility
✅ Better user experience

---

## 🆘 If You Get Stuck

1. **Check Python/Node versions**
2. **Use requirements-updated.txt** instead of requirements.txt
3. **Add OpenSSL flag** for Node 17+
4. **Clear npm cache**: `npm cache clean --force`
5. **Recreate virtual environment** if needed

The app works great once set up correctly! 🎬 