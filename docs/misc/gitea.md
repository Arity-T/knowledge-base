# Кастомизация Gitea

```sh
sudo su - git
cd /var/lib/gitea/custom
```

```sh
mkdir -p /var/lib/gitea/custom/public/css
mkdir -p /var/lib/gitea/custom/templates/custom
```

```sh
sudo nano /var/lib/gitea/custom/templates/custom
```

```html
<link rel="stylesheet" href="/custom/css/custom.css">
```

```sh
sudo -u git mkdir css
sudo -u git nano css/custom.css
```

```sh
sudo systemctl restart gitea
```

```sh
sudo nano /etc/gitea/app.ini
```
https://docs.gitea.com/administration/customizing-gitea
https://docs.gitea.com/administration/config-cheat-sheet

```ini title="app.ini"
[server]
LANDING_PAGE = explore

[other]
SHOW_FOOTER_VERSION = false
SHOW_FOOTER_TEMPLATE_LOAD_TIME = false
SHOW_FOOTER_POWERED_BY = false
ENABLE_FEED = false

[i18n]
LANGS = en-US,ru-RU
NAMES = English,Русский

[repository]
DISABLE_STARS = true

[ui.meta]
AUTHOR = Artem Tishenko: Personal Git Repository Hub
DESCRIPTION = A personal hub for managing Git repositories by Artem Tishenko.
KEYWORDS = Artem Tishenko, Artyom Tishchenko, Git, self-hosted, personal projects, repositories, Gitea
```


```sh
mkdir -p /var/lib/gitea/custom/templates/base
cd /var/lib/gitea/custom/templates/base
# перейти туда
wget https://raw.githubusercontent.com/go-gitea/gitea/refs/tags/v1.22.3/templates/base/footer_content.tmpl

# remove help - https://docs.gitea.com
# remove explore - explore.repos
# remove sign_in (just visit /user/login)
wget https://github.com/go-gitea/gitea/raw/refs/tags/v1.22.3/templates/base/head_navbar.tmpl


mkdir -p /var/lib/gitea/custom/templates/repo
cd /var/lib/gitea/custom/templates/repo
# remove packages
# remove wiki
# remove repo.activity
# remove repo.issues
# remove repo.pulls
# remove watch, fork
wget https://raw.githubusercontent.com/go-gitea/gitea/refs/tags/v1.22.3/templates/repo/header.tmpl
```

```sh
# <a class="item" href="https://kb.tishenko.dev/" target="_blank">Knowledge base</a>
/var/lib/gitea/custom/templates/custom/extra_links.tmpl
```