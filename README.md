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

Either run `Build.bat` if on Windows OR Manually build:

1. Download a copy of this Repo, Excalibur, and Excalibur Extras.

2. Extract Excalibur first. Then overwrite any files with those from Excalibur Extras and finally TamrielCraftPack. 

3. Remove "Optifine Blocks" listed in ExtraBlocks found in `assets/minecraft/optifine/ctm`

	```
	foliage\reeds
	foliage\sand_snow
	glass\white
	random\cauldron
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

Recommended that you use a 3rd party launcher with Instance support like Prism.

Use Fabulously Optimized as a base mod pack.

DISABLE enhancedblockentities!!!
	This mod will break culling on many blocks.

For Minecraft 1.20:

advancementinfo
animatica
antighost
bettermounthud
borderless-mining
capes
CITResewn
cloth-config
continuity
Controlify
Debugify
dynamic-fps
e4mc
entityculling
entity_model_features
entity_texture_features
fabric-api
fabric-language-kotlin
fabricskyboxes
fabrishot
fadeless
farsight
fastquit
ferritecore
fsb-interop
ImmediatelyFast
indium
iris
language-reload
lithium
main-menu-credits
memoryleakfix
mixintrace
modelfix
modernfix-fabric
modmenu
morechathistory
moreculling
NoChatReports
optigui
puzzle
reeses_sodium_options
Rrls
sodium-extra
sodium
yet-another-config-lib
yosbr
Zoomify

---
### Other mods

#### DistantHorizons-2.0.0-a-RC3-1.20.1
	LOD mod. 2.0 is a huge upgrade.
	
#### viafabricplus
	Lets you connect to older Minecraft servers... like the server on 1.16.5.
	