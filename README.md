# TamrielCraftPack
## About Tamrielcraft
Tamrielcraft is a Minecraft Build/RP server seeking to recreate the entire continent of Tamriel from the Elder Scrolls series! It's currently undergoing major overhauls to revamp it for a new era of Minecraft RP.

SERVER IP (MC Java 1.16.5): tamrielcraft.eu 

[Tamrielcraft wiki](https://wiki.tamrielcraft.eu/)
[Server Dynmap](map.tamrielcraft.eu/)
[Discord](https://discord.gg/ApShrYn)

## This repo
This repo is where you can suggest changes to Tamrielcraft's resource pack which is based on Excalibur by Maffhew

## Build instructions

1. Download and extract a copy of this Repo and Excalibur.

2. Copy/move contents of the extracted TamrielCraftPack folder into Excalibur overwriting files.

3. Remove "Optifine Blocks" listed in ExtraBlocks found in `assets/minecraft/optifine/ctm`

	```
	/foliage/cobweb/
	/foliage/reeds/ ~maybe?
	/foliage/sand_snow/
	/glass/1.png
	/glass/glass_white.properties
	/random/cauldron/
	/random/dragonegg/
	/random/glowstone/ ~maybe?
	/random/cobweb/
	/stone/orange_concrete/
	/stone/stone_pillar/
	```
(release) 4. Update `changelog.txt` and `pack.mcmeta`

(release) 5. Package contents into .zip file ie:

	```
	tcp.zip
		/assets/
		Changelog.txt
		etc...
	```
	
## Common issues

OpenGL Error 1281 - Generally causes by having VBOs, Render Regions, and Connected Textures (CTM) enabled while using a Nvidia GPU. If you experience this issue it is recommended that you disable OpenGL Errors in chat by:

`Options > Video Settings > Other... > Show GL Errors: Off`

