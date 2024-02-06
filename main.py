import openai
import config
import typer
from rich import print
from rich.table import Table
from openai import ChatCompletion

def __prompt() -> str:
    prompt = typer.prompt("\nHow can I assist you today?")

    if prompt == "-exit":
        exit = typer.confirm("Do you want finish the app execution?")
        if exit:
            print("Bye!👋")
            raise typer.Abort()

        return __prompt()

    return prompt

def main():

    # Key
    openai.api_key = config.api_key

    print("💬 [bold green]Welcome to your Smart Chat[/bold green]")
    table = Table("Commands", "Description")
    table.add_row("-exit", "Go out of the chat")
    table.add_row("-new", "Create a new chat")

    print(table)

    # Assistant context
    context = {"role": "system",
               "content": "You are the most useful and intelligent assistant in the universe. I would be glad if you could help me with my requests in the most accurate way. Please act as an expert software developer, giving technical answers focused on writing robust and clean code, but assume that I am a mid-level developer, so I'm expecting technical answers."}
    messages = [context]

    while True:

        content = __prompt()

        if content == "-new":
            print("💬 [bold green]New chat[/bold green]")
            messages = [context]
        elif content == "-exit":
            break
        else:
            # Add the user's message to the messages list
            messages.append({"role": "user", "content": content})

            # Generate a response from the model
            response = ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

            # Add the model's message to the messages list
            messages.append({"role": "assistant", "content": response['choices'][0]['message']['content']})

            # Print the model's message
            print("💬 [bold green]Assistant[/bold green]:", response['choices'][0]['message']['content'])


if __name__ == "__main__":
    typer.run(main)
