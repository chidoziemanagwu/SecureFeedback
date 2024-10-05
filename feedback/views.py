from django.shortcuts import render
from django.http import HttpResponse
from .models import Feedback
from twilio.rest import Client
from django.conf import settings
import requests

# Helper function to upload media to Pinata
def upload_to_pinata(file):
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        'pinata_api_key': settings.PINATA_API_KEY,
        'pinata_secret_api_key': settings.PINATA_SECRET_API_KEY,
    }
    files = {'file': file}
    response = requests.post(url, files=files, headers=headers)
    return response.json().get('IpfsHash')

# Feedback submission view (without Django forms)
def submit_feedback(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        sender_email = request.POST.get('sender_email')
        sender_phone = request.POST.get('sender_phone')
        file = request.FILES.get('media_file')

        # Upload file to Pinata (optional)
        media_url = None
        if file:
            media_url = upload_to_pinata(file)

        # Store feedback in database
        Feedback.objects.create(
            message=message,
            sender_email=sender_email,
            sender_phone=sender_phone,
            media_url=media_url
        )

        # Send SMS notification via Twilio
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=f"Feedback received from {sender_phone}: {message}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=sender_phone  # Sending an SMS to the user
        )

        return HttpResponse("Feedback submitted successfully!")

    return render(request, 'feedback_form.html')
