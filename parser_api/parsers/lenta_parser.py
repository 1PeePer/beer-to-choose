from playwright.async_api import async_playwright
from typing import List, Dict, Optional
import time
import re


from parser_api.config.browser import (
    BROWSER_SETTINGS,
    CONTEXT_SETTINGS,
    USER_AGENT,
    BASE_URL,
    TIMEOUT,
)

from parser_api.config.selectors import SELECTORS
from parser_api.utils.logging import setup_logging
from parser_api.utils.name_processor import process_product_name
from parser_api.models.product import Product

class AsyncLentaProductParse:
    def __init__(self, address: str) -> None:
        self.address = address
        self.list_products = []
        self.start_time = time.perf_counter()
        self.logger = setup_logging()
        self.logger.info("Parser initialized with address: %s", address)

    async def __store_selection(self) -> None:
        """Store selection"""
        try:
            self.logger.info("Selecting store ->")
            
            await self.page.wait_for_selector(SELECTORS["address_block"], timeout=TIMEOUT)
            self.logger.debug("Found address block")
            await self.page.click(SELECTORS["address_block"])
            self.logger.debug("Clicked address block")

            await self.page.wait_for_selector(SELECTORS["address_form"], timeout=TIMEOUT)
            self.logger.debug("Found address form")
            await self.page.type(
                SELECTORS["address_input"],
                self.address,
                delay=30
            )
            self.logger.debug(f"Entered address: {self.address}")

            await self.page.wait_for_selector(SELECTORS["address_item"], timeout=TIMEOUT)
            self.logger.debug("Found address item")
            await self.page.click(SELECTORS["address_item"])
            await self.page.click(SELECTORS["confirm_button"])
            self.logger.info("Store successfully selected")

        except Exception as e:
            self.logger.error(f"Error during store selection: {str(e)}", exc_info=True)
            raise

    async def __go_to_beer_catalog(self) -> None:
        """Navigate to catalog"""
        try:
            self.logger.info("Navigating to product catalog ->")
            
            await self.page.wait_for_selector(SELECTORS["catalog_button"])
            await self.page.click("button.p-button.p-button-tertiary.catalog-button")
            self.logger.debug("main catalog opened ...")

            await self.page.wait_for_selector(SELECTORS["alcohol_category"])
            await self.page.click(SELECTORS["alcohol_category"])
            self.logger.debug("sub-catalog opened ...")

            await self.page.wait_for_selector("div[class='product-categories-chips ng-star-inserted']")
            await self.page.click(SELECTORS["beer_category"])
            self.logger.info("<- successfully navigated to product catalog")

        except Exception as e:
            self.logger.error(f"Catalog navigation error: {str(e)}", exc_info=True)
            raise

    async def _get_element_text(self, parent, selector: str) -> str:
        """Safely get element text with timeout"""
        try:
            element = await parent.query_selector(selector)
            if element and await element.is_visible():
                return await element.inner_text()
            return "Not specified"
        except Exception as e:
            self.logger.warning(f"Error getting element text: {str(e)}")
            return "Error getting text"

    async def _get_attribute(self, parent, selector: str, attr: str) -> Optional[str]:
        """Safely get element attribute"""
        element = await parent.query_selector(selector)
        if element and await element.is_visible():
            return await element.get_attribute(attr)
        return None

    async def __number_of_pages(self) -> int:
        """Get total number of product pages"""
        try:
            await self.page.wait_for_selector(SELECTORS["pagination"])
            pagination = await self.page.query_selector(SELECTORS["pagination_list"])
            if not pagination:
                return 1
                
            last_page = await pagination.query_selector("li:last-child")
            return int(await last_page.inner_text()) if last_page else 1
        except Exception as e:
            print(f"Error getting page count: {e}")
            return 1

    async def __scroll_page(self) -> None:
        await self.page.wait_for_selector(SELECTORS["product_grid"])
        await self.page.evaluate("""() => {
                window.scrollTo({
                    top: document.body.scrollHeight / 2,
                    behavior: 'smooth'
                });
            }""")

    async def __get_beer_info(self, number_of_pages: int) -> List[Dict]:
        """Parsing products in catalog"""
        catalog = []
        self.logger.info(f"Starting page parsing ->")
        
        for i in range(1, number_of_pages + 1):
            try:
                self.logger.debug(f"processing page {i}/{number_of_pages} ...")
                
                await self.page.wait_for_selector(SELECTORS["product_grid"], state="attached")
                await self.__scroll_page()
                
                items = await self.page.query_selector_all(SELECTORS["product_item"])
                self.logger.debug(f"found {len(items)} products on page {i} ...")

                page_items = []
                for idx, item in enumerate(items, 1):
                    try:
                        raw_name = await self._get_element_text(item, SELECTORS["product_name"])
                        product_type, cleaned_name, color_type, is_alcoholic, filtering_type, pasteurization_type, alcohol_percentage, sweetness_type, packaging_type, clarification_type = process_product_name(raw_name)
                        
                        product = Product(
                            name=cleaned_name,
                            type=product_type,
                            color=color_type,
                            is_alcoholic=is_alcoholic,
                            filtering=filtering_type,
                            pasteurization=pasteurization_type,
                            alcohol_percentage=alcohol_percentage,
                            sweetness=sweetness_type,
                            packaging=packaging_type,
                            clarification=clarification_type,
                            volume=await self._get_element_text(item, SELECTORS["product_volume"]),
                            price=self.__clean_value(await self._get_element_text(item, SELECTORS["product_price"])),
                            image=await self._get_attribute(item, SELECTORS["product_image"], "src")
                        )
                        
                        page_items.append(product.to_dict())
                        
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
            self.logger.info(f"Starting parser for address: {self.address}")
            
            async with async_playwright() as p:
                self.logger.debug("Playwright context created")
                browser_settings = BROWSER_SETTINGS.copy()
                browser_settings["args"].append(f"--user-agent={USER_AGENT}")
                
                async with await p.chromium.launch(**browser_settings) as browser:
                    self.logger.debug("Browser launched")
                    async with await browser.new_context(**CONTEXT_SETTINGS) as context:
                        self.logger.debug("Browser context created")
                        await context.route("**/*", lambda route: route.continue_() if not route.request.resource_type == "geolocation" else route.abort())
                        
                        self.page = await context.new_page()
                        self.logger.debug("New page created")
                        await self.page.goto(BASE_URL, timeout=TIMEOUT)
                        self.logger.info("Main page loaded")

                        await self.__store_selection()
                        await self.__go_to_beer_catalog()

                        total_pages = await self.__number_of_pages()
                        self.logger.info(f"Total pages to parse: {total_pages}")

                        catalog = await self.__get_beer_info(total_pages)

                        elapsed_seconds = time.perf_counter() - self.start_time
                        hours, remainder = divmod(elapsed_seconds, 3600)
                        minutes, seconds = divmod(remainder, 60)
                        self.logger.info(
                            f"Parser finished. Execution time: "
                            f"{int(minutes)} min {seconds:.1f} sec"
                        )
                        return catalog

        except Exception as e:
            self.logger.critical(f"Critical error: {str(e)}", exc_info=True)
            return None