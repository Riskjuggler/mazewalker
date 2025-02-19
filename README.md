# aimazewalker
This project is a Proof of Concept to demonstrate my learning journey around agentic AI.

**Objective** 

During my senior year of High School I was spending most of my free time in the computer lab.   When my Pyschology class assignment came up
I decided to try to write a program that could act like a mouse learning to get through a maze.   This was 1986 so back then AI was a horror 
story or sci fi dream (see "Tron" or "Wargames").   I struggled for quite a while and got stuck because I couldn't get the sensing to work right
so the mouse kept running through the walls but it did decide and remember just fine.   Since I had run out of time, Chris Nack and I worked out
that we could connect two of the TRS 80 model III's using an cable.  We edited an early program for chatting (think unix's talk) so each user's 
response would come up after the other resulting in essentially the same experience as we get from any GPT with a chat interface today.   He sat 
on the other side while I gave my talk on my side to explain AI to my Pysch class while chatting with him (the AI).   The class was amazed until
I let them in on the truth.

Anyway, this is v2 of the mouse program I wrote in high school but using python and OpenAI to create the maze and decide which direction to go.   
FWIW, yes, I know I could have automated the decisions so this isn't exactly what most people mean when they say agentic AI but this is my first 
attempt at integrating LLMs into code so it was the next step on my AI Engineering journey and I learned a lot along the way.

**Usage**  

    *`mazewalker.py <debug>`*
    debug flag will show the decision prompts and response details

**Install Instructions**

    1. Install python if not already
    2. Rename example.env to .env and edit to add your own OpenAI API key
    3. If you don't have them installed yet, use pip or your preferred module installer to install dotenv, OpenAI, etc.

**Known issues**

- Sometimes it will find the end before it's actually the end and sometimes it won't recognize it as at the end - LLM hallucinations
- The prompt that creates the maze took several hours of trial and error to get to this point.   It still doesn't always produce a maze that can be completed.  The program will stop once the mouse gets trapped so no worries about endless loops or anything.
- For some reason I didn't take the time yet to sort out, occasionally it will generate a maze that is of odd lengths so the player position step will error out.   Just re-start.

**Learnings** 

- It's possible to over design as you're working through where and how you can integrate AI into your workflows.   Check out designdocs\Mouse_in_maze_SOP_Architecture.pdf for my initial analysis of the process and key decision points as I quested for where to get benefit from an AI planner.
- Exerimenting with LLMs can be expensive!  I used my Prompt Engineering helper GPT (https://chatgpt.com/g/g-675b2943ed54819181c72951991af3e8-there-is-a-prompt-for-that) to work through most of the deeper refinements but the multiple tests I ran to get the code where I wanted still added up quick to $2.01 USD.   
- Be sure to ask ChatGPT for alternative but still effective and efficient prompts to help reduce your prompt cost.  I have to imagine after all my trials that part of my challenge was LLM capability but the highest obstacle was just pure word choice.   Precision and efficiency are key to lean and effective prompting.  Everyone says so, but for a Philosophy major trained in college on old english and english translations of German and French philosophy tomes it's super easy to get over wordy.
- Thank you Arash for the pro-tip about the Heuristics weights in the prompt shortcut!!   I wouldn't have achieved a working maze creator without it!! Plain english wasn't enough for ChatGPT to figure it out with high accuracy.
- I'm glad I was also reading chapter 3: Evaluation Methodology and chapter 4: Evaluate AI Systems from Chip Huyen's AI Engineering: Building Applications with Foundational Models - (O'Reilly) Copyright 2025 Developer Experience Advisory LLC, 978-1-098-16630-4   This helped me overcome the challenge that almost stopped me again (the maze wouldn't draw right).
- I still have a lot to learn to get the most out of python without help.  That free Github Copilot was super helpful when I got stuck a few times but I can see how some who might not be able to clearly describe their product feature requirements might not get much out of it!

**Future improvement / learning ideas**

- Consider other LLMs to improve effectiveness and reduce cost
- Define a proper evaluation plan and execute to assure my LLM choice is least cost and optimally fit for purpose to work through those details on paper 
