import googlemaps
import pandas as pd
import os
from dotenv import load_dotenv

# Carregar a chave de API do Google Maps de forma segura
load_dotenv()
API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
gmaps = googlemaps.Client(key=API_KEY)

def obter_roteiro_otimizado(arquivo_csv, ponto_partida):
    # Carrega os clientes do arquivo CSV
    df = pd.read_csv(arquivo_csv)
    clientes = df.to_dict('records')

    rota_final = []

    local_atual = ponto_partida

    print(f"🚀 Iniciando roteirização a partir de: {local_atual}")

    while clientes:
        # Calcula as distâncias do local atual para cada cliente
        destinos = [c['Endereco'] for c in clientes]
        matriz = gmaps.distance_matrix(local_atual, destinos, mode='driving')

        # Lógica do Vizinho Mais Próximo
        distancias = matriz['rows'][0]['elements']

        # Encontra o indice do cliente com a menor duração de viagem
        melhor_indice = 0
        menor_tempo = float('inf')

        for i, info in enumerate(distancias):
            if info['status'] == 'OK':
                tempo = info['duration']['value'] # tempo em segundos
                if tempo < menor_tempo:
                    menor_tempo = tempo
                    melhor_indice = i

        # Move o cliente para a rota final e atualiza o local
        proximo_cliente = clientes.pop(melhor_indice)
        rota_final.append(proximo_cliente)
        local_atual = proximo_cliente['Endereco']

        print(f"✅ Próxima parada definida: {proximo_cliente['Nome']}")

    return rota_final

# Execução do roteirizador
if __name__ == "__main__":
    # Define o ponto de partida (pode ser um endereço ou coordenadas)
    PONTO_INICIAL = input("📍 Digite o endereço de partida [Rua,número,bairro,cidade-estado]: ")

    resultado = obter_roteiro_otimizado('clientes_teste.csv', PONTO_INICIAL)

    print("\n📍 ORDEM FINAL DO ROTEIRO:")
    for i, c in enumerate(resultado, 1):
        print(f"{i}. {c['Nome']} -> {c['Endereco']}")

