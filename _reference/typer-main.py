import typer

app = typer.Typer()

@app.command()
def hello(first: str,last: str):
    fullname = f"{first} {last}"
    typer.echo(f"Hello {fullname}")

@app.command()
def goodbye(first: str,last: str, formal: bool = False):
    fullname = f"{first} {last}"
    if formal:
        typer.echo(f"Goodbye Ms. {fullname}. Have a good day.")
    else:
        typer.echo(f"Bye {fullname}!")


if __name__ == "__main__":
   app()
