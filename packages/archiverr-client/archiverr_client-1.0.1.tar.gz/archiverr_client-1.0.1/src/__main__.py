import click
import yaml
import requests
import pandas as pd
from pathlib import Path
from os import remove
from os.path import isdir, abspath, join
from urllib.parse import urlencode
from .Config import Config
from .Utilities import Utilities
from tabulate import tabulate
# Charger la configuration
config = Config()

@click.group()
def cli():
    """Archiverr CLI: 
    A command-line tool for managing files archives."""
    pass


@cli.command("config")
@click.argument('section', type=str, required=False)
@click.argument('key', type=str, required=False)
@click.argument('value', required=False)
def get_set(section, key, value):
    """Show or set configuration values."""
    config = Config()

    if value is None:
        # Si aucune valeur n'est fournie, afficher la configuration actuelle
        if section is None or key is None:
            click.echo("Configuration actuelle :")
            click.echo(yaml.safe_dump(config.config_data, default_flow_style=False))
            exit(0)
        current_value = config.get(section, key)
        if current_value is None:
            click.echo(f"La clé '{key}' dans la section '{section}' n'existe pas.")
        else:
            click.echo(f"{section}.{key} = {current_value}")
    else:
        # Mettre à jour la configuration avec la nouvelle valeur
        config.set(section, key, value)
        click.echo(f"La clé '{key}' dans la section '{section}' a été mise à jour avec la valeur '{value}'.")

@cli.command("login")
@click.argument('username')
@click.argument('password')
def login(username, password):
    """Authenticate and retrieve a Bearer token."""
    url_auth = config.get('server', 'url') + '/auth'
    data = {'username': username, 'password': password}
    

    response = requests.post(url_auth, json=data)
    if not Utilities.handle_response(response):
        return
    
    token = response.json().get('token')
    if token:
        config.set('auth', 'token', token)
        click.echo("Login successful. Token saved.")
    else:
        click.echo("Login failed. No token received.", err=True)

#region Vault_Commands
@cli.command("new")
@click.argument('vault_name')
def vault_new(vault_name):
    """Create a new vault.

    VAULT_NAME: The name of the vault to create.
    """
    url_vault = config.get('server', 'url') + '/vaults'
    token = config.get('auth', 'token', None)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}' 
    }
    data = {'name': vault_name, 'description': 'Vault created by the CLI'}
    

    response = requests.post(url_vault, json=data, headers=headers)
    if not Utilities.handle_response(response):
        return
    click.echo(f'{response.json().get("message")}')
    vault_id = response.json()['id']
    config.set('vault', 'id_default', vault_id)
        


@cli.command("list")
@click.option('--id', default=None, help='Specify the ID of the vault to list.')
def vault_list(id):
    """List all vaults."""
    if id:
        url_vault = config.get('server', 'url') + f'/vaults/{id}'
        token = config.get('auth', 'token', None)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        response = requests.get(url_vault, headers=headers)
        if not Utilities.handle_response(response):
            return

        vault = response.json()

        click.echo(f'Vault {vault["name"]} details:')
        click.echo(f'ID: {vault["id"]}')
        click.echo(f'Description: {vault["description"]}')
        click.echo(f'Created at: {vault["created_at"]}')
        click.echo(f'Updated at: {vault["updated_at"]}')
    else:
        url_vault = config.get('server', 'url') + '/vaults'
        token = config.get('auth', 'token', None)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        response = requests.get(url_vault, headers=headers)
        if not Utilities.handle_response(response):
            return
        vaults = response.json()

        if vaults:
            click.echo('Vaults:')
            #Print the columns names
            click.echo('ID (Name)')
            for vault in vaults:
                # Afficher le nom du coffre et son id
                click.echo(f'{vault["id"]} ({vault["name"]})')

@cli.command("use")
@click.argument('vault_id')
def vault_use(vault_id):
    """Use a vault.

    VAULT_ID: The ID of the vault to use.
    """
    url_vault = config.get('server', 'url') + f'/vaults/{vault_id}/use'
    token = config.get('auth', 'token', None)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url_vault, headers=headers)
    if not Utilities.handle_response(response):
        return
    # Get the vault_id from the response to store in the config
    vault_id = response.json()['id']
    config.set('vault', 'id_default', vault_id)
    click.echo(f'{response.json().get("message")}')

