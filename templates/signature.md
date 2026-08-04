# SIGNATURE — appended to every outgoing email, automatically.
#
# scripts/format_html.py appends this to every .html twin it builds, so it lands
# in Outlook without sitting in each draft's .md. Edit it here and it changes
# everywhere on the next format_html run.
#
# It is NOT in the .md sources on purpose: it is identical on every email, and
# repeating it 200 times would bury the part that actually varies.
#
# Parsed by heading. Keep the headings exactly as they are.
#
# Contact: the line with an @ becomes a mailto link, the line starting www. or
# http becomes a website link. Everything else stays plain text.
#
# Logo: a path relative to the project root. It is downscaled to 180px wide and
# embedded in the email as a data URI, so no external image is ever fetched by
# the recipient. Leave the section empty to omit the logo.

## Contact
+421 910 955 005
jozef.martinak@valori-capital.com
www.valori-capital.com

## Logo
deck/Valori logo.jpg

## Disclaimer
The information contained in this communication is intended solely for the use of the individual or entity to whom it is addressed and others authorized to receive it. It may contain confidential or legally privileged information. If you are not the intended recipient you are hereby notified that any disclosure, copying, distribution or taking any action in reliance on the contents of this information is strictly prohibited and may be unlawful. If you have received this communication in error, please notify us immediately by responding to this email and then delete it from your system. Valori Capital is neither liable for the proper and complete transmission of the information contained in this communication nor for any delay in its receipt.
