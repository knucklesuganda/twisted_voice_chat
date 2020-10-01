from random import randint

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import pyaudio


class Client(DatagramProtocol):
    def startProtocol(self):
        py_audio = pyaudio.PyAudio()
        self.buffer = 1024  # 127.0.0.1
        self.another_client = input("Write address: "), int(input("Write port: "))

        self.output_stream = py_audio.open(format=pyaudio.paInt16,
                                           output=True, rate=44100, channels=2,
                                           frames_per_buffer=self.buffer)
        self.input_stream = py_audio.open(format=pyaudio.paInt16,
                                          input=True, rate=44100, channels=2,
                                          frames_per_buffer=self.buffer)
        reactor.callInThread(self.record)

    def record(self):
        while True:
            data = self.input_stream.read(self.buffer)
            self.transport.write(data, self.another_client)

    def datagramReceived(self, datagram, addr):
        self.output_stream.write(datagram)


if __name__ == '__main__':
    port = randint(1000, 3000)
    print("Working on port: ", port)

    reactor.listenUDP(port, Client())
    reactor.run()
