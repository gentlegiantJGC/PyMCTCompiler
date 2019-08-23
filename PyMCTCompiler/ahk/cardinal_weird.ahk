^+w::
clipboard =  ;
Send ^c
ClipWait  ;
ToolTip % clipboard
sleep 1000
ToolTip
f = numerical.compass("minecraft", "%clipboard%", {2: "north", 3: "south", 4: "west", 5: "east"})
FileDelete, %A_MyDocuments%\GitHub\Minecraft-Universal-Block-Mappings\Primitives\numerical\bedrock\vanilla\%clipboard%.pyjson
FileAppend %f%, %A_MyDocuments%\GitHub\Minecraft-Universal-Block-Mappings\Primitives\numerical\bedrock\vanilla\%clipboard%.pyjson
Send {Right}+{End}{Backspace}":{Space}"%clipboard%"
Return