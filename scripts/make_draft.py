#!/usr/bin/env python3
"""
LP Outreach — load a draft .html into an Outlook on the web compose window.

  .venv/bin/python scripts/make_draft.py drafts/insurance/2026-07-22-adriatic-osiguranje.html

It opens a browser, clicks New mail, fills in To, Subject and the body with the
bold labels and bullet list intact, and attaches the deck. Then it STOPS and
leaves the window open for you. It never clicks Send. You do the final check and
send by hand.

The deck is the newest .pdf in deck/, or whatever --deck points at. The body ends
with the signature and legal footer from templates/signature.md, added when the
.html twin is built.

First run opens Outlook and waits for you to log in. The session is saved to
.browser-profile/ so later runs go straight to the compose window.

Options:
  --dry-run     parse the file and print To/Subject/body, no browser
  --deck PATH   deck to attach (default: newest .pdf in deck/)
  --no-deck     do not attach anything
  --url URL     mailbox URL (default https://outlook.office.com/mail/)
  --profile DIR browser profile directory (default .browser-profile/)
"""

import argparse
import html as htmllib
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import quote

# Without this, Python block-buffers stdout whenever it is not a terminal, so a
# piped or backgrounded run shows nothing at all until the process exits.
try:
    sys.stdout.reconfigure(line_buffering=True)
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_URL = "https://outlook.office.com/mail/"
DEFAULT_PROFILE = ROOT / ".browser-profile"

# Present in the sign-off of every draft in every language, so it is the one
# safe "did the body land" marker. Do not swap it for a localised phrase.
SIGNOFF_MARKER = "Partner, Valori Capital"

# The deck. Shared by both programmes: one mailbox, one presentation.
DECK_DIR = ROOT / "deck"

# OWA exposes SEVERAL file inputs: one restricted to images for inline pictures,
# and the real attachment input. Feeding a PDF to the image one is what produces
# "wrong file type", so the accept attribute has to be checked, not just the tag.
JS_FILE_INPUTS = """
() => Array.from(document.querySelectorAll('input[type="file"]')).map((el, i) => ({
  i, accept: el.getAttribute('accept') || '', multiple: el.multiple,
  name: el.getAttribute('name') || '', id: el.id || '',
  label: el.getAttribute('aria-label') || ''
}))
"""

# Buttons that open the attach flow, in several UI languages.
SEL_ATTACH_BUTTON = [
    'button[aria-label*="Attach" i]',
    'button[aria-label*="Anfüg" i]',
    'button[aria-label*="Anlage" i]',
    'button[aria-label*="Priloži" i]',
    'button[aria-label*="Príloh" i]',
    'button[aria-label*="Přilož" i]',
    '[data-testid*="attach" i]',
    'button:has-text("Attach")',
]


def resolve_deck(explicit: str | None):
    """Path to the deck to attach, or None. Newest PDF in deck/ by default."""
    if explicit:
        p = Path(explicit).expanduser().resolve()
        if not p.exists():
            sys.exit(f"error: no deck at {p}")
        return p
    pdfs = sorted(DECK_DIR.glob("*.pdf"), key=lambda x: x.stat().st_mtime, reverse=True)
    return pdfs[0] if pdfs else None


def _accepts(accept: str, suffix: str) -> bool:
    """Would an input with this accept attribute take a file with this suffix?

    Handles the three forms browsers allow: a bare extension, a full MIME type,
    and a "type/*" wildcard. Getting the wildcard wrong is what sends a PDF into
    the inline-image input.
    """
    import mimetypes
    a = (accept or "").strip().lower()
    if not a or "*/*" in a:
        return True                                   # no restriction
    suffix = suffix.lower()
    mime = (mimetypes.guess_type("x" + suffix)[0] or "").lower()
    for token in (x.strip() for x in a.split(",")):
        if not token:
            continue
        if token.startswith("."):
            if token == suffix:
                return True
        elif token.endswith("/*"):
            if mime.startswith(token[:-1]):           # "image/" prefix match
                return True
        elif token == mime:
            return True
    return False


# Once one draft has found the working attach route, every later draft in the
# same run reuses it. Rediscovering it each time was most of the delay.
_ATTACH_ROUTE = {"kind": None, "frame_url": None, "sel": None, "index": None}


