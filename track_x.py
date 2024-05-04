import cv2

# Hàm xử lý sự kiện khi chuột di chuyển
def mouse_event(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        print(f"Tọa độ x: {x}")

# Đọc hình ảnh
image = cv2.imread('bg1.png')

# Tạo cửa sổ hiển thị hình ảnh
cv2.namedWindow('Image')

# Liên kết sự kiện chuột với hàm xử lý sự kiện
cv2.setMouseCallback('Image', mouse_event)

# Hiển thị hình ảnh và chờ sự kiện
while True:
    cv2.imshow('Image', image)
    if cv2.waitKey(1) & 0xFF == 27:  # ấn ESC để thoát
        break

# Đóng cửa sổ khi kết thúc
cv2.destroyAllWindows()
