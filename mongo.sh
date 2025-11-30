echo ">>> Installing Xcode command-line tools (required)..."
xcode-select --install 2>/dev/null

echo ">>> Tapping MongoDB Homebrew repo..."
brew tap mongodb/brew

echo ">>> Updating Homebrew..."
brew update

echo ">>> Installing MongoDB Community Edition 8.0..."
brew install mongodb-community@8.0

echo ">>> Starting MongoDB as a macOS service..."
brew services start mongodb-community@8.0

echo ">>> Creating default data & log directories (if missing)..."
mkdir -p /usr/local/var/mongodb
mkdir -p /usr/local/var/log/mongodb

echo ">>> Checking service status..."
brew services list | grep mongodb

echo ">>> MongoDB installation complete!"
echo ">>> Run 'mongosh' to connect to your MongoDB server."