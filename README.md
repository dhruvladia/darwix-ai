# This Django web application demonstrates two AI-powered features:
1. **Multilingual Audio Transcription with Diarization** — Using Sarvam AI's API (ASR)
2. **AI Title Suggestions** — Using OpenRouter API (LLM integration)

## Features

### 1. Audio Transcription with Diarization
- Upload audio files (MP3, WAV, etc.)
- Get transcriptions using Sarvam AI's speech-to-text API
- **Speaker diarization**: output includes speaker labels and segments if multiple speakers are detected

### 2. Blog Title Suggestions
- Input blog post content
- Receive 3 AI-generated title suggestions
- Output is a JSON object with a `titles` array
- Please find the sample implementation in a Django view showing how the model is integrated in: ai_features_app/views.py

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/dhruvladia/darwix-ai
   cd darwix-ai
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```
   SARVAM_AI_API_KEY="YOUR_SARVAM_AI_API_KEY_HERE"
   OPENROUTER_API_KEY="YOUR_OPENROUTER_API_KEY_HERE"
   ```
   - Get your Sarvam AI API key from: https://dashboard.sarvam.ai/admin
   - Get your OpenRouter API key from: https://openrouter.ai/keys

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   Open your browser and navigate to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Project Structure

```
darwix_project/
├── darwix_project/       # Main Django project settings
├── ai_features_app/      # Django app with API endpoints
├── templates/            # HTML templates
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
└── .env                # Environment variables (create this)
```

## API Endpoints

- `POST /api/transcribe/` - Audio transcription endpoint
- `POST /api/suggest-titles/` - Blog title suggestions endpoint

## Technologies Used

- **Backend**: Django (Python web framework)
- **Frontend**: HTML, Tailwind CSS, Vanilla JavaScript
- **APIs**: Sarvam AI (Speech-to-Text), OpenRouter (LLM)
- **Deployment**: Gunicorn-ready

## Development Notes

- The application uses CSRF exemption for API endpoints to simplify testing
- Temporary files are created for audio processing and cleaned up automatically
- Error handling is implemented for API failures
- The frontend uses AJAX for seamless interaction

## Production Deployment

For production deployment:
1. Set `DEBUG = False` in settings.py
2. Configure proper `ALLOWED_HOSTS`
3. Use environment variables for `SECRET_KEY`
4. Set up proper CSRF protection
5. Use a production database (PostgreSQL recommended)
6. Serve with Gunicorn behind Nginx/Apache

Example Gunicorn command:
```bash
gunicorn darwix_project.wsgi:application --bind 0.0.0.0:8000
``` 
