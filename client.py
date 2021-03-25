import os, sys
import argparse
import socket
import json
import pathlib


class Client:
    def create_socket(self):
         try:
            userInput = input().split()
            cmd = userInput[0]
            if cmd == 'connect':
                serverAddress = userInput[1]
                serverPort = int(userInput[2])
                serverAddress = (serverAddress, serverPort)
                clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                clientSocket.connect(serverAddress)
                print("Successfully connected")
                while True:
                    try:
                        userInput = input().split()
                        cmd = userInput[0]
                        if cmd == 'get' and len(userInput) == 2:
                            fileName = userInput[1].strip('/')
                            self.getFile(clientSocket,fileName)


                        elif cmd == 'put' and len(userInput) == 3:
                            sourceFile= userInput[1].strip('/')
                            fileName = userInput[2]
                            self.putFile(clientSocket, sourceFile, fileName)


                        elif cmd == 'delete' and len(userInput) == 2:
                            fileName = userInput[1].strip('/')
                            self.DeleteTheFile(clientSocket,fileName)

                        elif cmd == 'disconnect' and len(userInput) == 1:
                            self.disconnect(clientSocket)
                            break

                    except KeyboardInterrupt:
                        self.disconnect(clientSocket)
                        break
         except:
            print("No server")

    def getFile(self,clientSocket,fileName):
        data = {
            "message": "request",
            "type": "GET",
            "target": fileName
        }
        clientSocket.send(bytes(json.dumps(data), encoding='utf-8'))
        r_msg = clientSocket.recv(1024)
        msg = json.loads(r_msg)

        if msg["statuscode"] == 200:
            print(msg["content"])
        elif msg["statuscode"] == 400:
            print('Not Found')
        elif msg["statuscode"] == 401:
            print(msg["content"])


    def putFile(self, clientSocket, sourceFile, fileName):
            with open(sourceFile, 'r') as web:
                content = web.read()
            data = {
                    "message": "request",
                    "type": "PUT",
                    "target": fileName,
                    "content": content
                }
            clientSocket.send(bytes(json.dumps(data), encoding='utf-8'))
            msg = json.loads(clientSocket.recv(1024))
            if msg["statuscode"] == 201:
                print(msg['content'])
            elif msg["statuscode"] == 202:
                print(msg['content'])
            elif msg["statuscode"] == 401:
                print(msg["content"])


    def DeleteTheFile(self,clientSocket, fileName):
        data = {
            "message": "request",
            "type": "DELETE",
            "target": fileName,
        }
        clientSocket.send(bytes(json.dumps(data), encoding='utf-8'))
        msg = json.loads(clientSocket.recv(1024))
        if msg["statuscode"] == 203:
            print('Ok')
        elif msg["statuscode"] == 400:
            print('Not Found')
        elif msg["statuscode"] == 401:
            print(msg["content"])


    def disconnect(self, clientSocket):
        data = {
            "message": "request",
            "type": "DISCONNECT",
        }
        clientSocket.send(bytes(json.dumps(data), encoding='utf-8'))
        print("Successfully disconnected")
        clientSocket.close()




if __name__=='__main__':
    client = Client()
    client.create_socket()