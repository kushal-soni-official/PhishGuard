import os
import random
import pandas as pd
from email.message import EmailMessage

DATASET_PATH = os.path.join(os.path.dirname(__file__), 'phishing_data.csv')

def generate_synthetic_email(is_phishing: bool) -> str:
    msg = EmailMessage()
    
    if is_phishing:
        # Phishing traits
        senders = ["support@paypal.update.com", "admin@banc-of-america.net", "security@amazon-alerts.org", "no-reply@IRS-gov.net"]
        subjects = ["URGENT: Account Suspended", "Action Required: Verify Your Identity", "Invoice #99281 Attached", "Final Notice: Password Expiry"]
        bodies = [
            "Dear Customer, your account has been temporarily suspended due to suspicious activity. Please verify your identity immediately by clicking here: http://192.168.1.100/login or your account will be permanently deleted.\n\nThanks,\nSupport Team",
            "This is your final notice. Your Microsoft Office 365 password expires today. Update it now: http://bit.ly/update-pwd-xyz\n\nAttachments: invoice_urgent.exe",
            "You have received a secure document. Please download the attached file to view it. Kind regards, HR Dept.",
            "Confirm your recent transaction of $999.00. If you did not authorize this, please visit http://paypal-secure-auth.com/cancel"
        ]
        
        msg['From'] = random.choice(senders)
        msg['Subject'] = random.choice(subjects)
        msg['Date'] = "Mon, 01 Jan 2024 10:00:00 +0000"
        
        # Missing or failed auth in phishing
        if random.random() < 0.8:
            msg['Authentication-Results'] = "spf=fail; dkim=fail; dmarc=fail"
            
        body = random.choice(bodies)
        
        msg.set_content(body)
        
        if "invoice" in body.lower() or "attached" in body.lower():
            # Add malicious attachment
            msg.add_attachment(b"malicious payload", maintype="application", subtype="octet-stream", filename="invoice.exe")
    else:
        # Safe traits
        senders = ["newsletter@github.com", "john.doe@company.com", "notifications@slack.com", "jane.smith@university.edu"]
        subjects = ["Weekly Project Update", "Let's grab lunch tomorrow?", "Your GitHub digest", "Meeting notes from yesterday"]
        bodies = [
            "Hi team, attached are the meeting notes from yesterday's discussion. Let me know if you have any questions.\n\nBest, John",
            "Hey, are we still on for lunch tomorrow at 12? Let me know.",
            "Here is your weekly digest of activity. View it here: https://github.com/dashboard",
            "Update: The server migration has been completed successfully. No further action is required."
        ]
        
        msg['From'] = random.choice(senders)
        msg['Subject'] = random.choice(subjects)
        msg['Date'] = "Mon, 01 Jan 2024 10:00:00 +0000"
        msg['Authentication-Results'] = "spf=pass; dkim=pass; dmarc=pass"
        
        body = random.choice(bodies)
        msg.set_content(body)
        
        if "meeting notes" in body.lower():
            # Add safe attachment
            msg.add_attachment(b"meeting notes content", maintype="application", subtype="pdf", filename="meeting_notes.pdf")
            
    return msg.as_string()

def generate_dataset(num_samples: int = 5000):
    print(f"Generating synthetic dataset with {num_samples} samples...")
    data = []
    
    # Generate 50% phishing, 50% legitimate
    for i in range(num_samples):
        is_phishing = i < (num_samples / 2)
        raw_email = generate_synthetic_email(is_phishing)
        data.append({
            'raw_email': raw_email,
            'label': 1 if is_phishing else 0
        })
        
        if (i + 1) % 1000 == 0:
            print(f"Generated {i + 1} emails...")
            
    # Shuffle dataset
    random.shuffle(data)
    
    df = pd.DataFrame(data)
    df.to_csv(DATASET_PATH, index=False)
    print(f"Dataset saved to {DATASET_PATH}")
    
if __name__ == "__main__":
    generate_dataset()
