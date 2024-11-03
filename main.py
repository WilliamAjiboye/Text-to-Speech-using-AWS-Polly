import boto3
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir
from pypdf import PdfReader

# file_name="Titans_curse.pdf"
# page_number= PdfReader(file_name).get_num_pages()
# reader = PdfReader(file_name)
#
# file=open('book.txt',mode='w')
# file.close()
#
#
# for i in range(page_number):
#     page = reader.pages[i]
#     text = page.extract_text()
#     with open('book.txt',mode='a') as file:
#         file.write(text)
#
#



text=None
with open('book.txt',mode='r') as file:
    text=file.read()


print(text)


client = boto3.client('polly', region_name='us-east-1')  # Replace with your preferred AWS region

# try:
response = client.synthesize_speech(
    Engine='standard',
    LanguageCode='en-US',
    OutputFormat='mp3',
    Text=text,
    TextType='text',
    VoiceId='Hans',
    SampleRate='16000'
)

# except Exception as e:
#     print(e)


if 'Audiostream' in response:
    with closing(response['Audiostream']) as stream:
        output = os.path.join(gettempdir(),'speech.mp3')
        try:
            with open(output,'wb') as file:
                file.write(stream.read())
        except IOError as error:
            print(error)

else:
    print("couldn't stream audio")
