#!/bin/bash

# Màu sắc
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Banner
clear
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║        IP SCANNER v2.0                ║${NC}"
echo -e "${GREEN}║     by Phạm Quang Huy (@hiamhuy)     ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""

# Kiểm tra quyền root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}[!] Cần chạy với quyền root: sudo $0${NC}"
    exit 1
fi

# Kiểm tra masscan
if ! command -v masscan &> /dev/null; then
    echo -e "${RED}[!] masscan chưa được cài đặt${NC}"
    exit 1
fi

# ===== NHẬP THÔNG TIN =====

# 1. Nhập file range
echo -e "${BLUE}[?] Nhập tên file chứa IP ranges:${NC}"
read -p "    (Để trống = quét toàn bộ 0.0.0.0/0): " RANGE_FILE

if [ -z "$RANGE_FILE" ]; then
    echo -e "${YELLOW}[*] Sẽ quét toàn bộ Internet (0.0.0.0/0)${NC}"
    SCAN_TARGET="0.0.0.0/0"
    USE_FILE=false
else
    if [ ! -f "$RANGE_FILE" ]; then
        echo -e "${RED}[!] File $RANGE_FILE không tồn tại${NC}"
        exit 1
    fi
    echo -e "${GREEN}[✓] Đã tìm thấy file: $RANGE_FILE${NC}"
    SCAN_TARGET="-iL $RANGE_FILE"
    USE_FILE=true
fi

# 2. Nhập số lượng IP mong muốn
echo ""
echo -e "${BLUE}[?] Nhập số lượng IP muốn lấy:${NC}"
read -p "    (Để trống = không giới hạn): " IP_LIMIT_INPUT

if [ -z "$IP_LIMIT_INPUT" ]; then
    echo -e "${YELLOW}[*] Không giới hạn số lượng IP${NC}"
    USE_LIMIT=false
else
    # Chuyển đổi k/K/m/M sang số
    IP_LIMIT_INPUT=$(echo "$IP_LIMIT_INPUT" | tr '[:upper:]' '[:lower:]')
    
    if [[ $IP_LIMIT_INPUT =~ ^([0-9]+\.?[0-9]*)([km]?)$ ]]; then
        NUM="${BASH_REMATCH[1]}"
        UNIT="${BASH_REMATCH[2]}"
        
        case $UNIT in
            k)
                IP_LIMIT=$(echo "$NUM * 1000" | bc | cut -d'.' -f1)
                ;;
            m)
                IP_LIMIT=$(echo "$NUM * 1000000" | bc | cut -d'.' -f1)
                ;;
            *)
                IP_LIMIT=$NUM
                ;;
        esac
        
        echo -e "${GREEN}[✓] Sẽ dừng sau khi tìm được $IP_LIMIT IPs${NC}"
        USE_LIMIT=true
    else
        echo -e "${RED}[!] Format không hợp lệ${NC}"
        exit 1
    fi
fi

# 3. Chọn port
echo ""
echo -e "${BLUE}[?] Chọn port để quét:${NC}"
echo "    1) Port 80 (HTTP)"
echo "    2) Port 443 (HTTPS)"
echo "    3) Port 80,443 (cả hai)"
echo "    4) Tùy chỉnh"
read -p "    Lựa chọn [1-4]: " PORT_CHOICE

case $PORT_CHOICE in
    1) PORTS="80" ;;
    2) PORTS="443" ;;
    3) PORTS="80,443" ;;
    4) 
        read -p "    Nhập ports (VD: 80,443,22,8080): " PORTS
        ;;
    *) 
        echo -e "${YELLOW}[*] Mặc định dùng port 80${NC}"
        PORTS="80"
        ;;
esac

# 4. Chọn rate
echo ""
echo -e "${BLUE}[?] Chọn tốc độ quét:${NC}"
echo "    1) Chậm - 10,000 pps (an toàn)"
echo "    2) Trung bình - 30,000 pps (khuyến nghị)"
echo "    3) Nhanh - 50,000 pps"
echo "    4) Rất nhanh - 100,000 pps"
echo "    5) Tùy chỉnh"
read -p "    Lựa chọn [1-5]: " RATE_CHOICE

case $RATE_CHOICE in
    1) RATE="10000" ;;
    2) RATE="30000" ;;
    3) RATE="50000" ;;
    4) RATE="100000" ;;
    5) 
        read -p "    Nhập rate (packets/s): " RATE
        ;;
    *) 
        echo -e "${YELLOW}[*] Mặc định dùng rate 30000${NC}"
        RATE="30000"
        ;;
esac

# 5. Tên file output
echo ""
read -p "$(echo -e ${BLUE}[?] Tên file output \(mặc định: result.txt\): ${NC})" OUTPUT_FILE
OUTPUT_FILE=${OUTPUT_FILE:-result.txt}

