# FB Movies App \- Deployment Guide & Troubleshooting

## Overview

This guide covers the complete deployment process for the FB Movies App, including common issues encountered and their solutions. The app consists of an Angular frontend hosted on S3 and a Django backend on EC2.

---

## System Architecture

- **Frontend**: Angular 10 app hosted on AWS S3  
  - URL: [http://fb-movies-ui-test.s3-website-us-east-1.amazonaws.com/](http://fb-movies-ui-test.s3-website-us-east-1.amazonaws.com/)  
- **Backend**: Django 3.2.4 API hosted on AWS EC2  
  - URL: [http://44.204.168.187/admin/](http://44.204.168.187/admin/)  
  - IP: 44.204.168.187

---

## Complete Deployment Process

### 1\. Local Development Setup

#### Prerequisites

\# Check Node.js version compatibility

node \--version  \# Should be 14.x or 16.x for Angular 10

npm \--version

\# Check Python version

python3 \--version  \# Should be 3.8+

#### Frontend Setup

cd movies-ui-v2

npm install

npx ng build \--prod  \# For production deployment

#### Backend Setup

cd movies\_backend

python3 \-m venv venv

source venv/bin/activate

pip install \-r requirements.txt

### 2\. Git Workflow for Deployment

#### Safe Branch Management

\# 1\. Work on feature branch

git checkout \-b feature/your-feature-name

\# 2\. Make changes and commit

git add .

git commit \-m "feat: description of changes"

git push origin feature/your-feature-name

\# 3\. Merge to main (locally)

git checkout main

git merge feature/your-feature-name

git push origin main

### 3\. EC2 Backend Deployment

Log into AWS account → Search and enter EC2 → ‘Press Instances’ → Pick the instance with the URL [44.204.168.187](http://44.204.168.187/admin/)

The AWS terminal should open:

#### Deployment Commands

\# Navigate to project directory

cd /home/ubuntu/MOVIES/fb-movies-app-v2

\# Activate virtual environment

source venv/bin/activate

\# Check current status

git status

git branch

\# Handle existing changes safely

git stash push \-m "EC2 local changes"

\# Pull latest changes

git fetch origin

git pull origin main

\# Restore any necessary local configurations

git stash pop  \# If needed for environment-specific configs

\# Restart Apache

sudo service apache2 restart

\# Check Apache status

sudo systemctl status apache2

### 4\. Frontend S3 Deployment

#### Build Process

cd movies-ui-v2

npx ng build \--prod

#### Upload to S3

- Upload contents of `dist/movies-ui/` to S3 bucket `fb-movies-ui-test`  
- Ensure public read permissions are set  
- Test at: [http://fb-movies-ui-test.s3-website-us-east-1.amazonaws.com/](http://fb-movies-ui-test.s3-website-us-east-1.amazonaws.com/)

---

## Testing Framework

### Backend Testing Script

Create and run the comprehensive test script on the backend when changing e.g. distribution algorithm. 

### Manual Testing Checklist

#### Backend API Testing

1. **Django Admin Access**  
     
   - Go to: [http://44.204.168.187/admin/](http://44.204.168.187/admin/)  
   - Should show login page (not error)  
   - Login should work without database errors

   

2. **API Endpoints Testing**  
     
   \# Test user creation  
     
   curl \-X POST http://44.204.168.187/getuserid/  
     
   \# Test dynamics endpoint  
     
   curl \-X GET http://44.204.168.187/getdynamics/

#### Frontend Testing

1. **Application Load**  
     
   - Go to: [http://fb-movies-ui-test.s3-website-us-east-1.amazonaws.com/](http://fb-movies-ui-test.s3-website-us-east-1.amazonaws.com/)  
   - Should load without errors

   

2. **Survey Flow Testing**  
     
   - Create new user session  
   - Verify Timer 1 shows 42 movies (not 9\)  
   - Check movie selection validation  
   - Test timer expiry behavior

---

## Common Issues & Solutions

### 1\. Database Permission Errors

#### Error Symptoms

OperationalError: attempt to write a readonly database

#### Solution

\# Fix database permissions

sudo chown ubuntu:www-data movies\_backend/db.sqlite3

sudo chmod 664 movies\_backend/db.sqlite3

\# Fix directory permissions

sudo chown ubuntu:www-data movies\_backend/

sudo chmod 775 movies\_backend/

\# Restart Apache

sudo service apache2 restart

#### Prevention

- Always check permissions after git operations  
- Add to deployment checklist

### 2\. CSV File Path Errors

#### Error Symptoms

FileNotFoundError: selected\_faces.csv

#### Root Cause

- Local development uses relative paths  
- Production requires absolute paths

#### Solution

Ensure `movies_backend/movies/views.py` has correct production path:

\# Production (EC2) \- ACTIVE

images\_path \= "/home/ubuntu/MOVIES/selected\_images/"

df \= pd.read\_csv('/home/ubuntu/MOVIES/fb-movies-app-v2/movies\_backend/selected\_faces.csv',usecols=\['face\_number','type'\])

### 3\. Git Merge Conflicts

#### Common Conflict Scenario

\<\<\<\<\<\<\< Updated upstream

\# df \= pd.read\_csv('selected\_faces.csv',usecols=\['face\_number','type'\])

\=======

df \= pd.read\_csv('/home/ubuntu/MOVIES/fb-movies-app-v2/movies\_backend/selected\_faces.csv',usecols=\['face\_number','type'\])

\>\>\>\>\>\>\> Stashed changes

#### Resolution Process

\# 1\. Identify conflicted files

git status

\# 2\. Edit the conflicted file

nano movies\_backend/movies/views.py

\# 3\. Remove conflict markers and keep production version

\# Keep: df \= pd.read\_csv('/home/ubuntu/MOVIES/fb-movies-app-v2/movies\_backend/selected\_faces.csv',usecols=\['face\_number','type'\])

\# 4\. Mark as resolved

git add movies\_backend/movies/views.py

\# 5\. Complete merge

git commit \-m "Merge: resolve path conflict for EC2 production"

### 4\. Apache Configuration Issues

#### Check Apache Status

sudo systemctl status apache2

sudo journalctl \-u apache2 \-f  \# View real-time logs

#### Common Apache Fixes

\# Restart Apache

sudo service apache2 restart

\# Reload configuration

sudo systemctl reload apache2

\# Check configuration syntax

sudo apache2ctl configtest

### 5\. Virtual Environment Issues

#### Symptoms

- Python packages not found  
- Wrong Python version

#### Solution

\# Always activate venv on EC2

source venv/bin/activate

\# Verify correct environment

which python

python \--version

\# Reinstall packages if needed

pip install \-r requirements.txt

---

## Environment-Specific Configurations

### Local Development (movies\_backend/movies/views.py)

\# Local (commented out for production deployment)

\# images\_path \= "M:/MS\_STUDY/RA/MOVIE/selected gan faces/"

\# df \= pd.read\_csv('selected\_faces.csv',usecols=\['face\_number','type'\])

### Production EC2 (movies\_backend/movies/views.py)

\# Production (EC2) \- ACTIVE

images\_path \= "/home/ubuntu/MOVIES/selected\_images/"

df \= pd.read\_csv('/home/ubuntu/MOVIES/fb-movies-app-v2/movies\_backend/selected\_faces.csv',usecols=\['face\_number','type'\])

---

## Deployment Verification

### 1\. Backend Health Check

\# On EC2 server

curl \-I http://localhost/admin/

\# Should return 200 OK

### 2\. Frontend Health Check

- Navigate to: [http://fb-movies-ui-test.s3-website-us-east-1.amazonaws.com/](http://fb-movies-ui-test.s3-website-us-east-1.amazonaws.com/)  
- Should load main application  
- Console should show no critical errors

### 3\. Integration Test

- Start a survey session on frontend  
- Verify data flows to backend  
- Check database for new entries

### 4\. Algorithm Verification

- Timer 1 and Timer 2 both show 42 movies  
- Names show \~60% female, 40% male distribution  
- No duplicate names in single session  
- Race distribution: White 64%, Hispanic 22%, Black 14%

---

## File Structure Reference

fb-movies-app/

├── movies\_backend/

│   ├── movies/

│   │   ├── views.py                 \# Main algorithm 

│   │   └── models.py               \# Database models

│   ├── db.sqlite3                  \# Database (permissions critical)

│   ├── selected\_faces.csv          \# Required data file

│   ├── test\_name\_distribution.py   \# Test suite

├── movies-ui-v2/

│   ├── src/app/survey/

│   │   └── survey.component.ts     \# Frontend logic

│   └── dist/movies-ui/             \# Production build

└── README.md

---

## Emergency Rollback

If deployment fails:

\# 1\. Check last working commit

git log \--oneline \-5

\# 2\. Reset to last working state

git reset \--hard \<last-working-commit\>

\# 3\. Force push (use carefully)

git push \--force origin main

\# 4\. On EC2, pull the rollback

git pull origin main

sudo service apache2 restart

---

## Important Links

- **Repository**: [https://github.com/diagdavenport/fb-movies-app](https://github.com/diagdavenport/fb-movies-app)  
- **Frontend URL**: [http://fb-movies-ui-test.s3-website-us-east-1.amazonaws.com/](http://fb-movies-ui-test.s3-website-us-east-1.amazonaws.com/)  
- **Backend URL**: [http://44.204.168.187/admin/](http://44.204.168.187/admin/)  
- **EC2 IP**: 44.204.168.187

---

*Last updated: July 2025*  
