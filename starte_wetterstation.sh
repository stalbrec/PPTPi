#!/bin/bash

source ~/PPT-env/bin/activate 
trap_ctrlc() {
		echo "killing wetter ${wetter_pid}"
		kill $wetter_pid
        echo trap_ctrlc
        exit
}

trap trap_ctrlc SIGHUP SIGINT SIGTERM

nohup python3 ~/PPTPi/python/wetter.py &
wetter_pid=$!


cd ~/PPTPi/simple_dashboard

python3 -m http.server
server_pid=$!


