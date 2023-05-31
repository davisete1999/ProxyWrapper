import requests
import json
from concurrent.futures import ProcessPoolExecutor

from sys import argv

def get_proxy_list():
    url = "https://api.proxyscrape.com/proxytable.php?nf=true&country=all"

    try:
        response = requests.get(url)
        data = response.json()
        return data["http"].keys()
    except requests.exceptions.RequestException as e:
        print("Error al obtener la lista de proxies:", e)
        return []

def test_proxy(proxy):
    try:
        with requests.Session() as session:
            response = session.get(URL, proxies={'http': proxy, 'https': proxy}, timeout=1)
            if response.status_code == 200:
                print(f"Proxy {proxy} es válido.")
                return proxy
    except (requests.exceptions.RequestException, requests.exceptions.Timeout):
        print(f"Proxy {proxy} es inválido.")

    return None

if __name__ == "__main__":
    
    URL = argv[1]

    # Obtener la lista de proxies
    proxy_list = get_proxy_list()

    # Probar la validez de las proxies utilizando ProcessPoolExecutor
    valid_proxies = []
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(test_proxy, proxy) for proxy in proxy_list]

        for future in futures:
            proxy = future.result()
            if proxy is not None:
                valid_proxies.append(proxy)

    # Guardar las proxies válidas en un archivo JSON
    with open("proxies.json", "w") as file:
        json.dump(valid_proxies, file)

    print("Proxies válidos guardados en proxies.json.")
