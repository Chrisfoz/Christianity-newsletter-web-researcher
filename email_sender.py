"""
Email Newsletter Sender for AI for the Soul

This script sends the generated newsletter to subscribers using various email services:
- SendGrid (recommended for reliability)
- SMTP (for custom email servers)
- Mailgun (alternative option)

Setup Instructions:
1. Choose your email provider and set up an account
2. Add the necessary API keys/credentials as environment variables
3. Create a subscribers.txt file with one email per line
"""

import os
import json
from datetime import datetime
from pathlib import Path
from termcolor import colored

# SendGrid integration
try:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail, Email, To, Content
    SENDGRID_AVAILABLE = True
except ImportError:
    SENDGRID_AVAILABLE = False
    print(colored("SendGrid not installed. Run: pip install sendgrid", "yellow"))

# SMTP integration
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class NewsletterEmailer:
    def __init__(self, service='sendgrid'):
        """
        Initialize the email service

        Args:
            service: 'sendgrid', 'smtp', or 'mailgun'
        """
        self.service = service
        self.from_email = os.getenv('FROM_EMAIL', 'support@aiforthesoul.org')
        self.from_name = os.getenv('FROM_NAME', 'AI for the Soul')

        if service == 'sendgrid':
            self.api_key = os.getenv('SENDGRID_API_KEY')
            if not self.api_key:
                raise ValueError("SENDGRID_API_KEY environment variable not set")
        elif service == 'smtp':
            self.smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
            self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
            self.smtp_user = os.getenv('SMTP_USER')
            self.smtp_pass = os.getenv('SMTP_PASS')
            if not self.smtp_user or not self.smtp_pass:
                raise ValueError("SMTP_USER and SMTP_PASS environment variables must be set")

    def load_subscribers(self, filepath='subscribers.txt'):
        """Load subscriber emails from a file"""
        try:
            with open(filepath, 'r') as f:
                emails = [line.strip() for line in f if line.strip() and '@' in line]
            print(colored(f"Loaded {len(emails)} subscribers", "green"))
            return emails
        except FileNotFoundError:
            print(colored(f"Subscriber file not found: {filepath}", "red"))
            return []

    def load_newsletter_html(self, filepath):
        """Load the newsletter HTML content"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(colored(f"Newsletter file not found: {filepath}", "red"))
            return None

    def send_with_sendgrid(self, to_emails, subject, html_content):
        """Send email using SendGrid"""
        if not SENDGRID_AVAILABLE:
            print(colored("SendGrid library not available", "red"))
            return False

        try:
            sg = SendGridAPIClient(self.api_key)

            # Send individual emails (better for tracking)
            success_count = 0
            fail_count = 0

            for email in to_emails:
                try:
                    message = Mail(
                        from_email=Email(self.from_email, self.from_name),
                        to_emails=To(email),
                        subject=subject,
                        html_content=Content("text/html", html_content)
                    )

                    response = sg.send(message)
                    if response.status_code == 202:
                        success_count += 1
                        print(colored(f"✓ Sent to {email}", "green"))
                    else:
                        fail_count += 1
                        print(colored(f"✗ Failed to send to {email}: {response.status_code}", "red"))

                except Exception as e:
                    fail_count += 1
                    print(colored(f"✗ Error sending to {email}: {str(e)}", "red"))

            print(colored(f"\nEmail sending complete: {success_count} sent, {fail_count} failed", "cyan"))
            return True

        except Exception as e:
            print(colored(f"SendGrid error: {str(e)}", "red"))
            return False

    def send_with_smtp(self, to_emails, subject, html_content):
        """Send email using SMTP"""
        try:
            success_count = 0
            fail_count = 0

            # Create SMTP connection
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_pass)

            for email in to_emails:
                try:
                    msg = MIMEMultipart('alternative')
                    msg['From'] = f"{self.from_name} <{self.from_email}>"
                    msg['To'] = email
                    msg['Subject'] = subject

                    # Attach HTML content
                    html_part = MIMEText(html_content, 'html')
                    msg.attach(html_part)

                    server.send_message(msg)
                    success_count += 1
                    print(colored(f"✓ Sent to {email}", "green"))

                except Exception as e:
                    fail_count += 1
                    print(colored(f"✗ Error sending to {email}: {str(e)}", "red"))

            server.quit()
            print(colored(f"\nEmail sending complete: {success_count} sent, {fail_count} failed", "cyan"))
            return True

        except Exception as e:
            print(colored(f"SMTP error: {str(e)}", "red"))
            return False

    def send_newsletter(self, newsletter_path, subscribers_path='subscribers.txt', subject=None):
        """
        Send newsletter to all subscribers

        Args:
            newsletter_path: Path to the newsletter HTML file
            subscribers_path: Path to the subscribers list file
            subject: Email subject line (auto-generated if None)
        """
        # Load subscribers
        subscribers = self.load_subscribers(subscribers_path)
        if not subscribers:
            print(colored("No subscribers to send to", "yellow"))
            return False

        # Load newsletter
        html_content = self.load_newsletter_html(newsletter_path)
        if not html_content:
            return False

        # Generate subject if not provided
        if not subject:
            current_date = datetime.now().strftime("%B %d, %Y")
            subject = f"AI for the Soul Newsletter - {current_date}"

        print(colored(f"\nSending newsletter to {len(subscribers)} subscribers...", "cyan"))
        print(colored(f"Subject: {subject}", "cyan"))

        # Send based on service
        if self.service == 'sendgrid':
            return self.send_with_sendgrid(subscribers, subject, html_content)
        elif self.service == 'smtp':
            return self.send_with_smtp(subscribers, subject, html_content)
        else:
            print(colored(f"Unknown email service: {self.service}", "red"))
            return False


def main():
    """Main function for testing email sending"""
    import argparse

    parser = argparse.ArgumentParser(description='Send newsletter via email')
    parser.add_argument('--newsletter', required=True, help='Path to newsletter HTML file')
    parser.add_argument('--subscribers', default='subscribers.txt', help='Path to subscribers file')
    parser.add_argument('--service', default='sendgrid', choices=['sendgrid', 'smtp'], help='Email service to use')
    parser.add_argument('--subject', help='Email subject line')
    parser.add_argument('--test', help='Test email address (sends only to this address)')

    args = parser.parse_args()

    # If test mode, create temporary subscriber file
    if args.test:
        test_file = 'test_subscribers.txt'
        with open(test_file, 'w') as f:
            f.write(args.test)
        args.subscribers = test_file
        print(colored(f"TEST MODE: Sending to {args.test} only", "yellow"))

    # Create emailer and send
    emailer = NewsletterEmailer(service=args.service)
    success = emailer.send_newsletter(
        newsletter_path=args.newsletter,
        subscribers_path=args.subscribers,
        subject=args.subject
    )

    # Clean up test file
    if args.test and os.path.exists('test_subscribers.txt'):
        os.remove('test_subscribers.txt')

    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
