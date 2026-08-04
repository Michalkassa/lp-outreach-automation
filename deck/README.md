# The deck

Put the investor presentation here as a **PDF**. The sending scripts attach it
to every draft automatically.

    deck/valori-deck.pdf

## How it is chosen

1. `--deck path/to/file.pdf` if you pass it explicitly
2. otherwise the **newest `.pdf` in this folder**
3. if neither exists the run stops, unless you pass `--no-deck`

It stops rather than continuing because the v5 closing line says *"Please find
attached our presentation."* An email that promises an attachment and arrives
without one is worse than one that never mentions it.

## Versioning

Keep only the current deck here. If you keep several, the newest by modification
time wins, which is easy to get wrong. Move old versions out of this folder.

The file name is what the recipient sees, so name it for them, not for you:
`Valori Capital - Fund I.pdf` reads better than `deck_v7_FINAL_new.pdf`.
