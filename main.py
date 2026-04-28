from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("gitlab-mcp")

load_dotenv(override=True)
def main():
    print("Hello from gitlab-mcp!")


if __name__ == "__main__":
    mcp.run(transport='stdio', main=main)
