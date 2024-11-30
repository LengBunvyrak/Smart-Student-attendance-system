import tkinter as tk
from tkinter import messagebox, Toplevel, ttk 
import cv2 
import numpy as np 
import face_recognition as fr 
import os
from datetime import datetime
import sqlite3 
from PIL import ImageTk, Image 

# Database setup
def create_db():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                        id TEXT PRIMARY KEY,
                        name TEXT,
                        date_time TEXT,
                        attendance_status BOOLEAN
                    )''')
    conn.commit()
    conn.close()

def show_database_section():

    db_window = Toplevel(root)
    db_window.title("Student Database")
    
    tree = ttk.Treeview(db_window, columns=("ID", "Name", "Date Time", "Attendance Status"), show="headings", height=20)


    tree.heading("ID", text="ID")
    tree.column("ID", anchor=tk.CENTER, width=100)
    tree.heading("Name", text="Name")
    tree.column("Name", anchor=tk.W, width=200)
    tree.heading("Date Time", text="Date Time")
    tree.column("Date Time", anchor=tk.CENTER, width=200)
    tree.heading("Attendance Status", text="Attendance Status")
    tree.column("Attendance Status", anchor=tk.CENTER, width=150)

    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        tree.insert("", tk.END, values=row)


    scrollbar = ttk.Scrollbar(db_window, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    close_button = tk.Button(db_window, text="Close", command=db_window.destroy)
    close_button.pack(pady=10)

# Resize image
def resize(img, size):
    width = int(img.shape[1] * size)
    height = int(img.shape[0] * size)
    dimension = (width, height)
    return cv2.resize(img, dimension, interpolation=cv2.INTER_AREA)

# Find encodings of face images
def findEncoding(images):
    encodingList = []
    for idx, image in enumerate(images):
        try:
            resized_img = cv2.resize(image, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
            rgb_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
            encodings = fr.face_encodings(rgb_img)
            if encodings:  # Only add encoding if at least one face is detected
                encodingList.append(encodings[0])
            else:
                print(f"Warning: No face detected in image {idx + 1}. Skipping.")
        except Exception as e:
            print(f"Error processing image {idx + 1}: {str(e)}")
    return encodingList


# Update attendance status in the database
def mark_attendance_in_db(name):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO attendance (id, name, date_time, attendance_status) VALUES (?, ?, ?, ?)',
                   (id, name, now, True))
    conn.commit()
    conn.close()

# Load student images and names
path = 'final project/student_faces'
student_images = []
student_names = []

if os.path.exists(path):
    my_list = os.listdir(path)
    for cl in my_list:
        current_img = cv2.imread(os.path.join(path, cl))
        student_images.append(current_img)
        student_names.append(os.path.splitext(cl)[0])

encode_list = findEncoding(student_images)

# Face Attendance Function
def start_face_attendance():
    # Load student images and names
    studentImg = []
    studentName = []
    myList = os.listdir('final project/student_faces')

    for cl in myList:
        currentImg = cv2.imread(f'final project/student_faces/{cl}')
        studentImg.append(currentImg)
        studentName.append(os.path.splitext(cl)[0])  # Remove file extensions

    def findEncoding(images):
        encodingList = []
        for image in images:
            resized_img = cv2.resize(image, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
            rgb_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
            encodings = fr.face_encodings(rgb_img)
            if encodings:  # Only add encoding if a face is detected
                encodingList.append(encodings[0])
        return encodingList

    encodeList = findEncoding(studentImg)

    # Track already marked students
    marked_students = set()

    def mark_attendance(name):
        now = datetime.now()
        date_time = now.strftime('%Y-%m-%d %H:%M:%S')

        if name not in marked_students:
            marked_students.add(name)
            conn = sqlite3.connect('attendance.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE attendance SET date_time = ?, attendance_status = ? WHERE name = ?',
                           (date_time, True, name))
            conn.commit()
            conn.close()

            # Update the present students list
            present_list.insert(tk.END, f"{name} - {date_time}")

    # Open webcam and start video stream
    video = cv2.VideoCapture(0)

    if not video.isOpened():
        messagebox.showerror("Error", "Cannot access webcam.")
        return

    # Create a window to display the video feed and attendance list
    attendance_window = tk.Toplevel(root)
    attendance_window.title("Face Attendance")

    # Layout for video feed and present students
    video_frame = tk.Frame(attendance_window)
    video_frame.pack(side=tk.LEFT, padx=10, pady=10)

    list_frame = tk.Frame(attendance_window)
    list_frame.pack(side=tk.RIGHT, padx=10, pady=10)

    # Video feed label
    video_label = tk.Label(video_frame)
    video_label.pack()

    # List of present students
    tk.Label(list_frame, text="Present Students", font=("Arial", 14)).pack()
    present_list = tk.Listbox(list_frame, width=40, height=20)
    present_list.pack(pady=10)

    def process_video():
        while True:
            ret, frame = video.read()
            if not ret:
                break

            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            # Detect faces and encode
            face_locations = fr.face_locations(rgb_small_frame, model='cnn')
            face_encodings = fr.face_encodings(rgb_small_frame, face_locations)

            for face_encoding, face_location in zip(face_encodings, face_locations):
                matches = fr.compare_faces(encodeList, face_encoding)
                face_distances = fr.face_distance(encodeList, face_encoding)

                if matches:
                    match_index = np.argmin(face_distances)
                    if matches[match_index]:
                        name = studentName[match_index]
                        mark_attendance(name)
                        # Draw rectangle around the face
                        top, right, bottom, left = face_location
                        top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 2)

            # Display the video frame in the Tkinter label
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(frame_rgb))
            video_label.config(image=img)
            video_label.image = img

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release resources and return to main GUI
        video.release()
        cv2.destroyAllWindows()
        attendance_window.destroy()

    # Start the video processing in a separate thread to avoid freezing the GUI
    import threading
    thread = threading.Thread(target=process_video)
    thread.daemon = True
    thread.start()

    # Close attendance window
    def close_attendance():
        if video.isOpened():
            video.release()
        cv2.destroyAllWindows()
        attendance_window.destroy()

    close_button = tk.Button(list_frame, text="Close", command=close_attendance)
    close_button.pack(pady=10)

def open_registration_window():
    registration_window = tk.Toplevel(root)
    registration_window.title("Student Registration")

    def save_to_db():
        name = name_entry.get()
        student_id = id_entry.get()
        status = False  # Default attendance status is False
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if not name or not student_id:
            messagebox.showerror("Error", "Please fill out both Name and ID.")
            return

        conn = sqlite3.connect('attendance.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM attendance WHERE id = ?', (student_id,))
        existing_data = cursor.fetchone()

        if existing_data:
            messagebox.showerror("Error", f"Student ID {student_id} already exists.")
        else:
            cursor.execute('INSERT INTO attendance (id, name, date_time, attendance_status) VALUES (?, ?, ?, ?)',
                           (student_id, name, now, status))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Student {name} registered successfully!")
            registration_window.destroy()

    def capture_photo():
        name = name_entry.get()
        if not name:
            messagebox.showerror("Error", "Please enter the student's name to save the photo.")
            return

        ret, frame = cap.read()
        if ret:
            directory = "final project/student_faces"
            if not os.path.exists(directory):
                os.makedirs(directory)
            filename = os.path.join(directory, f"{name}.jpg")
            cv2.imwrite(filename, frame)
            capture_prompt_label.config(text="Photo captured and saved successfully!", fg="green")
            messagebox.showinfo("Success", f"Photo saved as {filename}")

            # Enable the register button after capturing the photo
            register_button.config(state=tk.NORMAL)
        else:
            messagebox.showerror("Error", "Failed to capture photo. Please try again.")

    tk.Label(registration_window, text="Name:").grid(row=0, column=0, padx=10, pady=10)
    name_entry = tk.Entry(registration_window)
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(registration_window, text="ID:").grid(row=1, column=0, padx=10, pady=10)
    id_entry = tk.Entry(registration_window)
    id_entry.grid(row=1, column=1, padx=10, pady=10)


    capture_button = tk.Button(registration_window, text="Capture Photo", command=capture_photo)
    capture_button.grid(row=2, column=0, padx=10, pady=10)

    register_button = tk.Button(registration_window, text="Register", command=save_to_db, state=tk.DISABLED)
    register_button.grid(row=2, column=1, padx=10, pady=10)

    capture_prompt_label = tk.Label(registration_window, text="", font=("Arial", 12))
    capture_prompt_label.grid(row=3, column=0, columnspan=2, pady=10)

def main_window():
    global root, cap
    cap = cv2.VideoCapture(0)  # Open webcam
    root = tk.Tk()
    root.title("Main Application")

    # Add some text to the main window
    welcome_label = tk.Label(root, text="Welcome to the Student Attendance System", font=("Arial", 16))
    welcome_label.pack(pady=20)

    # Button to open the registration window
    registration_button = tk.Button(root, text="Open Registration", command=open_registration_window)
    registration_button.pack(pady=10)


    # Button to start face attendance
    attendance_button = tk.Button(root, text="Start Face Attendance", command=start_face_attendance)
    attendance_button.pack(pady=10)

    database_button = tk.Button(root, text="View Student Data", command=show_database_section)
    database_button.pack(pady=10)
    
    root.mainloop()

# Start the application by opening the main window
if __name__ == "__main__":
    create_db()
    main_window()
