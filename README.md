# m4.link
A Self Hostable "LinkTree" Clone written with basic Python/Jinja/HTML/CSS. No admin/control server/interface - just configure a `.ini` file and deploy!

## Features
- **Light-Weight** - Generated static HTML at startup served by Python & Jinja
- **Config-Based** - Customize everything via `config.ini`
- **Docker Ready** - Single container deployment
- **Customizable** - Fully customizable style and settings
- **Responsive** - Mobile-friendly design
- **Fast** - It's just static HTML (use caching on your Rervse Proxy/Load Balancer)

## Quick Start

### 1. Create a working directory
We need a folder for our container's compose file and config to live in.

```bash
mkdir /location/of/choice/m4.link && cd /location/of/choice/m4.link
```

### 2. Create the config file
Create a `config.ini` file with your information:

```ini
[profile]
Name=Your Name
Picture=https://example.com/profile.jpg
Description=Your bio here
Avatar_Style=rounded

[settings]
button_style=rounded
button_color=#1DA1F2
Background=https://example.com/background.jpg

[link 1]
Title=My Website
URL=https://example.com
Icon=https://example.com/icon.png
Description=My personal website
Background=#1DA1F2

[link 2]
Title=Tangled
URL=https://tangled.org/
Icon=https://images.com/logo.png
```

### 3. Create the compose file
```yaml
services:
  m4link:
    image: 3rm4zy/m4.link:latest
    container_name: m4link
    user: 1000:1000
    ports:
      - "5000:5000"
    volumes:
      - ./config.ini:/app/config.ini:ro
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    read_only: true
    tmpfs:
      - /tmp
      - /run
      - /app/html:mode=1777
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 128M
        reservations:
          cpus: '0.25'
          memory: 64M
```

### 4. Deploy m4.link
Within the working directory:
```bash
docker-compose up -d
```

Visit `http://server-ip:5000` - your site should be ready!

### 4. Configure your Reverse Proxy

#### NGINX (example)
```
server {
    listen 80;
    server_name links.example.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_by;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_valid 200 1h;
        add_header X-Cache-Status $upstream_cache_status;
    }
}
```

#### Caddy (example)
```
links.example.com {
    reverse_proxy localhost:5000
    header Cache-Control "public, max-age=3600"
}
```

#### Traefik (example)
```
services:
  m4link:
    image: 3rm4zy/m4.link:latest
    container_name: m4link
    # ... the rest of the docker compose file...
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.m4link.rule=Host(`links.example.com`)"
      - "traefik.http.routers.m4link.entrypoints=websecure"
      - "traefik.http.routers.m4link.tls.certresolver=letsencrypt"
      - "traefik.http.services.m4link.loadbalancer.server.port=5000"
      - "traefik.http.middlewares.m4link-cache.headers.customresponseheaders.Cache-Control=public, max-age=3600"
      - "traefik.http.routers.m4link.middlewares=m4link-cache"
```

## Configuration

### [profile] Section
- **Name** (required) – Your display name
- **Picture** (required) – URL to profile picture
- **Description** (required) – Your bio/tagline
- **Avatar_Style** (optional) – `rounded` (circle) or `square` (default: rounded)


### [settings] Section
- **button_style** (required) – `square`, `rounded`, `pill`, `outline`, or `minimal`
- **button_color** (required) – Hex color code (e.g., `#1DA1F2`)
- **Background** (optional) – URL to background image
- **favicon** (not working) – URL to favicon


### [link X] Section (Repeatable)

Create as many links as needed: `[link 1]`, `[link 2]`, `[link 3]`, etc.

- **Title** (required) – Link display name
- **URL** (required) – Target URL
- **Icon** (required) – URL to icon/image
- **Description** (optional) – Link description (shown below title)
- **Background** (optional) – Override button color for this link only


### Button Styles
- **square** – 8px rounded corners
- **rounded** – 15px rounded corners
- **pill** – 50px rounded corners (very round)
- **outline** – Transparent with colored border
- **minimal** – Underline only


### Avatar Styles
- **rounded** – Circle (default)
- **square** – Square with slight rounding


### Update Configuration

Edit `config.ini` and restart the container:

```bash
docker-compose restart
```
That's it! No rebuild needed.

## How It Works
1. Container starts
2. `entrypoint.py` reads `config.ini`
3. Generates `html/index.html` from template
4. Flask serves the HTML on port 5000
5. Your reverse proxy forwards requests to it


## Troubleshooting
**Links not showing?**
Check `config.ini` sections are named exactly: `[link 1]`, `[link 2]`, etc.

**Changes not showing?**
Restart the container:
```bash
docker-compose restart
```

**Check logs**
```bash
docker-compose logs -f
```

**Delete old image and restart**
```bash
docker images
docker image rm 3rm4zy/m4.link:latest
docker pull 3rm4zy/m4.link:latest
docker compose up -d
```

## License
GPLv3

## Support
For issues and suggestions, open an issue.

Made with ❤️ - [3rm4zy](https://m4zy.link)