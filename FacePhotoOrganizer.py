import os
import shutil
import pickle
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
import io
import cv2
import face_recognition
from sklearn.cluster import DBSCAN
import numpy as np
from pathlib import Path

#define Google Drive API constantst
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
CREDENTIALS_FILE = 'credentials.json'
DOWNLOAD_DIR = 'downloaded_photos'

def authenticate_google_drive():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('drive', 'v3', credentials=creds)
    return service

def download_photos_from_drive(service, download_folder):
    results = service.files().list(q="mimeType='image/jpeg'", pageSize=100).execute()
    items = results.get('files', [])

    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    for item in items:
        request = service.files().get_media(fileId=item['id'])
        fh = io.FileIO(os.path.join(download_folder, item['name']), 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        print(f'Downloaded {item["name"]}')
    return [os.path.join(download_folder, file) for file in os.listdir(download_folder)]

def extract_face_encodings(image_path):
    image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_image)
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
    return face_encodings

def cluster_faces(encodings, eps=0.5, min_samples=2):
    clustering_model = DBSCAN(eps=eps, min_samples=min_samples, metric='euclidean')
    clustering_model.fit(encodings)
    return clustering_model.labels_

def organize_photos_by_faces(photo_paths):
    face_encodings = []
    photo_faces = []

    for photo_path in photo_paths:
        encodings = extract_face_encodings(photo_path)
        if encodings:
            face_encodings.extend(encodings)
            photo_faces.append((photo_path, len(encodings)))

    if face_encodings:
        clusters = cluster_faces(face_encodings)
        face_count = 0

        for i, (photo_path, num_faces) in enumerate(photo_faces):
            for j in range(num_faces):
                cluster_id = clusters[face_count]
                folder_name = f"Person_{cluster_id}" if cluster_id != -1 else "Unknown"
                target_dir = os.path.join('sorted_photos', folder_name)
                os.makedirs(target_dir, exist_ok=True)
                shutil.copy(photo_path, target_dir)
                face_count += 1

def main():
    #Authenticate and connect to Google Drive
    service = authenticate_google_drive()
    
    #Download all photos from Google Drive
    print("Downloading photos from Google Drive...")
    photo_paths = download_photos_from_drive(service, DOWNLOAD_DIR)
    
    #Organize photos by faces
    print("Organizing photos by detected faces...")
    organize_photos_by_faces(photo_paths)
    
    print("Photos have been organized successfully!")

if __name__ == '__main__':
    main()
