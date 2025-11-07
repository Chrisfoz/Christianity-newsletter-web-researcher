# Email Newsletter Setup Guide

This guide explains how to send your AI for the Soul newsletter to subscribers via email.

## Quick Start

1. Choose an email service provider (SendGrid recommended)
2. Set up your API credentials
3. Create a subscriber list
4. Send your newsletter

## Email Service Options

### Option 1: SendGrid (Recommended)

SendGrid is a reliable, easy-to-use email service with a generous free tier (100 emails/day).

#### Setup Steps:

1. **Create a SendGrid account** at https://sendgrid.com/
2. **Generate an API key:**
   - Go to Settings → API Keys
   - Click "Create API Key"
   - Give it a name (e.g., "AI for the Soul Newsletter")
   - Select "Full Access" or "Mail Send" permissions
   - Copy the API key (you'll only see it once!)

3. **Set environment variables:**
   ```bash
   export SENDGRID_API_KEY="your-api-key-here"
   export FROM_EMAIL="support@aiforthesoul.org"
   export FROM_NAME="AI for the Soul"
   ```

4. **Add to GitHub Secrets** (for automation):
   - Go to your repository Settings → Secrets → Actions
   - Add `SENDGRID_API_KEY` with your API key
   - Add `FROM_EMAIL` with your sender email
   - Add `FROM_NAME` with "AI for the Soul"

#### Verify Sender Email:
SendGrid requires sender verification. Go to Settings → Sender Authentication and verify your email address.

### Option 2: SMTP (Gmail, Outlook, etc.)

Use your existing email account to send newsletters.

#### Gmail Setup:

1. **Enable 2-Factor Authentication** on your Google account
2. **Create an App Password:**
   - Go to Google Account → Security → 2-Step Verification
   - Scroll to "App passwords"
   - Generate a new app password for "Mail"
   - Copy the 16-character password

3. **Set environment variables:**
   ```bash
   export SMTP_HOST="smtp.gmail.com"
   export SMTP_PORT="587"
   export SMTP_USER="your-email@gmail.com"
   export SMTP_PASS="your-app-password"
   export FROM_EMAIL="your-email@gmail.com"
   export FROM_NAME="AI for the Soul"
   ```

**Note:** Gmail has a sending limit of ~500 emails/day for free accounts.

## Managing Subscribers

### Create Subscriber List

1. Copy the example file:
   ```bash
   cp subscribers.txt.example subscribers.txt
   ```

2. Edit `subscribers.txt` and add one email per line:
   ```
   subscriber1@example.com
   subscriber2@example.com
   subscriber3@example.com
   ```

3. Lines starting with `#` are ignored (for comments)

### Privacy & Compliance

- **GDPR Compliance:** Only add subscribers who have opted in
- **Unsubscribe:** Include unsubscribe instructions in your newsletter
- **Data Security:** Keep `subscribers.txt` private (it's in .gitignore)

## Sending Newsletters

### Test Sending (Recommended First)

Before sending to all subscribers, test with your own email:

```bash
python email_sender.py \
  --newsletter newsletter/chrisitian_news_article_en.html \
  --service sendgrid \
  --test your-email@example.com
```

### Send to All Subscribers

```bash
python email_sender.py \
  --newsletter newsletter/chrisitian_news_article_en.html \
  --service sendgrid \
  --subscribers subscribers.txt
```

### Custom Subject Line

```bash
python email_sender.py \
  --newsletter newsletter/chrisitian_news_article_en.html \
  --service sendgrid \
  --subject "Weekly Christianity News - December 2024"
```

### Using SMTP Instead of SendGrid

```bash
python email_sender.py \
  --newsletter newsletter/chrisitian_news_article_en.html \
  --service smtp \
  --subscribers subscribers.txt
```

## Automation with GitHub Actions

To automatically send emails when the newsletter is generated, update `.github/workflows/generate-newsletter.yml`:

1. Add email credentials to GitHub Secrets (as shown above)

2. Add this step to the workflow after newsletter generation:

```yaml
- name: Send newsletter via email
  env:
    SENDGRID_API_KEY: ${{ secrets.SENDGRID_API_KEY }}
    FROM_EMAIL: ${{ secrets.FROM_EMAIL }}
    FROM_NAME: ${{ secrets.FROM_NAME }}
  run: |
    python email_sender.py \
      --newsletter newsletter/chrisitian_news_article_en.html \
      --service sendgrid \
      --subscribers subscribers.txt
```

**Important:** Make sure to commit `subscribers.txt` to your private repository, or use a service like MailChimp/Mailgun for subscriber management.

## Subscriber Management Services (Alternative)

For larger lists (1000+ subscribers), consider:

- **Mailchimp** - Popular, user-friendly, free up to 500 subscribers
- **Substack** - Newsletter platform with built-in subscriber management
- **ConvertKit** - Great for creators, free up to 1000 subscribers
- **Buttondown** - Simple, affordable newsletter service

These services handle:
- Subscriber opt-in/opt-out
- Compliance (GDPR, CAN-SPAM)
- Unsubscribe links
- Analytics and tracking
- Better deliverability

## Troubleshooting

### "SendGrid API key not set"
- Verify environment variable is set: `echo $SENDGRID_API_KEY`
- In GitHub Actions, check that the secret is added

### "SMTP Authentication failed"
- For Gmail, make sure you're using an App Password, not your regular password
- Check that 2-Factor Authentication is enabled

### Emails going to spam
- Verify your sender email with SendGrid
- Add SPF and DKIM records to your domain
- Avoid spam trigger words in subject lines
- Ask subscribers to whitelist your email

### Rate limiting
- SendGrid free: 100 emails/day
- Gmail: ~500 emails/day
- For larger lists, upgrade your plan or use a newsletter service

## Best Practices

1. **Always test first** with your own email
2. **Send at consistent times** (e.g., every Monday 9 AM)
3. **Monitor bounce rates** - remove invalid emails
4. **Provide value** - only send when you have quality content
5. **Include an unsubscribe link** (required by law in many countries)
6. **Track engagement** - use SendGrid analytics to see open rates

## Support

Questions? Email support@aiforthesoul.org