def attachment_present(page, name: str) -> bool:
    """Cheap presence probe. textContent avoids the layout pass innerText forces
    and the full-document serialisation page.content() does."""
    try:
        return bool(page.evaluate(
            "(n) => (document.body && document.body.textContent || '').toLowerCase().includes(n)",
            name.lower()))
    except Exception:
        return False


def _await_attachment(page, name: str, timeout_ms: int) -> bool:
    """Poll until the attachment shows up. Short interval, cheap probe."""
    deadline = time.time() + timeout_ms / 1000
    while time.time() < deadline:
        if attachment_present(page, name):
            return True
        page.wait_for_timeout(150)
    return False


def _try_input(frame, index, deck, page, timeout) -> bool:
    try:
        frame.locator('input[type="file"]').nth(index).set_input_files(
            str(deck), timeout=timeout)
    except Exception:
        return False
    return _await_attachment(page, deck.name, timeout)


def _try_button(frame, sel, deck, page, timeout) -> bool:
    try:
        btn = frame.locator(sel).first
        if btn.count() == 0:
            return False
        # A chooser opens immediately or not at all. Waiting 6s on each candidate
        # was pure dead time whenever the first selector was the wrong one.
        with page.expect_file_chooser(timeout=2500) as fc:
            btn.click(timeout=2000)
        fc.value.set_files(str(deck))
    except Exception:
        return False
    return _await_attachment(page, deck.name, timeout)


def attach_deck(page, deck: Path, timeout=30000) -> bool:
    """Attach the deck to the open compose window. True once Outlook shows it.

    Two routes, in order:
      1. Click the Attach control and answer the file chooser. This is what a
         person does and it always targets the attachment path, never the
         inline-image one.
      2. Fall back to setting a file input directly, skipping any input whose
         accept attribute rules out a PDF.

    The route that works is remembered for the rest of the run.
    """
    suffix = deck.suffix

    # -- fast path: whatever worked on the previous draft
    if _ATTACH_ROUTE["kind"]:
        for frame in frames_of(page):
            if _ATTACH_ROUTE["frame_url"] not in (None, frame.url):
                continue
            ok = (_try_button(frame, _ATTACH_ROUTE["sel"], deck, page, timeout)
                  if _ATTACH_ROUTE["kind"] == "button"
                  else _try_input(frame, _ATTACH_ROUTE["index"], deck, page, timeout))
            if ok:
                return True
        _ATTACH_ROUTE.update(kind=None, frame_url=None, sel=None, index=None)

    # -- route 1: the real attach flow
    for frame in frames_of(page):
        for sel in SEL_ATTACH_BUTTON:
            if _try_button(frame, sel, deck, page, timeout):
                _ATTACH_ROUTE.update(kind="button", frame_url=frame.url, sel=sel)
                return True

    # -- route 2: a file input that will actually take this file type
    for frame in frames_of(page):
        try:
            inputs = frame.evaluate(JS_FILE_INPUTS)
        except Exception:
            continue
        usable = [d for d in inputs if _accepts(d["accept"], suffix)]
        # prefer multi-file inputs, they are the attachment ones far more often
        usable.sort(key=lambda d: (not d["multiple"], d["i"]))
        for d in usable:
            if _try_input(frame, d["i"], deck, page, timeout):
                _ATTACH_ROUTE.update(kind="input", frame_url=frame.url, index=d["i"])
                return True
    return False


def inspect_attachment_inputs(page):
    """Print every file input with its accept attribute, for diagnosis."""
    print("\n--- file inputs visible to the script ---")
    for frame in frames_of(page):
        try:
            rows = frame.evaluate(JS_FILE_INPUTS)
        except Exception:
            continue
        if not rows:
            continue
        print(f"  frame: {frame.url[:70] or '(main)'}")
        for d in rows:
            ok = "takes .pdf" if _accepts(d["accept"], ".pdf") else "REJECTS .pdf"
            print(f"    [{d['i']}] accept={d['accept']!r} multiple={d['multiple']} "
                  f"id={d['id']!r} label={d['label']!r}  -> {ok}")
    print("--- end ---\n")


