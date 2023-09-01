import socket

HOST = '127.0.0.1'
PORT = 65432
BUFFER_SIZE = 4096  # 4KB
END_MARKER = b'END_OF_FILE'

print("Starting client...")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print(f"Connecting to {HOST}:{PORT}...")
    s.connect((HOST, PORT))
    
    print("Reading video file...")
    with open("your_video.mp4", "rb") as f:
        video_data = f.read()
        
    print(f"Sending {len(video_data)} bytes of data...")
    s.sendall(video_data)
    s.sendall(END_MARKER)
    print("Data sent.")

    
    print("Receiving compressed video data...")
    received_data = bytearray()  # ここでbytearrayを初期化
    while True:
        chunk = s.recv(BUFFER_SIZE)  # 4096バイトずつ受信
        if not chunk:
            break  # 受信データがなくなったらループを抜ける
        received_data.extend(chunk)  # 受信データをbytearrayに追加
    print(f"Received total of {len(received_data)} bytes of compressed data.")
    
    print("Writing received data to file...")
    with open("received_compressed_video.mp4", "wb") as f:
        f.write(received_data)
