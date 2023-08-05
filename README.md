## Download sorgente
```
git clone https://github.com/LucaMenzio/AOE2_friendlies_ITA.git
cd AOE2_friendlies_ITA
git config core.symlinks true
git submodule update --init --recursive
git restore ./rlink_client
```
Se `rlink_client` risulta essere un file invece di una cartella, provare a fare checkout di un altro branch e poi tornare su main.  
Link su stackoverflow sulla gestione dei symlink su windows: [link](https://stackoverflow.com/a/59761201)
