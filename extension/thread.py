import socket
import threading

def create_magic_packet(mac_address: str) -> bytes:
    mac_bytes = bytes.fromhex(mac_address.replace(":", "").replace("-", ""))
    magic_packet = b'\xff' * 6 + mac_bytes * 16
    return magic_packet

def send_wol(mac_address: str, ip_address: str, port: int = 9):
    packet = create_magic_packet(mac_address)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(packet, (ip_address, port))
    print(f"WOL 패킷 전송 완료: {mac_address} -> {ip_address}:{port}")

def send_wol_thread(mac, ip, port, count=1):
    threads = []
    for _ in range(count):
        t = threading.Thread(target=send_wol, args=(mac, ip, port))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

if __name__ == "__main__":
    mac = "30:9C:23:FF:FF:FF"
    external_ip = "163.152.0.0"
    internal_ip = "172.30.1.10"
    wol_port = 9
    send_count = 5  # 동시에 몇 번

    send_wol_thread(mac, external_ip, wol_port, send_count)
