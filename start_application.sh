#!/bin/bash

# 🎬 Movie Experiment - Quick Start Script

echo "🎬 Starting Movie Experiment Application..."
echo "=========================================="

# Check if we're in the right directory
if [ ! -d "movies_backend" ] || [ ! -d "movies-ui-v2" ]; then
    echo "❌ Error: Please run this script from the fb-movies-app directory"
    echo "Current directory: $(pwd)"
    exit 1
fi

echo "🐍 Starting Django Backend..."
cd movies_backend
source venv/bin/activate
python manage.py runserver 8000 &
DJANGO_PID=$!
echo "   Django started with PID: $DJANGO_PID"

echo "🅰️  Starting Angular Frontend..."
cd ../movies-ui-v2
npm start &
ANGULAR_PID=$!
echo "   Angular started with PID: $ANGULAR_PID"

echo ""
echo "✅ Both services are starting..."
echo "📋 Access URLs:"
echo "   🎯 Main Application: http://localhost:4200/"
echo "   🔧 Django Admin: http://localhost:8000/admin/"
echo "   📊 Admin Credentials: diag / diag@smulla"
echo ""
echo "⏳ Waiting for services to be ready..."

# Wait for services to start
sleep 10

# Test services
echo "🧪 Testing services..."
if curl -s -f http://localhost:8000/admin/ > /dev/null; then
    echo "   ✅ Django Backend: Running"
else
    echo "   ❌ Django Backend: Not responding"
fi

if curl -s -f http://localhost:4200/ > /dev/null; then
    echo "   ✅ Angular Frontend: Running"
else
    echo "   ⏳ Angular Frontend: Still compiling (this is normal)"
fi

echo ""
echo "🎉 Application is ready!"
echo "🛑 To stop: pkill -f 'npm start' && pkill -f 'runserver'"
echo "📖 See MOVIE_EXPERIMENT_PLAYBOOK.md for detailed instructions" 