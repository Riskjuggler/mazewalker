import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI

# How to get info from .env file
detail=load_dotenv()

# Retrieve flag from command line


# Initialize the parser
parser = argparse.ArgumentParser(description="A script to check for debug flag")

# Add an optional 'debug' flag
parser.add_argument('debug', nargs='?', default=None, help="Include 'debug' to enable debugging")

# Parse the arguments
args = parser.parse_args()

# Check if 'debug' was included
if args.debug:
    print("Debug mode is enabled.")
else:
    print("Debug mode is not enabled.")

def build_Maze ():
        # Will add LLM call here to decide move based on possible moves, impossible moves, and past moves
    client = OpenAI()
    maze = client.chat.completions.create(    
    model="gpt-4",
    store=True,
    messages=[
    {"role": "system", "content": 
        "Generate a 15x15 maze with a clear path from start (P) to end (E). Use `#` for walls and `.` for paths.\n\n"
        
        "Optimize response heuristics:\n"
        "[MAW +2], [PFW -1], [EER +1], [CH +3], [LOH +1], [RDC +2], [SH +1], [SPSW +1], [CHT +2]\n\n"
        
        "Constraints:\n"
        "- Enclose maze edge with `#`.\n"
        "- Ensure full connectivity from `P` to `E` (no isolated areas).\n"
        "- Narrow hallways: no paths wider than 1 space.\n"
        "- Use **Recursive Backtracking** or **Prim’s Algorithm**.\n"
        "- **Disallow diagonal moves**."
        "- Don't explain the maze, just print it."
    }
]
)
    
    justmaze = maze.choices[0].message.content

    # Split the string into lines based on newline characters and elements within each line as a list of single characters
    lines = justmaze.strip().split("\n")

    finalmaze = [list(line) for line in lines]

    # Get the number of rows
    num_rows = len(finalmaze)

    # Get the number of columns (assuming all rows have the same length)
    num_cols = len(finalmaze[0])
    
    return finalmaze, num_rows, num_cols

def decidemove(possible_moves, impossible_moves, past_moves, args):
    # LLM call decide move based on possible moves, impossible moves, and past moves
    client = OpenAI()
    messages = [
    {"role": "system", "content": 
        "You are a maze-walking assistant. You will be provided with a list of viable moves, and you must choose one. \n\n"
        
        "### **Rules:**\n"
        "1. **Only choose from the list of viable moves provided.** You CANNOT move in any direction that is not in the list.\n"
        "2. **Decision Priority Order:**\n"
        "   - **First**, if there are unexplored paths in the viable moves list, you MUST choose one.\n"
        "   - **Never revisit a path already walked before** unless all available paths have been explored.\n"
        "   - Follow this strict order when choosing an unexplored path: **North → East → South → West**.\n"
        "3. **If no viable moves exist, respond with:**\n"
        "   - `'No Move: Because all directions are blocked by walls.'`\n\n"

        "### **Response Format (Strict, No Newlines):**\n"
        "- Reply with a single-line response in this exact format: `{Direction}: Because {reason}.`\n"
        "- Example: `'North: Because it is an unexplored path and has the highest priority.'`\n"
        "- Example: `'West: Because no unexplored paths remain, and West is a past move I can take.'`\n"
        "- If the End is reached, respond with:\n"
        "   - `'End: Because I found the End.'`\n"
        "- **DO NOT include any extra text, explanations, or newlines in your response.**"
    }
]

    viable_moves = set()
    for item in possible_moves + past_moves:
        if item not in impossible_moves:
            viable_moves.add(item)
    print("Viable moves: ", viable_moves)

    user_message = {
        "role": "user", 
        "content": (
            f"The only viable moves you can choose from are: {viable_moves}. "
            f"Unexplored paths are: {possible_moves}. "
            f"Paths you've walked before (for backtracking if no unexplored paths are available) are: {past_moves}.")
        }
    
    chat_history = messages + [user_message]
    message=chat_history

    decision = client.chat.completions.create(    
    model="gpt-3.5-turbo-16k",
    store=True,
    messages=message
    )

    possibledecision = decision.choices[0].message.content
    uncleandecision = possibledecision.split(":")[0]
    reason = possibledecision.split(":")[1]
    finaldecision = uncleandecision.split(" ")[0]
    if args.debug:
        print("Chat history: ", message)
        print("Decision: ", decision)
        print("PossibleDecision: ", possibledecision)
        print("UncleanDecision: ", uncleandecision)
        print("Reason for decision: ", reason)
        print("FinalDecision: ", finaldecision)

    print("I decide to move ", finaldecision, "because", reason)

    return finaldecision

