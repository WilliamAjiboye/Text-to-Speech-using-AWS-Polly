import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
from tempfile import gettempdir
from pypdf import PdfReader

# Load PDF and extract text to a file
file_name = "Titans_curse.pdf"
reader = PdfReader(file_name)
page_number = len(reader.pages)

# Write PDF content to a text file
with open('book.txt', mode='w') as file:
    for i in range(page_number):
        page = reader.pages[i]
        text = page.extract_text()
        file.write(text)

# Read extracted text
with open('book.txt', mode='r') as file:
    text = file.read()[:2500]

# AWS Polly client
client = boto3.client('polly', region_name='us-east-1')  # Set preferred AWS region

try:
    # Request speech synthesis
    response = client.synthesize_speech(
        Engine='standard',
        LanguageCode='en-US',
        OutputFormat='mp3',
        Text=text,
        TextType='text',
        VoiceId='Matthew',
        SampleRate='16000'
    )

    # Check if AudioStream is in the response
    if 'AudioStream' in response:
        with closing(response['AudioStream']) as stream:
            output = os.path.join(os.getcwd(), 'speech.mp3')
            try:
                with open(output, 'wb') as file:
                    file.write(stream.read())
                print(f"Audio file saved at {output}")
            except IOError as error:
                print(f"Error writing audio file: {error}")
    else:
        print("Couldn't stream audio")

except ClientError as e:
    print(f"ClientError: {e}")
except BotoCoreError as e:
    print(f"BotoCoreError: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
