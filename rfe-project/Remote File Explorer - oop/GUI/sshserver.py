# from twisted.conch import avatar, recvline
# from twisted.conch.interfaces import IConchUser, ISession
# from twisted.conch.ssh import factory, keys, session
# from twisted.conch.insults import insults
# from twisted.cred import portal, checkers
# from twisted.internet import reactor
# from zope.interface import implements
#
#
# class SSHDemoProtocol(recvline.HistoricRecvLine):
#     def __init__(self, user):
#         self.user = user
#
#     def connectionMade(self):
#         recvline.HistoricRecvLine.connectionMade(self)
#         self.terminal.write("Welcome to my test SSH server.")
#         self.terminal.nextLine()
#         self.do_help()
#         self.showPrompt()
#
#     def showPrompt(self):
#         self.terminal.write("$ ")
#
#     def getCommandFunc(self, cmd):
#         return getattr(self, 'do_' + cmd, None)
#
#     def lineReceived(self, line):
#         line = line.strip()
#         if line:
#             print(line)
#             f = open('logfile.log', 'w')
#             f.write(line + '\n')
#             f.close()
#             cmdAndArgs = line.split()
#             cmd = cmdAndArgs[0]
#             args = cmdAndArgs[1:]
#             func = self.getCommandFunc(cmd)
#             if func:
#                 try:
#                     func(*args)
#                 except Exception as e:
#                     self.terminal.write("Error: %s" % e)
#                     self.terminal.nextLine()
#             else:
#                 self.terminal.write("No such command.")
#                 self.terminal.nextLine()
#         self.showPrompt()
#
#     def do_help(self):
#         publicMethods = filter(
#             lambda funcname: funcname.startswith('do_'), dir(self))
#         commands = [cmd.replace('do_', '', 1) for cmd in publicMethods]
#         self.terminal.write("Commands: " + " ".join(commands))
#         self.terminal.nextLine()
#
#     def do_echo(self, *args):
#         self.terminal.write(" ".join(args))
#         self.terminal.nextLine()
#
#     def do_whoami(self):
#         self.terminal.write(self.user.username)
#         self.terminal.nextLine()
#
#     def do_quit(self):
#         self.terminal.write("Thanks for playing!")
#         self.terminal.nextLine()
#         self.terminal.loseConnection()
#
#     def do_clear(self):
#         self.terminal.reset()
#
#
# class SSHDemoAvatar(avatar.ConchUser):
#     implements(ISession)
#
#     def __init__(self, username):
#         avatar.ConchUser.__init__(self)
#         self.username = username
#         self.channelLookup.update({'session': session.SSHSession})
#
#     def openShell(self, protocol):
#         serverProtocol = insults.ServerProtocol(SSHDemoProtocol, self)
#         serverProtocol.makeConnection(protocol)
#         protocol.makeConnection(session.wrapProtocol(serverProtocol))
#
#     def getPty(self, terminal, windowSize, attrs):
#         return None
#
#     def execCommand(self, protocol, cmd):
#         raise NotImplementedError()
#
#     def closed(self):
#         pass
#
#
# class SSHDemoRealm(object):
#     implements(portal.IRealm)
#
#     def requestAvatar(self, avatarId, mind, *interfaces):
#         if IConchUser in interfaces:
#             return interfaces[0], SSHDemoAvatar(avatarId), lambda: None
#         else:
#             raise NotImplementedError("No supported interfaces found.")
#
#
# def getRSAKeys():
#     with open('id_rsa') as privateBlobFile:
#         privateBlob = privateBlobFile.read()
#         privateKey = keys.Key.fromString(data=privateBlob)
#
#     with open('id_rsa.pub') as publicBlobFile:
#         publicBlob = publicBlobFile.read()
#         publicKey = keys.Key.fromString(data=publicBlob)
#
#     return publicKey, privateKey
#
#
# if __name__ == "__main__":
#     sshFactory = factory.SSHFactory()
#     sshFactory.portal = portal.Portal(SSHDemoRealm())
#
# users = {'admin': 'aaa', 'guest': 'bbb'}
# sshFactory.portal.registerChecker(
#     checkers.InMemoryUsernamePasswordDatabaseDontUse(**users))
# pubKey, privKey = getRSAKeys()
# sshFactory.publicKeys = {'ssh-rsa': pubKey}
# sshFactory.privateKeys = {'ssh-rsa': privKey}
# reactor.listenTCP(22222, sshFactory)
# reactor.run()

