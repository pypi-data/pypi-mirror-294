import typer
import re
import requests
import os.path
import subprocess
from rich import print
from cryptography import x509
from datetime import timedelta
from typing_extensions import Annotated
from cryptography.x509.oid import ExtensionOID
from rich.console import Console
from rich.table import Table


app = typer.Typer(no_args_is_help=True)
console = Console()

# Handle the file downloading
def downloadFile(url, download):
    # Extract the file name from the URL
    local_filename = url.split('/')[-1]

    # Send an HTTP GET request to the URL
    with requests.get(url, stream=True) as response:
        # Check if the request was successful
        if response.status_code == 200:
            # Open a file in the current directory with the extracted file name
            with open(local_filename, 'wb') as file:
                # Write the content of the response to the file in chunks
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            
            # Only show's the secess messagem if the user selected the keep the file
            if(download == True):
                print(f"Ficheiro descarregado com sucesso: {local_filename}")
            else:
                return
        else:
            print(f"Erro ao descarregar o ficheiro. HTTP Status Code: {response.status_code}")

# Handle the time conversion to GMT+1 and formating
def timeConvert(date):
    localTime = date + timedelta(hours=1)
    return localTime.strftime("%Y-%m-%d %H:%M:%S")

def updateCheck():
    # Check the installed version
    result = subprocess.run(['pip', 'show', 'certificate-check'], stdout=subprocess.PIPE)
    currentVersion = re.search(r"Version:\s*([^\s\\]+)", str(result.stdout)).group(1)

    # Get the latest version
    url = "https://pypi.org/pypi/certificate-check/json"
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()

        # Parse the JSON data
        json_data = response.json()

        # Extract the version key from the JSON data
        latestVersion = json_data.get("info", {}).get("version")
    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro: {e}")

    if(currentVersion != latestVersion):
        print("\nEstás a utilizar uma versão desatualizada, podes atualizar executando o comando[bold yellow] pip install certificate-check --upgrade [/bold yellow]")


# Check if the certificate is in the CRL provided
#@app.command()
#def crl_check(filename: Annotated[str, typer.Argument(help="The CRL file to use (must finish with .crl)")], 
        #serialnumber: Annotated[str, typer.Argument(help="The certificate serial number to find")]):

    ## Get and load the DER encoded file
    #data = open(filename,"rb").read()
    #certList = x509.load_der_x509_crl(data)

    ## Certificate Issuer
    ##certIssuer = str(certList.issuer)
    ##print("Certificado emitido por: \n" + certIssuer)

    ## Convert serial number to hexadecimal
    #x = int(serialnumber, 16)

    ## Tries to find the serial number in the revoked certificates
    #checkIfRevoked = certList.get_revoked_certificate_by_serial_number(x)

    #if(checkIfRevoked != None):
        #print("[bold red]The certificate is revoked :cross_mark:[/bold red]")
        #print("[bold]Revogation date[/bold]: " + str(timeConvert(checkIfRevoked.revocation_date_utc)))
    #else:
        #print("[bold green]Serial number not found in the provided revogation list :white_check_mark:[/bold green]")


# Gets a certificate and the corresponding CRL file
@app.command()
def revogate_check(filename: Annotated[str, typer.Argument(help="The certificate file to use (must finish with .cer)")],
                   keep: Annotated[bool, typer.Option(help="Keeps the downloaded CRL file")] = False):
    # Get and load the certificate
    data = open(filename,"rb").read()
    cert = x509.load_der_x509_certificate(data)

    # Gets the extensions and finds the distribution point
    certExtentions = cert.extensions
    certInfoAcess = certExtentions.get_extension_for_oid(ExtensionOID.CRL_DISTRIBUTION_POINTS).value
    
    # Deconstructs the result to get only the URL
    crlUrlLocation = re.search(r"(?P<url>https?://[^\s]+\.crl)", str(certInfoAcess)).group("url")
    downloadedFile = re.search(r"https?://[^\s]+/([^/]+\.crl)", str(crlUrlLocation)).group(1)

    #Check if the file already exists
    if(os.path.isfile(downloadedFile)) == True:
        if(keep == True):
            os.remove(downloadedFile)
            print("Ficheiro CRL local eliminado")

            # Downloads the CRL file to the folder
            downloadFile(crlUrlLocation, True)  
        else:
            print("O ficheiro CRL já existe e não será descarregado.")
    else:
        # Downloads the CRL file to the folder
        downloadFile(crlUrlLocation, False)  

    # Get certificate serial number and subject
    serialNumber = cert.serial_number

    # Get and load the DER encoded CRL
    crlData = open(downloadedFile,"rb").read()
    certList = x509.load_der_x509_crl(crlData)
    
    # Tries to find the serial number in the revoked certificates
    checkIfRevoked = certList.get_revoked_certificate_by_serial_number(serialNumber)

    # Create the table to display the information
    table = Table(show_header=False, show_lines=True)

    print(cert.subject)

    # Get the certificate subject
    try:
        dName = re.search(r'CN=(?:\[[^\]]*\]\s*)?([^,)>]+)', str(cert.subject)).group(1)
        table.add_row("Emitido para:", dName)
    except:
        print("Não foi possível obter o nome do detentor do certificado. Por favor reporta este problema.")

    table.add_row("Validade:", "[bold blue]" + str(timeConvert(cert.not_valid_before_utc)) + "[/bold blue] até [bold blue]" + str(timeConvert(cert.not_valid_after_utc)) + "[/bold blue]")

    if(checkIfRevoked != None):
        table.add_row("Estado revogação:","[bold red]O certificado está revogado :cross_mark:[/bold red]")
        table.add_row("Data revogação:",str(timeConvert(checkIfRevoked.revocation_date_utc)))
    else:
        #print("[bold green]Serial number not found in the provided revogation list :white_check_mark:[/bold green]")
        table.add_row("Estado revogação","[bold green]O certificado não se encontra na lista de revogações :white_check_mark:[/bold green]")

    console.print(table)

    # Delete the download file at the end of the process
    os.remove(downloadedFile)

    updateCheck()

#TESTING ONLY
#if __name__ == "__main__":
    #app()