# Shared Beads database

Dolt 2.2.0 for Beads 1.3.1. Database: `eden`, client user: `beads`.
Endpoint: `home-server.hydra-adelie.ts.net:3307` (`100.122.161.121`).
This is a MySQL-compatible database, not a website or HTTP API.

## Connect another computer

Install Beads **1.3.1**, connect Tailscale, and ensure `ssh home-server` works.
From the root of your **eden** checkout:

```sh
setup=$(mktemp)
scp home-server:home-server/productivity/beads/connect.py "$setup"
python3 "$setup"
rm "$setup"
bd list
```

The script preserves existing local databases and backs up metadata before
changing the checkout to server mode. It fetches the password over SSH and stores
it in `~/.config/beads/credentials` (or `BEADS_CREDENTIALS_FILE`) with mode 600.
It does **not** merge any changes from other computers' old local databases.
Unset conflicting `BEADS_DOLT_*` connection/password environment variables first.
If `.beads/config.yaml` explicitly configures a different Dolt mode/host/port/user,
remove those overrides before connecting. Verify the destination with `bd dolt show`.

All clients share this live database. No `bd sync` or `bd dolt push/pull` is
needed for cross-computer access. The server and Tailscale must be reachable.
Do not run `bd init --force` or independently migrate the shared schema.
Coordinate future Beads version/schema upgrades across all clients.

## Deployment

```sh
cd ~/home-server/productivity/beads
docker compose up -d --wait
docker compose ps
docker compose logs --tail 50
```

The service restarts automatically. `data/` persists all databases and server
privileges. `.env` contains separate random root and client passwords; never commit
it. Changing passwords in `.env` alone does not rotate an existing client account.
The root account is localhost-only and the client account has privileges on
`eden` and `inet_server`, not global administrator privileges.

Port 3307 is published **only on the host's Tailscale IPv4 address**, not on
0.0.0.0 or a LAN address. Tailnet ACLs still determine which peers can reach it.
Tailscale encrypts network traffic; database TLS is not configured. Do not expose
this port through a public proxy, router port forwarding, or Funnel.
Docker networks/other containers and the host can still reach the internal port.
TSDProxy 1.4.7 was left unchanged: this service uses raw TCP, not its HTTP proxy.
If the host's Tailscale IP changes, update `.env` and recreate the service.

## Scotty web UI

Scotty is available to the tailnet at **https://scotty.hydra-adelie.ts.net**.
Projects: `/p/eden` (Eden) and `/p/inet_server` (Inet.Server).
Anyone allowed to reach this service through tailnet ACLs can edit both projects;
Scotty has no application login. No host HTTP port or public Funnel is enabled.

The `scotty` Compose service builds upstream Bead Me Up, Scotty with Beads
**1.3.1**, matching the other clients. Initial source commit:
`dd00780a117c2fed413d0db5caedf371d22c2393`.
To restore the source directory on a fresh installation:

```sh
git clone https://github.com/brendan-appstart/bead-me-up-scotty.git scotty-src
git -C scotty-src checkout dd00780a117c2fed413d0db5caedf371d22c2393
```

`scotty-projects/{eden,inet_server}/.beads/` contains connection metadata only,
pointing at `dolt:3306` as `beads`, in server mode. These are not copies of the
database. The password comes from the existing `.env` via the container
environment. `scotty-config/` persists UI settings and the project registry.
Back up these two directories to preserve the UI setup. They and the upstream
source clone are gitignored. The container runs as host UID/GID 1000:1000.
Optional upstream usage telemetry is disabled with `POSTHOG_KEY=""`.

Rebuild/restart **only the UI** (does not recreate Dolt):

```sh
docker compose build scotty
docker compose up -d --no-deps --wait scotty
docker compose logs --tail 50 scotty
```

Do not upgrade the bundled Beads CLI independently of the other clients or
enable remote schema migration. UI edits write directly to the shared databases.
The upstream image does not include Claude Code, so its AI refinement feature
is unavailable. Database backups remain the responsibility of `backup.sh`.

## Backups and recovery

The initial full pre-migration snapshot is `backups/eden-pre-server.tar.gz`.
The original computer's `.beads/embeddeddolt/` also remains intact, but is no
longer live after switching that checkout to server mode.

Create/update an online full Dolt backup with:

```sh
sh backup.sh
```

The command backs up both databases to `backups/eden/` and `backups/inet_server/`.
No automatic backup schedule or
off-server backup is installed. Copy backups off this server for disaster recovery.
Back up `.env` and the server privilege files in `data/.doltcfg/` securely too;
the database-native backup does not include server credentials.

Restore into a **new** database first using a localhost administrator session:

```sql
CALL DOLT_BACKUP('restore', 'file:///backups/eden', 'eden_recovered');
```

Validate the recovered data before changing client database names or replacing
the live database. Do not extract the pre-migration tarball over a running database.

## Inet.Server

The same service also hosts `inet_server` for Inet.Server, separately from `eden`.
The `beads` client account can access both databases using the same server password.
These databases are separate projects, not security boundaries against that account.
The Eden `connect.py` helper intentionally refuses to configure Inet.Server.

The checkout `hq-lap-103-wsl:~/p/Inet.Server` was migrated from embedded mode on
2026-10-15, preserving 61 issue records (including the migration task) and 596
Dolt commits. Its `.beads` symlink to `local-files/.beads` remains unchanged.
Connection metadata uses database `inet_server`, the server endpoint above, and
user `beads`. The previous metadata is `.beads/metadata.pre-home-server.json`;
the original embedded database and native `home-server-transfer` backup remain
on WSL. The initial server-side native backup is `backups/home-server-transfer/`,
also archived in `backups/inet-server-native-backup.tar.gz`.
