import requests

HOST = "127.0.0.1"
PORT = 8899

CMDS = [
    "start",
    "stop",
]
if __name__ == '__main__':
    # Make a REPL
    while True:
        user_input = input("vocal studio>").strip()
        
        if not user_input:
            continue
        
        if user_input not in CMDS:
            print("Unknown command: %s" % user_input)
            continue

        user_command = user_input.lower()
        

        cmds = []
        
        if user_command == "start":
            cmds.append({"/song/start": {}})
        elif user_command == "stop":
            cmds.append({"/song/stop": {}})
        else:
            print("Unknown command: %s" % user_input)
            continue
        with requests.Session() as s: 
            response = s.post("http://%s:%s" % (HOST, PORT), headers = requests.utils.default_headers(), json=cmds)     
        

