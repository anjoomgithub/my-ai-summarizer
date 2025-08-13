# summarizer/views.py

import os
import google.generativeai as genai
from django.http import JsonResponse
from django.shortcuts import render
from dotenv import load_dotenv

load_dotenv()

# --- AI Model Configuration ---
try:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    print(f"CRITICAL ERROR: Could not configure Generative AI. {e}")
    model = None


def summarize_view(request):
    # --- Handle POST requests from our JavaScript ---
    if request.method == 'POST':
        try:
            # --- Get data from the form ---
            original_text = request.POST.get('text_to_summarize', '').strip()

            # --- Get NEW control values ---
            length = request.POST.get('summary_length', 'default')  # e.g., 'short', 'default', 'detailed'
            format_style = request.POST.get('output_format', 'a paragraph')  # e.g., 'a paragraph', 'bullet points'

            # --- Input validation ---
            if not model:
                return JsonResponse({'error': 'AI model is not available.'}, status=500)
            if not original_text:
                return JsonResponse({'error': 'No text provided to summarize.'}, status=400)

            # --- DYNAMIC PROMPT ENGINEERING ---
            # Build the prompt based on user selections for a much better result.
            prompt = f"""
            Analyze the following text. Provide a summary with the following characteristics:

            1.  **Length**: The summary should be {length}.
            2.  **Format**: The output must be in the format of {format_style}.

            Here is the text to summarize:
            ---
            {original_text}
            """

            response = model.generate_content(prompt)

            return JsonResponse({'summarized_text': response.text})

        except Exception as e:
            return JsonResponse({'error': f'An internal error occurred: {str(e)}'}, status=500)

    # --- Handle GET requests (page load) ---
    return render(request, 'summarizer/index.html')