# Each entry is tried in order until one is visible. OWA's DOM shifts between
# releases, so every field has fallbacks rather than one brittle selector.
SEL_NEW_MAIL = [
    'button[aria-label*="New mail" i]',
    'button[aria-label*="New message" i]',
    '[data-testid="newItemButton"]',
    'button:has-text("New mail")',
]
# OWA localises every aria-label, so English-only selectors silently miss on a
# German, Slovak or Czech mailbox. Structural selectors come last as the net.
SEL_TO = [
    'input[aria-label="To"]',
    'input[aria-label="An"]',
    'input[aria-label="Komu"]',
    'div[aria-label="To"] input',
    'input[aria-label*="To" i][role="combobox"]',
    'input[aria-label*="An" ][role="combobox"]',
    '[aria-label*="To recipients" i] input',
    '[aria-label*="Empfänger" i] input',
    '[data-testid*="ToRecipientWell" i] input',
    'div[role="textbox"][aria-label*="To" i]',
    'input[placeholder="To"]',
    'input[id^="To"]',
]
SEL_SUBJECT = [
    'input[aria-label="Add a subject"]',
    'input[aria-label*="Betreff" i]',
    'input[aria-label*="predmet" i]',
    'input[aria-label*="edmět" i]',
    'input[placeholder*="subject" i]',
    'input[placeholder*="Betreff" i]',
    'input[aria-label*="Subject" i]',
    '[data-testid*="subject" i] input',
    'input[id^="subject" i]',
]
SEL_BODY = [
    'div[aria-label="Message body"]',
    'div[aria-label*="Message body" i][contenteditable="true"]',
    'div[aria-label*="Nachrichtentext" i][contenteditable="true"]',
    'div[aria-label*="Telo správy" i][contenteditable="true"]',
    'div[aria-label*="Tělo zprávy" i][contenteditable="true"]',
    'div[aria-label*="Message body" i]',
    'div[aria-label*="Nachrichtentext" i]',
    'div[contenteditable="true"][id^="editor" i]',
    'div[role="textbox"][contenteditable="true"]',
]

# First visible match for a prioritised selector list, in one round trip. Instant
# by design: any blocking wait in here multiplies across selectors and frames and
# becomes the delay before the paste.
JS_FIND_LABELLED = """
(sels) => {
  for (const s of sels) {
    let els;
    try { els = document.querySelectorAll(s); } catch (e) { continue; }
    for (const el of els) {
      const r = el.getBoundingClientRect();
      const st = getComputedStyle(el);
      if (st.visibility === 'hidden' || st.display === 'none') continue;
      if (!r.width || !r.height) continue;
      return el;
    }
  }
  return null;
}
"""

# The compose body is reliably the largest editable box on the page. Finding it
# by geometry survives both UI languages and OWA redesigns, and it will not grab
# the search box the way a bare [contenteditable] selector does.
JS_FIND_BODY = """
() => {
  const cands = Array.from(document.querySelectorAll('[contenteditable="true"]'));
  let best = null, bestArea = 0;
  for (const el of cands) {
    const r = el.getBoundingClientRect();
    const st = getComputedStyle(el);
    if (st.visibility === 'hidden' || st.display === 'none' || !r.width || !r.height) continue;
    if (r.width < 200 || r.height < 60) continue;   // search boxes, chips, pills
    const area = r.width * r.height;
    if (area > bestArea) { bestArea = area; best = el; }
  }
  return best;
}
"""


# ---------------------------------------------------------------- parsing

def parse_draft(path: Path):
    """Pull (to, subject, body_html) out of a draft .html written by format_html.py."""
    raw = path.read_text(encoding="utf-8")

    m = re.search(
        r"<b>To:</b>\s*(.*?)\s*&nbsp;\s*<b>Subject:</b>\s*(.*?)</p>\s*<hr>",
        raw, re.DOTALL,
    )
    if not m:
        sys.exit(f"error: no To/Subject header found in {path}\n"
                 f"       is this a draft .html from scripts/format_html.py?")

    to = htmllib.unescape(m.group(1)).strip()
    subject = htmllib.unescape(m.group(2)).strip()

    body = raw[m.end():]
    body = re.sub(r"</div>\s*$", "", body.strip())  # drop the wrapper's closing tag

    if not to or to == "FIND":
        shown = to or "(empty)"
        sys.exit(f"error: recipient is '{shown}' in {path}\n"
                 f"       fill the `to:` field in the .md, re-run format_html.py, then retry.")
    if not subject:
        sys.exit(f"error: no subject line in {path}")

    return to, subject, body.strip()


# ---------------------------------------------------------------- browser

