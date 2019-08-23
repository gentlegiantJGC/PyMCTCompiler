^+d::
clipboard =  ;
Send ^c
ClipWait  ;
ToolTip % clipboard
ToolTip
materials := ["oak", "spruce", "birch", "jungle", "acacia", "dark_oak"]
FileCreateDir, %A_MyDocuments%\GitHub\Minecraft-Universal-Block-Mappings\compiler\primitives\blockstate\java_1_13+\vanilla\%clipboard%
for index, material in materials
{
	f = blockstate.wood("minecraft", "%material%_%clipboard%", "%material%", "universal_minecraft", "%clipboard%")
	FileDelete, %A_MyDocuments%\GitHub\Minecraft-Universal-Block-Mappings\compiler\primitives\blockstate\java_1_13+\vanilla\%clipboard%\%material%_%clipboard%.pyjson
	FileAppend %f%, %A_MyDocuments%\GitHub\Minecraft-Universal-Block-Mappings\compiler\primitives\blockstate\java_1_13+\vanilla\%clipboard%\%material%_%clipboard%.pyjson
}
Send {Right}Done
sleep 100
Send {Backspace}{Backspace}{Backspace}{Backspace}
Return