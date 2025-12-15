from mcp.server.fastmcp import FastMCP
import os

# 1. Initialize the Server
mcp = FastMCP("My Local Explorer")

# Define a safe folder to explore (Change this path to a real folder on your PC!)
TARGET_FOLDER = "./test_notes" 

# 2. Define a Tool (Action)
# The docstring is CRITICAL. The AI uses it to understand what the tool does.
@mcp.tool()
def list_files() -> str:
    """Lists all files in the target folder."""
    try:
        files = os.listdir(TARGET_FOLDER)
        return "\n".join(files)
    except Exception as e:
        return f"Error: {str(e)}"

# 3. Define another Tool
@mcp.tool()
def read_file(filename: str) -> str:
    """Reads the content of a specific file."""
    path = os.path.join(TARGET_FOLDER, filename)
    
    # Security Check (Sandboxing)
    if not os.path.abspath(path).startswith(os.path.abspath(TARGET_FOLDER)):
        return "Access Denied: You can only read files in the target folder."
        
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # This starts the server using 'stdio' transport (Standard Input/Output)
    mcp.run()