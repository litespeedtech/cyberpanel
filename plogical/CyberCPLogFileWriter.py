import subprocess
import time


class CyberCPLogFileWriter:
    fileName = "/home/cyberpanel/error-logs.txt"

    @staticmethod
    def writeToFile(message):
        try:
            file = open(CyberCPLogFileWriter.fileName,'a')
            file.writelines("[" + time.strftime(
                    "%m.%d.%Y_%H-%M-%S") + "] "+ message + "\n")
            file.close()

        except BaseException as msg:
            return "Can not write to error file."

    @staticmethod
    def writeforCLI(message, level, method):
        try:
            file = open(CyberCPLogFileWriter.fileName, 'a')
            file.writelines("[" + time.strftime(
                "%m.%d.%Y_%H-%M-%S") + "] [" + level + ":" + method + "] " + message + "\n")
            file.close()
            file.close()
        except BaseException:
            return "Can not write to error file!"

    @staticmethod
    def readLastNFiles(numberOfLines,fileName):
        try:

            lastFewLines = str(subprocess.check_output(["tail", "-n",str(numberOfLines),fileName]).decode("utf-8"))

            return lastFewLines

        except subprocess.CalledProcessError as msg:
            return "File was empty"

    @staticmethod
    def statusWriter(tempStatusPath, mesg, append = None):
        try:
            if append == None:
                statusFile = open(tempStatusPath, 'w')
            else:
                statusFile = open(tempStatusPath, 'a')
            statusFile.writelines(mesg + '\n')
            statusFile.close()
            print((mesg + '\n'))
        except BaseException as msg:
            CyberCPLogFileWriter.writeToFile(str(msg) + ' [statusWriter]')
            #print str(msg)


