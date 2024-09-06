"""Abstract base class for Tiktok Captcha Solvers"""

import time
from abc import ABC, abstractmethod
from typing import Literal

from undetected_chromedriver import logging

class Solver(ABC):

    @property
    def captcha_wrappers(self) -> list[str]:
        return [
            ".captcha-disable-scroll"
        ]

    @property
    def rotate_selectors(self) -> list[str]:
        return [
            "[data-testid=whirl-inner-img]",
            "[data-testid=whirl-outer-img]"
        ]

    @property
    def puzzle_selectors(self) -> list[str]:
        return [
            "img.captcha_verify_img_slide"
        ]

    @property
    def shapes_selectors(self) -> list[str]:
        return [
            ".verify-captcha-submit-button" 
        ]

    @property
    def douyin_frame_selector(self) -> Literal["#captcha_container > iframe"]:
        return "#captcha_container > iframe"

    def solve_captcha_if_present(self, captcha_detect_timeout: int = 15, retries: int = 3) -> None:
        """Solves any captcha that is present, if one is detected

        Args:
            captcha_detect_timeout: return if no captcha is detected in this many seconds
            retries: number of times to retry captcha
        """
        for _ in range(retries):
            if not self.captcha_is_present(captcha_detect_timeout):
                logging.debug("Captcha is not present")
                return
            if self.page_is_douyin():
                logging.debug("Solving douyin puzzle")
                try:
                    self.solve_douyin_puzzle()
                except ValueError:
                    logging.debug("Douyin puzzle was not ready, trying again in 5 seconds")
            else:
                match self.identify_captcha():
                    case "puzzle": 
                        logging.debug("Detected puzzle")
                        self.solve_puzzle()
                    case "rotate": 
                        logging.debug("Detected rotate")
                        self.solve_rotate()
                    case "shapes": 
                        logging.debug("Detected shapes")
                        self.solve_shapes()
                    case "icon":
                        logging.debug("Detected icon")
                        self.solve_icon()
            if self.captcha_is_not_present(timeout=5):
                return
            else:
                time.sleep(5)

    @abstractmethod
    def captcha_is_present(self, timeout: int = 15) -> bool:
        pass

    @abstractmethod
    def captcha_is_not_present(self, timeout: int = 15) -> bool:
        pass

    @abstractmethod
    def identify_captcha(self) -> Literal["puzzle", "shapes", "rotate", "icon"]:
        pass

    @abstractmethod
    def page_is_douyin(self) -> bool:
        pass

    @abstractmethod
    def solve_shapes(self) -> None:
        pass

    @abstractmethod
    def solve_rotate(self) -> None:
        pass

    @abstractmethod
    def solve_puzzle(self) -> None:
        pass

    @abstractmethod
    def solve_icon(self) -> None:
        pass

    @abstractmethod
    def solve_douyin_puzzle(self) -> None:
        pass

