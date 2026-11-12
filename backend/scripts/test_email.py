from app.services.email_service import send_password_reset_email

if __name__ == "__main__":
    # Replace with an inbox you control.
    recipient = input("Enter your test recipient email: ").strip()

    # Use a harmless placeholder token for this delivery test.
    send_password_reset_email(recipient, "smtp-test-token")

    print("SMTP accepted the test email for sending.")