#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

def parse_args():
    """ Parse command line arguments """
    try:
        import argparse
    except:
        print "python-argparse is needed"
        sys.exit(0)

    parser = argparse.ArgumentParser(description="Description of send_attachments program")
    parser.add_argument("--destination","-d",metavar="DESTINATIONS",type=lambda d:d.split(","),required=True,help="Destinations of mails")
    parser.add_argument("--cc",metavar="DESTINATIONS",type=lambda d:d.split(","),default=[],help="CC Destinations of mails")
    parser.add_argument("--bcc",metavar="DESTINATIONS",type=lambda d:d.split(","),default=[],help="BCC Destinations of mails")
    parser.add_argument("--sender","-s",metavar="SENDER",help="Sender of mails")
    parser.add_argument("--folder",metavar="FOLDER",help="Folder where to find attachment")
    parser.add_argument("--file",metavar="FILE",help="File to send")
    parser.add_argument("--subject","-t",metavar="SUBJECT",help="Subject of mails")
    parser.add_argument("--content","-c",metavar="CONTENT",help="Content of mails")
    parser.add_argument("--size-max",metavar="MAX_SIZE",type=lambda x:b2m(int(x)),default=b2m(10),help="Size max of a mail in mega")
    parser.add_argument("--server",metavar="SERVER",default="localhost",help="SMTP server to use")
    return parser.parse_args()

def b2m(b):
    """ Bytes to Mega """
    return b*1024*1024

def sizeof(path):
    return os.stat(path).st_size

def send_mail(sender,destinations,cc=[],bcc=[],subject="",content="",attachments=[],server="localhost"):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = COMMASPACE.join(destinations)
    if len(cc) > 0: msg['CC'] = COMMASPACE.join(cc)
    if len(bcc) > 0: msg['BCC'] = COMMASPACE.join(bcc)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(content))

    for a in attachments:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(a,"rb").read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(a))
        msg.attach(part)

    destinations = destinations + cc + bcc
    smtp = smtplib.SMTP(server)
    smtp.sendmail(sender, destinations, msg.as_string())
    smtp.close()

def regroup_files(files,size):
    # To be improved
    out = []
    i = 0
    while i<len(files):
        s = 0
        r = []
        while s<size and i<len(files):
            r.append(files[i])
            s += sizeof(files[i])
            i += 1
        out.append(r)
    return out

def main():
    """ Entry Point Program """
    args = parse_args()

    if args.folder:
        for root, dirs, files in os.walk(args.folder):
            attachments = regroup_files([os.path.join(root,f) for f in files],args.size_max)
        i = 1
        for attachment in attachments:
            send_mail(args.sender,args.destination,cc=args.cc,bcc=args.bcc,subject="%s Part %u/%u" % (args.subject,i,len(attachments)),content=args.content,attachments=attachment,server=args.server)
            i += 1
    else:
        send_mail(args.sender,args.destination,cc=args.cc,bcc=args.bcc,subject=args.subject,content=args.content,attachments=[args.file],server=args.server)

    return 0


if __name__ == "__main__":
   sys.exit(main())
