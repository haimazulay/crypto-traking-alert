import smtplib
from email.message import EmailMessage
import os

# Class configured to send email notifications utilizing SMTP connection
class EmailNotifier:
    # Initialization method taking credentials and configuration
    def __init__(self, sender_email, sender_password, receiver_email):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.receiver_email = receiver_email

    # Method handling the process of attaching files and generating email messages
    def send_email(self, max_price, graph_path):
        msg = EmailMessage()
        msg['Subject'] = 'Bitcoin Price Index (BPI) Report'
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email
        
        msg.set_content(
            f"The BPI monitor has finished running.\n"
            f"The maximum Bitcoin price recorded was: ${max_price}"
        )

        # Attach the graph image if it exists
        # If statement to check if the file graph exists before trying to read and attach
        if os.path.exists(graph_path):
            with open(graph_path, 'rb') as f:
                image_data = f.read()
                image_name = os.path.basename(f.name)
            
            msg.add_attachment(
                image_data, 
                maintype='image', 
                subtype='png', 
                filename=image_name
            )

        # Send the email via Gmail SMTP
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(self.sender_email, self.sender_password)
                smtp.send_message(msg)
        except Exception as e:
            print(f"Failed to send email: {e}")