@cli.command("update")
@click.argument('description')
def vault_update(description):
    """Update a vault.

    DESCRIPTION: The new description of the vault.
    """
    vault_id = config.get('vault', 'id_default')
    url_vault = config.get('server', 'url') + f'/vaults/{vault_id}'
    token = config.get('auth', 'token', None)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    data = {'description': description}
    response = requests.put(url_vault, json=data, headers=headers)
    if not Utilities.handle_response(response):
        return
    vault = response.json()
    click.echo(f'Vault {vault["name"]} details:')
    click.echo(f'ID: {vault["id"]}')
    click.echo(f'Description: {vault["description"]}')
    click.echo(f'Created at: {vault["created_at"]}')
    click.echo(f'Updated at: {vault["updated_at"]}')

@cli.command("delete")
@click.argument('vault_id')
def vault_delete(vault_id):
    """Delete a vault.

    VAULT_ID: The ID of the vault to delete.
    """
    url_vault = config.get('server', 'url') + f'/vaults/{vault_id}'
    token = config.get('auth', 'token', None)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.delete(url_vault, headers=headers)
    if not Utilities.handle_response(response):
        return

    click.echo(f'{response.json()}')
#endregion
 
@cli.command(name='import')
@click.argument('path', type=click.Path(exists=True))
def import_file(path):
    """Import a file or a directory into the archive."""
    
    is_compressed = bool(False)
    file_details = {}
    
    if isdir(path):
        # Zip the folder
        path, file_details = Utilities.zip_folder(path)
        is_compressed = True
        # Display the files in the zip
    else:
        # get the absolute path of the file
        path_abs = abspath(path)
        #folder = abspath(path) 
        #print("FOLDER: ", folder)
        #file_details['folder'] = {
        #    'path_abs': abspath(folder),
        #    'path_rel': folder,
        #    'date_modification': Utilities.get_date_modification(folder).isoformat(),
        #    'date_creation': Utilities.get_date_creation(folder).isoformat()
        #}
        
        file_details['file'] = {
            'path_abs': path_abs,
            'path_rel': path,
            'date_modification': Utilities.get_date_modification(path).isoformat(),
            'date_creation': Utilities.get_date_creation(path).isoformat()
        }
        
        print(file_details)

    
    # Prepare the data to be sent
    files = {'file': open(path, 'rb')}
    data = {
        'isCompressed': str(is_compressed),
        'fileDetails': str(file_details)
    }
    url_resources = config.get('server', 'url') + '/vaults/' + str(config.get('vault', 'id_default')) + '/archiveItemFile'
    token = config.get('auth', 'token', None)
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.post(url_resources, files=files, data=data, headers=headers)
    if not Utilities.handle_response(response):
        return
    click.echo(f'{response.json().get("message")}')
    if is_compressed:
        remove(path)

