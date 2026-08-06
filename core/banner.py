from rich.console import Console

console = Console()


def show_banner():
    console.print(
        """
[bold green]
==================================================
███████╗███████╗ █████╗ ██╗   ██╗
██╔════╝██╔════╝██╔══██╗██║   ██║
█████╗  ███████╗███████║██║   ██║
██╔══╝  ╚════██║██╔══██║██║   ██║
███████╗███████║██║  ██║╚██████╔╝
╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝
==================================================
[/bold green]
        """
    )

    console.print("[bold cyan]Autonomous Meme Coin Hunter[/bold cyan]")
    console.print("[yellow]Version 0.1.0 - Genesis[/yellow]\n")