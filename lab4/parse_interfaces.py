import json
import os

def load_data(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def print_table(data):
    print("Interface Status")
    print("=" * 80)
    print("{:<50} {:<20} {:<8} {:<8}".format("DN", "Description", "Speed", "MTU"))
    print("-" * 80)
    for item in data.get("imdata", []):
        attributes = {}
        if "l1PhysIf" in item:
            attributes = item["l1PhysIf"].get("attributes", {})
        else:
            for v in item.values():
                if isinstance(v, dict) and "attributes" in v:
                    attributes = v.get("attributes", {})
                    break
        dn = attributes.get("dn", "")
        descr = attributes.get("descr", "")
        speed = attributes.get("speed", "")
        mtu = attributes.get("mtu", "")
        print("{:<50} {:<20} {:<8} {:<8}".format(dn, descr, speed, mtu))

if __name__ == "__main__":
    data = load_data("sample-data.json")
    print_table(data)
