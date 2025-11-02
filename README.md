# FacePhotoOrganizer
An AI-powered tool to organize Google Drive photos by unique faces. It detects faces, clusters them by individuals, and saves sorted images into local folders. Built with Python, OpenCV, and the Google Drive API, it ensures efficient, scalable face-based photo organization.
Features
Face Detection and Clustering: Identifies unique faces in each photo and clusters images by individual.
Google Drive Integration: Accesses and downloads photos securely from Google Drive.
Automated Local Organization: Saves grouped photos into folders based on unique faces.
Scalable and Efficient: Optimized for handling thousands of images.
Cross-Platform Compatibility: Works on Windows and macOS.
Prerequisites
Python 3.x
pip for Python package management
CMake (for compiling face_recognition)
Google Cloud Project with the Google Drive API enabled
Client credentials from Google for OAuth 2.0 access
Installation
Step 1: Install Dependencies
Clone the repository:
git clone https://github.com/yourusername/FacePhotoOrganizer.git
cd FacePhotoOrganizer
Install required libraries:
pip install -r requirements.txt
Key dependencies:

face_recognition!!
opencv-python
google-auth, google-auth-oauthlib, google-auth-httplib2
google-api-python-client
scikit-learn
Install CMake:

Download and install CMake if it’s not already installed.
Step 2: Set Up Google Drive API
Create a Google Cloud Project:

Go to Google Cloud Console.
Create a new project and enable the Google Drive API for it.
Set up OAuth 2.0 Client ID:

Under APIs & Services > Credentials, create an OAuth 2.0 Client ID.
Download the credentials as a credentials.json file and save it in your project folder.
Set up the OAuth Consent Screen:

Add test users (like your own email) to allow access during development.
Step 3: Authenticate with Google Drive
When you run the program, you’ll be prompted to authenticate your Google account.
This will open a browser window. Grant access to your Google Drive.
The program will save a token for future access, so you won’t need to re-authenticate every time.
Usage
Run the Program:

bash
Copy code
python face_photo_organizer.py
How It Works:

The program will connect to your Google Drive, download all images, detect faces, and group photos based on unique faces.
It then saves all images into a local folder named after each detected individual (e.g., Person1, Person2).
Output:

The photos are saved in organized folders on your computer, grouped by the individuals detected.
Example Workflow
Authenticate with Google Drive.
Download all photos.
Detect faces and extract face embeddings.
Group images by unique faces.
Save grouped photos to folders on the local machine.
Troubleshooting
Error: CMake Not Found: Make sure CMake is installed and added to your system PATH.
Access Blocked Error: Add yourself as a "Test User" in the Google Cloud Console.
Face Recognition Not Detected: Ensure face_recognition and dlib libraries are installed correctly.
AttributeError: face_recognition has no attribute 'face_locations': Update face_recognition or check for any conflicting file names in the project.
License
This project is licensed under the MIT License.
