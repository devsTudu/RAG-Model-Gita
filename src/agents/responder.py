from phi.agent import Agent
from phi.model.google import Gemini 
from phi.tools.duckduckgo import DuckDuckGo
from phi.playground import Playground, serve_playground_app

from dotenv import load_dotenv
load_dotenv()

web_agent = Agent(
    name="Web Agent",
    model=Gemini(id="gemini-2.0-flash"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources and the tools provided"],
    show_tool_calls=True,
    markdown=True,
    monitoring=True,
)

app = Playground(agents=[ web_agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("responder:app", reload=True)