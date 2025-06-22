import os
import json
import requests
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from sarvamai import SarvamAI

# --- Feature 1: Audio Transcription with Diarization ---
@csrf_exempt
def transcribe_audio(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

    if 'audio_file' not in request.FILES:
        return JsonResponse({'error': 'No audio file provided'}, status=400)

    audio_file = request.FILES['audio_file']
    api_key = os.getenv('SARVAM_AI_API_KEY')
    
    if not api_key:
        return JsonResponse({'error': 'Sarvam AI API key not configured'}, status=500)

    try:
        # Get your Sarvam AI API subscription key here: https://dashboard.sarvam.ai/admin
        client = SarvamAI(api_subscription_key=api_key)
        
        # Save the uploaded file temporarily
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.name)[1]) as tmp_file:
            for chunk in audio_file.chunks():
                tmp_file.write(chunk)
            tmp_file_path = tmp_file.name
        
        # Use the Sarvam SDK for transcription with diarization
        # Note: Using transcribe (not translate) for diarization support
        with open(tmp_file_path, 'rb') as audio_data:
            response = client.speech_to_text.transcribe(
                file=audio_data,
                model="saarika:v2.5",  # Saarika model supports diarization
                language_code="unknown"  # Specify the language (adjust as needed)
            )
        
        # Clean up the temporary file
        os.unlink(tmp_file_path)
        
        # Build response data
        response_data = {
            'transcript': getattr(response, 'transcript', ''),
            'language_code': getattr(response, 'language_code', ''),
            'model': getattr(response, 'model', 'saarika:v2'),
        }
        
        # Add diarization data if available
        if hasattr(response, 'speaker_segments') or hasattr(response, 'diarization'):
            response_data['diarization'] = getattr(response, 'speaker_segments', getattr(response, 'diarization', None))
        
        # Add word-level timestamps if available
        if hasattr(response, 'words'):
            response_data['words'] = response.words
            
        # Add any other attributes from the response
        if hasattr(response, '__dict__'):
            for key, value in response.__dict__.items():
                if key not in response_data and not key.startswith('_'):
                    response_data[key] = value
        
        return JsonResponse(response_data, status=200)

    except Exception as e:
        # Clean up temp file if it exists
        if 'tmp_file_path' in locals() and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
        return JsonResponse({'error': f'Transcription failed: {str(e)}'}, status=500)

# --- Feature 2: Blog Post Title Suggestions ---
@csrf_exempt
def suggest_blog_titles(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        blog_content = data.get('content')
        if not blog_content:
            return JsonResponse({'error': 'Blog content is required'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        return JsonResponse({'error': 'OpenRouter API key not configured'}, status=500)
        
    # Craft a precise prompt for the LLM
    prompt_text = f"""Based on the following blog post content, generate exactly 3 creative, engaging, and SEO-friendly title suggestions.
Return the output as a valid JSON object with a single key "titles" containing an array of 3 strings.
Example output: {{"titles": ["Title 1", "Title 2", "Title 3"]}}

Blog Content:
---
{blog_content}
---"""

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "model": "mistralai/mistral-7b-instruct:free",  # A good, free model on OpenRouter
                "messages": [
                    {"role": "user", "content": prompt_text}
                ],
                "temperature": 0.7,
                "max_tokens": 200
            })
        )
        response.raise_for_status()
        
        # Return the entire raw response from OpenRouter
        response_data = response.json()
        
        return JsonResponse({
            'raw_response': response_data,
            'content': response_data.get('choices', [{}])[0].get('message', {}).get('content', ''),
            'model': response_data.get('model'),
            'usage': response_data.get('usage')
        }, status=200)

    except requests.exceptions.RequestException as e:
        error_detail = ""
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = e.response.json()
            except:
                error_detail = e.response.text
        return JsonResponse({'error': f'API request failed: {str(e)}', 'details': error_detail}, status=502)
    except Exception as e:
        return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)

# --- View to render the main page ---
def index(request):
    return render(request, 'index.html') 