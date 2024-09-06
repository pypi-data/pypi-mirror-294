from icrawler.builtin import GoogleImageCrawler
import logging
import os

logging.disable(logging.CRITICAL)

def searchGoogle(term, path, max_images = 30):
    print(f"Fetching Images of '{term}' from Google...")
    if not os.path.exists(path):
        os.makedirs(path)
    
    google_crawler = GoogleImageCrawler(storage={'root_dir': path})
    
    google_crawler.crawl(keyword=term, max_num=max_images)
    
    for idx, file_name in enumerate(os.listdir(path)):
        if file_name.startswith('google_'):
            continue  # Skip already renamed files
        new_name = f'google_{idx + 1:06d}.jpg'
        os.rename(os.path.join(path, file_name), os.path.join(path, new_name))


def search_google_entry():
    import argparse
    parser = argparse.ArgumentParser(description='Search for images on Google.')
    parser.add_argument('--term', type=str, help='Search term')
    parser.add_argument('--path', type=str, help='Directory to save images')
    parser.add_argument('--max_images', type=int, default=10, help='Maximum number of images to download')
    args = parser.parse_args()
    searchGoogle(term=args.term, path=args.path, max_images=args.max_images)