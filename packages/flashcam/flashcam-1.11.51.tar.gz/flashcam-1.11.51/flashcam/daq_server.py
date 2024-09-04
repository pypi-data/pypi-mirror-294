#!/usr/bin/env python3
from fire import Fire
from flashcam.version import __version__
from flashcam.mmapwr import mmwrite # for daq
from console import fg, bg
import os
from flashcam import config
import time
import datetime as dt
#
import tdb_io.influx as influx
import sys
import signal

import logging
logging.basicConfig(
    filename=os.path.expanduser("~/flashcam_daq.log"),
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.INFO,

)
logger = logging.getLogger(__name__)


"""
The idea is
 1/ to take care about PORTS and PIPES, accept just a number (ideally)
 2/ use cfg.json to understand the number
 3/  PIPE is defined HERE like /tmp/flashcam_fifo_x001 ....
"""

PRIMARY_PORT = None # on startup - port is correct, with load_config - can change
MAX_PORTS = 6 # this is UNO+Shield limit to plugin

def test():
    #cmd_ls( ip = ip,db = i['name'], series="all", qlimit = qlimit, output =output)
    if influx.check_port() :
        print("i... influx port present localy")
        commavalues = "a=1,b=2"
        influx.influxwrite( DATABASE="local", MEASUREMENT="flashcam",
                 values=commavalues,
                 IP="127.0.0.1"
                 )
    sys.exit(0)

def is_int(n):
    if str(n).find(".")>=0:  return False
    if n is None:return False
    try:
        float_n = float(n)
        int_n = int(float_n)
    except ValueError:
        return False
    else:
        return float_n == int_n



import socket
import threading

def is_float(n):
    if n is None:return False
    try:
        float_n = float(n)
    except ValueError:
        return False
    else:
        return True

def recalibrate(d, title ):
    """
    d comes as string BUT is sure it is a number; whatever happens, return rounded thing
    """
    res = d
    newtitle = title
    logger.info(f"D...RECAL  {d} ... {type(d)}   /{float(d)}/    /{title}/ ")
    print(f"D...  {d} ... {type(d)}   /{float(d)}/    /{title}/ ")
    if title.endswith("TEMP_phid"):
        res = round( float(d) / 1024* 222.2 - 61.111, 1)
        if title != "TEMP_phid": newtitle = title.replace("TEMP_phid", "")
    elif title.endswith("HUMI_phid"):
        res = round( float(d) / 1024* 190.6 - 40.2, 1)
        if title != "HUMI_phid": newtitle = title.replace("HUMI_phid", "")
    else:
        res = round( float(d), 1)
    print(f"D... ... {res}   {type(res)}  ")
    if newtitle[-1] == "_" and len(newtitle) > 2:
        newtitle = newtitle[:-1]
    logger.info(f"D...RECALfin  {res} ... {newtitle}")
    return res, newtitle


def process_data(data, index):
    """
    fit the incomming data into the format template
    AND - possibly recalculate raw data :)!
 "mminput1_cfg": "dial xxx;22;28;5;signal1",
 "mminput2_cfg": "dial xxx;22;28;5;dial2",
 "mminput3_cfg": "dial xxx;22;28;5;tacho3",
 "mminput4_cfg": "dial xxx;22;28;5;box4",
 "mminput5_cfg": "sub xxx;22;28;5;title5"

    """
    global PRIMARY_PORT
    mynetport = int(PRIMARY_PORT)+index
    d = None # DATA
    try:
        d = data.decode('utf8').strip()
    except:
        d = str(data).strip()
    print(f"i...  {bg.blue}   receivd: /{d}/  on port {mynetport}  {bg.default}")
    print()
    logger.info(f"D...  PDa receivd: /{d}/  on port {mynetport} ")

    if f"mminput{index}" in config.CONFIG:
        mmfile = config.CONFIG[f"mminput{index}"]
    else:
        mmfile = None
        print(fg.red, "X... mmfile not defined", index, fg.default)
        return

    if f"mminput{index}_cfg" in config.CONFIG:
        mmtemplate = config.CONFIG[f"mminput{index}_cfg"]
    else:
        mmtemplate is None
        print(fg.red, "X... template not defined", mynetport, fg.default)
        return


    # prepare recalibration, you need to know title
    #
    if is_float(d) or is_int(d):
        logger.info(f"D...  PDa  1 /{d}/  on port {mynetport} ")
        print(f"DEBUG1 {d}", flush=True)
        mytitle = " ".join(mmtemplate.split(" ")[1:]).split(";")[4]
        print(f"DEBUG2 {d}", flush=True)
        logger.info(f"D...  PDa  2 /{d}/  on port {mynetport} ")
        d, newtitle= recalibrate( d, mytitle ) #  d goes as string returns as float
        print(f"DEBUG3 {d}", flush=True)
        logger.info(f"D...  PDa  3 /{d}/  on port {mynetport} ")
        mmtemplate = mmtemplate.replace("xxx", str(d) ) # FIT THE DATA INTO THE FIELD
        mmtemplate = mmtemplate.replace(mytitle, newtitle ) # FIT THE DATA INTO THE FIELD
        print(f"DEBUG4 {d}", flush=True)
        logger.info(f"D...  PDa  4 /{d}/  on port {mynetport} ")
        mmwrite( mmtemplate, mmfile, PORT_override=PRIMARY_PORT)
        print(f"DEBUG5 {d}", flush=True)
        logger.info(f"D...  PDa  5 /{d}/  on port {mynetport} ")
        print("i... SUCCESS  MMWRITE -----", bg.white, fg.black, mmtemplate, fg.default, bg.default)
        if influx.check_port():
            #print("i... influx port present localy")
            commavalues = f"{mytitle}={d}"
            try:
                influx.influxwrite( DATABASE="local", MEASUREMENT="flashcam",
                                    values=commavalues, IP="127.0.0.1" )
                print("i... OK      WRITING  INFLUX")
                logger.info(f"D...  PDa  InOK /{commavalues}/  on port {mynetport} ")
            except:
                logger.info(f"D...  PDa  InXX /{commavalues}/  on port {mynetport} ")
                print("X... ERROR  WRITING  INFLUX")

    else:# if not float.... make it a box
        mmtemplate = mmtemplate.replace("xxx", d ) # FIT THE DATA INTO THE FIELD
        mmtemplate = mmtemplate.replace("signal", "box" )
        mmtemplate = mmtemplate.replace("dial", "box" )
        mmtemplate = mmtemplate.replace("tacho", "box" )
        logger.info(f"D...  PDa  txt1 /{mmtemplate}/  on port {mynetport} ")
        mmwrite( mmtemplate, mmfile , PORT_override=PRIMARY_PORT)
        print("i... SUCCESS  MMWRITE -----", bg.white, fg.black, mmtemplate, fg.default, bg.default)
        logger.info(f"D...  PDa  txt2 /{mmtemplate}/  on port {mynetport} ")
    print("_____________________________________", dt.datetime.now() )
    pass
