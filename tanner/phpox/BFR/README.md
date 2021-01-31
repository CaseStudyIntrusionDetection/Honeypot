# BFR #

## Better Function Replacer based on APD ##

APD http://pecl.php.net/package/apd started to have issues with the current Zend API. As some of my tools strongly rely on APD's function renaming and overwriting features, I had to get my hands dirty. I finally was successful in extracting those features and bundling them into a 'new' Zend extension. All credits go to the original developers. Sadly they don't respond to issues with the original version.

### Installation Linux ###

Install requirements:
```
# sudo apt install php-dev
```

Get the source github style and run the following in the source directory:
```
# cd BFR
# phpize
```

Output on my system looked like this. May vary depending on system.
```
Configuring for:
PHP Api Version:         20151012
Zend Module Api No:      20151012
Zend Extension Api No:   320151012
```

Run the usual stuff:
```
# ./configure --enable-bfr
# make && make install
```
```
Build complete.
Don't forget to run 'make test'.

Installing shared extensions:     /usr/lib/php/20131226/
```

Modify your php.ini accordingly. Add:
```
zend_extension = /usr/lib/php/20131226/bfr.so
```

You should see the extension on the output of:
```
# php --version

PHP 7.0.7 (cli) (built: Jun  1 2016 00:58:54) ( NTS )
Copyright (c) 1997-2016 The PHP Group
Zend Engine v3.0.0, Copyright (c) 1998-2016 Zend Technologies
    with Better Function Replacer (BFR) v0.1, Copyright (C) 2015, by Lukas Rist
```

