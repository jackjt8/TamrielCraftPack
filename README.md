# TamrielCraftPack
## About Tamrielcraft

Tamrielcraft is a Minecraft Build/RP server seeking to recreate the entire continent of Tamriel from the Elder Scrolls series! It's currently undergoing major overhauls to revamp it for a new era of Minecraft RP.

SERVER IP (MC Java 1.20): tamrielcraft.eu 

[Tamrielcraft wiki](https://wiki.tamrielcraft.eu/)
[Server Dynmap](map.tamrielcraft.eu/)
[Discord](https://discord.gg/ApShrYn)


## This repo

This repo is where you can suggest or make changes to Tamrielcraft's resource pack which is based on Excalibur by Maffhew. Please feel free to open issues, PRs, etc. Any help is welcome. 


## Build instructions

Either run `Build.bat` if on Windows OR Manually build:

1. Download a copy of this Repo, [Excalibur](https://modrinth.com/resourcepack/excal), and [Excalibur Extras](https://www.curseforge.com/minecraft/mc-addons/excalibur-extras).

2. Extract Excalibur to a temp directory. Then extract Excalibur Extras to the same directory, overwriting any files. And finally extract/copy TamrielCraftPack over the same structure and overwrite as needed.

	ie
	```
	temp/
		/assets/
		Changelog.txt
		ExtraBlocks.txt
		etc...
	```

3. Then remove the following `Optifine` features in `assets/minecraft/optifine/` --- Vanilla players have rights.

	```
	cit
	ctm\dragonegg
	ctm\foliage\reeds
	ctm\foliage\sand_snow
	ctm\glass\white
	ctm\random\cauldron
	ctm\random\prismarine
	ctm\stone\orange_concrete
	ctm\stone\stone_brick_pillar
	```
	
3.5. Remove `extras.txt` - It's a leftover from Excalibut Extras.


(release) 4. Update `changelog.txt`, `pack.mcmeta`, `extras.txt`, `pack.png`

		Naming/versioning should be `TCP-YYMMDD.revision`/`YYMMDD.revision`
	
		ie - 	20[24]/[09]/[11].rev[0] = `TCP-240911.zip`
				20[24]/[09]/[11].rev[1] = `TCP-240911.1.zip`
			
		Revision only shows if multiple versions get released the same day. Probably won't be used.
		
(release) 5. Package contents into .zip file ie:

	```
	tcp_YYMMDD.zip
		/assets/
		Changelog.txt
		ExtraBlocks.txt
		etc...
	```
	
## Common issues

Transparent textures do not display correctly - Minecraft bug tracked via MC-164001. A core-shader is included in this Resource Pack to fix it. You will need a mod like [Transparent (Fabric)](https://modrinth.com/mod/transparent) if you wish to use shaders via Iris as core-shaders get disabled.


## Recommended Mods

Recommended that you use a 3rd party launcher with Instance support like Prism. ie different setups of Minecraft each with their own version, mod(pack)(s), servers, etc.

Use [Fabulously Optimized](https://modrinth.com/modpack/fabulously-optimized) OR [Simply Optimized](https://modrinth.com/modpack/sop) as a base mod pack. These mod pack contain everything you need to improve graphics and/or performance with a few QOL mods included.

**Enhanced Block Entities** - This mod will break culling on many blocks though will improve performance.


### Distant Horizons

Adds LODs to minecraft. Allows for massively increased render distances without costing too much performance. Works with Iris shaders.

[Link](https://modrinth.com/mod/distanthorizons)


### Falling Leaves

Adds falling leaf particle effects to leaf blocks. Looks nice

[Link](https://modrinth.com/mod/fallingleaves)


### Nvidium (Experimental)

Uses Nvidia mesh shaders to boost rendering performance and allows increased render distances at minimal cost. Works with Distant Horizons but auto disables for shaders.

[Link](https://modrinth.com/mod/nvidium)


### Transparent

This mod fixes a Minecraft bug, MC-164001, where transparent textures do not display correctly.

[Link](https://modrinth.com/mod/transparent)


### ViaFabricPlus

Lets you connect to EVERY minecraft server with QoL fixes. Introduces latency so you might not want to use it...

[Link](https://modrinth.com/mod/viafabricplus)


