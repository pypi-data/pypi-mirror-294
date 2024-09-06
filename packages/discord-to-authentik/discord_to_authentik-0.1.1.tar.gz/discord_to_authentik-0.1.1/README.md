# Discord to Authentik

A Discord bot that synchronizes your discord roles to Authentik groups.

# Preamble

I really like using the Discord Login functionality of Authentik. And also the great Guides that have been written for it.

Although it did bother me that i had to create the groups manually instead of Authentik syncing them from my Discord instance on demand.

So i created this solution that allows you to synchronize all your Discord roles to Authentik groups with the required `discord_role_id` attribute!

This is a great complimentary application to [this](https://docs.goauthentik.io/docs/sources/discord/#syncing-discord-roles-to-authentik-groups) guide!

## Sounds great. How do i install and use it?

The installation is as simple as executing those following commands:
```
pipx install --global discord-to-authentik
sudo discord-to-authentik-setup
```

Then you type `!sync` into the Discord Guild your bot runs in to synchronize the slash command `sync_roles`.
From this point you can just do `/sync_roles` whenever you want to synchronize your discord roles with your Authentik instance.

Enjoy ✨

## Installing on NixOS

TODO