# Honeypot

## Tools
### Tanner
> Safe executions environment for *hacks*.

#### Used Sources
-  PHP OX: PHP Sandbox
	- (Better) Function Replacer for PHP ([PHP License](https://github.com/CaseStudyIntrusionDetection/Honeypot/blob/master/tanner/phpox/BFR/LICENSE))
- Redis: Key value storage used by tanner
- Alpine Linux: as environment for command and file injections

### Snare
> Website proxy to make it a target.

## Run
> Run both via docker-compose
1. First start TANNER
	- `cd tanner`
	- `docker-compose up`
	- Will create a docker network, also used by SNARE
2. Now start the target (proxied by SNARE)
	- `cd target`
	- `docker-compose up`
3. Now start SNARE
	- `cd snare`
	- `docker-compose up`
4. Visit http://127.0.0.1:80 and run attacks against

> Or use `./start.sh` for first three steps

## License
All components are licensed under [GPLv3 License](https://github.com/CaseStudyIntrusionDetection/Honeypot/blob/master/LICENSE) 
except (Better) Function Replacer for PHP.

The initial code was developed by http://mushmush.org/, all later changes and where made by 
the CaseStudy IntrusionDetection Developers.

```
Honeypot System for the CaseStudy IntrusionDetection
Copyright (C) 2021 CaseStudy IntrusionDetection Developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```