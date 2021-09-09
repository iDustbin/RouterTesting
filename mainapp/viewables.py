import os,sys
sys.path.append(os.path.abspath(os.path.join('..','mainapp')))

from flask import Blueprint,render_template,request,jsonify
from . import db
import json
from .models import Iperf

from subprocess import check_output
import subprocess
import io,json,xmltodict,base64
import urllib

import subprocess

viewables = Blueprint('viewables',__name__)


@viewables.route('/')
def home():
   return render_template('views/home.html')

@viewables.route('/index')
def index():
   return render_template('viewables/index.html')


@viewables.route('/ookla')
def ookla():
   serverList = getServersJson()
   return render_template('viewables/speedtest/ookla.html',serverList=serverList)

@viewables.route('/Ookla_Result',methods=['POST'])
def ooklaPost():
   data = request.data
   jsonData = json.loads(data)

   result = getResult(jsonData['code'])
   obj = {
      "Jitter" : str(result['ping']['jitter']) +" ms",
      "Latency" : str(result['ping']['latency']) + " ms",
      "Download" : str("{0:.2f}".format(int(result['download']['bandwidth'])*0.0000076294)) + " Mbps",
      "Upload" : str("{0:.2f}".format(int(result['upload']['bandwidth'])*0.0000076294)) + " Mbps",
      "Packet Loss" : str("{0:.2f}".format(int(result['packetLoss']))) + " %",
      "ISP" : result['isp'],
      "Location" : result['server']['location'],
      "Server" : result['server']['name'],
   }
   return jsonify(obj)
   print(obj)


@viewables.route('/iperf')
def iperf():
   return render_template('viewables/speedtest/iperf.html')

@viewables.route('/cellmap')
def cellmap():
   return render_template('viewables/cellmap/map.html')

@viewables.route('/ansible')
def ansible():
   return render_template('viewables/ansible/ansible.html')


@viewables.route('/iperf_Result',methods=['POST'])
def iperfPost():
   data = request.data
   jsonData = json.loads(data)

   host,port,para = jsonData['host_name'],jsonData['port'],jsonData['para']
   out = iperfRes(host,port,para)
   out = out.decode()
   print(data)
   return jsonify({"res":out})


# ----------------------------- WebSSH -----------------------------------
@viewables.route('/webssh')
def webssh_view():
   print("SERVER STARTING")
   run_web_ssh_TORNADO()
   print("SERVER STARTED")
   return render_template('webssh/webssh_view.html')

@viewables.route('/datamodel')
def cfgcli():
   print("SERVER STARTING")
   run_web_ssh_TORNADO()
   print("SERVER STARTED")
   return render_template('webssh/cfgcli.html')

@viewables.route('/cfgcli_commands/<load_url>')
def cfgcli_commands(load_url):
   load_url = base64.b64decode(load_url.encode())
   data = getCFGI_COMMANDS(load_url)
   return jsonify({"response":data})

@viewables.route('/cfgcli_execute/<command>/')
def cfgcli_execute(command):
   run_web_ssh_TORNADO()
   return render_template("webssh/cfgcli_execute.html",command=command)


