# Cloudflare Tunnel

Runs a remotely managed tunnel alongside tsdproxy. No inbound ports are
published. Existing services remain unchanged; public routes are opt-in and
managed in the Cloudflare dashboard. Domain names do not need to be stored here.

## Start the connector

1. Add your domain to Cloudflare and wait for it to become active.
2. In the Cloudflare dashboard, create a Cloudflared tunnel and select Docker
   to obtain its token. Do not commit or share the token.
3. From this directory, prepare the local environment:

   ```sh
   cp .env.example .env
   chmod 600 .env
   ```

4. Set `CLOUDFLARE_TUNNEL_TOKEN` in `.env` (ignored by Git).
5. Start the connector:

   ```sh
   docker compose up -d
   docker compose logs --tail=50 cloudflared
   ```

The tunnel should appear healthy in Cloudflare. Starting it creates the shared
`public-proxy` Docker network but does not publish any applications by itself.

## Opt a service into public routing

Attach only the chosen web-facing container to the shared network, retaining
its existing networks and tsdproxy labels. For example, in that app's Compose file:

```yaml
services:
  my-app:
    # Existing app configuration stays here.
    networks:
      - default
      - public-proxy

networks:
  public-proxy:
    external: true
    name: public-proxy
```

Start cloudflared before deploying an app that uses this external network.
Do not attach databases or unrelated services. Use distinct service names or
network aliases to avoid name collisions on the shared network.

In Cloudflare, add a published application route for the selected hostname,
pointing to `http://my-app:3000` (replace the service name and internal port).
Do not use `localhost`: that would refer to the cloudflared container itself.
Cloudflare provides public HTTPS; HTTP here is local Docker-network traffic.
Check the application's trusted-proxy and external-URL settings as needed.

**A published route is internet-accessible.** For restricted browser apps,
configure a Cloudflare Access application and explicit allow policy for the
hostname before adding the route. Access can interfere with native clients,
APIs, and webhooks; those need an appropriate authentication strategy.
Avoid wildcard routes and keep administration tools Tailscale-only.

Test public access with Tailscale disabled and verify unauthorized users are
blocked where applicable. Remove the published route in Cloudflare to revoke
that public entry point; Tailscale access remains independent.

## Update

```sh
docker compose pull
docker compose up -d
```

Cloudflared's in-container updater is disabled; updates use the container image.
