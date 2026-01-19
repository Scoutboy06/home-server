# Fabric Server Mod List – Minecraft 1.21.10

This document describes the mods used on the server, grouped by purpose. Only server‑side or server+client mods are included—no gameplay‑changing content mods.

---

## 🎧 Communication & Social (Server + Client)

### Simple Voice Chat

**Link:** [https://modrinth.com/mod/simple-voice-chat](https://modrinth.com/mod/simple-voice-chat)
Adds proximity‑based voice chat to Minecraft. Players hear others based on distance and direction. Requires the mod on both server and client for full functionality.

---

## 📘 Gameplay Utilities (Server + Client)

### Roughly Enough Items (REI)

**Link:** [https://modrinth.com/mod/rei](https://modrinth.com/mod/rei)
Recipe and item browser that lets players view crafting recipes, usages, and search for items. Integrates with the server so all players see the correct recipe data.

---

## 🛠 Administration & Monitoring (Server Only)

### TabTPS

**Link:** [https://modrinth.com/mod/tabtps](https://modrinth.com/mod/tabtps)
Displays server performance information such as TPS and MSPT directly in the player list and via commands. Useful for diagnosing lag.

### Mod Viewer

**Link:** [https://modrinth.com/mod/modviewer](https://modrinth.com/mod/modviewer)
Allows administrators to inspect which mods are installed on the server and helps with troubleshooting version mismatches.

---

## ⚡ Performance & Optimization (Server Only)

### Lithium

**Link:** [https://modrinth.com/mod/lithium](https://modrinth.com/mod/lithium)
General-purpose server optimization focused on tick logic, mob AI, and game physics without altering vanilla behavior.

### FerriteCore

**Link:** [https://modrinth.com/mod/ferrite-core](https://modrinth.com/mod/ferrite-core)
Reduces RAM usage by optimizing Minecraft’s internal data structures, especially helpful for larger worlds.

### Krypton

**Link:** [https://modrinth.com/mod/krypton](https://modrinth.com/mod/krypton)
Improves the Minecraft networking stack, reducing CPU usage and improving packet handling on multiplayer servers.

### Memory Leak Fix

**Link:** [https://modrinth.com/mod/memoryleakfix](https://modrinth.com/mod/memoryleakfix)
Fixes several vanilla memory leaks to improve long‑term stability on servers that run for many hours or days.

### LazyDFU

**Link:** [https://modrinth.com/mod/lazydfu](https://modrinth.com/mod/lazydfu)
Speeds up server startup time by deferring DataFixerUpper initialization until it is actually needed.

### C2ME (Concurrent Chunk Management Engine)

**Link:** [https://modrinth.com/mod/c2me-fabric](https://modrinth.com/mod/c2me-fabric)
Parallelizes chunk generation and loading across multiple CPU cores, greatly improving world‑generation performance.

### ScalableLux / Starlight

**ScalableLux (1.21+):** [https://modrinth.com/mod/scalablelux](https://modrinth.com/mod/scalablelux)
**Starlight (older versions):** [https://modrinth.com/mod/starlight](https://modrinth.com/mod/starlight)
Replaces the vanilla lighting engine with a faster system, reducing lag when chunks are loaded or updated.

### Very Many Players (VMP)

**Link:** [https://modrinth.com/mod/vmp-fabric](https://modrinth.com/mod/vmp-fabric)
Improves server scalability for higher player counts by optimizing entity tracking and networking.

### Alternate Current

**Link:** [https://modrinth.com/mod/alternate-current](https://modrinth.com/mod/alternate-current)
More efficient redstone dust calculations that remain extremely close to vanilla behavior while reducing lag.

### Noisium

**Link:** [https://modrinth.com/mod/noisium](https://modrinth.com/mod/noisium)
Optimizes world generation noise calculations to speed up chunk creation.

### Chunky

**Link:** [https://modrinth.com/mod/chunky](https://modrinth.com/mod/chunky)
Tool for pre‑generating chunks so that exploration does not cause lag spikes during normal gameplay.

---

## 🌄 Distant Terrain & LOD Generation (Server + Client)

### Distant Horizons

**Link:** [https://modrinth.com/mod/distanthorizons](https://modrinth.com/mod/distanthorizons)
Client mod with optional server component that generates Level‑of‑Detail (LOD) terrain so players can see extremely far distances. When installed on the server it can run `/dh pregen <radius>` to create LOD data **without generating real vanilla chunks**, allowing distant visuals around spawn while keeping the world itself ungenerated and future‑proof.

---

## Notes

* Only Simple Voice Chat and REI require installation on both server and client.
* All performance mods are server‑side and do not require players to install anything.
* This setup aims to stay as close to vanilla mechanics as possible while providing better performance and quality of life.

