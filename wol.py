import socket

def create_magic_packet(mac_address: str) -> bytes:
    """
    주어진 MAC 주소 문자열을 이용해 매직 패킷을 생성한다.
    매직 패킷은 6바이트의 0xFF + (MAC 바이트 * 16) 으로 구성된다.
    예: FF FF FF FF FF FF + (MAC * 16)
    """
    mac_bytes = bytes.fromhex(mac_address.replace(":", "").replace("-", ""))

    magic_packet = b'\xff' * 6 + mac_bytes * 16
    return magic_packet

def send_wol_packet(mac_address: str, ip_address: str, port: int = 9):
    """
    Wake-On-LAN 매직 패킷을 전송한다.
      - mac_address: 대상 PC의 MAC 주소 (예: '30:9C:FF:FF:FF:FF')
      - ip_address : 매직 패킷을 보낼 IP 주소 (공유기 외부 IP 혹은 내부 IP)
      - port       : 목적지 포트 (보통 7 또는 9 사용), 기본값 9
    """
    packet = create_magic_packet(mac_address)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        s.sendto(packet, (ip_address, port))
    
    print(f"WOL 패킷 전송 완료: {mac_address} -> {ip_address}:{port}")

if __name__ == "__main__":
    mac = "30:9C:23:FF:FF:FF"

    external_ip = "163.152.0.0"
    #internal_ip = "172.30.1.10"    # 내부망에서 직접 보내거나 NAT Loopback 시에 사용
    wol_port = 9

    # 1) 외부 IP로 매직 패킷 보내기 (공유기에서 UDP 9번 포트 포워딩 설정 필요)
    send_wol_packet(mac, external_ip, wol_port)

    # 2) 내부 IP로 매직 패킷 보내기 (같은 내부망이거나 NAT Loopback이 허용되는 환경)
    # send_wol_packet(mac, internal_ip, wol_port)