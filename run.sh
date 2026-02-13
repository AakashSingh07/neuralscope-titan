# Create venv if missing
python3 -m venv venv

# Activate
source venv/bin/activate

# Install packages
pip install -r requirements.txt

# Run app
python main.py
