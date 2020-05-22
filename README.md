# TamrielCraftPack
TamrielCraft's Minecraft Resource Pack

## Release build instructions

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
	/stone/orange_concrete/
	/stone/stone_pillar/
	```
	
## Common issues

OpenGL Error 1281 - Generally causes by having VBOs, Render Regions, and Connected Textures (CTM) enabled while using a Nvidia GPU. If you experience this issue it is recommended that you disable OpenGL Errors in chat by:

`Options > Video Settings > Other... > Show GL Errors: Off`
	
	
	