# AI for the Soul - Christianity Newsletter 📰

An automated AI-powered newsletter system that researches, generates, and publishes Christianity news with a focus on faith and technology.

## 🌟 Features

### Core Functionality
- **Automated News Research**: Uses Exa API to find the latest Christianity news from reputable sources
- **AI-Generated Content**: OpenAI GPT-4o creates well-structured, engaging newsletter articles
- **Multi-language Support**: Translate newsletters into Spanish, French, German, Italian, and Portuguese
- **Beautiful HTML Templates**: Modern, responsive design with Tailwind CSS
- **Mobile-Responsive**: Optimized for all device sizes

### Automation & Deployment
- **GitHub Actions**: Automatically generates newsletters on a schedule (default: weekly)
- **Vercel Integration**: Auto-deploys to Vercel with every update
- **Newsletter Archive**: Automatically builds an archive page of past issues
- **SEO Optimized**: Includes sitemap, robots.txt, and structured metadata

### Distribution & Engagement
- **Email Integration**: Send newsletters via SendGrid or SMTP
- **Social Sharing**: Built-in Twitter, Facebook, and LinkedIn sharing buttons
- **Open Graph Tags**: Optimized for social media previews
- **Subscriber Management**: Simple text-file based subscriber list

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- GitHub account
- Vercel account
- [Exa API key](https://exa.ai/)
- [OpenAI API key](https://platform.openai.com/)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Chrisfoz/Christianity-newsletter-web-researcher.git
   cd Christianity-newsletter-web-researcher
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   export EXA_API_KEY="your-exa-api-key"
   export OPENAI_API_KEY="your-openai-api-key"
   ```

4. **Run manually (interactive mode)**
   ```bash
   python researcher.py
   ```

5. **Or run automated (non-interactive)**
   ```bash
   python researcher_auto.py
   ```

## 📖 Documentation

- **[SETUP.md](SETUP.md)** - Complete automation setup guide
- **[EMAIL_SETUP.md](EMAIL_SETUP.md)** - Email integration instructions
- **[Contributing](#)** - How to contribute to this project

## 🔧 Project Structure

```
.
├── .github/
│   └── workflows/
│       └── generate-newsletter.yml   # GitHub Actions automation
├── researcher.py                      # Interactive newsletter generator
├── researcher_auto.py                 # Automated newsletter generator
├── email_sender.py                    # Email distribution system
├── build_archive.py                   # Archive page builder
├── build_sitemap.py                   # SEO sitemap generator
├── index.html                         # Latest newsletter (auto-updated)
├── archive.html                       # Newsletter archive (auto-generated)
├── vercel.json                        # Vercel deployment config
├── robots.txt                         # SEO crawler instructions
├── sitemap.xml                        # SEO sitemap (auto-generated)
└── newsletter/                        # Generated newsletter files
    ├── chrisitian_news_article_en.html
    ├── chrisitian_news_article_en.md
    └── search_results.json
```

## 🤖 Automation Setup

### GitHub Actions (Recommended)

1. **Add GitHub Secrets**
   - Go to repository Settings → Secrets → Actions
   - Add `EXA_API_KEY`
   - Add `OPENAI_API_KEY`

2. **Configure Schedule**
   - Edit `.github/workflows/generate-newsletter.yml`
   - Modify the cron expression:
     ```yaml
     schedule:
       - cron: '0 9 * * 1'  # Every Monday at 9 AM UTC
     ```

3. **Manual Trigger**
   - Go to Actions tab → Generate Christianity Newsletter
   - Click "Run workflow"

### Vercel Deployment

1. **Connect Repository**
   - Import your GitHub repo in Vercel
   - Framework: Other
   - Build Command: (leave empty)
   - Output Directory: `./`

2. **Auto-Deploy**
   - Vercel automatically redeploys on every push
   - Your newsletter is live immediately

## 📧 Email Distribution

Send newsletters to subscribers via email:

```bash
# Test with your email first
python email_sender.py \
  --newsletter newsletter/chrisitian_news_article_en.html \
  --service sendgrid \
  --test your-email@example.com

# Send to all subscribers
python email_sender.py \
  --newsletter newsletter/chrisitian_news_article_en.html \
  --service sendgrid \
  --subscribers subscribers.txt
```

See [EMAIL_SETUP.md](EMAIL_SETUP.md) for detailed instructions.

## 🎨 Customization

### Update Newsletter Content

Edit `researcher_auto.py` around line 280:

```python
query = "Your custom search query here"
num_results = 10  # Number of articles to search
```

### Modify Design

The HTML template is in both `researcher.py` and `researcher_auto.py` in the `prepare_html_template()` function. Update:
- Colors and fonts
- Layout and spacing
- Header and footer content
- Social sharing buttons

### Change Schedule

Edit `.github/workflows/generate-newsletter.yml`:

```yaml
# Daily at 8 AM
- cron: '0 8 * * *'

# Twice weekly (Monday & Thursday)
- cron: '0 10 * * 1,4'

# Monthly (1st at noon)
- cron: '0 12 1 * *'
```

## 🌐 Live Demo

- **Latest Newsletter**: https://html-starter-ko9cvrztp-christopher-foster-mcbrides-projects.vercel.app/
- **Archive**: https://html-starter-ko9cvrztp-christopher-foster-mcbrides-projects.vercel.app/archive
- **Main Website**: https://www.aiforthesoul.org/

## 📊 Features Checklist

- ✅ Automated news research with Exa API
- ✅ AI content generation with GPT-4o
- ✅ Modern, responsive HTML templates
- ✅ GitHub Actions automation
- ✅ Vercel auto-deployment
- ✅ Newsletter archive system
- ✅ Email distribution (SendGrid/SMTP)
- ✅ Social sharing buttons
- ✅ SEO optimization (meta tags, sitemap)
- ✅ Multi-language support
- ✅ Mobile-responsive design

## 🛠️ Technologies Used

- **Python** - Core scripting language
- **OpenAI GPT-4o** - AI content generation
- **Exa API** - Web search and research
- **Tailwind CSS** - Modern styling
- **GitHub Actions** - CI/CD automation
- **Vercel** - Static site hosting
- **SendGrid** - Email delivery
- **Google Fonts** - Typography (Inter & Merriweather)

## 📝 License

This project is open source and available under the MIT License.

## 💬 Support

- **Email**: support@aiforthesoul.org
- **Website**: https://www.aiforthesoul.org/
- **Issues**: [GitHub Issues](https://github.com/Chrisfoz/Christianity-newsletter-web-researcher/issues)

## 🙏 Credits

Created by Christopher Foster-McBride for AI for the Soul.

This newsletter uses AI to curate and analyze Christianity news, helping readers stay informed about faith and technology.
