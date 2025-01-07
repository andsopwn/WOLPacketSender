import socket
import schedule
import time

def create_magic_packet(mac_address: str) -> bytes:
    mac_bytes = bytes.fromhex(mac_address.replace(":", "").replace("-", ""))
    magic_packet = b'\xff' * 6 + mac_bytes * 16
    return magic_packet

def send_wol(mac_address: str, ip_address: str, port: int = 9):
    packet = create_magic_packet(mac_address)
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(packet, (ip_address, port))
    
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] WOL 패킷 전송 완료: {mac_address} -> {ip_address}:{port}")

def job():
    mac = "30:9C:23:FF:FF:FF"
    ip = "172.30.1.10"
    port = 9
    send_wol(mac, ip, port)

if __name__ == "__main__":
    schedule.every().day.at("07:00").do(job)
    
    print("스케줄러 시작. 종료하려면 Ctrl+C를 누르세요.")
    while True:
        schedule.run_pending()
        time.sleep(1)