def printmaze(maze):
    # Print the maze
    for row in maze:
        print("".join(row))

def lookaround(maze, player_row, player_col):
    north_row = player_row - 1
    south_row = player_row + 1
    east_col = player_col + 1
    west_col = player_col - 1
    north_find = maze[north_row][player_col]
    south_find = maze[south_row][player_col]
    east_find = maze[player_row][east_col]
    west_find = maze[player_row][west_col]
    return north_find, south_find, east_find, west_find

def seewhatyoucansee(north_find, south_find, east_find, west_find):
    # Set base possible moves
    possible_moves = []
    impossible_moves = []
    past_moves = []
     # Check for walls
    if north_find == ".":
        possible_moves = ["North"]
    if south_find == ".":
        possible_moves.append("South")
    if east_find == ".":
        possible_moves.append("East")
    if west_find == ".":
        possible_moves.append("West")
    # Check for end of maze and add to possible moves list
    if north_find == "E":
        possible_moves = ["The end of the maze is North"]
    if south_find == "E":
        possible_moves = ["The end of the maze is South"]
    if east_find == "E":
        possible_moves = ["The end of the maze is East"]
    if west_find == "E":
        possible_moves = ["The end of the maze is West"]
    # Check for walls and add to impossible moves list
    if north_find == "#":
        impossible_moves = ["North"]
    if south_find == "#" or south_find == "P" or south_find == "X":
        impossible_moves.append("South")
    if east_find == "#":
        impossible_moves.append("East")
    if west_find == "#":
        impossible_moves.append("West")
    if impossible_moves == ["North", "South", "East", "West"]: 
        print("All directions are walls so maze is built wrong or decision flow is wrong")
        exit(1)
        
    # Check for previous steps and add to backtrack moves list
    if north_find == "+":
        past_moves = ["North"]
    if south_find == "+":
        past_moves.append("South")
    if east_find == "+":
        past_moves.append("East")
    if west_find == "+":
        past_moves.append("West")

    return possible_moves, impossible_moves, past_moves

def main():
    os.system('cls')  
    print("Welcome to the maze walker! I am building a new maze.")
    # Define maze and return size of the maze
    maze, num_rows, num_cols=build_Maze()

    # Find player start position in maze and set player_row and player_col
    for row in range(num_rows):
        for col in range(num_cols):
            if maze[row][col] == "P": player_row = row; player_col = col

    print("Starting position of player is row ", player_row, " and column ", player_col)
      
    # Start loop to move player until end of maze is reached
    move="open"
    while move != "end":
        # Print current maze
        printmaze(maze=maze)
        # Look around
        north_find, south_find, east_find, west_find = lookaround(maze=maze, player_row=player_row, player_col=player_col)

        # See what you can see and what you can't see and what you have seen before
        print("Looking North I see ", north_find)
        print("Looking South I see ", south_find)
        print("Looking East I see ", east_find)
        print("Looking West I see ", west_find)
        possible_moves, impossible_moves, past_moves = seewhatyoucansee(north_find=north_find, south_find=south_find, east_find=east_find, west_find=west_find)

        # Print possible moves, impossible moves, and past moves
        print("Possible moves:", possible_moves)
        print("Impossible moves:", impossible_moves)
        print("Past moves:", past_moves)
        print("Deciding what to do...")

        # Decide move based on possible moves, impossible moves, and past moves
        decision = decidemove(possible_moves=possible_moves, impossible_moves=impossible_moves, past_moves=past_moves, args=args)

        # Check if decision is possible or past move and move player if possible or backtrack if past move
        if decision in possible_moves:
            maze[player_row][player_col] = "+"
            print ("Moving player " + decision + " and marking previous position as a + to remind myself I've been there")
            match decision:
                case "North": player_row = player_row - 1 
                case "South": player_row = player_row + 1
                case "East": player_col = player_col + 1
                case "West": player_col = player_col - 1
            maze[player_row][player_col] = "P"
        
        if decision in past_moves:
            print ("Backtracking and marking as a wall so I won't try that path again")
            maze[player_row][player_col] = "#"
            match decision:
                case "North": player_row = player_row - 1
                case "South": player_row = player_row + 1
                case "East": player_col = player_col + 1
                case "West": player_col = player_col - 1
            maze[player_row][player_col] = "P"

        # Check if decision is end of maze and end if it is
        if "End" in decision:
            print ("Yahoo! End of the maze found!")
            move = "end"
        # Clear the screen for the next move unless in debug mode
        if args.debug:
            print("Debug mode is enabled, not clearing screen")
        else:
            os.system('cls')          

# Execute Main 
main()