# 6. Timeout (tùy chọn)
echo ""
read -p "$(echo -e ${BLUE}[?] Giới hạn thời gian \(giây, để trống = không giới hạn\): ${NC})" TIMEOUT

# ===== XÁC NHẬN =====
echo ""
echo -e "${YELLOW}════════════════════════════════════════${NC}"
echo -e "${YELLOW}         XÁC NHẬN THÔNG TIN${NC}"
echo -e "${YELLOW}════════════════════════════════════════${NC}"
if [ "$USE_FILE" = true ]; then
    echo -e "File ranges  : ${GREEN}$RANGE_FILE${NC}"
else
    echo -e "Target       : ${GREEN}0.0.0.0/0 (toàn bộ Internet)${NC}"
fi
echo -e "Ports        : ${GREEN}$PORTS${NC}"
echo -e "Rate         : ${GREEN}$RATE pps${NC}"
if [ "$USE_LIMIT" = true ]; then
    echo -e "Giới hạn IP  : ${GREEN}$IP_LIMIT IPs${NC}"
else
    echo -e "Giới hạn IP  : ${GREEN}Không giới hạn${NC}"
fi
if [ ! -z "$TIMEOUT" ]; then
    echo -e "Timeout      : ${GREEN}$TIMEOUT giây${NC}"
else
    echo -e "Timeout      : ${GREEN}Không giới hạn${NC}"
fi
echo -e "Output file  : ${GREEN}$OUTPUT_FILE${NC}"
echo -e "${YELLOW}════════════════════════════════════════${NC}"
echo ""

read -p "$(echo -e ${GREEN}Bắt đầu quét? \(y/n\): ${NC})" CONFIRM
if [[ ! $CONFIRM =~ ^[Yy]$ ]]; then
    echo -e "${RED}[!] Đã hủy${NC}"
    exit 0
fi

# ===== CHẠY QUÉT =====
echo ""
echo -e "${GREEN}[+] Bắt đầu quét...${NC}"
echo -e "${YELLOW}[*] Nhấn Ctrl+C để dừng${NC}"
echo ""

TEMP_FILE="temp_scan_$$.txt"
START_TIME=$(date +%s)

# Xây dựng lệnh masscan
if [ "$USE_FILE" = true ]; then
    MASSCAN_CMD="masscan -iL $RANGE_FILE -p $PORTS --rate $RATE -oL $TEMP_FILE"
else
    # Chỉ thêm --exclude khi quét toàn bộ Internet
    MASSCAN_CMD="masscan 0.0.0.0/0 -p $PORTS --rate $RATE --exclude 255.255.255.255 -oL $TEMP_FILE"
fi

# Thêm timeout nếu có
if [ ! -z "$TIMEOUT" ]; then
    MASSCAN_CMD="timeout $TIMEOUT $MASSCAN_CMD"
fi

# Chạy masscan
eval $MASSCAN_CMD

SCAN_EXIT_CODE=$?

# Xử lý kết quả
echo ""
echo -e "${YELLOW}[*] Đang xử lý kết quả...${NC}"

if [ -f "$TEMP_FILE" ]; then
    # Lọc IP
    if [ "$USE_LIMIT" = true ]; then
        awk '/open/ {print $4}' "$TEMP_FILE" | sort -u | head -n "$IP_LIMIT" > "$OUTPUT_FILE"
    else
        awk '/open/ {print $4}' "$TEMP_FILE" | sort -u > "$OUTPUT_FILE"
    fi
    
    # Xóa file tạm
    rm -f "$TEMP_FILE"
    
    # Thống kê
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))
    IP_COUNT=$(wc -l < "$OUTPUT_FILE")
    
    echo ""
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    echo -e "${GREEN}         KẾT QUẢ QUÉT${NC}"
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    echo -e "Số IP tìm thấy : ${GREEN}$IP_COUNT${NC}"
    echo -e "Thời gian      : ${GREEN}${DURATION}s ($(($DURATION/60))m $(($DURATION%60))s)${NC}"
    echo -e "File kết quả   : ${GREEN}$OUTPUT_FILE${NC}"
    
    if [ $SCAN_EXIT_CODE -eq 124 ]; then
        echo -e "Trạng thái     : ${YELLOW}Dừng do timeout${NC}"
    elif [ $SCAN_EXIT_CODE -eq 0 ]; then
        echo -e "Trạng thái     : ${GREEN}Hoàn thành${NC}"
    else
        echo -e "Trạng thái     : ${YELLOW}Dừng giữa chừng${NC}"
    fi
    
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    
    # Hiển thị preview
    if [ $IP_COUNT -gt 0 ]; then
        echo ""
        echo -e "${YELLOW}[*] Preview 10 IP đầu tiên:${NC}"
        head -n 10 "$OUTPUT_FILE"
        if [ $IP_COUNT -gt 10 ]; then
            echo "..."
        fi
    fi
else
    echo -e "${RED}[!] Không tìm thấy kết quả${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}[✓] Done!${NC}"FV 