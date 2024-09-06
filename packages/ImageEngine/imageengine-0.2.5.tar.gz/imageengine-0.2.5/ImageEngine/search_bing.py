from icrawler.builtin import BingImageCrawler
import logging
import os

logging.disable(logging.CRITICAL)

def searchBing(term, path, max_images = 30):
    print(f"Fetching Images of '{term}' from Bing...")
    if not os.path.exists(path):
        os.makedirs(path)
    
    bing_crawler = BingImageCrawler(storage={'root_dir': path})
    
    bing_crawler.crawl(keyword=term, max_num=max_images)
    
    for idx, file_name in enumerate(os.listdir(path)):
        if file_name.startswith('bing_'):
            continue  # Skip already renamed files
        new_name = f'bing_{idx + 1:06d}.jpg'
        os.rename(os.path.join(path, file_name), os.path.join(path, new_name))

def search_bing_entry():
    import argparse
    parser = argparse.ArgumentParser(description='Search for images on Bing.')
    parser.add_argument('--term', type=str, help='Search term')
    parser.add_argument('--path', type=str, help='Directory to save images')
    parser.add_argument('--max_images', type=int, default=10, help='Maximum number of images to download')
    args = parser.parse_args()
    searchBing(term=args.term, path=args.path, max_images=args.max_images)