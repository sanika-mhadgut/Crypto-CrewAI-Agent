import requests
from bs4 import BeautifulSoup

# ✅ Handle version compatibility across crewai-tools versions
try:
    from crewai_tools.base_tool import BaseTool  # for most recent versions
except ImportError:
    try:
        from crewai_tools.tools.base_tool import BaseTool  # fallback for older versions
    except ImportError:
        from crewai.tools.base_tool import BaseTool  # final fallback


class ScrapeWebsiteTool(BaseTool):
    name: str = "Read website content"
    description: str = "Scrapes and summarizes website textual data."

    def _run(self, url: str = None) -> str:
        """Actual scraping logic used by CrewAI"""
        try:
            if not url:
                return "⚠️ Website URL must be provided."

            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/117.0.0.0 Safari/537.36"
                )
            }

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = [p.get_text().strip() for p in soup.find_all("p")]
            text = " ".join(paragraphs)

            return text[:8000] if text else "⚠️ No readable text found."
        except Exception as e:
            return f"⚠️ Error scraping {url}: {e}"
