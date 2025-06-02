#!/bin/bash

# 🎬 Movie Experiment - Stop Script

echo "🛑 Stopping Movie Experiment Application..."
echo "========================================="

# Stop Angular frontend
echo "🅰️  Stopping Angular Frontend..."
if pkill -f "npm start"; then
    echo "   ✅ Angular stopped"
else
    echo "   ℹ️  Angular was not running"
fi

# Stop Django backend
echo "🐍 Stopping Django Backend..."
if pkill -f "runserver"; then
    echo "   ✅ Django stopped"
else
    echo "   ℹ️  Django was not running"
fi

# Verify services are stopped
echo ""
echo "🧪 Verifying services are stopped..."
if lsof -i :8000 >/dev/null 2>&1; then
    echo "   ⚠️  Something still running on port 8000"
else
    echo "   ✅ Port 8000 is free"
fi

if lsof -i :4200 >/dev/null 2>&1; then
    echo "   ⚠️  Something still running on port 4200"
else
    echo "   ✅ Port 4200 is free"
fi

echo ""
echo "🎉 Application stopped successfully!"
echo "🚀 To start again: ./start_application.sh" 