#############################################################

# from twisted.internet import reactor, protocol
#
# class ClientEcho(protocol.Protocol):
#     def connectionMade(self):
#         self.transport.write("Hello, world!".encode('utf-8'))
#
#     def dataReceived(self, data):
#         print ("Server: ", data)
#         self.transport.loseConnection()
#
# class FactoryEcho(protocol.ClientFactory):
#     def buildProtocol(self, addr):
#         return ClientEcho()
#
#     def clientConnectionFailed(self, connector, reason):
#         print ("Connection failed")
#         reactor.stop()
#
#     def clientConnectionLost(self, connector, reason):
#         print ("Connection lost")
#         reactor.stop()
#
# reactor.connectTCP("localhost", 8080, FactoryEcho())
# reactor.run()


###############################################################


# from twisted.cred.portal import Portal
# from twisted.conch.ssh.factory import SSHFactory
# from twisted.internet import reactor
# from twisted.conch.ssh.keys import Key
# from twisted.cred.checkers import FilePasswordDB
# from twisted.conch.interfaces import IConchUser
# from twisted.conch.avatar import ConchUser
# from twisted.conch.ssh.channel import SSHChannel
# from twisted.conch.ssh.session import parseRequest_pty_req
# from twisted.internet.protocol import Protocol
# from twisted.conch.ssh.session import SSHSession, SSHSessionProcessProtocol, wrapProtocol
#
# from twisted.python import log
# import sys
#
# log.startLogging(sys.stderr)
#
# with open('id_rsa') as privateBlobFile:
#     privateBlob = privateBlobFile.read()
#     privateKey = Key.fromString(data=privateBlob)
#
# with open('id_rsa.pub') as publicBlobFile:
#     publicBlob = publicBlobFile.read()
#     publicKey = Key.fromString(data=publicBlob)
#
#
# class EchoProtocol(Protocol):
#     def connectionMade(self):
#         self.transport.write("Echo protocol connected\r\n")
#
#     def dataReceived(self, bytes):
#         self.transport.write("echo: " + repr(bytes) + "\r\n")
#
#     def connectionLost(self, reason):
#         print('Connection lost', reason)
#
#
# def nothing():
#     pass
#
#
# class SimpleSession(SSHChannel):
#     name = 'session'
#
#     def dataReceived(self, bytes):
#         self.write("echo: " + repr(bytes) + "\r\n")
#
#     def request_shell(self, data):
#         protocol = EchoProtocol()
#         transport = SSHSessionProcessProtocol(self)
#         protocol.makeConnection(transport)
#         transport.makeConnection(wrapProtocol(protocol))
#         self.client = transport
#         return True
#
#     def request_pty_req(self, data):
#         return True
#
#     def eofReceived(self):
#         print('eofReceived')
#
#     def closed(self):
#         print('closed')
#
#     def closeReceived(self):
#         print('closeReceived')
#
#
# class SimpleRealm(object):
#     def requestAvatar(self, avatarId, mind, *interfaces):
#         user = ConchUser()
#         user.channelLookup['session'] = SimpleSession
#         return IConchUser, user, nothing
#
#
# factory = SSHFactory()
# factory.privateKeys = {'ssh-rsa': privateKey}
# factory.publicKeys = {'ssh-rsa': publicKey}
#
# factory.portal = Portal(SimpleRealm())
# factory.portal.registerChecker(FilePasswordDB("ssh-passwords"))
#
# reactor.listenTCP(2022, factory)
# reactor.run()

#######################################################################

from twisted.cred import portal, checkers, credentials

from twisted.conch import error, avatar, recvline, interfaces as conchinterfaces

from twisted.conch.ssh import factory, userauth, connection, keys, session, common

from twisted.conch.insults import insults

from twisted.application import service, internet

from zope.interface import implements

import os



