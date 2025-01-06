import os

def save_upload_image(fileObj):
    # Get the filename from the uploaded file's name attribute
    filename = fileObj.name
    upload_dir = "uploads"  # Change this to your desired upload directory

    # Ensure the upload directory exists
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    # Define the path where the file will be saved
    file_path = os.path.join(upload_dir, filename)

    # Save the uploaded file
    with open(file_path, "wb") as f:
        f.write(fileObj.getbuffer())  # Write the content of the uploaded file

    return file_path  # Return the path of the saved file
