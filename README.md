executar pre-commit manualmente em todos os arquivos

```bash
pre-commit run --all-files
```


Incluido teste da extensão [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) com ela podemos programar com VS Code de dentro de um container Docker
É gerado alguns arquivos dentro da pasta .devcontainer para configurar esse ambiente, para fazer a configuração inicial siga os seguintes passos:
- Tive que criar a pasta workspaces mapeada no devcontainer/docker-compose.yml dentro do container do docker, outra alternativa seria criar via dockerfile
- use ctrl + shift + P e digite Dev Containers: Add Dev Container Configuration Files
    - aqui escolhi como base o meu docker-compose.yaml
- Após isso selecione a opção Dev Containers: Rebuild and Reopen in Container
