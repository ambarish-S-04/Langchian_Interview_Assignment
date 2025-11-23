import os
import json
import click
from pathlib import Path
from dotenv import load_dotenv
from src.embeddings import compute_embeddings
from src.query import get_character_info
from src.utils import ensure_directory_exists, validate_character_name, format_character_info

# Load environment variables from api.env file
load_dotenv('api.env')

def check_data_directory():
    data_dir = Path("Data")
    if not data_dir.exists():
        click.echo(f"Error: Data directory '{data_dir}' not found.")
        click.echo(f"Please create it and add your .txt story files.")
        return False
    return True

@click.group()
def cli():
    """CLI for story character information extraction."""
    pass

@cli.command(name='compute-embeddings')
def compute_embeddings_cmd():
    """Compute and store embeddings for all story files."""
    try:
        if not check_data_directory():
            return
            
        click.echo("Computing embeddings for story files...")
        compute_embeddings()
        click.echo("Embeddings computed and stored successfully!")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

@cli.command(name='get-character-info')
@click.argument('character_name')
def get_character_info_cmd(character_name: str):
    """Get information about a character from the stories."""
    try:
        if not validate_character_name(character_name):
            click.echo("Error: Invalid character name.")
            return
            
        if not os.getenv("MISTRAL_API_KEY"):
            click.echo("Error: MISTRAL_API_KEY not found in api.env file.")
            return
            
        click.echo(f"Searching for information about '{character_name}'...")
        result = get_character_info(character_name)
        
        if "error" in result:
            click.echo(f"Error: {result['error']}")
        else:
            click.echo("\n" + "=" * 50)
            click.echo("Character Information:")
            click.echo("=" * 50)
            click.echo(format_character_info(result))
            click.echo("\nRaw JSON Output:")
            click.echo("-" * 50)
            click.echo(json.dumps(result, indent=2))
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    cli()