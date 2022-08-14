import subprocess
import optparse
import random
import re

def options():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Read wich interface you wanna use")
    parser.add_option("-m", "--mac", dest="new_mac", help="Read you'r the new mac adress")
    parser.add_option("-r", "--random",action='store_true', dest="random", help="If you write -r options you will be have random MAC adress")
    (values, key) = parser.parse_args()

    if not values.interface:
        parser.error("[-] Place enter the interface name, or use the --hellp option")
    elif values.random:
        values.new_mac = rndom_MAC()
    elif not values.new_mac and values.random or values.interface:
        parser.error("[-] Place use the --hellp option")
    return values

def rndom_MAC():
    mac = [ random.randint(0x00,0x9f),
            random.randint(0x00,0x9f),
            random.randint(0x00,0x9f),
            random.randint(0x00, 0x9f),
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0x7f) ]
    return ':'.join(map(lambda x: "%02x" % x, mac))

def changer(interface, new_mac):
    print("[+] Changing MAC adress of interface " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

values = options()
ifconfig_result = subprocess.check_output(["ifconfig", values.interface])
old_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
print(f"[+] you'r old MAC {old_mac}")
changer(values.interface, values.new_mac)
