import importlib.util
import shutil
import subprocess
import sys
import datetime

# Definir idioma
def escolher_idioma():
    print("Choose language / Escolha o idioma:")
    print("1 - English")
    print("2 - Português")
    opcao = input("Option / Opção: ")
    return 'pt' if opcao == '2' else 'en'

# Mensagens nos dois idiomas
mensagens = {
    'check_python_nmap': {
        'en': "Checking if 'python-nmap' is installed...",
        'pt': "Verificando se o 'python-nmap' está instalado..."
    },
    'install_python_nmap': {
        'en': "❌ 'python-nmap' is not installed.",
        'pt': "❌ O módulo 'python-nmap' não está instalado."
    },
    'prompt_install': {
        'en': "Do you want to install it now? (y/n): ",
        'pt': "Deseja instalar automaticamente agora? (s/n): "
    },
    'installed_success': {
        'en': "✅ 'python-nmap' installed successfully.",
        'pt': "✅ Módulo 'python-nmap' instalado com sucesso."
    },
    'install_fail': {
        'en': "🚨 Error installing 'python-nmap'. Install manually with:",
        'pt': "🚨 Ocorreu um erro ao instalar o módulo. Instale manualmente com:"
    },
    'need_nmap': {
        'en': "❌ 'nmap' is not installed or not in PATH.",
        'pt': "❌ O programa Nmap não está instalado ou não está no PATH do sistema."
    },
    'install_nmap': {
        'en': "👉 Install Nmap. On Linux: sudo apt install nmap | On Windows: https://nmap.org/download.html",
        'pt': "👉 Instale o Nmap. No Linux: sudo apt install nmap | No Windows: https://nmap.org/download.html"
    },
    'scan_start': {
        'en': "Starting scan on network {} with ports {}",
        'pt': "Iniciando scan na rede {} nas portas {}"
    },
    'scan_done': {
        'en': "✅ Scan completed. Report saved in relatorio_scan.txt",
        'pt': "✅ Scan finalizado. Relatório salvo em relatorio_scan.txt"
    },
    'exit_need_module': {
        'en': "🚫 Script needs 'python-nmap' to continue. Exiting...",
        'pt': "🚫 O script precisa do módulo 'python-nmap' para continuar. Saindo..."
    }
}

# Funções adaptadas ao idioma
def checar_python_nmap(lang):
    print(mensagens['check_python_nmap'][lang])
    if importlib.util.find_spec("nmap") is None:
        print(mensagens['install_python_nmap'][lang])
        escolha = input(mensagens['prompt_install'][lang])
        if escolha.lower() in ('s', 'y'):
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "python-nmap"])
                print(mensagens['installed_success'][lang])
            except subprocess.CalledProcessError:
                print(mensagens['install_fail'][lang])
                print("    pip install python-nmap")
                sys.exit(1)
        else:
            print(mensagens['exit_need_module'][lang])
            sys.exit(1)

def checar_nmap(lang):
    if shutil.which("nmap") is None:
        print(mensagens['need_nmap'][lang])
        print(mensagens['install_nmap'][lang])
        sys.exit(1)

def rodar_scan(lang):
    import nmap
    scanner = nmap.PortScanner()
    rede = '192.168.1.0/24'
    portas = '22,80,443,3389'

    print(f"[{datetime.datetime.now()}] " + mensagens['scan_start'][lang].format(rede, portas))
    scanner.scan(hosts=rede, arguments=f'-p {portas} --open')

    with open('relatorio_scan.txt', 'w') as f:
        f.write(f"Report generated at / Relatório gerado em {datetime.datetime.now()}\n")
        for host in scanner.all_hosts():
            f.write(f"\nHost: {host} ({scanner[host].hostname()})\n")
            for proto in scanner[host].all_protocols():
                ports = scanner[host][proto].keys()
                for port in ports:
                    f.write(f"  Port {port}/{proto} open\n")
    print(mensagens['scan_done'][lang])

# Execução principal
if __name__ == "__main__":
    lang = escolher_idioma()
    checar_python_nmap(lang)
    checar_nmap(lang)
    rodar_scan(lang)
    