class SSHDemoProtocol(recvline.HistoricRecvLine):

 def _ _init_ _(self, user):

 self.user = user



 def connectionMade(self):

 recvline.HistoricRecvLine.connectionMade(self)

 self.terminal.write("Welcome to my test SSH server.")

 self.terminal.nextLine( )

 self.do_help( )

 self.showPrompt( )



 def showPrompt(self):

 self.terminal.write("$ ")



 def getCommandFunc(self, cmd):

 return getattr(self, 'do_' + cmd, None)



 def lineReceived(self, line):

 line = line.strip( )

 if line:

 cmdAndArgs = line.split( )

 cmd = cmdAndArgs[0]

 args = cmdAndArgs[1:]

 func = self.getCommandFunc(cmd)

 if func:

 try:

 func(*args)

 except Exception, e:

 self.terminal.write("Error: %s" % e)

 self.terminal.nextLine( )

 else:

 self.terminal.write("No such command.")

 self.terminal.nextLine( )

 self.showPrompt( )



 def do_help(self, cmd=''):

 "Get help on a command. Usage: help command"

 if cmd:

 func = self.getCommandFunc(cmd)

 if func:

 self.terminal.write(func._ _doc_ _)

 self.terminal.nextLine( )

 return



 publicMethods = filter(

 lambda funcname: funcname.startswith('do_'), dir(self))

 commands = [cmd.replace('do_', '', 1) for cmd in publicMethods]

 self.terminal.write("Commands: " + " ".join(commands))

 self.terminal.nextLine( )



 def do_echo(self, *args):

 "Echo a string. Usage: echo my line of text"

 self.terminal.write(" ".join(args))

 self.terminal.nextLine( )



 def do_whoami(self):

 "Prints your user name. Usage: whoami"

 self.terminal.write(self.user.username)

 self.terminal.nextLine( )



 def do_quit(self):

 "Ends your session. Usage: quit"

 self.terminal.write("Thanks for playing!")

 self.terminal.nextLine( )

 self.terminal.loseConnection( )



 def do_clear(self):

 "Clears the screen. Usage: clear"

 self.terminal.reset( )



class SSHDemoAvatar(avatar.ConchUser):

 implements(conchinterfaces.ISession)



 def _ _init_ _(self, username):

 avatar.ConchUser._ _init_ _(self)

 self.username = username

 self.channelLookup.update({'session':session.SSHSession})



 def openShell(self, protocol):
     serverProtocol = insults.ServerProtocol(SSHDemoProtocol, self)
     serverProtocol.makeConnection(protocol)
     protocol.makeConnection(session.wrapProtocol(serverProtocol))



 def getPty(self, terminal, windowSize, attrs):
     return None



 def execCommand(self, protocol, cmd):
     raise NotImplementedError



 def closed(self):
     pass



class SSHDemoRealm:

 implements(portal.IRealm)



 def requestAvatar(self, avatarId, mind, *interfaces):

 if conchinterfaces.IConchUser in interfaces:

 return interfaces[0], SSHDemoAvatar(avatarId), lambda: None

 else:

 raise Exception, "No supported interfaces found."



def getRSAKeys( ):

 if not (os.path.exists('public.key') and os.path.exists('private.key')):

 # generate a RSA keypair

 print "Generating RSA keypair..."

 from Crypto.PublicKey import RSA

 KEY_LENGTH = 1024

 rsaKey = RSA.generate(KEY_LENGTH, common.entropy.get_bytes)

 publicKeyString = keys.makePublicKeyString(rsaKey)

 privateKeyString = keys.makePrivateKeyString(rsaKey)

 # save keys for next time

 file('public.key', 'w+b').write(publicKeyString)

 file('private.key', 'w+b').write(privateKeyString)

 print "done."

 else:

 publicKeyString = file('public.key').read( )

 privateKeyString = file('private.key').read( )

 return publicKeyString, privateKeyString



if __name__ == "_ _main_ _":

 sshFactory = factory.SSHFactory( )

 sshFactory.portal = portal.Portal(SSHDemoRealm( ))

 users = {'admin': 'aaa', 'guest': 'bbb'}

 sshFactory.portal.registerChecker(

 checkers.InMemoryUsernamePasswordDatabaseDontUse(**users))



 pubKeyString, privKeyString = getRSAKeys( )

 sshFactory.publicKeys = {

 'ssh-rsa': keys.getPublicKeyString(data=pubKeyString)}

 sshFactory.privateKeys = {

 'ssh-rsa': keys.getPrivateKeyObject(data=privKeyString)}



 from twisted.internet import reactor

 reactor.listenTCP(2222, sshFactory)

 reactor.run( )