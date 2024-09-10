# LugaNodes_Avail_Client_Node
# Live End points

http://52.158.44.230/api
http://52.158.44.230/metrics

# **Setting Up a VM in Azure**

### Step 1: Create a Free Trial Account in Azure

- Go to the Azure website and sign up for a free trial account.

### Step 2: Start a New VM

### Prerequisites

- 2/4 CPU
- 8GB or 16GB RAM
- Ubuntu OS

### Step 3: Download the .pem Key

- Download the `.pem` key file from Azure.

### Step 4: Connect via SSH using the .pem Key

- Open a terminal and run the following command:

```bash
ssh -i /home/cynik/Downloads/Availnodes_key.pem azureuser@52.158.44.230
```

- This will start a CLI session via SSH.

Setting up avail client node

- Install the prerequisites
    
    ### **1. Setting Up Abel Lite Client**
    
    ### **Prerequisites**
    
    1. **Install Rust & Cargo**
        
        ```bash
        curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
        source $HOME/.cargo/env
        ```
        
    2. Install Go
        
        ```bash
        wget https://dl.google.com/go/go1.19.4.linux-amd64.tar.gz
        sudo tar -C /usr/local -xzf go1.19.4.linux-amd64.tar.gz
        export PATH=$PATH:/usr/local/go/bin
        ```
        
    3. Update the system 
        
        ```bash
        sudo apt update
        sudo apt upgrade -y
        sudo apt dist-upgrade -y
        sudo apt-get full-upgrade
        sudo apt autoremove -y
        sudo apt clean
        ```
        

### 2. Cloning & Building up the Avail light client

- **Clone the Repository**
    
    ```bash
    git clone https://github.com/availproject/avail-light.git
    cd /avail-light/target/release/
    ```
    
- Buiding the Client
    
    ```bash
    cargo build --release
    ```
    

### 3. Configuring Avail light client node

- Editing the config file
    
    ```bash
    sudo nano /home/azureuser/.avail/mainnet/config/config.yml
    ```
    
- Configuring to turn on the rpc and prometheus via config.yml
    
    ```yaml
    bootstraps=['/dns/bootnode.1.lightclient.mainnet.avail.so/tcp/37000/p2p/12D3KooW9x9qnoXhkHAjdNFu92kMvBRSiFBMAoC5NnifgzXjsuiM']
    full_node_ws=['wss://mainnet-rpc.avail.so/ws','wss://mainnet.avail-rpc.com','wss://avail-mainnet.public.blastapi.io']
    confidence=80.0
    avail_path='/home/azureuser/.avail/mainnet/data'
    kad_record_ttl=43200
    genesis_hash='b91746b45e0346cc2f815a520b9c6cb4d5c0902af848db0a80f85932d2e8276a'
    ot_collector_endpoint='http://otel.lightclient.mainnet.avail.so:4317'
    prometheus_port=9000
    ```
    
- Testing & Running the Node
    
    ```yaml
    ./home/avail-light/target/release/avail-light-client --configure /home/azureuser/.avail/mainnet/config/config.yml
    
    ```
    

### **4. Install Prometheus**

1. **Download Prometheus:**
    
    ```bash
    wget <https://github.com/prometheus/prometheus/releases/download/v2.43.0/prometheus-2.43.0.linux-amd64.tar.gz>
    ```
    
2. **Extract the Tarball:**
    
    ```bash
    tar xvf prometheus-2.43.0.linux-amd64.tar.gz
    ```
    
3. **Move to /usr/local/bin:**
    
    ```bash
    sudo mv prometheus-2.43.0.linux-amd64/prometheus /usr/local/bin/
    sudo mv prometheus-2.43.0.linux-amd64/promtool /usr/local/bin/
    ```
    
4. **Create Directories for Prometheus Data and Config:**
    
    ```bash
    sudo mkdir /etc/prometheus
    sudo mkdir /var/lib/prometheus
    ```
    
5. **Move Configuration Files:**
    
    ```bash
    sudo mv prometheus-2.43.0.linux-amd64/prometheus.yml /etc/prometheus/
    ```
    
6. **Clean Up:**
    
    ```bash
    rm -rf prometheus-2.43.0.linux-amd64
    rm prometheus-2.43.0.linux-amd64.tar.gz
    ```
    

### **5. Configure Prometheus**

1. **Edit the Configuration File:**
    
    ```bash
    sudo nano /etc/prometheus/prometheus.yml
    ```
    
    My Configuration
    
    ```yaml
    # my global config
    global:
      scrape_interval: 15s 
      evaluation_interval: 15s
    alerting:
      alertmanagers:
        - static_configs:
            - targets:
    rule_files:
      # - "first_rules.yml"
      # - "second_rules.yml"
    scrape_configs:
      - job_name: "prometheus"
        static_configs:
          - targets: ["localhost:9090"]
      - job_name: "availnode"
    	  static_config:
    		  -targets: ["localhost:9000"]
    ```
    

**Check Prometheus Status:**

```bash
sudo systemctl status prometheus
```

