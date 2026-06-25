# Simple LinkedIn Post Scraper

This project lets you safely download posts from your LinkedIn home feed and save them as a clean, readable Markdown text file (`.md`). 

It uses **Crawl4AI** and copy-pastes your login cookies so you do not have to type your password into a script. It also randomizes its scrolling speed to act like a real human.

---

## 📁 How Your Project Folder Should Look

Create a folder on your computer and place your files inside it like this:

```text
linkedin_scraper/
│
├── scraper.py # The main script that downloads the posts      
├── linkedin_cookies.json # The file where you will paste your login token
```

---

## 🛠️ Step-by-Step Setup

### Step 1: Install the Scraper Library
Open your computer's terminal (Command Prompt or Terminal app) and run this command:
```bash
pip install crawl4ai
```

### Step 2: Get Your LinkedIn Cookie (So you don't have to log in)
LinkedIn blocks automated scripts that try to type passwords. The safest way is to borrow your normal browser's active session:

1. Open your regular web browser (Chrome, Edge, or Brave) and go to your **LinkedIn Home Feed**.
2. **Right-click** anywhere on the page and select **Inspect** (or press `F12` on your keyboard).
3. Go to the **Application** tab at the top of the menu that pops up (on Firefox, it is called **Storage**).
4. In the left sidebar, click the little arrow next to **Cookies**, then click `https://linkedin.com`.
5. Look for a item in the list named **`li_at`**. 
6. Double-click its **Value** (a very long line of letters and numbers) and **copy it**.

### Step 3: Create Your Cookie File
Create a new text file inside your project folder named `linkedin_cookies.json`. Open it and paste your copied text into it exactly like this:

```json
[
  {
    "name": "li_at",
    "value": "PASTE_YOUR_LONG_COOKIE_HERE",
    "domain": ".www.linkedin.com",
    "path": "/"
  }
]
```

---

## 💻 How to Run It

Open your terminal, navigate to your project folder, and run the script. You can tell it exactly how many unique posts you want to collect using the `--target` option.

### Example:
```bash
python scraper.py --company [company_name] --url [linkedian_url_of_your_home_page]
```

## 📝 What the Output Looks Like

When the script finishes, it creates a folder with company name and inside it will store all the `post.md` files:

```markdown
# Extracted LinkedIn Feed Posts

## Post 1
🚀 Big News! We are excited to announce our new partnership...

---

## Post 2
What if customers could try on clothes virtually before buying? Our team built...

---
```

---

## ⚠️ Safety Tips to Protect Your Account

LinkedIn does not like automated tools. To keep your personal profile completely safe:
* **Do not scrape too much:** Keep your target number under **50 posts** per run.
* **Take breaks:** Do not run the script multiple times in a row. Wait at least **2 hours** before running it again.
