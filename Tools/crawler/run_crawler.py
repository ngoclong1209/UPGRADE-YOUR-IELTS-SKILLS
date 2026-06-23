import sys
import argparse
import requests
import json
import os
import time
from scraper import YouPassScraper

def main():
    parser = argparse.ArgumentParser(description="YouPass.vn Exercise Scraper")
    parser.add_argument("--skill", type=str, choices=["listening", "reading", "writing", "speaking", "all"], default="listening",
                        help="Specify the skill to crawl (default: listening)")
    parser.add_argument("--limit", type=int, default=10,
                        help="Maximum number of exercises to crawl (default: 10)")
    parser.add_argument("--delay", type=float, default=2.0,
                        help="Delay in seconds between requests to avoid rate limits (default: 2.0)")
    args = parser.parse_args()

    scraper = YouPassScraper()
    if not scraper.auth_token:
        print("Error: Active session not loaded. Please run 'login_cdp.py' to authenticate.")
        return

    # Map skills to API type parameters
    # Type 1 & 9 -> Reading
    # Type 2 & 10 -> Listening
    # Type 7 -> Writing
    # Type 8 -> Speaking
    type_filters = {
        "reading": [1, 9],
        "listening": [2, 10],
        "writing": [7],
        "speaking": [8]
    }

    selected_types = []
    if args.skill == "all":
        selected_types = [1, 2, 7, 8, 9, 10]
    else:
        selected_types = type_filters[args.skill]

    print("="*60)
    print(f"Starting crawl for skill: {args.skill.upper()}")
    print(f"Target types: {selected_types}")
    print(f"Limit: {args.limit} items")
    print(f"Polite delay: {args.delay} seconds")
    print("="*60 + "\n")

    # Fetch quizzes list with pagination
    page = 1
    crawled_count = 0
    
    # Build endpoint to fetch quizzes of selected types
    types_query = "&".join([f"types={t}" for t in selected_types])
    
    while crawled_count < args.limit:
        url = f"https://api.youpass.vn/v1/quizzes?page_size=50&page={page}&status=published&is_test=true&{types_query}"
        print(f"Fetching quizzes list page {page}...")
        
        try:
            r = requests.get(url, headers=scraper.headers)
            if r.status_code != 200:
                print(f"Failed to fetch quizzes list. Status: {r.status_code}")
                break
                
            data = r.json()
            items = data.get("data", {}).get("items", [])
            if not items:
                print("No more exercises found in catalog.")
                break
                
            print(f"Found {len(items)} exercises on page {page}.")
            
            for item in items:
                if crawled_count >= args.limit:
                    break
                    
                q_id = item.get("id")
                title = item.get("title", f"Quiz_{q_id}")
                
                print(f"\n[{crawled_count+1}/{args.limit}] ID: {q_id} | Title: {title}")
                
                try:
                    success = scraper.scrape_quiz(q_id)
                    if success:
                        crawled_count += 1
                        # Polite delay
                        time.sleep(args.delay)
                except Exception as e:
                    print(f"Error scraping quiz {q_id}: {e}")
                    
            page += 1
            
        except Exception as e:
            print(f"Network error: {e}")
            break

    print("\n" + "="*60)
    print(f"CRAWL COMPLETE: Successfully downloaded {crawled_count} exercises!")
    print(f"Data saved to: {scraper.clean_filename(DATA_DIR)}")
    print("="*60)

if __name__ == "__main__":
    main()
