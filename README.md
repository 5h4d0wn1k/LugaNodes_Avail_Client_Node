# LugaNodes Avail Client Node Monitor

[![last commit](https://img.shields.io/github/last-commit/5h4d0wn1k/LugaNodes_Avail_Client_Node)](https://github.com/5h4d0wn1k/LugaNodes_Avail_Client_Node)
[![issues](https://img.shields.io/github/issues/5h4d0wn1k/LugaNodes_Avail_Client_Node)](https://github.com/5h4d0wn1k/LugaNodes_Avail_Client_Node)

Avail light client availability monitoring stack: a Flask web dashboard that
proxies the Avail Light Client REST API, Prometheus scrape config for node
metrics, and an nginx reverse-proxy template in front of both services.

## Why

Running an Avail (Availproject) light client means staying on top of block
height, confidence, and node health — but the raw JSON API is not friendly to
inspect. This project wraps the official `api.lightclient.mainnet.avail.so`
endpoints (`/v1/*` and `/v2/*`) behind a clean Flask UI, so availability can be
monitored from a browser, and exposes the node's Prometheus metrics behind the
same proxy. It is a practical, self-hosted observability setup for Avail node
operators who want a quick dashboard without a full monitoring stack.

## Features

- **Flask API proxy + web UI** (`app.py`) — hyperlinks every Avail Light Client
  v1 and v2 endpoint (`latest_block`, `confidence`, `appdata`,
  `operating_mode`, `status`, `block_status`, `block_header`, `block_data`,
  `submit_data`) and renders the JSON response in the browser.
- **REST passthrough** — GET and POST requests are forwarded to the Avail API
  with query parameters and JSON bodies preserved.
- **Prometheus scraping** (`prometheus.yml`) — a ready job (`availnode`) that
  scrapes the light client's Prometheus exporter on port `9000`, plus the
  standard Prometheus self-scrape.
- **nginx reverse proxy** (`nginxdefault`) — routes `/api` to the Flask app
  (port `5000`) and `/metrics` to Prometheus (port `9090`).
- **Sample node config** (`avail.config.yml`) — example Avail light-client
  bootstrap / RPC / confidence / Prometheus settings for reference.

## Quickstart

### Prerequisites

- Python 3.8+ with `flask` and `requests` installed.

### Run the dashboard

```bash
pip install flask requests
python app.py
```

Open `http://localhost:5000/api` to browse the endpoint list.

### Monitor with Prometheus

```bash
prometheus --config.file=prometheus.yml
```

Prometheus UI: `http://localhost:9090`. The `availnode` scrape target is
`localhost:9000`.

### Reverse proxy (optional)

Apply `nginxdefault` to a site config (replace `server_name` with your host),
then reload nginx so `/api` and `/metrics` are reachable over HTTP.

## Project structure

```
app.py             Flask web UI + REST proxy for the Avail Light Client API
avail.config.yml   Sample Avail light client configuration
prometheus.yml     Prometheus scrape config (availnode job, port 9000)
nginxdefault       nginx reverse-proxy template for /api and /metrics
```

## Contributing

Issues and pull requests are welcome. Please keep changes focused and update
the README only if user-facing behavior changes.

## License

This repository does not currently ship a LICENSE file. Contact the owner
before reuse.