#!/bin/bash

# Create project directory
mkdir plant-identifier-app
cd plant-identifier-app

# Create virtual environment and activate it
python3 -m venv venv
source venv/bin/activate

# Install required dependencies
pip install streamlit google-auth google-auth-oauthlib requests pandas

# Tailwind CSS and Flowbite setup
mkdir -p static/css
mkdir -p static/js
curl -o static/css/tailwind.min.css https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css
curl -o static/js/flowbite.min.js https://unpkg.com/flowbite@1.3.4/dist/flowbite.min.js

# Create .env file to store API keys securely
touch .env

echo "STREAMLIT_APP_TITLE='Plant Identifier App'" > .env
echo "GOOGLE_GEMINI_API_KEY='your-google-gemini-api-key'" >> .env

# Create README.md for GitHub documentation
touch README.md
echo "# Plant Identifier App" >> README.md
echo "This is a plant identification app using Google Gemini API, built with Streamlit, Tailwind, and Flowbite." >> README.md

# Print message
echo "Project setup complete! Remember to fill in your Google Gemini API key in the .env file."
