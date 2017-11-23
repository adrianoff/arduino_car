import RPi.GPIO as GPIO
import time
import socket

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)

sock = socket.socket()
sock.connect(('coder-life.ru', 9999))
sock.send("HELLO".encode())
sleep_time = 0.04

while True:
    data = sock.recv(1)
    data = data.decode()
    print(data)

    if data == "F":
        GPIO.output(7, GPIO.HIGH)
        time.sleep(sleep_time)
        GPIO.output(7, GPIO.LOW)

    if data == "B":
        GPIO.output(11, GPIO.HIGH)
        time.sleep(sleep_time)
        GPIO.output(11, GPIO.LOW)

    if data == "L":
        GPIO.output(13, GPIO.HIGH)
        time.sleep(sleep_time)
        GPIO.output(13, GPIO.LOW)

    if data == "R":
        GPIO.output(15, GPIO.HIGH)
        time.sleep(sleep_time)
        GPIO.output(15, GPIO.LOW)

    GPIO.output(7, GPIO.LOW)
    GPIO.output(11, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    GPIO.output(15, GPIO.LOW)


GPIO.cleanup()
