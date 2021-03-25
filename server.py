import argparse
import sys, os
import socket
import json
import pathlib
from pathlib import Path
from threading import Thread
#from SocketServer import ThreadingMixIn

parser = argparse.ArgumentParser()
parser.add_argument('-p',type=int)
args = parser.parse_args()

class Server(Thread):
    def __init__(self, serverPort):
        Thread.__init__(self)
        self.serverPort = serverPort
        path = 'www'
        isdir = os.path.isdir(path)
        if not isdir:
            os.mkdir(path)
            print("created")
        os.chdir('www')

    def create_socket(self):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind(('127.0.0.1', self.serverPort))
        serverSocket.listen(1)
        cmd, clientAddress = serverSocket.accept()
        while True:
            try:
                data_rec = cmd.recv(1024)
                data = json.loads(data_rec)

                if (data['type']) == 'GET':
                    fileName = data['target']
                    self.sendFileToClient(cmd, fileName)

                elif (data['type']) == 'PUT':
                    fileName = os.path.join(data['target'])
                    fileName = fileName.split(os.path.sep)
                    contentToWrite = data['content']
                    self.getFileFromClient(cmd, fileName, contentToWrite)

                elif (data['type']) == 'DELETE':
                    fileName = data['target']
                    self.deleteTheFile(cmd,fileName)

                elif (data['type']) == 'DISCONNECT':
                    serverSocket.close()
                    print("successfully disconnected")
                    break
                else:
                    data = {
                        "message": "response",
                        "statuscode": 401,
                        "content": "Bad Request"
                    }
                    cmd.send(bytes(json.dumps(data)+'\n','utf-8'))
            except KeyboardInterrupt:
                data = {
                    "content": "interrupt"
                }
                cmd.send(bytes(json.dumps(data),'utf-8'))
                cmd.close()
                break

    def sendFileToClient(self,cmd, fileName):
        if os.path.exists(fileName):
            with open(fileName, 'r') as f:
                bytesToSend = f.read(1024)
                data = {
                    "message": "response",
                    "statuscode": 200,
                    "content": bytesToSend
                }
                cmd.send(bytes(json.dumps(data), 'utf-8'))

        else:
            data = {
                "message": "response",
                "statuscode": 400,
                "content": "Not Found"
            }
            cmd.send(bytes(json.dumps(data) + '\n', 'utf-8'))



    def getFileFromClient(self, cmd, fileName, contentToWrite):
        directory = fileName[1]
        file_name = fileName[2]
        p = Path(directory)
        p.mkdir(exist_ok=True)
        if os.path.exists(file_name):
            (p / file_name ) .open('w').write(contentToWrite)
            data = {
                    "message": "response",
                    "statuscode": 201,
                    "content": "Ok"
            }
            cmd.send(bytes(json.dumps(data) + '\n', 'utf-8'))

        else:
            (p / file_name).open('w').write(contentToWrite)
            data = {
                "message": "response",
                "statuscode": 202,
                "content": "Modified"
            }
            cmd.send(bytes(json.dumps(data) + '\n', 'utf-8'))


    def deleteTheFile(self, cmd, fileName):
        try:
            os.remove(fileName)
            data = {
                "message":"response",
                "statuscode": 203 ,
                "content":"Ok"
                }
            cmd.send(bytes(json.dumps(data)+'\n','utf-8'))

        except:
            data = {
            "message":"response",
            "statuscode": 400 ,
            "content":"Not Found"
            }
            cmd.send(bytes(json.dumps(data)+'\n','utf-8'))



if __name__=='__main__':
    server=Server(args.p) # add args to final program
    server.create_socket()

