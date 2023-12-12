# TamrielCraftPack
## About Tamrielcraft
Tamrielcraft is a Minecraft Build/RP server seeking to recreate the entire continent of Tamriel from the Elder Scrolls series! It's currently undergoing major overhauls to revamp it for a new era of Minecraft RP.

SERVER IP (MC Java 1.20): tamrielcraft.eu 

[Tamrielcraft wiki](https://wiki.tamrielcraft.eu/)
[Server Dynmap](map.tamrielcraft.eu/)
[Discord](https://discord.gg/ApShrYn)

## This repo
This repo is where you can suggest changes to Tamrielcraft's resource pack which is based on Excalibur by Maffhew

## Build instructions

Either run `Build.bat` if on Windows OR Manually build:

1. Download a copy of this Repo, Excalibur, and Excalibur Extras.

2. Extract Excalibur first. Then overwrite any files with those from Excalibur Extras and finally TamrielCraftPack. 

3. Remove "Optifine Blocks" listed in ExtraBlocks found in `assets/minecraft/optifine/ctm`

	```
	dragonegg
	foliage\reeds
	foliage\sand_snow
	glass\white
	random\cauldron
	random\prismarine
	stone\orange_concrete
	stone\stone_brick_pillar
	```
(release) 4. Update `changelog.txt`, `pack.mcmeta`, `extras.txt`, `pack.png`

(release) 5. Package contents into .zip file ie:

	```
	tcp.zip
		/assets/
		Changelog.txt
		etc...
	```
	
## Common issues

OptiFine OpenGL Error 1281 - Generally causes by having VBOs, Render Regions, and Connected Textures (CTM) enabled while using a Nvidia GPU. If you experience this issue it is recommended that you disable OpenGL Errors in chat by:

`Options > Video Settings > Other... > Show GL Errors: Off`

Transparent textures do not display correctly - Minecraft bug tracked via MC-164001. The patch, included with this resource pack as of v1.18.1b1, only works on Minecraft 1.17. For 1.16.5 you need to use a mod to fix this issue like [Transparent (Fabric)](https://www.curseforge.com/minecraft/mc-mods/transparent).


## Recommended Mods

Recommended that you use a 3rd party launcher with Instance support like Prism. This means that you can easily have different setups for different versions, modpacks, servers, etc.

Use **Fabulously Optimized** as a base mod pack. Everything just works together.

**DISABLE Enhanced Block Entities**
	This mod will break culling on many blocks.


### Distant Horizons Alpha 2.0.1

Adds LODs to minecraft. Allows for massively increased render distances without costing too much performance. Works with Iris shaders.

[Link](https://modrinth.com/mod/distanthorizons)


#### Blendium

Adds alpha blending for Distant Horizons and Sodium. Also has some stuff for Iris so that shaders work better with Distant Horizons.

[Link](https://modrinth.com/mod/blendium)


### Nvidium

Uses Nvidia mesh shaders to boost rendering performance and allows increased render distances at minimal cost. Works with Distant Horizons but auto disables for shaders.

[Link](https://modrinth.com/mod/nvidium)


### viafabricplus

Lets you connect to EVERY minecraft server with QoL fixes.

[Link](https://modrinth.com/mod/viafabricplus)


### Better Anvil / RP Renames

Was recommended. Need to investigate.


	