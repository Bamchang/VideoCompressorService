# server.py
import socket
import subprocess

def compress_video(input_file, output_file):
    command = [
        "ffmpeg",
        "-i",
        input_file,
        "-c:v",
        "libx264",
        "-preset",
        "ultrafast",
        "-crf",
        "40",
        output_file,
    ]
    subprocess.run(command)

HOST = '127.0.0.1'
PORT = 65432
BUFFER_SIZE = 4096  # 4KB
input_file = "received_video.mp4"
output_file = "compressed_video.mp4"
END_MARKER = b'END_OF_FILE'

print("Server started. Waiting for connection...")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")

        total_received = 0
        buffer = bytearray()
        print("Receiving data...")
        
        while True:
            chunk = conn.recv(BUFFER_SIZE)  # この行を追加
            if END_MARKER in chunk:  # マーカーを検出
                buffer.extend(chunk[:-len(END_MARKER)])  # マーカー以外の部分を保存
                break
            if not chunk:
                break
            total_received += len(chunk)
            buffer.extend(chunk)
            print(f"Received {total_received} bytes.")
        
        data = buffer
        print(f"Received {len(data)} bytes.")

        print("Writing received data to file...")
        with open(input_file, 'wb') as f:
            f.write(data)

        print("Compressing video...")
        compress_video(input_file, output_file)

        print("Sending compressed video back...")
        with open(output_file, 'rb') as f:
            compressed_data = f.read()
            print(f"Compressed data size: {len(compressed_data)} bytes")
        conn.sendall(compressed_data)
        print("Data sent back to client.")