@cli.command()
@click.option('--per_page', default=10, help='Number of results per page.')
def search(per_page):
    """Search every file unique or not in the default vault.

    Options:
      --per_page   Specify the number of results per page.
    """
    
    mode_file = config.get('search','mode_file')
    mode_folder = config.get('search','mode_folder')
    # Construire les paramètres de requête
    params = {}
    current_mode = config.get('search', 'mode_default')
    # Pagination parameters
    page = 1
    params['page'] = page
    params['per_page'] = per_page
    # Construire l'URL avec les paramètres de requête
    url_vault = config.get('server', 'url') + f"/vaults/{config.get('vault', 'id_default')}/fileMetadata"

    if params:
        url_vault += '?' + urlencode(params)
        while True:
            token = config.get('auth', 'token', None)
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }
            # Faire la requête HTTP GET
            
            response = requests.get(url_vault, headers=headers)
            if not Utilities.handle_response(response):
                return
            if response.status_code == 203:
                click.echo(response.json().get('message'))
                config.set('search', 'mode_default', mode_folder)

                exit(0)
            data = response.json()
            
            if current_mode == mode_file:
                file_metadata = data.get('file_metadata', [])
                df = pd.DataFrame(file_metadata)
            elif current_mode == mode_folder:
                file_metadata = data.get('archive_item_folder', [])
                df = pd.DataFrame(file_metadata)
            else:
                file_metadata = data.get('file_metadata', [])
                df = pd.DataFrame(file_metadata)
            pagination = data.get('pagination', {})

            
            # Réordonner les colonnes pour que 'id' soit la première colonne
            if current_mode == mode_file:
                columns = ['id'] + ['file_name'] + ['extension'] + [col for col in df.columns if col != 'id' and col != 'file_name' and col != 'extension' and col != 'archive_item_file.md5']
            elif current_mode == mode_folder:
                columns = ['md5'] + [col for col in df.columns if col != 'md5']
            df = df[columns]
            # Afficher le DataFrame sous forme de tableau avec tabulate
            click.echo(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
            # Afficher les options de navigation
            options = ['s: Switch mode between file and folder imported',
                       'p: Previous page' if pagination.get('has_prev', False) else '',
                       'n: Next page' if pagination.get('has_next', False) else '',
                       'e: Extract files by ID',
                       'f: Filter files',
                       'q: Quit']
            options = [opt for opt in options if opt]
            click.echo(f'Page {page}/{pagination.get("total_pages", 1)} - Mode: {current_mode}')
            choice = click.prompt(f"Options: {', '.join(options)}", type=str)
            if choice == 'p' and pagination.get('has_prev', False):
                page -= 1
            elif choice == 'n' and pagination.get('has_next', False):
                page += 1
            elif choice == 'e':
                if current_mode == mode_file:
                    ids = click.prompt("Enter a comma-separated list of IDs to extract", type=str)
                elif current_mode == mode_folder:
                    ids = click.prompt("Enter a MD5 to extract", type=str)
                    # Check if the is multiple ids
                    if ',' in ids:
                        click.echo("You can only extract one MD5 at a time")
                        continue
                    
                
                if current_mode == mode_file:
                    id_list = ids.split(',')
                    extract_url = config.get('server', 'url') + f"/vaults/{config.get('vault', 'id_default')}/fileMetadata/extract"
                    extract_response = requests.get(extract_url, json={'file_metadata_ids': id_list})
                    if not Utilities.handle_response(extract_response):
                        return
                    
                    content_disposition = extract_response.headers.get('Content-Disposition')
                    if content_disposition:
                        filename = content_disposition.split('filename=')[-1].strip('\"')
                        print(filename)
                        file_path = join(Utilities.get_download_folder(), filename)
                        with open(file_path, 'wb') as f:
                            f.write(extract_response.content)
                        # Unzip the file if it is a zip file
                        if filename.endswith('.zip'):
                            Utilities.unzip_folder(file_path)
                            remove(file_path)
                        print(f"File {filename} downloaded successfully")
                    else:
                        print("No filename found in the response headers")
                elif current_mode == mode_folder:
                    extract_url = config.get('server', 'url') + f"/vaults/{config.get('vault', 'id_default')}/archiveItemFolder/extract"
                    extract_response = requests.get(extract_url, json={'archive_item_folder_md5s': id_list})
                    if not Utilities.handle_response(extract_response):
                        return
                    content_disposition = extract_response.headers.get('Content-Disposition')
                    if content_disposition:
                        filename = content_disposition.split('filename=')[-1].strip('\"')
                        file_path = join(Utilities.get_download_folder(), filename)
                        with open(file_path, 'wb') as f:
                            f.write(extract_response.content)
                        # Unzip the file if it is a zip file
                        if filename.endswith('.zip'):
                            Utilities.unzip_folder(file_path)
                            remove(file_path)
                        print(f"File {filename} downloaded successfully")
                    else:
                        print("No filename found in the response headers")
            elif choice == 's':
                if current_mode == mode_file:
                    current_mode = mode_folder
                else:
                    current_mode = mode_file
            elif choice == 'f':
                click.echo("Select a column to filter by:")
                column_options = {str(index + 1): col for index, col in enumerate(df.columns)}
                for index, col in column_options.items():
                    click.echo(f"{index}: {col}")
                col_choice = click.prompt("Enter the number corresponding to the column", type=str)
                if col_choice in column_options:
                    search_column = column_options[col_choice]
                    search_value = click.prompt(f"Enter the value to search in {search_column}", type=str, default='')
                    params[search_column] = search_value
            elif choice == 'q':
                break
            else:
                click.echo("Invalid choice. Please choose again.")
            # Mettre à jour les paramètres de la page
            params['page'] = page
            if current_mode == mode_file:
                click.echo("Mode file")
                url_vault = config.get('server', 'url') + f"/vaults/{config.get('vault', 'id_default')}/fileMetadata"
            elif current_mode == mode_folder:
                url_vault = url_vault = config.get('server', 'url') + f"/vaults/{config.get('vault', 'id_default')}/archive_item_folder"
            else:
                url_vault = config.get('server', 'url') + f"/vaults/{config.get('vault', 'id_default')}/fileMetadata"
            
            
            url_vault += '?' + urlencode(params)




