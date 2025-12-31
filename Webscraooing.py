import requests
from bs4 import BeautifulSoup

def get_crypto_price(symbol):
    """
    Função para obter preço de criptomoedas do Yahoo Finance
    """
    url = f'https://finance.yahoo.com/quote/{symbol}'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    }
    
    try:
        # Fazer requisição
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Verificar se houve erro HTTP
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # TENTATIVA 1: Buscar pelos data-testid (mais recente)
        price_element = soup.find('span', {'data-testid': 'qsp-price'})
        change_element = soup.find('span', {'data-testid': 'qsp-price-change'})
        
        # TENTATIVA 2: Buscar por fin-streamer (formato antigo)
        if not price_element:
            price_element = soup.find('fin-streamer', {'data-symbol': symbol, 'data-field': 'regularMarketPrice'})
        if not change_element:
            change_element = soup.find('fin-streamer', {'data-symbol': symbol, 'data-field': 'regularMarketChange'})
        
        # TENTATIVA 3: Buscar por classes específicas
        if not price_element:
            price_div = soup.find('div', {'class': 'D(ib) Mend(20px)'})
            if price_div:
                spans = price_div.find_all('span')
                if len(spans) >= 2:
                    price_element = spans[0]
                    change_element = spans[1]
        
        # Extrair textos
        price = price_element.text.strip() if price_element else "Não encontrado"
        change = change_element.text.strip() if change_element else "Não encontrado"
        
        return price, change
        
    except requests.exceptions.ConnectionError:
        return "Erro de conexão", "Verifique sua internet"
    except requests.exceptions.Timeout:
        return "Timeout", "Demorou muito para responder"
    except Exception as e:
        return f"Erro: {str(e)[:50]}", ""

# Testar
print("=" * 50)
print("YAHOO FINANCE SCRAPER - ETHEREUM")
print("=" * 50)

price, change = get_crypto_price('ETH-USD')
print(f"💰 Preço: {price}")
print(f"📈 Variação: {change}")

# Testar com outras criptomoedas
print("\n" + "=" * 50)
print("OUTRAS CRIPTOMOEDAS:")
print("=" * 50)

cryptos = ['BTC-USD', 'ETH-USD', 'BNB-USD', 'ADA-USD']
for crypto in cryptos:
    p, c = get_crypto_price(crypto)
    print(f"{crypto}: {p} | Variação: {c}")