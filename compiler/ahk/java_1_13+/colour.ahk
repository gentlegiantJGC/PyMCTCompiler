^+d::
clipboard =  ;
Send ^c
ClipWait  ;
ToolTip % clipboard
sleep 1000
ToolTip
colours := ["white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray", "light_gray", "cyan", "purple", "blue", "brown", "green", "red", "black", "black"]
FileCreateDir, %A_MyDocuments%\GitHub\Minecraft-Universal-Block-Mappings\compiler\primitives\blockstate\java_1_13+\vanilla\%clipboard%
for index, colour in colours
{
	f = blockstate.colour("minecraft", "%colour%_%clipboard%", "%colour%", "universal_minecraft", "%clipboard%")
	FileDelete, %A_MyDocuments%\GitHub\Minecraft-Universal-Block-Mappings\compiler\primitives\blockstate\java_1_13+\vanilla\%clipboard%\%colour%_%clipboard%.pyjson
	FileAppend %f%, %A_MyDocuments%\GitHub\Minecraft-Universal-Block-Mappings\compiler\primitives\blockstate\java_1_13+\vanilla\%clipboard%\%colour%_%clipboard%.pyjson
}
Send {Right}Done
sleep 100
Send {Backspace}{Backspace}{Backspace}{Backspace}
Return