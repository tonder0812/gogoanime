# GogoAnime downloader

A python application to auto download anime from the https://gogoanime.tel website (windows only)

It's necessary to have a logged in gogoanime account

## Instalation

Run the install script to create the config folder

```
> ./install.bat
```

## Usage

```
> python check.py [-c]
```

The `-c` flag makes the program run continually (every five minutes)

Use the up and down arrows to scroll

## Config

The config folder has 4 files inside:

- **config.json** a json file that can have the following options
  - **download_path** the path to a folder where to save the downloaded anime. **Defaults to `./Downloads`**
  - **notification_file_location** the path to a folder containing 2 files `new.txt` and `downloaded.txt` and appends a new line with `<anime_name> - <episode>` to each every time that an episode starts or finishes downloading an episode respectively. **Defaults to `null`** making it not write anything
  - **browser** the browser that has the gogoanime account logged in one of `(chrome, chromium, opera, brave, edge, vivaldi, firefox, safari)` if set to `null` the code will try to guess which browser to use. **Defaults to `chrome`**
  - **cookies_location** the path directly to the cookie file of the corresponding browser. If not set the code uses the default location for the browser
- **new.txt** a text file used to add new anime to the watching list safely if the program is running (one file per line in the format `<anime-id> |` or `<anime-id> | <anime-name>`)
- **quit.txt** if this file has any content inside the program will finish any download it is doing and close (only works if running in continuous mode)
- **watching.txt** a text file containing the currently queued anime, which episodes have already been downloaded separated only by a `,` and, if provided, a name for the anime, if omited the name present in the anime page will be used. The anime are listed one per line in one of the following formats:
  - `<anime-id>`
  - `<anime-id> <list of episodes>`
  - `<anime-id> | <anime-name>`
  - `<anime-id> <list of episodes> | <anime-name>`