def profile_owner(profile_dir) -> int | None:
    """PID of a live Chromium already using this profile, else None.

    Chromium allows one process per user-data-dir. A second launch otherwise
    dies deep inside Playwright with an unreadable ProcessSingleton error, so
    we check the lock ourselves and say something useful. A lock left behind by
    a crashed browser is reported as free, which is what Chromium assumes too.
    """
    lock = Path(profile_dir) / "SingletonLock"
    if not lock.is_symlink():
        return None
    try:
        pid = int(os.readlink(lock).rsplit("-", 1)[-1])
    except (OSError, ValueError):
        return None
    try:
        os.kill(pid, 0)          # signal 0 only tests for existence
        return pid
    except ProcessLookupError:
        return None              # stale lock, safe to reuse
    except PermissionError:
        return pid               # alive, just not ours


def pause(msg: str):
    """Wait for Enter, but only when a human is actually at the terminal."""
    if not sys.stdin.isatty():
        print(f"[non-interactive, not waiting] {msg}")
        return
    try:
        input(msg)
    except (EOFError, KeyboardInterrupt):
        print()


def watch_until_closed(ctx, hours=6):
    """Poll the window and return once you close it."""
    deadline = time.time() + hours * 3600
    while time.time() < deadline:
        try:
            if not ctx.pages:
                break
        except Exception:
            break
        time.sleep(3)


def capture_body(el):
    """Read the compose body back, so a sent record reflects any edits made."""
    try:
        return el.inner_html()
    except Exception:
        return None


