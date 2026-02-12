# Kitchen MCP

Kitchen MCP is a backend server designed to connect a large language model like Gemini Pro to a "source of truth" for a kitchen assistant application. It uses the `FastMCP` framework to expose a set of tools that allow the AI to interact with a Supabase database containing recipes, ingredients, and cost information.

This bridge enables a conversational AI to accurately answer questions, manage kitchen inventory, calculate recipe costs, and scale production plans based on structured, real-time data.

## Features

The server exposes the following tools for the AI to use:

*   **`check_connection`**: Verifies the connection to the Supabase database.
*   **`add_ingredient`**: Adds a new ingredient to the kitchen catalog.
*   **`update_ingredient_price`**: Updates the cost of an existing ingredient.
*   **`create_full_recipe`**: Creates a new recipe with a list of ingredients.
*   **`scale_recipe`**: Calculates the total ingredients and cost for multiple servings of a recipe.
*   **`calculate_recipe_cost`**: Calculates the total production cost for a single recipe.

## Setting Up

Follow these steps to get the server running locally.

### 1. Prerequisites

*   **Python 3.13** or newer.
*   **uv**: This project uses `uv` for package management. You can install it with `pip install uv`.
*   **Supabase Credentials**: You must have access to a Supabase project. The server requires a `SUPABASE_URL` and a `SUPABASE_SERVICE_ROLE_KEY`. Consult with your project administrator to obtain these.

### 2. Installation

First, clone the repository to your local machine:

```sh
git clone https://github.com/javieroc/kitchen-mcp.git
cd kitchen-mcp
```

Create a virtual environment and install the dependencies:

```sh
uv sync
source .venv/bin/activate
```

### 3. Configuration

The server is configured using environment variables. Create a `.env` file in the root of the project:

```sh
touch .env
```

Add your Supabase credentials to this file. **Do not commit this file to version control.**

```env
# .env
SUPABASE_URL="your-supabase-project-url"
SUPABASE_SERVICE_ROLE_KEY="your-supabase-service-role-key"
```

## Running the Server

Once you have configured your environment, you can start the server with the following command:

```sh
uv run fastapi dev app/main.py
```

The server will start on `http://127.0.0.1:8000` by default.


### 4. VS Code Integration

To use these tools directly within GitHub Copilot Chat or the Gemini extension in VS Code:

Ensure the server is running `(uv run fastapi dev app/main.py)`.

In your project root, create a directory named .vscode if it doesn't exist.

Create a file named mcp.json inside the .vscode folder:

```JSON
{
	"servers": {
		"kitchen-orchestator": {
			"url": "http://127.0.0.1:8000/mcp ",
			"type": "http"
		}
	},
	"inputs": []
}
```

Open the Copilot Chat panel.

Click the Tools (wrench icon) and ensure kitchen-orchestrator is enabled.

You can now ask questions like: "How much does it cost to make a Margherita pizza?"
