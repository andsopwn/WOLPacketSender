#!/bin/bash

# ===== 사용자 정의 설정 =====

MAC_ADDRESS="30:9C:23:FF:FF:FF"
EXTERNAL_IP="163.152.0.0"
INTERNAL_IP="172.30.1.10"

PORT=9

# ================================

mac_to_hex() {
    echo "$1" | tr -d ':-'
}

create_magic_packet() {
    mac_hex=$(mac_to_hex "$1")
    magic_hex="FFFFFFFFFFFF${mac_hex}${mac_hex}${mac_hex}${mac_hex}${mac_hex}${mac_hex}${mac_hex}${mac_hex}${mac_hex}${mac_hex}${mac_hex}${mac_hex}${mac_hex}${mac_hex}${mac_hex}${mac_hex}"
    echo "$magic_hex" | xxd -r -p
}

send_wol_packet() {
    mac="$1"
    ip="$2"
    port="$3"

    packet=$(create_magic_packet "$mac")

    echo -n "$packet" | nc -u -w1 "$ip" "$port"

    if [ $? -eq 0 ]; then
        echo "WOL 패킷 전송 성공: $mac -> $ip:$port"
    else
        echo "WOL 패킷 전송 실패: $mac -> $ip:$port" >&2
    fi
}

echo "Wake-On-LAN 매직 패킷 전송을 시작합니다..."

send_wol_packet "$MAC_ADDRESS" "$EXTERNAL_IP" "$PORT"
# send_wol_packet "$MAC_ADDRESS" "$INTERNAL_IP" "$PORT"

echo "모든 WOL 패킷 전송이 완료되었습니다."
