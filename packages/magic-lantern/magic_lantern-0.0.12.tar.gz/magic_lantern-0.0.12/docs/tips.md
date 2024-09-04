
# Tips


# Some test images
```
git clone https://github.com/hampusborgos/country-flags.git
```



## Running over ssh

Add this to `~/.bashrc`
```bash
export DISPLAY=:0
```

## Fixing photo orientation 
[ImageMagick](https://imagemagick.org/script/mogrify.php)

```bash
mogrify -auto-orient *.jpg
```

## Fixing missing dates
e.g.: 

```bash
exiftool -datetimeoriginal="2009:08:08 00:00:00" -overwrite_original -m *
```

## What's with the name?
[Magic lantern](https://en.wikipedia.org/wiki/Magic_lantern)