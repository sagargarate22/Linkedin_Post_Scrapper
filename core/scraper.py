import asyncio
import json
import os
import argparse
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

async def scrape_linkedin_posts(company, url):
    with open("linkedin_cookies.json", "r") as f:
        saved_state = json.load(f)

    schema = {
        "name": "LinkedIn Direct Posts Extraction",
        "baseSelector": "div.feed-shared-update-v2__description, div.update-components-update-v2__commentary", # main card class nested 
        "fields": [
            {
                "name": "post_text",
                "selector": "span.break-words.tvm-parent-container > span[dir='ltr']", # actual post content span tag
                "type": "text"
            }
        ]
    }
    extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)

    browser_config = BrowserConfig(
        headless=False,
        use_persistent_context=True,
        cookies=saved_state,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
    )

    # Smart Scroll Logic: Stops if target posts (15) are hit OR if scrolling loads nothing new
    smart_scroll_js = """
    async () => {
        let attempts = 0;
        const maxAttempts = 12;       // Maximum absolute ceiling for scrolls
        const targetPostCount = 20;   // Stop immediately if we hit this target
        
        let previousPostCount = 0;
        let emptyScrollsCounter = 0;   // Tracks continuous failures to load data

        while (attempts < maxAttempts) {
            let currentPostCount = document.querySelectorAll('div.feed-shared-update-v2, .update-components-text').length;
            
            // Condition 1: Target reached, stop.
            if (currentPostCount >= targetPostCount) {
                return true; 
            }
            
            // Condition 2: Check if this scroll actually loaded anything new
            if (attempts > 0 && currentPostCount === previousPostCount) {
                emptyScrollsCounter++;
                console.log(`No new posts loaded on this scroll. Failure count: ${emptyScrollsCounter}`);
                
                // ONLY stop if it fails 3 times in a row (gives LinkedIn network time to breathe)
                if (emptyScrollsCounter >= 3) {
                    console.log("Hit real dead end or login wall. Stopping.");
                    return true;
                }
            } else {
                // Reset counter if a scroll successfully appends new posts
                emptyScrollsCounter = 0;
            }
            
            previousPostCount = currentPostCount;
            
            // Scroll down further to trigger next network batch
            window.scrollBy(0, window.innerHeight * 1.5);
            attempts++;
            
            // Wait random seconds per attempt between 3 to 5
            const randomScrollDelay = Math.floor(Math.random() * (5000 - 3000 + 1)) + 3000;
            await new Promise(resolve => setTimeout(resolve, randomScrollDelay)); 
        }
        return true; 
    }
    """

    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=extraction_strategy,
        # css_selector="main#main, div.scaffold-layout__main div.feed-shared-update-v2",
        wait_for=f"js:{smart_scroll_js}"
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        target_url = url 
        print("Launching automated scraper...")
        
        result = await crawler.arun(url=target_url, config=run_config)

        if result.success:
            if not os.path.exists(company):
                os.mkdir(company)

            posts_markdown = json.loads(result.extracted_content)

            seen_post = set()
            post_index = 0

            for item in posts_markdown:
                text_content = item.get("post_text").strip()

                if not text_content:
                    continue

                if  text_content in seen_post:
                    continue

                seen_post.add(text_content)

                post_index += 1
                markdown_content = f"## Post {post_index}\n"
                markdown_content += f"{text_content}\n\n"
                markdown_content += "---\n\n"


                file_name = f'{company}/Post {post_index}.md'
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write(markdown_content)
                
            print(f"\nSuccess! Filtered post data saved to")
        else:
            print(f"Scraping failed: {result.error_message}")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--company', type=str)
    parser.add_argument('--url', type=str)

    args = parser.parse_args()
    
    asyncio.run(scrape_linkedin_posts(args.company, args.url))
