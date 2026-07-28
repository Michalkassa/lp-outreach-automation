#!/usr/bin/env python3
"""
LP Outreach — create an Outlook draft for EVERY unsent draft, one after another.

  python scripts/make_all_drafts.py --lang en        # all English drafts
  python scripts/make_all_drafts.py --all            # every unsent draft
  python scripts/make_all_drafts.py --dry-run        # list what it would do

Opens ONE browser session and walks the whole queue: for each LP it opens a
compose window, fills To, Subject and the body, saves it to Outlook Drafts, and
moves on. You are not asked anything between drafts.

It NEVER sends and it NEVER attaches the deck. Every message lands in your
Outlook Drafts folder for you to check, attach the deck, and send by hand.

It also never marks anything as sent. Stage stays `drafted` until the email
actually goes out, which you log with scripts/log_sent.py or /log-sent.

Drafts that fail a readiness check (unconfirmed recipient, missing bold labels,
retired subject ending) are skipped and listed at the end.
"""

import argparse
import sys
import time
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import make_draft as md          # noqa: E402  parse_draft, find_body, fill_body, selectors
import send_queue as sq          # noqa: E402  the same filtering and readiness checks

DEFAULT_URL = "https://outlook.office.com/mail/"


def build_queue(args):
    """Reuse send_queue's filtering so both tools agree on what is ready."""
    rows = sq.load_rows()
    drafts = sq.draft_map()
    folder_of = {"Insurance": "insurance", "Pension funds": "pension-funds"}

    ready, blocked, held = [], [], []
    seen = {}
    candidates = []
    for r in rows:
        if r.get("stage") != "drafted":
            continue
        if args.lang and r.get("language") != args.lang:
            continue
        if args.lp_list and folder_of.get(r.get("list")) != args.lp_list:
            continue
        path = drafts.get(r["slug"])
        if not path:
            continue
        to, subject, problems = sq.check(path, r.get("language", "en"))
        score = int(r["score"]) if str(r.get("score", "")).strip().isdigit() else 0
        item = {"score": score, "company": r["company"], "to": to or "",
                "subject": subject or "", "path": path, "lang": r.get("language", "")}
        if problems:
            blocked.append({**item, "problems": problems})
        else:
            candidates.append(item)

    candidates.sort(key=lambda e: (-e["score"], e["company"].lower()))
    for e in candidates:
        key = e["to"].lower()
        if key in seen:
            held.append((e, seen[key]))
        else:
            seen[key] = e
            ready.append(e)

    if not args.all:
        ready = ready[:max(args.limit, 0)]
    return ready, held, blocked


def save_draft(page):
    """Ask Outlook to persist the message to Drafts before we navigate away.

    OWA autosaves on its own, but an explicit save plus a short settle makes the
    difference between a draft that is there and one that lost its last edit.
    """
    combo = "Meta+S" if sys.platform == "darwin" else "Control+S"
    try:
        page.keyboard.press(combo)
    except Exception:
        pass
    page.wait_for_timeout(1200)


def main():
    ap = argparse.ArgumentParser(
        description="Create an Outlook draft for every unsent draft. Never sends.")
    ap.add_argument("--lang", choices=["en", "sk", "de"], help="only this language bucket")
    ap.add_argument("--list", dest="lp_list", choices=["insurance", "pension-funds"],
                    help="only this list")
    ap.add_argument("--limit", type=int, default=sq.DAILY_CAP,
                    help=f"how many to build (default {sq.DAILY_CAP})")
    ap.add_argument("--all", action="store_true", help="ignore the limit, build everything ready")
    ap.add_argument("--dry-run", action="store_true", help="list the queue and exit, no browser")
    ap.add_argument("--url", default=DEFAULT_URL, help=f"mailbox URL (default {DEFAULT_URL})")
    ap.add_argument("--profile", default=str(ROOT / ".browser-profile"),
                    help="browser profile directory")
    ap.add_argument("--pause", type=float, default=1.0, metavar="SECS",
                    help="seconds to settle between drafts (default 1)")
    ap.add_argument("--keep-open", action="store_true",
                    help="leave the browser open at the end instead of closing it")
    args = ap.parse_args()

    ready, held, blocked = build_queue(args)

    print(f"to build : {len(ready)}")
    print(f"held     : {len(held)}   (shared recipient, one email per person)")
    print(f"blocked  : {len(blocked)} (failed a readiness check)")
    for e, kept in held:
        print(f"  held    [{e['score']}] {e['company']} shares {e['to']} with {kept['company']}")
    for e in blocked:
        print(f"  blocked [{e['score']}] {e['company']}: {'; '.join(e['problems'])}")

    if args.dry_run or not ready:
        print()
        for i, e in enumerate(ready, 1):
            print(f"{i:>3}. [{e['score']}] {e['company']}  ->  {e['to']}")
        if not ready:
            print("nothing to build.")
        return

    owner = md.profile_owner(args.profile)
    if owner is not None:
        sys.exit(f"error: another Chromium (pid {owner}) is using {args.profile}\n"
                 f"       close that window and run again.")

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("error: playwright is not installed.\n"
                 "       .venv/bin/pip install playwright && .venv/bin/playwright install chromium")

    base = args.url.rstrip("/").removesuffix("/mail")
    done, failed = [], []

    print(f"\nbuilding {len(ready)} Outlook drafts. Nothing will be sent.\n")
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            args.profile, headless=False, viewport={"width": 1440, "height": 900},
            args=["--disable-blink-features=AutomationControlled"])
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.set_default_navigation_timeout(120000)
        page.on("dialog", lambda d: d.accept())   # "keep editing?" prompts

        for i, e in enumerate(ready, 1):
            label = f"{i}/{len(ready)}  [{e['score']}] {e['company']}"
            try:
                link = (f"{base}/mail/deeplink/compose"
                        f"?to={quote(e['to'])}&subject={quote(e['subject'])}")
                page.goto(link, wait_until="domcontentloaded")
                frame, body_el = md.wait_for_body(page, timeout=45000)
                if body_el is None:
                    print(f"  SKIP  {label}: no compose body appeared")
                    failed.append((e, "no compose body"))
                    continue

                _, _, body_html = md.parse_draft(e["path"])
                how = md.fill_body(page, frame, body_el, body_html)
                if how == "FAILED":
                    print(f"  SKIP  {label}: body insert failed")
                    failed.append((e, "body insert failed"))
                    continue

                save_draft(page)
                print(f"  ok    {label}  ->  {e['to']}")
                done.append(e)
                time.sleep(max(args.pause, 0))
            except KeyboardInterrupt:
                print("\ninterrupted. Drafts built so far are in Outlook Drafts.")
                break
            except Exception as exc:
                print(f"  SKIP  {label}: {type(exc).__name__}: {exc}")
                failed.append((e, str(exc)[:80]))

        print("\n" + "=" * 62)
        print(f"built {len(done)} of {len(ready)} drafts. NOTHING WAS SENT.")
        print("They are in your Outlook Drafts folder.")
        print("Your turn: check each one, ATTACH THE DECK, send by hand.")
        print("After sending, log it:  .venv/bin/python scripts/log_sent.py <draft.html>")
        print("=" * 62)
        if failed:
            print("\nnot built:")
            for e, why in failed:
                print(f"  [{e['score']}] {e['company']}: {why}")

        if args.keep_open:
            md.hold_open(ctx)
        else:
            try:
                ctx.close()
            except Exception:
                pass


if __name__ == "__main__":
    main()
