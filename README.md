# didgitaldoo.github.io

Die Website von Didgitaldoo, gebaut mit Jekyll.

## Lokal ansehen mit Docker Compose

Jekyll und Ruby müssen dafür nicht installiert sein, nur Docker.

Starten (beim ersten Mal wird das Image gebaut, das dauert ein paar Minuten):

```bash
docker compose up --build
```

Sobald im Log `Server running...` steht, ist die Seite im Browser erreichbar unter:

**http://localhost:4000**

Änderungen an den Dateien werden automatisch neu gebaut, und der Browser lädt die Seite per LiveReload von selbst neu. Falls trotzdem das alte Design erscheint, hilft ein Hard-Reload (Cmd+Shift+R).

Im Hintergrund starten und wieder stoppen:

```bash
docker compose up -d
docker compose down
```

Logs ansehen, wenn im Hintergrund gestartet wurde:

```bash
docker compose logs -f
```

Ändert sich das `Gemfile`, einmal neu bauen mit `docker compose up --build`.
