import json
from pyvis.network import Network

def load_network_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def build_network_graph(data):
    net = Network(height="1080px", width="1920px")
    
    devices = {device['id']: device for device in data['devices']}
    

    for device in data['devices']:
        net.add_node(device['id'], label=device['name'], title=device['ip'])
    
    for link in data['links']:
        if '10G' in link['souce_capacity'] and '10G' in link['target_capacity']:
            edge_color = 'green'
        elif   '10G' in link['souce_capacity'] or '10G' in link['target_capacity']:
            edge_color = 'yellow'
        elif '1G' in link['souce_capacity'] and '1G' in link['target_capacity']:
            edge_color = 'red'
        else:
            edge_color = 'grey'
        net.add_edge(link['source'], link['target'], title= f"Up:{link['souce_capacity']} -> Down:{link['target_capacity']}", color=edge_color, width=5)
    
    return net, devices

def highlight_path(net, devices, target_ip):
    target_device = next((device for device in devices.values() if device['ip'] == target_ip), None)
    
    if not target_device:
        print("Device with IP not found in the network.")
        return

    path = []
    visited = set()

    def dfs(device_id):
        if device_id in visited:
            return False
        visited.add(device_id)
        path.append(device_id)
        if devices[device_id]['ip'] == target_ip:
            return True
        for neighbor in net.neighbors(device_id):
            if dfs(neighbor):
                return True
        path.pop()
        return False

    start_device = next(iter(devices))
    dfs(start_device)

    for node in net.nodes:
        if node['id'] in path:
            node['color'] = 'red'
    
    for edge in net.edges:
        if edge['from'] in path and edge['to'] in path:
            edge['color'] = 'red'
    
    # Print verbose path as str
            
        

def main(file_path, target_ip):
    data = load_network_data(file_path)
    net, devices = build_network_graph(data)
    highlight_path(net, devices, target_ip)
    net.show('network.html', notebook=False)

# Example usage
json_file = 'network.json'
target_ip = '10.255.4.73'
main(json_file, target_ip)