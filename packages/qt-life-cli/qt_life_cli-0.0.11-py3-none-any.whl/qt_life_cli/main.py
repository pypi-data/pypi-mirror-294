import click
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.output import ColorDepth
from colorama import Fore, init
import asyncio
from typing import Callable

init(autoreset=True)

WELCOME_ART = f"""
{Fore.GREEN}
     ╔══════════════════════════════════════╗
     ║         QUANTUM LIFE TERMINAL        ║
     ╠══════════════════════════════════════╣
     ║ [1] INIT QUANTUM CORE                ║
     ║ [2] ADD QUANTUM PLUGIN               ║
     ║ [3] ABOUT QUANTUM LIFE               ║
     ║ [4] EXIT SYSTEM                      ║
     ╚══════════════════════════════════════╝
{Fore.LIGHTGREEN_EX}
   > ENTER 'help' FOR COMMAND LIST
   > 'exit' TO DISENGAGE QUANTUM FIELD
"""

STYLE = Style.from_dict({
    'prompt': '#00ff00 bold',
    'command': '#00ff00',
    'description': '#008000',
})

class AnimatedPrompt:
    def __init__(self):
        self.animation = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
        self.index = 0

    def get_prompt(self) -> FormattedText:
        symbol = self.animation[self.index]
        self.index = (self.index + 1) % len(self.animation)
        return FormattedText([
            ('class:animation', f"{symbol} "),
            ('class:prompt', 'quantum>'),
            ('', ' ')
        ])

def print_welcome() -> None:
    """Print the welcome message and art."""
    click.echo(WELCOME_ART)

def print_help() -> None:
    """Print the help message with available commands."""
    click.echo(f"{Fore.YELLOW}Available hacks:")
    click.echo(f"{Fore.GREEN}help{Fore.WHITE}  - Access the Quantum Life Guide")
    click.echo(f"{Fore.GREEN}init{Fore.WHITE}  - Initiate Quantum Core")
    click.echo(f"{Fore.GREEN}add{Fore.WHITE}   - Add Quantum Plugin")
    click.echo(f"{Fore.GREEN}about{Fore.WHITE} - About Quantum Life CLI")
    click.echo(f"{Fore.GREEN}exit{Fore.WHITE}  - EXIT")

def init_quantum_core() -> None:
    """Initialize the Quantum Core."""
    click.echo(f"{Fore.GREEN}Initializing Quantum Core... Done.")

def add_quantum_plugin() -> None:
    """Add a Quantum Plugin."""
    click.echo(f"{Fore.GREEN}Add Quantum Plugin... Done.")

def about_quantum_life() -> None:
    """Display information about Quantum Life CLI."""
    click.echo(f"{Fore.GREEN}This is Quantum Life CLI")

def handle_command(command: str) -> bool:
    """
    Handle the user input command.
    
    :param command: The user input command
    :return: True if the CLI should continue, False if it should exit
    """
    command_handlers: dict[str, Callable[[], None]] = {
        'init': init_quantum_core,
        'help': print_help,
        'add': add_quantum_plugin,
        'about': about_quantum_life,
        '1': init_quantum_core,
        '2': add_quantum_plugin,
        '3': about_quantum_life,
    }

    if command in command_handlers:
        command_handlers[command]()
    elif command in ['exit', '4']:
        click.echo(f"{Fore.GREEN}Exiting System...")
        return False
    else:
        click.echo(f"{Fore.RED}Error 404: Quantum entanglement failed for command: {command}")
    return True

async def interactive_cli() -> None:
    """Run the interactive Quantum Life CLI."""
    animated_prompt = AnimatedPrompt()
    session = PromptSession(
        message=animated_prompt.get_prompt,
        style=STYLE,
        refresh_interval=0.1,
        color_depth=ColorDepth.DEPTH_24_BIT
    )
    print_welcome()
    
    while True:
        try:
            user_input = await session.prompt_async()
            user_input = user_input.strip().lower()
            if not handle_command(user_input):
                click.echo(f"{Fore.GREEN}Hi there, root? :)")
                break
        except KeyboardInterrupt:
            click.echo("\nExiting...")
            break
        except Exception as e:
            click.echo(f"An error occurred: {e}")
    
    click.echo("Quantum Life CLI session ended.")

@click.command()
def cli() -> None:
    """Entry point for the Quantum Life CLI."""
    asyncio.run(interactive_cli())

if __name__ == "__main__":
    cli()