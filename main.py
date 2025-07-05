import socket
import threading
from concurrent.futures import ThreadPoolExecutor
import datetime
import argparse
import sys
import time
import ipaddress

class PortScanner:
    def __init__(self, max_threads=100, timeout=1):
        self.max_threads = max_threads
        self.timeout = timeout
        self.open_ports = []
        self.lock = threading.Lock()
        self.scanned_ports = 0
        self.total_ports = 0
        
    def validate_target(self, target):
        """Valida se o target é um IP ou hostname válido"""
        try:
            # Tenta validar como IP
            ipaddress.ip_address(target)
            return True
        except ValueError:
            # Se não for IP, tenta resolver como hostname
            try:
                socket.gethostbyname(target)
                return True
            except socket.gaierror:
                return False
    
    def scan_port(self, target, port):
        """Escaneia uma porta específica"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                result = sock.connect_ex((target, port))
                if result == 0:
                    with self.lock:
                        self.open_ports.append(port)
                        
            # Atualiza contador thread-safe
            with self.lock:
                self.scanned_ports += 1
                if self.scanned_ports % 100 == 0:
                    progress = (self.scanned_ports / self.total_ports) * 100
                    print(f"Progresso: {progress:.1f}% ({self.scanned_ports}/{self.total_ports})", end='\r')
                    
        except Exception:
            with self.lock:
                self.scanned_ports += 1
    
    def scan_ports(self, target, start_port, end_port):
        """Escaneia um range de portas"""
        if not self.validate_target(target):
            raise ValueError(f"Target inválido: {target}")
        
        if start_port > end_port or start_port < 1 or end_port > 65535:
            raise ValueError("Range de portas inválido")
        
        self.total_ports = end_port - start_port + 1
        self.scanned_ports = 0
        self.open_ports = []
        
        start_time = time.time()
        
        print(f"Iniciando scan de {target} (portas {start_port}-{end_port})...")
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = []
            for port in range(start_port, end_port + 1):
                future = executor.submit(self.scan_port, target, port)
                futures.append(future)
            
            # Aguarda todas as threads terminarem
            for future in futures:
                future.result()
        
        end_time = time.time()
        scan_duration = end_time - start_time
        
        print(f"\nScan concluído em {scan_duration:.2f} segundos")
        return sorted(self.open_ports)
    
    def get_service_name(self, port):
        """Tenta identificar o serviço comum para uma porta"""
        common_ports = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
            53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
            443: "HTTPS", 993: "IMAPS", 995: "POP3S",
            3389: "RDP", 5432: "PostgreSQL", 3306: "MySQL",
            1433: "MSSQL", 27017: "MongoDB", 6379: "Redis"
        }
        return common_ports.get(port, "Unknown")
    
    def log_scan_result(self, target, start_port, end_port, open_ports, duration):
        """Salva o resultado do scan em um arquivo de log"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_filename = "scan_log.txt"
        
        with open(log_filename, "a", encoding="utf-8") as log_file:
            log_file.write(f"[{timestamp}] Scan realizado\n")
            log_file.write(f"Alvo: {target}\n")
            log_file.write(f"Range de portas: {start_port}-{end_port}\n")
            log_file.write(f"Duração: {duration:.2f} segundos\n")
            
            if open_ports:
                log_file.write(f"Portas abertas ({len(open_ports)}):\n")
                for port in open_ports:
                    service = self.get_service_name(port)
                    log_file.write(f"  {port} ({service})\n")
            else:
                log_file.write("Nenhuma porta aberta encontrada\n")
            
            log_file.write("-" * 50 + "\n\n")

def main():
    parser = argparse.ArgumentParser(description="Scanner de Portas TCP")
    parser.add_argument("target", help="IP ou hostname do alvo")
    parser.add_argument("-s", "--start", type=int, default=1, help="Porta inicial (padrão: 1)")
    parser.add_argument("-e", "--end", type=int, default=1000, help="Porta final (padrão: 1000)")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Número de threads (padrão: 100)")
    parser.add_argument("--timeout", type=float, default=1.0, help="Timeout em segundos (padrão: 1.0)")
    parser.add_argument("--common", action="store_true", help="Escanear apenas portas comuns")
    
    args = parser.parse_args()
    
    # Portas comuns para scan rápido
    common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3389, 5432, 3306, 1433, 27017, 6379]
    
    scanner = PortScanner(max_threads=args.threads, timeout=args.timeout)
    
    try:
        if args.common:
            print("Escaneando portas comuns...")
            open_ports = []
            total_ports = len(common_ports)
            
            start_time = time.time()
            
            with ThreadPoolExecutor(max_workers=args.threads) as executor:
                futures = []
                for port in common_ports:
                    future = executor.submit(scanner.scan_port, args.target, port)
                    futures.append(future)
                
                for future in futures:
                    future.result()
            
            end_time = time.time()
            duration = end_time - start_time
            open_ports = sorted(scanner.open_ports)
            
        else:
            start_time = time.time()
            open_ports = scanner.scan_ports(args.target, args.start, args.end)
            end_time = time.time()
            duration = end_time - start_time
        
        # Exibe resultados
        print(f"\nResultados para {args.target}:")
        if open_ports:
            print(f"Portas abertas encontradas ({len(open_ports)}):")
            for port in open_ports:
                service = scanner.get_service_name(port)
                print(f"  {port} ({service})")
        else:
            print("Nenhuma porta aberta encontrada")
        
        # Salva no log
        if args.common:
            scanner.log_scan_result(args.target, min(common_ports), max(common_ports), open_ports, duration)
        else:
            scanner.log_scan_result(args.target, args.start, args.end, open_ports, duration)
        
        print(f"\nResultado salvo em scan_log.txt")
        
    except ValueError as e:
        print(f"Erro: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nScan interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"Erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Se executado sem argumentos, usa modo interativo
    if len(sys.argv) == 1:
        try:
            target = input("Digite o endereço IP ou hostname do alvo: ")
            start_port = int(input("Digite a porta inicial (padrão 1): ") or "1")
            end_port = int(input("Digite a porta final (padrão 1000): ") or "1000")
            
            scanner = PortScanner()
            start_time = time.time()
            open_ports = scanner.scan_ports(target, start_port, end_port)
            end_time = time.time()
            duration = end_time - start_time
            
            print(f"\nResultados para {target}:")
            if open_ports:
                print(f"Portas abertas encontradas ({len(open_ports)}):")
                for port in open_ports:
                    service = scanner.get_service_name(port)
                    print(f"  {port} ({service})")
            else:
                print("Nenhuma porta aberta encontrada")
            
            scanner.log_scan_result(target, start_port, end_port, open_ports, duration)
            print(f"\nResultado salvo em scan_log.txt")
            
        except KeyboardInterrupt:
            print("\nScan interrompido pelo usuário")
        except Exception as e:
            print(f"Erro: {e}")
    else:
        main()