HELP = '''
Usage: iperf [-s|-c host] [options]
iperf [-h|--help] [-v|--version]

Server or Client:
  -p, --port      #         server port to listen on/connect to
  -f, --format    [kmgKMG]  format to report: Kbits, Mbits, KBytes, MBytes
  -i, --interval  #         seconds between periodic bandwidth reports
  -F, --file name           xmit/recv the specified file
  -B, --bind      <host>    bind to a specific interface
  -V, --verbose             more detailed output
  -J, --json                output in JSON format
  --logfile f               send output to a log file
  -d, --debug               emit debugging output
  -v, --version             show version information and quit
  -h, --help                show this message and quit
Server specific:
  -s, --server              run in server mode
  -D, --daemon              run the server as a daemon
  -I, --pidfile file        write PID file
  -1, --one-off             handle one client connection then exit
Client specific:
  -c, --client    <host>    run in client mode, connecting to <host>
  -u, --udp                 use UDP rather than TCP
  -b, --bandwidth #[KMG][/#] target bandwidth in bits/sec (0 for unlimited)
                            (default 1 Mbit/sec for UDP, unlimited for TCP)
                            (optional slash and packet count for burst mode)
  -t, --time      #         time in seconds to transmit for (default 10 secs)
  -n, --bytes     #[KMG]    number of bytes to transmit (instead of -t)
  -k, --blockcount #[KMG]   number of blocks (packets) to transmit (instead of -t or -n)
  -l, --len       #[KMG]    length of buffer to read or write
                            (default 128 KB for TCP, 8 KB for UDP)
  --cport         <port>    bind to a specific client port (TCP and UDP, default: ephemeral port)
  -P, --parallel  #         number of parallel client streams to run
  -R, --reverse             run in reverse mode (server sends, client receives)
  -w, --window    #[KMG]    set window size / socket buffer size
  -M, --set-mss   #         set TCP/SCTP maximum segment size (MTU - 40 bytes)
  -N, --no-delay            set TCP/SCTP no delay, disabling Nagle's Algorithm
  -4, --version4            only use IPv4
  -6, --version6            only use IPv6
  -S, --tos N               set the IP 'type of service'
  -Z, --zerocopy            use a 'zero copy' method of sending data
  -O, --omit N              omit the first n seconds
  -T, --title str           prefix every output line with this string
  --get-server-output       get results from server
  --udp-counters-64bit      use 64-bit counters in UDP test packets

[KMG] indicates options that support a K/M/G suffix for kilo-, mega-, or giga-

iperf3 homepage at: http://software.es.net/iperf/
Report bugs to:     https://github.com/esnet/iperf
        '''.encode()


def iperfRes(host,port,para):
    para = para.split(" ")
    para = [x for x in para if x != ""]
    parameter = ["iperf3","-c",host,"-p",port]
    [parameter.append(x) for x in para]
    if not host or not port or "-h" in parameter:
        return HELP
    try:
        out = check_output(parameter)
        add_result = Iperf(
            result=out.decode()
        )
        db.session.add(add_result)
        db.session.commit()
        print(add_result)  
    except:
        out = "iPerf Returned Error! Something wrong happed (Server Busy / Wrong Parameter)".encode()
    return out
    print(add_result)

def run_web_ssh_TORNADO():
    try:
        subprocess.Popen(["python3","Features/main.py"],stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    except:
        subprocess.Popen(["python","Features/main.py"],stdin=subprocess.PIPE, stdout=subprocess.PIPE)

def getCFGI_COMMANDS(load_url):
    json_data = []
    data_dict = None

    try:
        link = load_url.decode()
        f = urllib.request.urlopen(link)
        myfile = f.read()
        data_dict = xmltodict.parse(myfile)
        try:
            try:
                for obj in data_dict['dm:document']['model']['object']:
                    json_data.append(obj)
                return json_data
            except:
                for obj in data_dict['dm:document']['model']:
                    for ob in obj['object']:
                        json_data.append(ob)
                return json_data
        except :
            for components in data_dict['dm:document']['component']:
                try:
                    for obj in components['object']:
                        if type(obj)!=type('str'):
                            json_data.append(obj)
                except:
                    pass
            return json_data
    except:
        return {
            "ERROR" : "INVALID STRUCTURE OR URL"
        }
    


def getServers():
    out = check_output(["speedtest","--list","--accept-license","--accept-gdpr"],shell=True)
    buf = io.StringIO(out.decode())

    servers = []
    for line in buf.readlines():
        line = line.replace(" ", "")
        lists = line.split(")")
        if len(lists)==3:
            code = lists[0].replace(" ", "")
            name = lists[1]+")"
            distance = lists[2].replace("\r\n", "")
            obj = {
                "code":code,
                "name":name,
                "distance":distance,
            }
            servers.append(obj)
    return servers

def getServersJson():
    out = check_output(["./bins/armhf/speedtest","-L","-p","no","-f","json"])
    out = json.loads(out)
    return out

def getResult(sid):
    out = check_output(["./bins/armhf/speedtest","--accept-license","-s",sid,"-p","no","-f","json"])
    out = json.loads(out)
    return out
