# Cersei

Transferring files securely is a pain in the ass, especially if you work
in an office environment where the technologies are heavily fragmented,
and/or you're working with users who are not particularly technically
savvy.

The common denominator for many office environments consists of two
tools: websites and (unencrypted) email.  Slightly more advanced
companies may make use of IRC, Slack, and maybe some combination of
Dropbox and Google Drive.  None of these tools make it easy to transfer
files one-to-one safely & securely so I wrote this... in a few hours.

Do with it as you will.

## The User Journey

1. Sender uploads file and gives it a password, and optionally provides
   a time limit value.
2. The server symmetrically encrypts the file and stores it locally.
3. The sender is redirected to a thank you page with a URL for the file.
4. The sender copy/pastes this URL into whatever channel they might have
   to communicate with their target user and passes on the password to
   them (hopefully) by some other means.
5. The recipient goes to the URL, types in the password, and gets the
   file.
6. Depending on the rules set by the sending user, the file is deleted
   once it's been downloaded, or is deleted after a fixed time.

## Why Cersei?

Because she's ruthless and only a fool would cross her, because she
breaks the rules and has no patience for fiddly process (like getting
PGP setup and working across your company), and because I wanted another
awesome fictional female character to name my next project after.
