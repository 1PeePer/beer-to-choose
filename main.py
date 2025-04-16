from playwright.async_api import async_playwright
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path
import logging
import asyncio
import time
import sys
import re

async def main() -> None:
    addresses = [
        #"Москва, Чонгарский бул., 7",
        "Ижевск, Кирова ул., 146"
    ]
    
    for address in addresses:
        catalog = await AsyncLentaProductParse(address).parse()
        
        if catalog:
            print(f"\nРезультаты для {address}:")
            for idx, item in enumerate(catalog[:2], 1):  # Выводим первые 2 товара для примера
                print(f"{idx}. {item['name']} - {item['volume']} - {item['price']} - {item['image']}")
            print(" - -" * 50)
            print(f"{len(catalog)}. {catalog[-1]['name']} - {catalog[-1]['volume']} - {catalog[-1]['price']} - {catalog[-1]['image']}")
        else:
            print(f"\nНе удалось получить данные для {address}")

class AsyncLentaProductParse:
    def __init__(self, address: str) -> None:
        self.address = address
        self.list_products = []
        self.start_time = time.perf_counter()
        self.logger = self._setup_logging()
        
    def _setup_logging(self):
        """Logging system setup"""
        log_dir = Path(__file__).parent / "logs"
        log_dir.mkdir(exist_ok=True)

        self._clean_logs_if_needed(log_dir, max_size_mb=1)
        
        logging.basicConfig(
            level=logging.INFO,
            datefmt="%Y-%m-%d %H:%M:%S",
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_dir / f"lenta_parser_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
                logging.StreamHandler(sys.stdout)
            ]
        )
        return logging.getLogger("LentaParser")
    
    def _clean_logs_if_needed(self, log_dir: Path, max_size_mb: float):
        """Clearing logs if necessary"""
        total_size = sum(f.stat().st_size for f in log_dir.glob('*') if f.is_file())
        if total_size > max_size_mb * 1024 * 1024:
            for log_file in log_dir.glob('*'):
                log_file.unlink()

    async def __store_selection(self) -> None:
        """Store selection"""
        try:
            self.logger.info("Selecting store ->")
            
            await self.page.wait_for_selector("div.address-block.ng-star-inserted")
            await self.page.click("div.address-block.ng-star-inserted")
            self.logger.debug("clicked address block ...")

            await self.page.wait_for_selector("form.ng-untouched.ng-pristine.ng-valid")
            await self.page.type(
                "input.p-element.p-autocomplete-input.p-inputtext.p-component.ng-star-inserted",
                self.address,
                delay=30
            )
            self.logger.debug(f"entered address: {self.address} ...")

            await self.page.wait_for_selector("li.p-ripple.p-element.p-autocomplete-item.ng-star-inserted")
            await self.page.click("li.p-ripple.p-element.p-autocomplete-item.ng-star-inserted")
            await self.page.click("button.p-element.p-button.p-button-primary.large.w-100.p-component.ng-star-inserted")
            self.logger.info("<- store successfully selected")

        except Exception as e:
            self.logger.error(f"Error during store selection: {str(e)}", exc_info=True)
            raise

    async def __go_to_beer_catalog(self) -> None:
        """Navigate to catalog"""
        try:
            self.logger.info("Navigating to product catalog ->")
            
            await self.page.wait_for_selector("lu-catalog-button.ng-star-inserted")
            await self.page.click("button.p-button.p-button-tertiary.catalog-button")
            self.logger.debug("main catalog opened ...")

            await self.page.wait_for_selector("a[href='https://lenta.com/catalog/alkogol-17036/']")
            await self.page.click("a[href='https://lenta.com/catalog/alkogol-17036/']")
            self.logger.debug("sub-catalog opened ...")

            await self.page.wait_for_selector("lu-search-categories-chips.ng-star-inserted")
            await self.page.click("a[href^='https://lenta.com/catalog/pivo-sidr']")
            self.logger.info("<- successfully navigated to product catalog")

        except Exception as e:
            self.logger.error(f"Catalog navigation error: {str(e)}", exc_info=True)
            raise

    async def __get_beer_info(self, number_of_pages: int) -> List[Dict]:
        """Parsing products in catalog"""
        catalog = []
        self.logger.info(f"Starting page parsing ->")
        
        for i in range(1, number_of_pages + 1):
            try:
                self.logger.debug(f"processing page {i}/{number_of_pages} ...")
                
                await self.page.wait_for_selector("div.lu-grid", state="attached")
                await self.__scroll_page()
                
                items = await self.page.query_selector_all("div[class='lu-grid__item ng-star-inserted']")
                self.logger.debug(f"found {len(items)} products on page {i} ...")

                page_items = []
                for idx, item in enumerate(items, 1):
                    try:
                        product_data = {
                            "name": await self._get_element_text(item, "span.card-name_content"),
                            "volume": await self._get_element_text(item, "p.card-name_package"),
                            "price": self.__clean_value(await self._get_element_text(item, "span.main-price, span[class^='main-price']")),
                            "image": await self._get_attribute(item, "img.lu-product-card-image", "src")
                        }
                        page_items.append(product_data)
                        
                        if idx % 10 == 0:
                            self.logger.debug(f"processed {idx}/{len(items)} products on page {i} ...")
                    
                    except Exception as e:
                        self.logger.warning(f"Error parsing product {idx} on page {i}: {str(e)}")

                catalog.extend(page_items)
                self.logger.info(f"page {i} processed. Products: {len(page_items)} ...")

                if i < number_of_pages:
                    next_selector = f"a[aria-label='перейти на страницу {i + 1}']"
                    if await self.page.query_selector(next_selector):
                        await self.page.click(next_selector)
                        self.logger.debug(f"navigating to page {i + 1} ...")
                    else:
                        self.logger.warning(f"Next page button not found for page {i + 1}")
                        break
                        
            except Exception as e:
                self.logger.error(f"Error processing page {i}: {str(e)}", exc_info=True)
                continue
        self.logger.info(f"<- parsing completed! Total products processed: {len(catalog)}")

        return catalog

    async def _get_element_text(self, parent, selector: str) -> str:
        """Safely get element text"""
        element = await parent.query_selector(selector)
        if element and await element.is_visible():
            return await element.inner_text()
        return "Not specified"

    async def _get_attribute(self, parent, selector: str, attr: str) -> Optional[str]:
        """Safely get element attribute"""
        element = await parent.query_selector(selector)
        if element and await element.is_visible():
            return await element.get_attribute(attr)
        return None

    async def __number_of_pages(self) -> int:
        """Get total number of product pages"""
        try:
            await self.page.wait_for_selector("nav.ng-star-inserted")
            pagination = await self.page.query_selector("ul.pagination")
            if not pagination:
                return 1
                
            last_page = await pagination.query_selector("li:last-child")
            return int(await last_page.inner_text()) if last_page else 1
        except Exception as e:
            print(f"Error getting page count: {e}")
            return 1

    async def __scroll_page(self) -> None:
        await self.page.wait_for_selector("div[class='lu-grid']")
        await self.page.evaluate("""() => {
                window.scrollTo({
                    top: document.body.scrollHeight / 2,
                    behavior: 'smooth'
                });
            }""")
    
    def __clean_value(self, value: str) -> str:
        """Clean price value"""
        try:
            price_match = re.search(r'(\d+,\d+)', value)
            return f"{price_match.group(1)} ₽" if price_match else "Price not specified"
        except Exception as e:
            print(f"Error processing price: {e}")
            return "Price error"

    async def parse(self) -> Optional[List[Dict]]:
        """Main parser method"""
        try:
            self.logger.info(f"Starting parser for address: {self.address} -> -> ->")
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=False,
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        "--disable-dev-shm-usage",
                        "--disable-accelerated-2d-canvas",
                        "--no-first-run",
                        "--no-zygote",
                        "--disable-gpu",
                        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                    ],
                    timeout=3000
                )
                self.context = await browser.new_context(
                    locale="ru-RU",
                    viewport={"width": 1920, "height": 1080},
                    extra_http_headers={
                        "Referer": "https://lenta.com/",
                        "Sec-Fetch-Dest": "document"
                    }
                )
                self.page = await self.context.new_page()

                await self.page.goto("https://lenta.com/", timeout=5000)
                self.logger.info("Main page loaded -> ->")

                await self.__store_selection()
                await self.__go_to_beer_catalog()

                total_pages = await self.__number_of_pages()
                self.logger.info(f"Total pages to parse: {total_pages} -> ->")

                catalog = await self.__get_beer_info(total_pages)

                elapsed_seconds = time.perf_counter() - self.start_time
                hours, remainder = divmod(elapsed_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                self.logger.info(
                    f"<- <- <- parser finished. Execution time: "
                    f"{int(minutes)} min {seconds:.1f} sec"
                )
                return catalog

        except Exception as e:
            self.logger.critical(f"Critical error: {str(e)}", exc_info=True)
            return None

if __name__ == "__main__":
    asyncio.run(main())