# AI for the Soul - Newsletter Automation Setup Guide

This guide will help you set up automated newsletter generation and deployment.

## Prerequisites

- GitHub account with this repository
- Vercel account connected to your GitHub repository
- EXA API key (from https://exa.ai/)
- OpenAI API key (from https://platform.openai.com/)

## Step 1: Configure GitHub Secrets

You need to add your API keys as GitHub repository secrets:

1. Go to your GitHub repository
2. Click on **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add the following secrets:

   - **Name:** `EXA_API_KEY`
     **Value:** Your Exa API key

   - **Name:** `OPENAI_API_KEY`
     **Value:** Your OpenAI API key

## Step 2: Connect to Vercel

1. Go to [Vercel](https://vercel.com/)
2. Import your GitHub repository
3. Configure the project:
   - **Framework Preset:** Other
   - **Build Command:** Leave empty
   - **Output Directory:** `./`
4. Deploy the project

Vercel will automatically redeploy whenever you push changes to your repository.

## Step 3: Configure the Schedule

The newsletter is set to generate automatically every Monday at 9 AM UTC. To change the schedule:

1. Edit `.github/workflows/generate-newsletter.yml`
2. Modify the cron expression:
   ```yaml
   schedule:
     - cron: '0 9 * * 1'  # Minutes Hour Day Month DayOfWeek
   ```

### Common Cron Schedules:
- Every Monday at 9 AM: `0 9 * * 1`
- Every day at 8 AM: `0 8 * * *`
- Twice a week (Mon & Thu at 10 AM): `0 10 * * 1,4`
- First day of month at noon: `0 12 1 * *`

## Step 4: Manual Trigger

You can manually trigger newsletter generation:

1. Go to your GitHub repository
2. Click **Actions** tab
3. Select **Generate Christianity Newsletter** workflow
4. Click **Run workflow**
5. Select your branch and click **Run workflow**

## Step 5: Customize Newsletter Content

To customize the search query or number of results, edit `researcher_auto.py`:

```python
# Around line 250
query = "Christianity news, Christian churches, Christianity and AI, faith and technology, Christian social impact"
num_results = 10
```

## How It Works

1. **GitHub Actions** runs the Python script on schedule
2. The script searches for Christianity news using the Exa API
3. OpenAI GPT-4o generates a well-structured newsletter article
4. The HTML newsletter is generated with your branding
5. Files are committed back to the repository
6. **Vercel** automatically detects the changes and redeploys
7. Your newsletter is live at your Vercel URL

## File Structure

```
.
├── .github/
│   └── workflows/
│       └── generate-newsletter.yml  # GitHub Actions workflow
├── newsletter/                       # Generated newsletter files
│   ├── chrisitian_news_article_en.md
│   ├── chrisitian_news_article_en.html
│   └── search_results.json
├── researcher.py                     # Interactive version
├── researcher_auto.py                # Automated version
├── index.html                        # Main page (latest newsletter)
├── vercel.json                       # Vercel configuration
└── requirements.txt                  # Python dependencies
```

## Troubleshooting

### Workflow fails with API errors
- Check that your GitHub secrets are correctly set
- Verify your API keys are valid and have sufficient credits

### Newsletter not updating on Vercel
- Check GitHub Actions logs for errors
- Ensure the workflow completed successfully
- Vercel should auto-deploy when changes are pushed

### Want to test locally first?
```bash
# Set environment variables
export EXA_API_KEY="your-key"
export OPENAI_API_KEY="your-key"

# Run the automated script
python researcher_auto.py
```

## Support

For questions or issues, contact support@aiforthesoul.org
