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

- Transparent textures do not display correctly - Minecraft bug tracked via MC-164001. A core-shader is included in this Resource Pack to fix it. You will need a mod like [Just Make Paintings Transparent](https://modrinth.com/mod/jumapat) or [Transparent (Fabric)](https://modrinth.com/mod/transparent) if you wish to use shaders via Iris as core-shaders get disabled.

- More Culling - `BlockState Culling` is known to be problematic on multiple models. Disable it.


