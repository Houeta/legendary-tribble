import json
import os



def check_if_file_exists(filename):
    if not os.path.isfile(filename):
        print(f"File {filename} doesn't exists. Creating..")
        with open(filename, 'w') as f:
            json.dumps({'devices':[],'links':[]})
        
def load_network_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def get_last_id(data):
    last_id = 0
    for device in data['devices']:
        if device['id'] > last_id:
            last_id = device['id']
    return last_id
        
def find_id_by_ip(data, target_ip):
    for device in data['devices']:
        if device['ip'] == target_ip:
            return device['id']

def write_json(new_data, key, filename):
    with open(filename, 'r+',) as file:
        file_data = json.load(file)
        # print(file_data)
        # print(new_data)
        file_data[key].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=2)
        

if __name__ == '__main__':
    json_file = "network.json"
    check_if_file_exists(json_file)
    
    json_data = load_network_data(json_file)
    last_id = get_last_id(json_data)
    
    print('Add node to netowrk sctructure')
    vendor = input("Vendor: ")
    city = input("City: ")
    ip = input("IP: ")
    uplink_ip = input("Uplink IP: ")
    uplink_id = find_id_by_ip(json_data,uplink_ip)
    if uplink_id is None and uplink_ip:
        raise Exception('This uplink IP doesn\'t exists. Please, enter primary node first.')
    check_id = find_id_by_ip(json_data, ip)
    if check_id:
        raise Exception(f"IP {ip} already exists. ID:{check_id}")
    capacity = {
        'downlink': input('Downlink capacity: '),
        'uplink': input('Uplink capacity: ')
    }
    
    x = {
            'id': int(last_id) + 1,
            'name': f"{vendor}-{city}",
            'vendor': vendor,
            'city': city,
            'ip': ip,
        }
    write_json(x, 'devices', json_file)
    if uplink_ip and capacity:
        links = {
                'source': uplink_id,
                'target': int(last_id) + 1,
                'souce_capacity': capacity['uplink'],
                'target_capacity': capacity['downlink']
                }
        write_json(links, 'links', filename=json_file)