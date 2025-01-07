# **Manual de Utilização do Docker Swarm**

## **O que é Docker Swarm?**
Docker Swarm é uma ferramenta de orquestração que permite gerenciar múltiplos contêineres como um cluster. Ele organiza os contêineres em serviços, permite escalabilidade e facilita a implantação de aplicações em ambientes distribuídos.

---

## **1. Configuração do Ambiente**

### Pré-requisitos
- Docker instalado em todas as máquinas do cluster.
- Rede configurada para comunicação entre os nós.

### Inicializar o Docker Swarm
1. No nó principal, inicialize o Swarm:
   ```bash
   docker swarm init --advertise-addr <IP_DO_NÓ_PRINCIPAL>
   ```
   - O `--advertise-addr` define o IP que será usado para comunicação com outros nós.

2. Após a inicialização, você verá um comando para adicionar novos nós ao cluster. Por exemplo:
   ```bash
   docker swarm join --token <TOKEN> <IP_DO_NÓ_PRINCIPAL>:2377
   ```

3. No(s) nó(s) secundário(s), execute o comando acima para ingressar no cluster.

4. Verifique os nós no cluster:
   ```bash
   docker node ls
   ```

---

## **2. Criar e Configurar a Stack**

### Estrutura do Arquivo `docker-compose.yml`
Um exemplo de stack para aplicação Python com Flask e MySQL:
```yaml
version: "3.9"

services:
  web:
    image: your-dockerhub-username/apppython_web:latest
    ports:
      - "5000:5000"
    networks:
      - app_network
    depends_on:
      - db

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: testdb
    ports:
      - "3306:3306"
    networks:
      - app_network

networks:
  app_network:
    driver: overlay
```

---

## **3. Implantar a Stack**

1. Suba a stack no Swarm:
   ```bash
   docker stack deploy --compose-file docker-compose.yml <NOME_DA_STACK>
   ```
   Exemplo:
   ```bash
   docker stack deploy --compose-file docker-compose.yml apppython
   ```

2. Verifique os serviços da stack:
   ```bash
   docker service ls
   ```

3. Verifique o status das tarefas dos serviços:
   ```bash
   docker service ps <NOME_DO_SERVIÇO>
   ```

4. Acompanhe os logs dos serviços:
   ```bash
   docker service logs <NOME_DO_SERVIÇO>
   ```
   Exemplo:
   ```bash
   docker service logs apppython_web
   ```

---

## **4. Escalar Serviços**

Para aumentar o número de réplicas de um serviço:
```bash
docker service scale <NOME_DA_STACK>_<NOME_DO_SERVIÇO>=<NÚMERO_DE_RÉPLICAS>
```
Exemplo:
```bash
docker service scale apppython_web=3
```

---

## **5. Atualizar a Stack**

Caso você precise fazer alterações no `docker-compose.yml` (como atualizar a imagem ou configuração), reimplemente a stack:
```bash
docker stack deploy --compose-file docker-compose.yml <NOME_DA_STACK>
```

O Docker Swarm aplicará as mudanças sem interrupção (se configurado corretamente).

---

## **6. Remover a Stack**

Para remover a stack:
```bash
docker stack rm <NOME_DA_STACK>
```
Exemplo:
```bash
docker stack rm apppython
```

---

## **7. Diagnóstico e Solução de Problemas**

### Verificar o Status dos Nós
Para verificar o status dos nós no cluster:
```bash
docker node ls
```

### Verificar Logs
Acompanhe os logs para identificar erros:
```bash
docker service logs <NOME_DO_SERVIÇO>
```

### Diagnóstico de Serviços
Para detalhes sobre as tarefas de um serviço:
```bash
docker service ps <NOME_DO_SERVIÇO>
```

### Verificar Imagens
Certifique-se de que as imagens necessárias estão disponíveis nos nós:
```bash
docker images
```

### Atualizar Imagens nos Nós
Se a imagem está faltando, envie-a para um registro como o Docker Hub ou um registro local. Exemplo de envio para o Docker Hub:
```bash
docker tag apppython_web:latest your-dockerhub-username/apppython_web:latest
docker push your-dockerhub-username/apppython_web:latest
```

---

## **8. Melhor Práticas**

- Sempre use um registro centralizado (Docker Hub, AWS ECR, etc.) para armazenar imagens.
- Use versões específicas de imagens para garantir estabilidade (evite apenas `latest`).
- Configure redes `overlay` para comunicação eficiente entre os serviços no Swarm.
- Teste localmente com `docker-compose` antes de implantar no Swarm.

---

## **9. Comandos Resumidos**

| Comando                                 | Descrição                                              |
|-----------------------------------------|-------------------------------------------------------|
| `docker swarm init`                     | Inicializa o Swarm no nó principal.                  |
| `docker swarm join`                     | Adiciona um nó ao cluster.                           |
| `docker stack deploy`                   | Implanta uma stack no Swarm.                         |
| `docker service ls`                     | Lista os serviços ativos no Swarm.                   |
| `docker service logs <SERVIÇO>`         | Mostra os logs de um serviço.                        |
| `docker service ps <SERVIÇO>`           | Verifica o status das tarefas de um serviço.         |
| `docker service scale <SERVIÇO>=<N>`    | Escala o serviço para o número N de réplicas.        |
| `docker stack rm <STACK>`               | Remove uma stack do Swarm.                           |
| `docker node ls`                        | Lista os nós do cluster Swarm.                       |

---

Esse manual cobre os passos principais para usar o Docker Swarm no gerenciamento de contêineres. Se precisar personalizar algo, só avisar! 🚀
