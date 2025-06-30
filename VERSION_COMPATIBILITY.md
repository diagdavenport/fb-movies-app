# Version Compatibility Guide

## Overview
This document ensures consistent environments across development, testing, and production to avoid deployment issues.

## Backend (Django)
- **Python**: 3.9 (required)
- **Django**: 3.2.4
- **Virtual Environment**: Use `movies_backend/venv/` with Python 3.9

### Backend Setup:
```bash
cd movies_backend
source venv/bin/activate  # Activates Python 3.9 environment
pip install -r requirements.txt
```

## Frontend (Angular)
- **Node.js**: 14.21.3 (preferred) or 14.x LTS
- **npm**: ~6.x (comes with Node 14)
- **Angular CLI**: ~10.0.3
- **Angular**: ~10.0.4

### Frontend Setup:
```bash
cd movies-ui-v2
# Use Node 14.x if available, otherwise Node 16+ may work but not guaranteed
npm install  # Uses package-lock.json lockfileVersion 1
npx ng version  # Should show Angular CLI 10.0.8
```

## Important Notes:

### Apple Silicon (M1/M2) Users:
- Node 14 doesn't have official Apple Silicon binaries
- Node 16+ may work for development but test thoroughly
- Production deployment should use exact versions

### Version Mismatch Issues:
- **package-lock.json**: Keep original lockfileVersion 1
- **npm version difference**: May cause dependency conflicts
- **Angular compatibility**: Angular 10 designed for Node 12-14

### Deployment Safety:
1. Test locally with exact production versions when possible
2. Always use `package-lock.json` from repository
3. Don't upgrade major versions without testing
4. Production environment should match these exact versions

## Production Environment:
- **AWS EC2**: Must use Node 14.x and Python 3.9
- **Backend URL**: http://44.204.168.187/
- **Angular build**: `ng build --prod`

## If Version Issues Occur:
1. Revert package-lock.json: `git checkout package-lock.json`
2. Use Node Version Manager (nvm) to switch Node versions
3. Clear node_modules and reinstall: `rm -rf node_modules && npm install`
4. For Python: Use virtual environment with Python 3.9 