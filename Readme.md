# 🔍 Scanner de Portas TCP

Um scanner de portas TCP robusto e multi-threaded implementado em Python, projetado para análise de segurança e auditoria de redes.

## ✨ Características

- **Multi-threading**: Utiliza ThreadPoolExecutor para scans paralelos e eficientes
- **Flexível**: Suporte a ranges personalizados de portas ou scan de portas comuns
- **Identificação de Serviços**: Identifica automaticamente serviços comuns em portas abertas
- **Logging Detalhado**: Salva resultados em arquivos de log com timestamp
- **Indicador de Progresso**: Mostra o progresso em tempo real durante o scan
- **Validação de Entrada**: Valida IPs e hostnames antes do scan
- **Interface Dupla**: Modo interativo e linha de comando
- **Configurável**: Timeout e número de threads ajustáveis

## 🚀 Instalação

### Requisitos

- Python 3.6 ou superior
- Bibliotecas padrão do Python (não requer instalação adicional)

### Clone o Repositório

```bash
git clone https://github.com/seu-usuario/tcp-port-scanner.git
cd tcp-port-scanner
```

## 📖 Uso

### Modo Interativo

Execute o script sem argumentos para usar o modo interativo:

```bash
python port_scanner.py
```

### Linha de Comando

```bash
# Scan básico (portas 1-1000)
python port_scanner.py 192.168.1.1

# Scan com range personalizado
python port_scanner.py 192.168.1.1 -s 1 -e 65535

# Scan de portas comuns (rápido)
python port_scanner.py google.com --common

# Scan com configurações personalizadas
python port_scanner.py 192.168.1.1 -s 80 -e 443 -t 50 --timeout 2.0
```

### Opções Disponíveis

| Opção | Descrição | Padrão |
|-------|-----------|---------|
| `target` | IP ou hostname do alvo | Obrigatório |
| `-s, --start` | Porta inicial | 1 |
| `-e, --end` | Porta final | 1000 |
| `-t, --threads` | Número de threads | 100 |
| `--timeout` | Timeout em segundos | 1.0 |
| `--common` | Escanear apenas portas comuns | False |
| `-h, --help` | Exibir ajuda | - |

## 🎯 Exemplos de Uso

### Scan Básico de Rede Local

```bash
python port_scanner.py 192.168.1.1
```

**Saída:**
```
Iniciando scan de 192.168.1.1 (portas 1-1000)...
Progresso: 100.0% (1000/1000)
Scan concluído em 12.34 segundos

Resultados para 192.168.1.1:
Portas abertas encontradas (3):
  22 (SSH)
  80 (HTTP)
  443 (HTTPS)

Resultado salvo em scan_log.txt
```

### Scan de Portas Comuns

```bash
python port_scanner.py google.com --common
```

**Saída:**
```
Escaneando portas comuns...

Resultados para google.com:
Portas abertas encontradas (2):
  80 (HTTP)
  443 (HTTPS)

Resultado salvo em scan_log.txt
```

### Scan Completo com Configurações Personalizadas

```bash
python port_scanner.py 192.168.1.100 -s 1 -e 65535 -t 200 --timeout 0.5
```

## 📊 Portas Comuns Identificadas

O scanner identifica automaticamente os seguintes serviços:

| Porta | Serviço | Descrição |
|-------|---------|-----------|
| 21 | FTP | File Transfer Protocol |
| 22 | SSH | Secure Shell |
| 23 | Telnet | Telnet Protocol |
| 25 | SMTP | Simple Mail Transfer Protocol |
| 53 | DNS | Domain Name System |
| 80 | HTTP | Hypertext Transfer Protocol |
| 110 | POP3 | Post Office Protocol v3 |
| 143 | IMAP | Internet Message Access Protocol |
| 443 | HTTPS | HTTP Secure |
| 993 | IMAPS | IMAP over SSL |
| 995 | POP3S | POP3 over SSL |
| 3389 | RDP | Remote Desktop Protocol |
| 5432 | PostgreSQL | PostgreSQL Database |
| 3306 | MySQL | MySQL Database |
| 1433 | MSSQL | Microsoft SQL Server |
| 27017 | MongoDB | MongoDB Database |
| 6379 | Redis | Redis Database |

## 📝 Logs

O scanner salva automaticamente os resultados em `scan_log.txt` com o formato:

```
[2025-07-05 14:30:25] Scan realizado
Alvo: 192.168.1.1
Range de portas: 1-1000
Duração: 12.34 segundos
Portas abertas (3):
  22 (SSH)
  80 (HTTP)
  443 (HTTPS)
--------------------------------------------------
```

## ⚡ Otimização de Performance

### Configurações Recomendadas

- **Rede Local**: `-t 200 --timeout 0.5`
- **Internet**: `-t 50 --timeout 2.0`
- **Scan Rápido**: `--common`

### Dicas de Performance

1. **Ajuste o número de threads**: Mais threads = mais velocidade, mas pode sobrecarregar a rede
2. **Configure o timeout**: Timeouts menores são mais rápidos, mas podem perder portas lentas
3. **Use portas comuns**: Para reconhecimento rápido, use a opção `--common`

## 🔒 Considerações de Segurança

### ⚠️ Aviso Legal

Este scanner foi desenvolvido para fins educacionais e de segurança legítima. **Use apenas em:**

- Redes próprias
- Sistemas com autorização explícita
- Ambientes de teste controlados

### Uso Ético

- ✅ Auditoria de segurança autorizada
- ✅ Teste de penetração com permissão
- ✅ Análise de redes próprias
- ❌ Scanning não autorizado
- ❌ Atividades maliciosas

### Detecção e Prevenção

- Firewalls podem detectar scans agressivos
- IDS/IPS podem gerar alertas
- Use com moderação para evitar bloqueios

## 🛠️ Desenvolvimento

### Estrutura do Projeto

```
tcp-port-scanner/
├── port_scanner.py      # Script principal
├── scan_log.txt        # Arquivo de log (gerado automaticamente)
├── README.md           # Este arquivo
└── requirements.txt    # Dependências (vazio - usa bibliotecas padrão)
```

### Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

### Melhorias Futuras

- [ ] Suporte a scan UDP
- [ ] Detecção de versão de serviços
- [ ] Exportação para XML/JSON
- [ ] Interface gráfica
- [ ] Scan de múltiplos hosts
- [ ] Integração com bases de dados de vulnerabilidades

## 📜 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🤝 Suporte

Se você encontrar bugs ou tiver sugestões:

1. Abra uma [issue](https://github.com/seu-usuario/tcp-port-scanner/issues)
2. Envie um email para: seu-email@example.com
3. Contribua com código via Pull Request

## 📚 Referências

- [Python Socket Programming](https://docs.python.org/3/library/socket.html)
- [ThreadPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html)
- [IANA Port Numbers](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml)

