from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        # Go to one of the generated blog pages
        page.goto("file:///app/blogs/training-at-larger-scale/part1.html")
        page.wait_for_selector(".prose")
        # Take a screenshot
        page.screenshot(path="/home/jules/verification/code_verification.png", full_page=True)
        browser.close()

if __name__ == "__main__":
    main()
