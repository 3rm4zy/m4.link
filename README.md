# m4.link

>[!warning] Project is still new and in early stage development

A Self Hostable "LinkTree" Clone written with basic HTML/CSS/Javascript. No backend/admin server needed! - just configure a `.ini` file and deploy!

## Features

- **Zero Backend** - Generates static HTML at startup
- **Config-Based** - Customize everything via `config.ini`
- **Docker Ready** - Single container deployment
- **Customizable** - Multiple button styles, colors, and avatar options
- **Responsive** - Mobile-friendly design
- **Fast** - Pre-generated static HTML

## Quick Start

### 1. Create `config.ini`

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

### 2. Create `docker-compose.yml`

```yaml
services:
  m4.link:
    image: 3rm4zy/m4.link:latest
    container_name: m4.link
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
      - /app/html
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

### 3. Deploy

```bash
docker-compose up -d
```

Visit `http://server-ip:5000` - your site is ready!

### 4. Configure Reverse Proxy

Point your reverse proxy to `http://server-ip:5000`

Example NGINX:
```nginx
location / {
    proxy_pass http://server-ip:5000;
}
```

## Configuration

### [profile] Section

- **Name** (required) – Your display name
- **Picture** (required) – URL to profile picture
- **Description** (required) – Your bio/tagline
- **Avatar_Style** (optional) – `rounded` (circle) or `square` (default: rounded)

---

### [settings] Section

- **button_style** (required) – `square`, `rounded`, `pill`, `outline`, or `minimal`
- **button_color** (required) – Hex color code (e.g., `#1DA1F2`)
- **Background** (optional) – URL to background image
- **favicon** (not working) – URL to favicon

---

### [link X] Section (Repeatable)

Create as many links as needed: `[link 1]`, `[link 2]`, `[link 3]`, etc.

- **Title** (required) – Link display name
- **URL** (required) – Target URL
- **Icon** (required) – URL to icon/image
- **Description** (optional) – Link description (shown below title)
- **Background** (optional) – Override button color for this link only

---

## Button Styles

- **square** – 8px rounded corners
- **rounded** – 15px rounded corners
- **pill** – 50px rounded corners (very round)
- **outline** – Transparent with colored border
- **minimal** – Underline only

---

## Avatar Styles

- **rounded** – Circle (default)
- **square** – Square with slight rounding

---

## Update Configuration

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

## Security

- Read-only filesystem (except `/tmp` and `/run`)
- No privilege escalation allowed
- `config.ini` mounted read-only

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

MIT

## Support

For issues and suggestions, open an issue.

---

Made with ❤️ - [3rm4zy](https://m4zy.link)
