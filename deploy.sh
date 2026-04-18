#!/bash/bin

# JobMax Production Deployment Script
echo "🚀 Preparing JobMax for Deployment..."
echo "===================================="

# 1. Install Python Dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# 2. Build C++ Engine
echo "🔨 Building C++ Optimization Engine..."
if [ -f "build.sh" ]; then
    bash build.sh
else
    mkdir -p build && cd build
    cmake ..
    make
    cd ..
fi

# 3. Environment Check
echo "🔍 Checking environment configuration..."
if [ ! -f "serviceAccountKey.json" ]; then
    echo "⚠️  WARNING: serviceAccountKey.json not found!"
    echo "Firebase cloud storage will not work in production without this file."
fi

# 4. Final Instructions
echo "✅ Build Complete!"
echo ""
echo "To start the production server locally, run:"
echo "export SECRET_KEY=\$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
echo "export PORT=9001"
echo "gunicorn --bind 0.0.0.0:\$PORT app:app"
echo ""
echo "For cloud platforms (like Render, Railway, or Heroku):"
echo "1. Set the Build Command: bash deploy.sh"
echo "2. Set the Start Command: gunicorn --bind 0.0.0.0:\$PORT app:app"
echo "3. Add your Environment Variables (SECRET_KEY, PORT) in the platform dashboard."