- Access web interface and due to our configuration in prometheus
    - it will host all the metrices of Avail Client Node and all metrices in
    - `http://localhost:9090/metrices`
    - And its web interface will be at
    - `http://localhost:9090/`
    

## 5. Getting the /api

From documentation from here 
https://docs.availproject.org/api-reference/avail-lc-api

I can get all the details via api directly but since I wasn’t able to understand much about it 

I tried running multiple commands in the curl with the links of avail api

for ex 

```bash
curl "https://api.lightclient.mainnet.avail.so/v2/version"
```

from there i got the little idea about all the things of api and tried to implement it with making my own flask server with web interface to get the api end points 

I hosted it localy 

first 

- Create a [app.py](http://app.py) file

```bash
sudo nano app.py
```

- Creating the flask server hosted on local host on :5000 port for api

```python
from flask import Flask, jsonify, request, render_template_string
import requests

app = Flask(__name__)

# Base URL for the Avail Light Client API
BASE_URL = "https://api.lightclient.mainnet.avail.so"

# List of available endpoints
ENDPOINTS = [
    "/v1/latest_block",
    "/v1/confidence",
    "/v1/appdata",
    "/v1/operating_mode",
    "/v1/status",
    "/v2/latest_block",
    "/v2/status",
    "/v2/block_status",
    "/v2/block_header",
    "/v2/block_data",
    "/v2/submit_data"
]

# HTML template for the home page
HOME_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>Avail Light Client API</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        h1 { color: #333; }
        a { display: block; margin: 10px 0; color: #1a73e8; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>Welcome to the Avail Light Client API!</h1>
    <p>Available endpoints:</p>
    {% for endpoint in endpoints %}
        <a href="{{ url_for('show_endpoint_result', path=endpoint.strip('/')) }}" target="_blank">{{ request.host_url }}api{{ endpoint }}</a>
    {% endfor %}
</body>
</html>
"""

# HTML template for displaying API results
RESULT_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>API Result</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        h1 { color: #333; }
        pre { background-color: #f0f0f0; padding: 10px; border-radius: 5px; overflow-x: auto; }
        .error { color: red; }
        a { color: #1a73e8; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>{% if error %}Error{% else %}Result for Endpoint: {{ url }}{% endif %}</h1>
    <pre{% if error %} class="error"{% endif %}>{{ response }}</pre>
    <a href="{{ url_for('home') }}">Back to Home</a>
</body>
</html>
"""

@app.route('/api')
def home():
    return render_template_string(HOME_TEMPLATE, endpoints=ENDPOINTS)

def forward_request(url, method, params=None, data=None):
    try:
        if method == 'GET':
            response = requests.get(url, params=params)
        elif method == 'POST':
            response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json(), False
    except requests.RequestException as e:
        return {"error": str(e)}, True

@app.route('/api/<path:path>', methods=['GET', 'POST'])
def dynamic_endpoint(path):
    url = f"{BASE_URL}/{path}"
    if request.method == 'GET':
        response_data, is_error = forward_request(url, 'GET', params=request.args)
    elif request.method == 'POST':
        response_data, is_error = forward_request(url, 'POST', data=request.json)
    return jsonify(response_data), 500 if is_error else 200

@app.route('/api/show/<path:path>', methods=['GET'])
def show_endpoint_result(path):
    url = f"{BASE_URL}/{path}"
    response_data, is_error = forward_request(url, 'GET', params=request.args)
    response_str = jsonify(response_data).data.decode('utf-8')
    return render_template_string(RESULT_TEMPLATE, url=url, response=response_str, error=is_error)

if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0', port=5000)
```

To run it in the background 

```python
# to run it in back ground 
nohup python3 app.py > app.log 2>&1 &
```

This code runned all the api commands in the machine and showed the results on the web 

### 6. Setting up End points via nginx http server

### **1. Install Nginx**

**Update & Installation & Setup of Package :**

```
sudo apt update
sudo apt install nginx -y
sudo systemctl start nginx
sudo systemctl status nginx
sudo ufw allow 'Nginx Full'
```

**Configure Nginx**

Nginx configuration files are typically located in /etc/nginx/. The main configuration file is /etc/nginx/nginx.conf, and site-specific configurations are stored in /etc/nginx/sites-available/ and linked to /etc/nginx/sites-enabled/.

```
sudo nano /etc/nginx/sites-available/default
```

Replace the existing content with the following configuration:

```
server {
    listen 80;
    server_name 52.158.44.230;

    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /metrics {
        proxy_pass http://localhost:9090/metrics;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Then save it and test it 

```python
sudo nginx -t
sudo systemctl reload nginx
sudo systemctl restart nginx
curl http://52.158.44.230/api
curl http://52.158.44.230/metrics
```

## Optional

1. Install Grafana

On Debian/Ubuntu:

```python
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
sudo apt update
sudo apt install -y grafana
```

Start Grafana

```python
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
```

Access Grafana

Open your web browser and go to [http://localhost:3000](http://localhost:3000/). The default login credentials are:

```
Username: admin
Password: admin
```

Connect it to targets and data sources of this 

```python
http://localhost:9090 

	prometheus
```

Then you can setup your dashboard accordingly
