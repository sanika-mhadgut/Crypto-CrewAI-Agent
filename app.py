import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langfuse.decorators import observe
from langfuse_config import langfuse
from crewai_tools.tools import SerperDevTool
from tools.scraper_tool import ScrapeWebsiteTool

load_dotenv()

# Initialize tools
serper = SerperDevTool()
scraper = ScrapeWebsiteTool()
serper_api_key = os.getenv("SERPER_API_KEY")


@observe()
def run_crypto_agent(user_query: str, user_id: str = "anonymous"):
    """
    Main CrewAI crypto agent logic.
    Searches, scrapes, and summarizes crypto-related information.
    """

    # Step 1: Search the web
    search_results = serper.run(query=user_query)
    print("DEBUG: Serper response:", search_results)

    # Step 2: Extract useful links safely
    links = []
    if isinstance(search_results, dict):
        if "organic" in search_results:
            links = [item.get("link", "") for item in search_results["organic"] if "link" in item]
        elif "results" in search_results:
            links = [item.get("link", "") for item in search_results["results"] if "link" in item]
        elif "links" in search_results:
            links = search_results["links"]
        else:
            print("⚠️ No recognized keys in Serper response.")
    else:
        print("⚠️ Unexpected response type:", type(search_results))

    if not links:
        print("⚠️ No links found. Try another query or check your SERPER_API_KEY.")
        return "No relevant links found."

    reasoning = f"Found relevant links for '{user_query}': {links}"

    # Step 3: Scrape website contents manually before passing to the agent
    scraped_data = ""
    for link in links[:5]:
        try:
            scraped_content = scraper.run(link)
            scraped_data += f"--- {link} ---\n{scraped_content}\n\n"
        except Exception as e:
            print(f"Error scraping {link}: {e}")

    if not scraped_data.strip():
        scraped_data = "No readable content was scraped from the selected links."

    # Step 4: Define CrewAI Agent
    crypto_agent = Agent(
        role="Crypto Market Analyst",
        goal="Analyze and summarize current cryptocurrency market trends accurately.",
        backstory="An expert analyst specialized in blockchain, DeFi, and crypto asset movements.",
        tools=[serper, scraper],
        verbose=True,
        allow_delegation=False,
    )

    # Step 5: Create and run Task
    task = Task(
        description=f"User asked: '{user_query}'. "
                    f"Analyze and summarize insights from the scraped data below:\n\n{scraped_data[:2000]}",
        agent=crypto_agent,
        expected_output="A concise, insightful, and up-to-date crypto market summary.",
    )

    crew = Crew(agents=[crypto_agent], tasks=[task])
    result = crew.kickoff()

    # Step 6: Log with Langfuse
    langfuse.trace(
        name="CryptoAgentSession",
        user_id=user_id,
        input=user_query,
        output=result,
        metadata={"search_links": links, "reasoning": reasoning},
    )

    # Extract final text safely from CrewAI or Langfuse-traced output
    if hasattr(result, "raw"):
        return result.raw
    elif isinstance(result, dict) and "raw" in result:
        return result["raw"]
    else:
        return str(result)



if __name__ == "__main__":
    print("🚀 CryptoCoins CrewAI Agent Ready!")
    while True:
        query = input("\n💬 Ask me about any crypto coin or market movement:\n> ")
        response = run_crypto_agent(query, user_id="test_user")
        print("\n🤖 Agent Response:\n", response)
