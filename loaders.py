import logging
import asyncio
import nodriver as uc


class NoDriver:
    def __init__(self):
        self.result = None
        self.browser = None
        asyncio.get_event_loop().run_until_complete(self.initialize_browser())

    async def initialize_browser(self):
        self.browser = await uc.start(headless=True, browser_args=['--window-position=-2400,-2400'])

    async def async_getter(self, url):
        try:
            page = await self.browser.get(url)
            self.result = await page.get_content()
        except Exception as e:
            logging.error(f"An error occurred: {e}")

    def get_response(self, url):
        try:
            asyncio.get_event_loop().run_until_complete(self.async_getter(url))
        except Exception as e:
            logging.error(f"Failed to run async task: {e}")
        return self.result