#
#
#
def serve_port( PORT, TCP=True):
    """
    watch on PORT
    """
    global PRIMARY_PORT
    PRIMARY_PORT = int(config.CONFIG['netport'])
    s = None
    if TCP:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    ok = False
    try:
        s.bind(('0.0.0.0', PORT))  # Replace 12345 with your port number
        ok = True
    except:
        print(f"X... {bg.orange}{fg.black} DaQ PORT NOT ALLOCATED {PORT} {bg.default}{fg.default} ")

    if not ok:
        try:
            time.sleep(6)
            if TCP:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            else:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('0.0.0.0', PORT))  # Replace 12345 with your port number
            ok = True
        except:
            print(f"X...   {bg.red} DaQ PORT NOT ALLOCATED {PORT} {bg.default} ")

    if not ok: return
    s.listen(5)
    print(f"i...   {bg.blue} Data Acquisition Server started on port {PORT} ;  TCP{TCP} / UDP{not TCP}  {bg.default}")
    while True:


        conn, addr = s.accept() # I hope this is waiting, else 12% of processor taken by load_config
        with conn:
            data = conn.recv(1024)
            if data:
                config.load_config()
                print(f'i... port data Received: {data};  config reloaded')
                process_data(data, PORT - int(PRIMARY_PORT))


# ************************************************************************
#
#
#
# ************************************************************************

def watch_named_fifo(PORT, fifon = '/tmp/flashcam_fifo'):
    """
    In client - use `os.path.exists` to check if the named pipe exists and `os.open` with `os.O_NONBLOCK` to check if it's open:
    """
    global PRIMARY_PORT
    fifoname = f"{fifon}_{PORT}"
    print(f"i...   {bg.darkgreen} Data Acquisition PIPE  started on {fifoname}   {bg.default}")
    if not os.path.exists(fifoname):
        os.mkfifo(fifoname)
    # Wait for the named pipe to be created
    #while not os.path.exists(fifo):
    #    time.sleep(1)
    with open(fifoname, 'r') as fifo_file:
        while True:
            data = fifo_file.readline().strip() # get what comes to PIPE
            if data:
                logger.info(f"*** fifo-readline data=={data} on PORT {PORT} ")
                print(f'i... named pipe Received: {data};  reloading config')
                config.load_config()
                process_data(data, PORT - int(PRIMARY_PORT))
                time.sleep(0.1) # it runs all time.......
            else:
                time.sleep(0.1) # it runs all time.......

# ***************************************************
# ***************************************************
#
#
#
# ***************************************************
# ***************************************************

def main():
    global PRIMARY_PORT
    PRIMARY_PORT = int(config.CONFIG['netport'])
    print()
    def signal_handler(sig, frame):
        print("Exiting with signal handler @bin...")
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    print("D... daq command - starting servers - start separatelly in FG")
    #web.start_daq_servers()
    #def start_daq_servers():
    daq_threads = []
    for i in range(MAX_PORTS ):  # 012345 for 6UNO
        P = int(PRIMARY_PORT) + i + 1 #1-7  resp 8001-8007
        print(f"D... starting server {i} - port {P} *****************")
        daq_threads.append( threading.Thread(
            target=serve_port,  args=( P, )  )  )
        #config.daq_threads[i].daemon = True
        daq_threads[i].start()

    print("D... daq command - starting PIPES - start separatelly in FG")
    #web.start_daq_servers()
    #def start_daq_servers():
    daq_threads_FF = []
    for i in range(MAX_PORTS ): # 012345 for 6UNO
        P = int(PRIMARY_PORT) + i + 1
        print(f"D... starting PIPE {i} - port {P} ********************")
        daq_threads_FF.append( threading.Thread(
            target=watch_named_fifo,  args=( P, )  )  )
        #config.daq_threads[i].daemon = True
        daq_threads_FF[i].start()


    for i in range(MAX_PORTS ): # 012345 for 6UNO
        daq_threads[i].join()
        daq_threads_FF[i].join()
    exit(0)

if __name__ == "__main__":
    Fire(test)
    Fire(main)