def confirm_sent(company: str) -> bool:
    """Ask once. Closing the window is not by itself proof that it went out.

    A false 'sent' is the expensive mistake: the row leaves the queue and that
    LP is never contacted again, silently. One keystroke is cheaper than that.
    """
    if not sys.stdin.isatty():
        print("[non-interactive, not logging] run scripts/log_sent.py if this was sent")
        return False
    try:
        ans = input(f"Did you send it to {company}? [y/N] ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print()
        return False
    return ans in ("y", "yes")


def hold_open(ctx, hours=6, on_close=None):
    """Keep the compose window up until you are done with it.

    At a terminal we wait on Enter. Without one (a backgrounded or piped run)
    there is no Enter to wait for, so we watch the window instead. Either way
    we never close a compose window out from under you, and we never leave a
    raw traceback behind if stdin closes or you hit Ctrl+C.

    `on_close` runs while the page is still alive, so the body can be read back
    before anything is torn down.
    """
    if sys.stdin.isatty():
        try:
            input("press Enter here when you are done to close the browser...")
        except (EOFError, KeyboardInterrupt):
            # stdin vanished or Ctrl+C: fall back to watching rather than
            # yanking the window away mid-edit.
            print("\nleaving the browser open, close the window when you are done.")
            watch_until_closed(ctx, hours)
            print("browser closed.")
            if on_close:
                on_close(None)
            return
        snapshot = on_close(None, capture=True) if on_close else None
        try:
            ctx.close()
        except Exception:
            pass
        if on_close:
            on_close(snapshot)
        return

    print("Leaving the browser open. Close the window yourself when you are done.")
    last = None
    deadline = time.time() + hours * 3600
    while time.time() < deadline:
        try:
            if not ctx.pages:
                break
            if on_close:
                last = on_close(None, capture=True) or last
        except Exception:
            break
        time.sleep(3)
    print("browser closed.")
    if on_close:
        on_close(last)


def first_visible(page, selectors, timeout=15000):
    """Return the first selector in the list that becomes visible, else None."""
    per_try = max(timeout // len(selectors), 1500)
    for sel in selectors:
        loc = page.locator(sel).first
        try:
            loc.wait_for(state="visible", timeout=per_try)
            return loc
        except Exception:
            continue
    return None


def field_has_value(page, selectors, expected: str) -> bool:
    """True if one of these fields already carries `expected` (the deeplink filled it)."""
    head = expected[:25]
    for sel in selectors:
        loc = page.locator(sel).first
        try:
            if loc.count() == 0:
                continue
            val = loc.input_value(timeout=1500)
        except Exception:
            try:
                val = loc.inner_text(timeout=1500)
            except Exception:
                continue
        if val and head in val:
            return True
    return False


def set_clipboard_html(body_html: str):
    """macOS fallback: put real HTML on the clipboard so Cmd+V keeps formatting."""
    hexed = body_html.encode("utf-8").hex()
    subprocess.run(
        ["osascript", "-e", f'set the clipboard to «data HTML{hexed}»'],
        check=True, capture_output=True,
    )


def frames_of(page):
    """Main frame first, then any child frame. OWA sometimes hosts the editor in one."""
    return [page.main_frame] + [f for f in page.frames if f != page.main_frame]


def find_body(page):
    """Locate the compose body. Returns (frame, element_handle) or (None, None).

    Wholly non-blocking: an explicit label wins if one is present, geometry
    covers a localised or redesigned UI, and neither waits. Waiting is the poll
    loop's job in wait_for_body, which keeps the deadline honest and stops the
    per-selector timeouts from stacking into a long pause before the paste.
    """
    for finder, arg in ((JS_FIND_LABELLED, SEL_BODY), (JS_FIND_BODY, None)):
        for frame in frames_of(page):
            try:
                handle = (frame.evaluate_handle(finder, arg) if arg is not None
                          else frame.evaluate_handle(finder))
                el = handle.as_element()
                if el:
                    return frame, el
            except Exception:
                continue
    return None, None


def still_attached(frame, el) -> bool:
    """True if a previously found handle is still live in the DOM."""
    try:
        return bool(frame.evaluate("(n) => n.isConnected", el))
    except Exception:
        return False


def wait_for_body(page, timeout=45000):
    """Poll for the compose body while the compose surface finishes rendering."""
    deadline = time.time() + timeout / 1000
    while True:
        frame, el = find_body(page)
        if el:
            return frame, el
        if time.time() >= deadline:
            return None, None
        page.wait_for_timeout(250)


def landed(el) -> bool:
    """True once the body is really in the editor.

    Checks the sign-off title, which stays English in every language template
    (EN "Kind regards", DE "Mit freundlichen Grüßen", SK "S pozdravom" all sit
    above the same "Partner, Valori Capital"). Matching the English sign-off
    instead would report a false failure on every DE and SK draft.
    """
    try:
        return SIGNOFF_MARKER in (el.inner_text() or "")
    except Exception:
        return False


def fill_body(page, frame, el, body_html: str) -> str:
    """Insert the formatted body. Returns which method worked."""
    try:
        el.scroll_into_view_if_needed(timeout=3000)
    except Exception:
        pass
    try:
        el.click()
    except Exception:
        pass

    # Preferred: insertHTML straight into the contenteditable, keeps <strong>/<ul>.
    try:
        frame.evaluate(
            "([node, h]) => { node.focus(); document.execCommand('insertHTML', false, h); }",
            [el, body_html],
        )
    except Exception:
        pass
    if landed(el):
        return "execCommand insertHTML"

    # Fallback: real clipboard paste (macOS), which OWA always accepts. Clear first,
    # otherwise a partial insertHTML would leave a duplicated body behind.
    if sys.platform == "darwin":
        try:
            frame.evaluate(
                "(node) => { node.focus();"
                " document.execCommand('selectAll', false, null);"
                " document.execCommand('delete', false, null); }",
                el,
            )
        except Exception:
            pass
        set_clipboard_html(body_html)
        try:
            el.click()
        except Exception:
            pass
        page.keyboard.press("Meta+V")
        page.wait_for_timeout(900)
        if landed(el):
            return "clipboard paste"

    return "FAILED"


def inspect_dom(page):
    """Print every plausible compose field, so bad selectors can be diagnosed."""
    js = """
    () => Array.from(document.querySelectorAll(
            'input,textarea,[contenteditable="true"],[role="textbox"],[role="combobox"]'))
      .map(el => {
        const r = el.getBoundingClientRect();
        return {tag: el.tagName.toLowerCase(), type: el.getAttribute('type') || '',
                role: el.getAttribute('role') || '', label: el.getAttribute('aria-label') || '',
                ph: el.getAttribute('placeholder') || '', id: el.id || '',
                editable: el.getAttribute('contenteditable') || '',
                w: Math.round(r.width), h: Math.round(r.height)};
      }).filter(e => e.w > 0 && e.h > 0);
    """
    for frame in frames_of(page):
        try:
            rows = frame.evaluate(js)
        except Exception as exc:
            print(f"  [frame {frame.url[:60]}] not readable: {exc}")
            continue
        if not rows:
            continue
        print(f"\n  frame: {frame.url[:80] or '(main)'}")
        for e in rows:
            print(f"    <{e['tag']}> {e['w']}x{e['h']} role={e['role']!r} "
                  f"aria-label={e['label']!r} placeholder={e['ph']!r} "
                  f"id={e['id']!r} contenteditable={e['editable']!r}")


def main():
    ap = argparse.ArgumentParser(description="Load a draft .html into an Outlook web compose window. Never sends.")
    ap.add_argument("draft", help="path to a draft .html")
    ap.add_argument("--dry-run", action="store_true", help="parse and print only, no browser")
    ap.add_argument("--url", default=DEFAULT_URL, help=f"mailbox URL (default {DEFAULT_URL})")
    ap.add_argument("--profile", default=str(DEFAULT_PROFILE), help="browser profile directory")
    ap.add_argument("--no-deeplink", action="store_true",
                    help="skip the compose deeplink, click New mail and type into the fields instead")
    ap.add_argument("--inspect", action="store_true",
                    help="open the compose window and dump every field it can see, then stop")
    ap.add_argument("--body-timeout", type=float, default=5.0, metavar="SECS",
                    help="seconds to wait for the message body before giving up (default 5)")
    ap.add_argument("--no-log", action="store_true",
                    help="do not offer to log the send when the window closes")
    ap.add_argument("--deck", metavar="PATH",
                    help="deck to attach (default: newest .pdf in deck/)")
    ap.add_argument("--no-deck", action="store_true",
                    help="do not attach a deck. The email still says one is attached.")
    ap.add_argument("--inspect-attach", action="store_true",
                    help="list every file input in the compose window and stop")
    args = ap.parse_args()

    path = Path(args.draft).resolve()
    if not path.exists():
        sys.exit(f"error: no such file: {path}")
    if path.suffix != ".html":
        sys.exit(f"error: expected a draft .html, got {path.suffix}\n"
                 f"       (the .md is the source; the .html is the paste-ready twin)")

    to, subject, body_html = parse_draft(path)

    deck = None
    if not args.no_deck:
        deck = resolve_deck(args.deck)
        if deck is None:
            sys.exit("error: no deck found in deck/ and --deck not given.\n"
                     "       The email says \"Please find attached our presentation\", so\n"
                     "       sending without one is worse than not mentioning it.\n"
                     "       Put a PDF in deck/, pass --deck PATH, or use --no-deck.")

    print(f"draft   : {path.name}")
    print(f"to      : {to}")
    print(f"subject : {subject}")
    print(f"body    : {len(body_html)} chars html")
    print(f"deck    : {deck.name if deck else 'NONE (--no-deck)'}")

    if args.dry_run:
        print("\n--- body html ---")
        print(body_html)
        return

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("error: playwright is not installed.\n"
                 "       .venv/bin/pip install playwright && .venv/bin/playwright install chromium")

    owner = profile_owner(args.profile)
    if owner is not None:
        sys.exit(
            f"error: another Chromium (pid {owner}) is already using the profile\n"
            f"       {args.profile}\n"
            f"       Chromium allows one process per profile, so this run cannot start.\n"
            f"       Close that browser window and try again, or run a second copy with\n"
            f"       its own profile and a separate login:\n"
            f"         --profile .browser-profile-2")

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            args.profile,
            headless=False,
            viewport={"width": 1440, "height": 900},
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.set_default_navigation_timeout(120000)

        # Preferred route: Outlook's compose deeplink puts the recipient and the
        # subject in the URL, so we never have to find those two fields. Only the
        # message body still needs a selector.
        used_deeplink = False
        if not args.no_deeplink:
            base = args.url.rstrip("/").removesuffix("/mail")
            link = (f"{base}/mail/deeplink/compose"
                    f"?to={quote(to)}&subject={quote(subject)}")
            print("\nopening the compose deeplink...")
            page.goto(link, wait_until="domcontentloaded")
            # Keep the handle. Re-scanning for it later was doubling the wait.
            frame, body_el = wait_for_body(page, timeout=45000)
            used_deeplink = body_el is not None
            if not used_deeplink:
                print("deeplink did not open a compose window, falling back to New mail")

        if not used_deeplink:
            page.goto(args.url, wait_until="domcontentloaded")
            print("\nwaiting for the mailbox to load...")
            new_mail = first_visible(page, SEL_NEW_MAIL, timeout=20000)
            if new_mail is None:
                print("not logged in yet (or the mailbox is slow).")
                print("log in in the browser window, then press Enter here.")
                pause("")
                new_mail = first_visible(page, SEL_NEW_MAIL, timeout=60000)
            if new_mail is None:
                print("error: could not find the 'New mail' button. Leaving the browser open.")
                pause("press Enter to close...")
                ctx.close()
                sys.exit(1)
            new_mail.click()
            print("clicked New mail")

        if args.inspect:
            print("\n--- fields visible to the script ---")
            inspect_dom(page)
            print("\n(inspect mode: nothing was filled)")
            hold_open(ctx)
            return

        # With the deeplink these are already filled from the URL. Only top up what
        # is genuinely missing, and stay quiet when the deeplink already did the job.
        if field_has_value(page, SEL_TO, to):
            print(f"To already set: {to}")
        else:
            to_el = first_visible(page, SEL_TO, timeout=6000)
            if to_el is not None:
                to_el.click()
                to_el.type(to, delay=20)
                page.keyboard.press("Enter")      # resolve the address into a pill
                print(f"filled To: {to}")
            elif used_deeplink:
                print(f"To: set by the deeplink (field not readable) - confirm it shows {to}")
            else:
                print(f"warning: could not find the To field. Add by hand: {to}")

        if field_has_value(page, SEL_SUBJECT, subject):
            print(f"Subject already set: {subject}")
        else:
            subj_el = first_visible(page, SEL_SUBJECT, timeout=6000)
            if subj_el is not None:
                subj_el.click()
                subj_el.type(subject, delay=10)
                print(f"filled Subject: {subject}")
            elif used_deeplink:
                print("Subject: set by the deeplink (field not readable)")
            else:
                print(f"warning: could not find the Subject field. Add by hand: {subject}")

        # Reuse the handle from the deeplink wait. Only look again if it went
        # stale or we never had one, and cap that at --body-timeout seconds.
        if body_el is None or not still_attached(frame, body_el):
            frame, body_el = wait_for_body(page, timeout=int(args.body_timeout * 1000))
        if body_el is None:
            print("warning: could not find the message body, skipping it.")
            print("         run again with --inspect to dump the fields, and send me the output.")
        else:
            how = fill_body(page, frame, body_el, body_html)
            if how != "FAILED":
                print(f"filled body via {how}")
            else:
                print("warning: body insert failed, paste it by hand from the .html")
                print("         run again with --inspect to dump the fields, and send me the output.")

        if args.inspect_attach:
            inspect_attachment_inputs(page)
            hold_open(ctx)
            return

        if deck is not None:
            ok = attach_deck(page, deck)
            print(f"attached: {deck.name}" if ok
                  else f"warning: could not attach {deck.name}, add it by hand")

        print("\n" + "=" * 62)
        print("STOPPED. Nothing was sent. The draft is open in the browser.")
        print("Your turn:  check it  ->  confirm the attachment  ->  send by hand.")
        print("Outlook autosaves it to Drafts.")
        if not args.no_log:
            print("When you close this, I will ask whether it went out and log it.")
        print("=" * 62)

        def on_close(snapshot, capture=False):
            """Two phases: capture while the page lives, then log after it closes."""
            if capture:
                return capture_body(body_el) if body_el is not None else None
            if args.no_log:
                return None
            lp = path.stem
            try:
                sys.path.insert(0, str(ROOT / "scripts"))
                import log_sent
                company = lp
                rows = log_sent.read_rows()
                slug = log_sent.slug_of(path)
                row = next((r for r in rows if r["slug"] == slug), None)
                if row is None:
                    print(f"not in the tracker, nothing logged: {slug}")
                    return None
                if row["stage"] == "sent":
                    print(f"already logged as sent: {row['company']}")
                    return None
                if not confirm_sent(row["company"]):
                    print("left as drafted. Nothing logged.")
                    return None
                res = log_sent.log_send(path, to, subject, snapshot)
                print(f"logged: {res['company']} -> {res['md'].relative_to(ROOT)}"
                      f"  (edits: {res['edits']}, stage=sent)")
            except SystemExit as exc:
                print(f"could not log: {exc}")
            except Exception as exc:
                print(f"could not log ({type(exc).__name__}: {exc}). "
                      f"Run scripts/log_sent.py {path.name} by hand.")
            return None

        hold_open(ctx, on_close=on_close)


if __name__ == "__main__":
    main()
