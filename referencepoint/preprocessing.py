import os
os.environ['CLASSPATH'] = 'java/preprocessing.jar:java/math.jar:java/protobufs.jar:java/protobuf-lite-3.0.1.jar'
os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-11-openjdk-amd64/'

from jnius import autoclass

Preprocessing = autoclass('com.navatar.preprocessing.Preprocessing')
String = autoclass("java.lang.String")

prepro = Preprocessing()

prepro.main([String('maps/Luther Blissett School of Urban Geography'), String('test.nvm')])

