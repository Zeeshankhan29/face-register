from src.flora.entity import DataIngestionConfig
import os
from pathlib import Path
import matplotlib.pyplot as plt
from PIL import Image
import cv2
import face_recognition
import base64
import uuid
from datetime import datetime
import numpy as np
import csv




class DataIngestion:
    def __init__(self,DataIngestion_config= DataIngestionConfig):
        self.dataingestion_config = DataIngestion_config
        self.curr_dir = Path(os.getcwd())


    def crop_images(self):
        image_dir = Path(self.dataingestion_config.images_dir)
        image_path = os.path.join(self.curr_dir,image_dir)
        files = os.listdir(image_path)
        for file in files:
            single_file = os.path.join(image_path,file )
            filename = os.path.basename(single_file)
            
            filename = filename.split(".")[0]

            image = face_recognition.load_image_file(single_file)
            
            face_locations = face_recognition.face_locations(image,model='cnn')
            for face_location in face_locations:

                # Print the location of each face in this image
                top, right, bottom, left = face_location
                print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

                # You can access the actual face itself like this:
                face_image = image[top:bottom, left:right]
                crop_dir = self.dataingestion_config.crop_images_dir
                crop_path = os.path.join(self.curr_dir,crop_dir)
                print('crop_path',crop_path)
                face_image_rgb = cv2.cvtColor(face_image,cv2.COLOR_BGR2RGB)
                cv2.imwrite(f'{crop_path}/{filename}.jpg', face_image_rgb)
                pil_image = Image.fromarray(face_image)
            
                pil_image.show()
    

    def webcam_capture(self,number_of_images):
        videoCaptureObject = cv2.VideoCapture(0)
        
        result = True
        while(result):
            web_dir = Path(self.dataingestion_config.webcam_img_dir)
            web_path = os.path.join(self.curr_dir,web_dir)
            ret,frame = videoCaptureObject.read()
            for i in range(1,number_of_images+1):
                
                # print(i)
                if i<=number_of_images:
                    cv2.imwrite(f"{web_path}/Image{i}.jpg",frame)
                    result = False
                    
                else:
                    result = True
                        
        videoCaptureObject.release()
        cv2.destroyAllWindows()



    def decode_webcam_images(self):
        web_dir = Path(self.dataingestion_config.webcam_img_dir)
        web_path = os.path.join(self.curr_dir,web_dir)
        decode_dir = Path(self.dataingestion_config.decode_img_dir)
        decode_path = os.path.join(self.curr_dir,decode_dir)
        files = os.listdir(web_path)
        for file in files:
            single_file = os.path.join(web_path,file)
            filename = os.path.basename(single_file)
            filename = filename.split('.')[0]

  
  
            with open(f"{web_path}/{filename}.jpg", "rb") as image2string:
                converted_string = base64.b64encode(image2string.read())
            print(converted_string)
            
            with open(f'{decode_path}/{filename}.bin', "wb") as file:
                file.write(converted_string)


    def identify_persons(self):
        image_dir = Path(self.dataingestion_config.images_dir)
        unknown_dir = Path(self.dataingestion_config.unknown_faces_dir)
        image_path = os.path.join(self.curr_dir, image_dir)
        Unknown_path = os.path.join(self.curr_dir, unknown_dir)
        files = os.listdir(image_path)
        # files = files.sort()
        self.now = datetime.now()
        self.current_date = self.now.strftime("%Y-%m-%d")
        self.f = open(self.current_date + '.csv', 'a+', newline='')
        self.Imwriter = csv.writer(self.f)

        if self.f.tell() == 0:
            self.Imwriter.writerow(['UUID','Date', 'Timestamp'])
        
        
        
        known_face_encodings = []
        known_face_names = []
        known_face_counts = {}  # Store the counts of known faces
        for file in files:
            single_file = os.path.join(image_dir, file)
            print(single_file)
            filename = os.path.basename(single_file)
            filename = filename.split('.')[0]

            file = face_recognition.load_image_file(single_file)
            encodings = face_recognition.face_encodings(file)
            if len(encodings) > 0:
                encoding = encodings[0]
                known_face_encodings.append(encoding)
                known_face_names.append(filename)
                known_face_counts[filename] = 0  # Initialize the count to 0
            else:
                print(f"No face detected in {filename}")

        print(known_face_encodings)
        print(known_face_names)

        persons = known_face_names.copy()
        tracked_persons = {}  # Store the tracked persons' information

        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        previous_unknown_face_names = []  # Track previous unknown face names

        timeout_duration = 5  # Timeout duration in seconds
        timeout_threshold = 30  # Number of consecutive frames for timeout detection
        timeout_counter = 0  # Counter to track consecutive frames without person detection

        video_capture = cv2.VideoCapture(0)

        while True:
            # Grab a single frame of video
            ret, frame = video_capture.read()

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    if name in tracked_persons:
                        tracked_persons[name]["timeout_counter"] = 0  # Reset timeout counter
                else:
                    # Generate a unique ID for the unknown person
                    unknown_person_id = str(uuid.uuid4())

                    # Save the unknown face encoding and name
                    unknown_face_encoding = face_encoding
                    unknown_face_name = f"U_{unknown_person_id}"

                    if unknown_face_name not in previous_unknown_face_names:
                        # Save the unknown face image
                        unknown_face_image = cv2.resize(frame, (160, 160))  # Resize for consistency
                        cv2.imwrite(f"{image_path}/{unknown_face_name}.jpg", unknown_face_image)
                        cv2.imwrite(f"{Unknown_path}/{unknown_face_name}.jpg", unknown_face_image)

                        # Update the known face data
                        known_face_encodings.append(unknown_face_encoding)
                        known_face_names.append(unknown_face_name)
                        known_face_counts[unknown_face_name] = 1  # Initialize the count to 1

                        previous_unknown_face_names.append(unknown_face_name)
                    else:
                        # Existing unknown face reappears
                        known_face_counts[unknown_face_name] += 1

                face_names.append(name)

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, f'{name}', (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Track persons and update timeout counter
            for personid in tracked_persons:
                if personid not in face_names:
                    tracked_persons[personid]["timeout_counter"] += 1
                    if tracked_persons[personid]["timeout_counter"] >= timeout_threshold:
                        # Person is considered out of the frame
                        tracked_persons[personid]["timeout_counter"] = 0  # Reset timeout counter
                        current_time = self.now.strftime("%H:%M:%S")
                        current_date  = self.now.strftime("%d/%m/%Y")
                        self.Imwriter.writerow([personid,current_date, current_time])

            # Log the unknown person's ID and timestamp
            for unknown_face_name, count in known_face_counts.items():
                if unknown_face_name.startswith("U_"):
                    if unknown_face_name in persons:
                        persons.remove(unknown_face_name)
                        current_time = self.now.strftime("%H:%M:%S")
                        current_date  = self.now.strftime("%d/%m/%Y")
                        self.Imwriter.writerow([unknown_face_name,current_date, current_time])

            # Add newly detected persons to the tracked_persons dictionary
            for face_name in face_names:
                if face_name not in tracked_persons and face_name not in persons:
                    tracked_persons[face_name] = {"timeout_counter": 0}

            # Display the resulting image
            cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()
        self.f.close()





            